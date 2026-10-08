import asyncio
import math
import json
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

import httpx
import pytest

from scripts.reproduce_sampled import configure, make_sample, save_run_config, summarize
from src import llm_client


def fake_clock(monkeypatch):
    clock = SimpleNamespace(now=0.0, sleeps=[])

    async def sleep(delay):
        clock.sleeps.append(delay)
        clock.now = max(clock.now + delay, math.nextafter(clock.now, float('inf')))

    monkeypatch.setattr(llm_client, "time", SimpleNamespace(monotonic=lambda: clock.now))
    monkeypatch.setattr(llm_client.asyncio, "sleep", sleep)
    monkeypatch.setattr(llm_client.random, "uniform", lambda low, high: 0)
    return clock


def test_paired_sampling_is_balanced_and_reproducible():
    manifest, subsets = make_sample(0.3, 42)
    assert manifest["total_instances"] == 429
    assert manifest["total_base_cases"] == 143
    assert make_sample(0.3, 42) == (manifest, subsets)
    assert make_sample(0.3, 43)[0] != manifest
    for alias, count in [("PIE", 49), ("LIP", 49), ("PIC", 45)]:
        selected = [[row["case_id"] for row in subsets[f"{alias}/{state}"]]
                    for state in ("session", "memory", "skill")]
        assert selected[0] == selected[1] == selected[2]
        assert len(selected[0]) == len(set(selected[0])) == count


def test_summary_counts_execution_failures_and_keeps_pending_separate():
    manifest = {"slices": [{"key": "PIE/session", "sample_size": 3}]}
    records = {"PIE/session": [
        {"final_output": {"attack_success": True}, "execution_status": {"success": True}},
        {"final_output": {"attack_success": False}, "execution_status": {"success": False}},
    ]}
    partial = summarize(manifest, records)["overall"]
    assert partial["asr"] is None
    assert partial["asr_completed"] == 0.5
    assert partial["execution_failures"] == 1
    records["PIE/session"].append(records["PIE/session"][1])
    complete = summarize(manifest, records)["overall"]
    assert complete["asr"] == 1 / 3
    assert complete["execution_failures"] == 2


def test_retry_exponential_and_retry_after_without_replaying_tools(monkeypatch):
    clock = fake_clock(monkeypatch)
    calls = []

    async def handler(request):
        calls.append((clock.now, request.content))
        if len(calls) <= 3:
            return httpx.Response(429, json={"error": {"message": "limited"}},
                                  headers={"Retry-After": "40"} if len(calls) == 3 else {})
        return httpx.Response(200, json={"ok": True})

    async def scenario():
        policy = llm_client.RequestPolicy(backoff_base=8, max_retries=3)
        transport = llm_client.RateLimitedTransport("retry", policy, httpx.MockTransport(handler))
        async with httpx.AsyncClient(transport=transport) as client:
            response = await client.post("https://example.test", content=b'{"model":"test"}')
            assert response.status_code == 200
        assert llm_client.request_stats() == {"attempts": 4, "rate_limits": 3, "exhausted": 0}

    asyncio.run(scenario())
    assert [when for when, _ in calls] == [0, 8, 24, 64]
    assert len(set(body for _, body in calls)) == 1


def test_agent_and_simulator_clients_share_rate_budget(monkeypatch):
    clock = fake_clock(monkeypatch)
    starts = []

    async def handler(request):
        starts.append(clock.now)
        return httpx.Response(200, json={"ok": True})

    async def scenario():
        policy = llm_client.RequestPolicy()
        first = llm_client.RateLimitedTransport("same_endpoint", policy, httpx.MockTransport(handler))
        second = llm_client.RateLimitedTransport("same_endpoint", policy, httpx.MockTransport(handler))
        async with httpx.AsyncClient(transport=first) as agent, httpx.AsyncClient(transport=second) as sim:
            await agent.get("https://example.test")
            await sim.get("https://example.test")
            await agent.get("https://example.test")
        assert llm_client.request_stats()["attempts"] == 3

    asyncio.run(scenario())
    assert starts == pytest.approx([0, 3.1, 6.2])


def test_exhaustion_is_bounded_and_recorded(monkeypatch):
    fake_clock(monkeypatch)

    async def handler(request):
        return httpx.Response(429, json={"error": {"message": "limited"}})

    async def scenario():
        failures = []
        token = llm_client.request_failures.set(failures)
        try:
            transport = llm_client.RateLimitedTransport(
                "exhaust", llm_client.RequestPolicy(max_retries=2), httpx.MockTransport(handler))
            async with httpx.AsyncClient(transport=transport) as client:
                response = await client.get("https://example.test")
                assert response.status_code == 429
                assert response.json()["error"]["message"] == "limited"
            assert llm_client.request_stats() == {"attempts": 3, "rate_limits": 3, "exhausted": 1}
            assert failures == ["HTTP 429 exhausted request retries"]
        finally:
            llm_client.request_failures.reset(token)

    asyncio.run(scenario())


def test_stream_holds_slot_until_closed(monkeypatch):
    fake_clock(monkeypatch)

    async def handler(request):
        return httpx.Response(200, stream=httpx.ByteStream(b'data: test\n\n'))

    async def scenario():
        policy = llm_client.RequestPolicy(max_in_flight=1)
        transport = llm_client.RateLimitedTransport("stream", policy, httpx.MockTransport(handler))
        async with httpx.AsyncClient(transport=transport) as client:
            request = client.build_request("GET", "https://example.test")
            response = await client.send(request, stream=True)
            gate = llm_client._gate_for("stream", policy)
            assert gate.slots.locked()
            await response.aclose()
            assert not gate.slots.locked()
            await response.aclose()
            assert gate.slots._value == 1

    asyncio.run(scenario())


def test_non_rate_limit_errors_are_not_retried(monkeypatch):
    fake_clock(monkeypatch)

    async def scenario():
        transport = llm_client.RateLimitedTransport(
            "auth", llm_client.RequestPolicy(),
            httpx.MockTransport(lambda request: httpx.Response(401, json={"error": "bad credential"})))
        async with httpx.AsyncClient(transport=transport) as client:
            response = await client.get("https://example.test")
            assert response.status_code == 401
        assert llm_client.request_stats()["attempts"] == 1

    asyncio.run(scenario())


def test_retry_after_formats():
    assert llm_client.retry_after_seconds({"retry-after": "30"}) == 30
    assert llm_client.retry_after_seconds({"retry-after-ms": "1250"}) == 1.25
    assert llm_client.retry_after_seconds({"retry-after": "invalid"}) == 0
    assert llm_client.retry_after_seconds({"retry-after": "nan"}) == 0
    assert llm_client.retry_after_seconds({"retry-after": "Thu, 01 Jan 1970 00:00:00 GMT"}) == 0


def test_prepare_resume_rejects_changed_sample_and_prevents_overwrite(tmp_path):
    root = Path(__file__).resolve().parents[1]
    command = [sys.executable, str(root / "scripts/reproduce_sampled.py"),
               "--output-dir", str(tmp_path)]
    prepared = subprocess.run(command, capture_output=True, text=True)
    assert prepared.returncode == 0, prepared.stderr
    original = (tmp_path / "manifest.json").read_bytes()
    assert json.loads(original)["total_instances"] == 429
    repeated = subprocess.run(command, capture_output=True, text=True)
    assert repeated.returncode == 2
    resumed = subprocess.run(command + ["--resume"], capture_output=True, text=True)
    assert resumed.returncode == 0, resumed.stderr
    changed = subprocess.run(command + ["--resume", "--seed", "43"], capture_output=True, text=True)
    assert changed.returncode == 2
    assert (tmp_path / "manifest.json").read_bytes() == original


def test_openai_sdk_uses_retry_transport(monkeypatch):
    from openai import AsyncOpenAI

    fake_clock(monkeypatch)
    attempts = []

    async def handler(request):
        attempts.append(request)
        if len(attempts) == 1:
            return httpx.Response(429, json={"error": {"message": "limited", "type": "rate_limit"}})
        return httpx.Response(200, json={
            "id": "chatcmpl-test", "object": "chat.completion", "created": 0, "model": "test",
            "choices": [{"index": 0, "message": {"role": "assistant", "content": '{"ok":true}'},
                         "finish_reason": "stop"}],
        })

    async def scenario():
        transport = llm_client.RateLimitedTransport(
            "sdk", llm_client.RequestPolicy(), httpx.MockTransport(handler))
        async with AsyncOpenAI(api_key="test", base_url="https://example.test/v1", max_retries=0,
                               http_client=httpx.AsyncClient(transport=transport)) as client:
            response = await client.chat.completions.create(
                model="test", messages=[{"role": "user", "content": "test"}])
            assert response.choices[0].message.content == '{"ok":true}'
        assert len(attempts) == 2

    asyncio.run(scenario())


def test_reproduction_ignores_proxy_environment(monkeypatch, tmp_path):
    for key, value in {"F_DEEPSEEK_MODEL": "test-model", "F_DEEPSEEK_BASE_URL": "https://example.test/v1",
                       "F_DEEPSEEK_API_KEY": "test-key", "HTTP_PROXY": "http://unreachable.test:80",
                       "HTTPS_PROXY": "http://unreachable.test:80", "ALL_PROXY": "http://unreachable.test:80",
                       "http_proxy": "http://unreachable.test:80", "https_proxy": "http://unreachable.test:80",
                       "all_proxy": "http://unreachable.test:80"}.items():
        monkeypatch.setenv(key, value)
    settings = configure(SimpleNamespace(output_dir=tmp_path, max_agent_turns=30, timeout=120,
                                        rpm=20, max_in_flight=2, retries=12, backoff_base=6,
                                        backoff_cap=120, concurrency=2))
    import os
    assert settings["network"] == "direct_no_proxy"
    assert not any(os.getenv(key) for key in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY",
                                             "http_proxy", "https_proxy", "all_proxy"))
    assert os.environ["NO_PROXY"] == os.environ["no_proxy"] == "*"

    async def scenario():
        # Reinsert proxy variables to prove the HTTP client also ignores them.
        monkeypatch.setenv("HTTPS_PROXY", "http://unreachable.test:80")
        client = llm_client.create_async_client("test-key", "https://example.test/v1", 30)
        assert client._client._trust_env is False
        assert not client._client._mounts
        await client.close()

    asyncio.run(scenario())



def test_resume_allows_rpm_change_and_preserves_results(tmp_path):
    previous = {"model": "test-model", "endpoint_sha256": "same-endpoint", "case_concurrency": 2,
                "evaluation": "original", "settings": {"LLM_REQUESTS_PER_MINUTE": "10",
                "MAX_AGENT_TURNS": "30", "LLM_MAX_IN_FLIGHT": "2", "REQUEST_TIMEOUT": "120"}}
    save_run_config(tmp_path, previous, 0)
    result_path = tmp_path / "results" / "PIE" / "session.json"
    result_path.parent.mkdir(parents=True)
    result_path.write_text('[{"case_info":{"case_id":"already-completed"}}]')
    original_results = result_path.read_bytes()
    settings = json.loads(json.dumps(previous))
    settings["settings"]["LLM_REQUESTS_PER_MINUTE"] = "20"
    save_run_config(tmp_path, settings, 128)
    assert result_path.read_bytes() == original_results
    assert json.loads((tmp_path / "run_config.json").read_text()) == settings
    history = json.loads((tmp_path / "run_config_history.json").read_text())
    assert len(history) == 1
    assert history[0]["completed_instances"] == 128
    assert history[0]["previous_config"] == previous
    assert history[0]["config"] == settings
    save_run_config(tmp_path, settings, 129)
    assert json.loads((tmp_path / "run_config_history.json").read_text()) == history


@pytest.mark.parametrize("section, key, value", [
    ("model", None, "other-model"),
    ("endpoint_sha256", None, "other-endpoint"),
    ("case_concurrency", None, 3),
    ("evaluation", None, "other-evaluator"),
    ("settings", "MAX_AGENT_TURNS", "40"),
    ("settings", "LLM_MAX_IN_FLIGHT", "3"),
    ("settings", "REQUEST_TIMEOUT", "90"),
])
def test_resume_still_rejects_other_configuration_changes(tmp_path, section, key, value):
    previous = {"model": "test-model", "endpoint_sha256": "same-endpoint", "case_concurrency": 2,
                "evaluation": "original", "settings": {"LLM_REQUESTS_PER_MINUTE": "10",
                "MAX_AGENT_TURNS": "30", "LLM_MAX_IN_FLIGHT": "2", "REQUEST_TIMEOUT": "120"}}
    save_run_config(tmp_path, previous, 0)
    settings = json.loads(json.dumps(previous))
    settings["settings"]["LLM_REQUESTS_PER_MINUTE"] = "20"
    if key is None:
        settings[section] = value
    else:
        settings[section][key] = value
    with pytest.raises(ValueError, match="only RPM may change"):
        save_run_config(tmp_path, settings, 128)
    assert json.loads((tmp_path / "run_config.json").read_text()) == previous
    assert not (tmp_path / "run_config_history.json").exists()


def test_resume_with_unchanged_configuration_does_not_create_history(tmp_path):
    settings = {"model": "test-model", "settings": {"LLM_REQUESTS_PER_MINUTE": "20"}}
    save_run_config(tmp_path, settings, 0)
    save_run_config(tmp_path, settings, 128)
    assert json.loads((tmp_path / "run_config.json").read_text()) == settings
    assert not (tmp_path / "run_config_history.json").exists()

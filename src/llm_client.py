"""Opt-in, process-wide HTTP pacing and safe retries of rejected LLM requests.

Agent and simulator clients share a gate for the same endpoint and credential.
Only HTTP 429 responses are replayed; partially consumed streams are never replayed.
"""
from __future__ import annotations

import asyncio
import contextvars
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import hashlib
import logging
import math
import os
import random
import time
import weakref

import httpx
from openai import AsyncOpenAI

logger = logging.getLogger(__name__)
_gates = weakref.WeakKeyDictionary()
request_failures = contextvars.ContextVar("llm_request_failures", default=None)


@dataclass(frozen=True)
class RequestPolicy:
    rpm: float = 20
    max_in_flight: int = 2
    max_retries: int = 12
    backoff_base: float = 6
    backoff_cap: float = 120

    def __post_init__(self):
        if not math.isfinite(self.rpm) or self.rpm <= 0:
            raise ValueError("LLM_REQUESTS_PER_MINUTE must be positive and finite")
        if self.max_in_flight < 1 or self.max_retries < 0:
            raise ValueError("Invalid LLM concurrency or retry count")
        if not (0 < self.backoff_base <= self.backoff_cap < float('inf')):
            raise ValueError("Invalid LLM backoff bounds")

    @property
    def interval(self):
        # A small margin also avoids a burst at rolling-window boundaries.
        return 60 / self.rpm + 0.1


class RequestGate:
    def __init__(self, policy):
        self.policy = policy
        self.slots = asyncio.Semaphore(policy.max_in_flight)
        self.lock = asyncio.Lock()
        self.next_start = 0.0
        self.cooldown_until = 0.0
        self.attempts = 0
        self.rate_limits = 0
        self.exhausted = 0

    async def acquire(self):
        await self.slots.acquire()
        try:
            async with self.lock:
                while True:
                    delay = max(self.next_start, self.cooldown_until) - time.monotonic()
                    if delay <= 0:
                        break
                    await asyncio.sleep(delay)
                self.next_start = time.monotonic() + self.policy.interval
                self.attempts += 1
        except BaseException:
            self.slots.release()
            raise

    def defer(self, delay):
        self.cooldown_until = max(self.cooldown_until, time.monotonic() + delay)


def _gate_for(key, policy):
    loop = asyncio.get_running_loop()
    gates = _gates.setdefault(loop, {})
    if key not in gates:
        gates[key] = RequestGate(policy)
    gate = gates[key]
    if gate.policy != policy:
        raise ValueError("Clients sharing credentials must share the request policy")
    return gate


def request_stats():
    gates = _gates.get(asyncio.get_running_loop(), {})
    return {name: sum(getattr(gate, name) for gate in gates.values())
            for name in ("attempts", "rate_limits", "exhausted")}


def retry_after_seconds(headers):
    try:
        if headers.get("retry-after-ms"):
            value = float(headers["retry-after-ms"]) / 1000
        else:
            raw = headers.get("retry-after", "0")
            try:
                value = float(raw)
            except ValueError:
                date = parsedate_to_datetime(raw)
                if date.tzinfo is None:
                    date = date.replace(tzinfo=timezone.utc)
                value = (date - datetime.now(timezone.utc)).total_seconds()
        return max(0, value) if math.isfinite(value) else 0
    except (ValueError, TypeError, OverflowError):
        return 0


class _SlotStream(httpx.AsyncByteStream):
    """Hold the concurrency slot until the response (including SSE) is closed."""
    def __init__(self, stream, gate):
        self.stream = stream
        self.gate = gate
        self.closed = False

    async def __aiter__(self):
        async for chunk in self.stream:
            yield chunk

    async def aclose(self):
        if not self.closed:
            self.closed = True
            try:
                await self.stream.aclose()
            finally:
                self.gate.slots.release()


class RateLimitedTransport(httpx.AsyncBaseTransport):
    def __init__(self, key, policy, transport=None):
        self.key = key
        self.policy = policy
        self.transport = transport if transport is not None else httpx.AsyncHTTPTransport(trust_env=False)

    async def handle_async_request(self, request):
        # OpenAI JSON request bodies are replayable. Buffer before retrying.
        await request.aread()
        gate = _gate_for(self.key, self.policy)
        for retry in range(self.policy.max_retries + 1):
            await gate.acquire()
            logger.info("LLM HTTP attempt %d (retry %d/%d)",
                        gate.attempts, retry, self.policy.max_retries)
            try:
                response = await self.transport.handle_async_request(request)
            except BaseException:
                gate.slots.release()
                raise
            logger.info("LLM HTTP attempt %d received status %d", gate.attempts, response.status_code)
            if response.status_code != 429:
                if response.is_closed:
                    gate.slots.release()
                else:
                    response.stream = _SlotStream(response.stream, gate)
                return response
            gate.rate_limits += 1
            try:
                await response.aread()
            finally:
                await response.aclose()
                gate.slots.release()
            # Jitter is additive so the actual delay never falls below the base.
            exponential = min(self.policy.backoff_cap,
                              self.policy.backoff_base * 2 ** min(retry, 30))
            delay = max(retry_after_seconds(response.headers),
                        min(self.policy.backoff_cap,
                            exponential + random.uniform(0, exponential * 0.25)))
            gate.defer(delay)
            if retry == self.policy.max_retries:
                gate.exhausted += 1
                failures = request_failures.get()
                if failures is not None:
                    failures.append("HTTP 429 exhausted request retries")
                logger.error("HTTP 429 exhausted %d retries", self.policy.max_retries)
                return response
            logger.warning("HTTP 429: retry %d/%d after %.1fs (shared cooldown)",
                           retry + 1, self.policy.max_retries, delay)
        raise AssertionError("unreachable")

    async def aclose(self):
        await self.transport.aclose()


def create_async_client(api_key, base_url, timeout):
    # Other entry points retain the SDK's original behavior unless opted in.
    if not os.getenv("LLM_REQUESTS_PER_MINUTE", "").strip():
        return AsyncOpenAI(api_key=api_key, base_url=base_url, timeout=timeout)
    policy = RequestPolicy(
        rpm=float(os.environ["LLM_REQUESTS_PER_MINUTE"]),
        max_in_flight=int(os.getenv("LLM_MAX_IN_FLIGHT", "2")),
        max_retries=int(os.getenv("LLM_429_MAX_RETRIES", "12")),
        backoff_base=float(os.getenv("LLM_RETRY_BASE_SECONDS", "6")),
        backoff_cap=float(os.getenv("LLM_RETRY_MAX_SECONDS", "120")),
    )
    key = (str(base_url).rstrip("/"), hashlib.sha256(api_key.encode()).hexdigest())
    http_client = httpx.AsyncClient(
        transport=RateLimitedTransport(key, policy), timeout=timeout, trust_env=False,
    )
    # Disable nested SDK retries: every HTTP attempt must pass the shared gate.
    return AsyncOpenAI(api_key=api_key, base_url=base_url, timeout=timeout,
                       max_retries=0, http_client=http_client)

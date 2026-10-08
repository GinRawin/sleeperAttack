"""Minimal OpenAI-compatible server for AgentDoG coarse-grained moderation."""

from __future__ import annotations

import argparse
import os
import time
import uuid
from typing import Any

import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from transformers import AutoModelForCausalLM, AutoTokenizer


class ChatMessage(BaseModel):
    role: str
    content: str | None = None


class ChatCompletionRequest(BaseModel):
    model: str | None = None
    messages: list[ChatMessage]
    temperature: float | None = 0.0
    max_tokens: int | None = Field(default=512, alias="max_tokens")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Serve AgentDoG as an OpenAI-compatible chat-completions API.")
    parser.add_argument("--model", default=os.getenv("AGENTDOG_HF_MODEL", "AI45Research/AgentDoG1.5-Qwen3.5-4B"))
    parser.add_argument("--host", default=os.getenv("AGENTDOG_HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.getenv("AGENTDOG_PORT", "18100")))
    parser.add_argument("--max-new-tokens", type=int, default=int(os.getenv("AGENTDOG_MAX_NEW_TOKENS", "512")))
    return parser.parse_args()


app = FastAPI(title="AgentDoG OpenAI-compatible server")
_tokenizer = None
_model = None
_default_max_new_tokens = 512


def load_model(model_name: str, max_new_tokens: int) -> None:
    global _tokenizer
    global _model
    global _default_max_new_tokens

    _default_max_new_tokens = max_new_tokens
    _tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    _model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype="auto",
        device_map="auto",
        trust_remote_code=True,
    )
    _model.eval()


def render_messages(messages: list[ChatMessage]) -> str:
    raw_messages = [{"role": msg.role, "content": msg.content or ""} for msg in messages]
    if hasattr(_tokenizer, "apply_chat_template"):
        return _tokenizer.apply_chat_template(
            raw_messages,
            tokenize=False,
            add_generation_prompt=True,
        )
    return "\n".join(f"{msg['role']}: {msg['content']}" for msg in raw_messages) + "\nassistant:"


@app.get("/health")
def health() -> dict[str, Any]:
    return {"ok": _model is not None, "cuda": torch.cuda.is_available()}


@app.post("/v1/chat/completions")
def chat_completions(request: ChatCompletionRequest) -> dict[str, Any]:
    if _model is None or _tokenizer is None:
        raise HTTPException(status_code=503, detail="model not loaded")

    text = render_messages(request.messages)
    model_inputs = _tokenizer([text], return_tensors="pt").to(_model.device)
    max_new_tokens = int(request.max_tokens or _default_max_new_tokens)
    with torch.no_grad():
        generated = _model.generate(
            **model_inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
        )
    output_ids = generated[0][len(model_inputs.input_ids[0]):].tolist()
    content = _tokenizer.decode(output_ids, skip_special_tokens=True).strip()
    return {
        "id": f"chatcmpl-{uuid.uuid4().hex}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": request.model or "agentdog",
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": content},
                "finish_reason": "stop",
            }
        ],
    }


def main() -> None:
    args = parse_args()
    load_model(args.model, args.max_new_tokens)
    import uvicorn

    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()

"""Verify Nebius Token Factory access and make one tiny NVIDIA-model request.

Loads credentials from environment or a local .env file. Never prints the API key.
This performs a real inference request and may consume account credits.
"""
from __future__ import annotations

import os
import sys
import time

from dotenv import load_dotenv
from openai import OpenAI


def main() -> int:
    load_dotenv()
    api_key = os.getenv("NEBIUS_API_KEY", "").strip()
    base_url = os.getenv(
        "NEBIUS_BASE_URL", "https://api.tokenfactory.nebius.com/v1"
    ).strip().rstrip("/")
    model = os.getenv("NEBIUS_MODEL", "nvidia/Nemotron-3_5-Lightning").strip()

    if not api_key:
        print("MISSING: NEBIUS_API_KEY is not set.")
        print("Create a local .env from .env.example and add your key there.")
        return 2
    if not model:
        print("MISSING: NEBIUS_MODEL is empty. Use the exact model ID in your catalog.")
        return 2

    print(f"Endpoint: {base_url}")
    print(f"Selected model: {model}")
    print("Checking model catalog and authentication...")

    client = OpenAI(api_key=api_key, base_url=base_url, timeout=30.0, max_retries=0)
    try:
        catalog = client.models.list()
        available_ids = [entry.id for entry in catalog.data]
        print(f"Authentication/catalog check: OK ({len(available_ids)} model IDs returned)")
        matches = [
            model_id for model_id in available_ids
            if "nvidia" in model_id.lower() or "nemotron" in model_id.lower()
        ]
        if matches:
            print("NVIDIA/Nemotron IDs returned by this account:")
            for model_id in matches[:30]:
                print(f"  - {model_id}")
        else:
            print("NOTE: the catalog response did not include obvious NVIDIA/Nemotron IDs.")
        if model not in available_ids:
            print("NOTE: selected ID was not an exact match in the catalog listing.")
            print("The inference request below will verify whether the endpoint accepts it.")

        print("Sending one minimal live inference request (may use credits)...")
        started = time.perf_counter()
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Reply with exactly: PATCHPILOT_OK"}],
            max_tokens=12,
            temperature=0,
        )
        latency_ms = round((time.perf_counter() - started) * 1000)
        answer = (response.choices[0].message.content or "").strip()
        returned_model = getattr(response, "model", None) or model
        print("LIVE INFERENCE: SUCCESS")
        print(f"Returned model: {returned_model}")
        print(f"Latency: {latency_ms} ms")
        print(f"Response preview: {answer[:160]}")
        print("Keep this output (without credentials) as setup evidence.")
        return 0
    except Exception as exc:  # provider/client errors vary by endpoint
        # Avoid printing request headers or arbitrary exception data that might
        # contain sensitive information. The class name is useful for triage.
        print(f"CHECK FAILED: {type(exc).__name__}")
        print("Review the endpoint, billing/credits, key permissions, and exact model ID.")
        print("Do not share your API key. If you need help, share only the error class/status.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

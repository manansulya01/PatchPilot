# Nebius Token Factory setup for PatchPilot

This checklist gets a real NVIDIA open-model inference call working. It does not require sharing your API key with anyone.

## 1. Create your Token Factory credentials

1. Open [Nebius Token Factory](https://tokenfactory.nebius.com/) and sign in.
2. Complete the account's required onboarding/billing steps. New accounts may receive starter credits, but availability and billing requirements depend on the account. Do not add funds unless you have permission to do so.
3. Select the project you intend to use, open **API keys**, create a key, and copy it somewhere private. The dashboard may show the key only once.
4. Open the model catalog for that project and find an available NVIDIA open-source model, preferably an NVIDIA Nemotron model for this project. Copy the exact model ID as shown; IDs are case-sensitive and availability can differ by account.

Official references: [Token Factory](https://tokenfactory.nebius.com/), [API reference](https://api.tokenfactory.nebius.com/docs), and [billing documentation](https://docs.tokenfactory.nebius.com/other-capabilities/billing).

## 2. Store the key locally

From the PatchPilot repository in PowerShell:

```powershell
Copy-Item .env.example .env
notepad .env
```

Fill in these values in `.env` using the exact model ID you found:

```dotenv
NEBIUS_API_KEY=put_your_private_key_here
NEBIUS_BASE_URL=https://api.tokenfactory.nebius.com/v1
NEBIUS_MODEL=exact/model-id-from-your-catalog
PATCHPILOT_ALLOW_RUNTIME_CONFIG=true
PATCHPILOT_ALLOW_LIVE_INFERENCE=true
```

Save the file. Do not paste the key into chat, a GitHub issue, a screenshot, frontend code, or a committed file. The repository's `.gitignore` excludes `.env`; verify it remains untracked before committing anything.

## 3. Run the connection preflight

Install dependencies and run the preflight from the repository root:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts/check_nebius.py
```

The preflight checks the model catalog, prints NVIDIA/Nemotron model IDs returned by your account, and sends one tiny chat completion using `NEBIUS_MODEL`. That real inference request may consume credits. It prints the returned model and latency but never prints the key or raw provider exception text.

- **LIVE INFERENCE: SUCCESS** means this key, endpoint, and selected model completed a real request.
- **401/403 or authentication errors** usually mean the key/project/permissions need checking.
- **Model not found / 404** means choose the exact model ID listed for your account and try again.
- **Insufficient balance / billing errors** mean review the account balance and billing setup; don't try to bypass regional or account restrictions.

If it fails, share only the error class/status and sanitized output—not the key.

## 4. Verify the app itself

Run the server:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app:app --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000), open **Model connection**, and use the same key, base URL, and exact model ID. Click **Test live call**. Then run one small sample bug analysis in live mode. This is a separate request and may use additional credits.

For evidence, record the date, exact model ID, success/failure, and latency. Never include the API key in screenshots or the hackathon submission.

## 5. Public deployment safety

The Render blueprint intentionally disables live inference by default. Do not turn on billable inference on an unrestricted public endpoint. Before enabling it on a hosted demo, add authentication, per-user rate limits, request-size limits, and suitable abuse/cost controls, and configure the key as a private hosting environment variable. Keep public demo mode enabled until those controls exist.

A successful preflight proves the connection works; it does **not** prove that PatchPilot's proposed patch is correct or that any suggested regression tests ran. The current MVP does not execute generated code.

# PatchPilot

**Verification-first AI debugging.** PatchPilot helps developers investigate a bug, propose a minimal patch, and inspect verification evidence instead of blindly trusting generated code.

> Status: MVP. The built-in demo mode is deterministic and clearly labeled as simulated. For real model analysis, configure a Nebius Token Factory API key and an available NVIDIA Nemotron model. Never present demo-mode output as model-generated or as executed test evidence.

## Features

- Dark, responsive debugging workspace.
- Example bug scenarios to try immediately.
- Nebius Token Factory integration through the OpenAI-compatible chat completions API.
- Server-side API key handling; keys are kept in process memory and are not written to disk.
- Clearly separated live-model and demo modes.
- Safe-by-default workflow: the MVP proposes code and tests but does not execute arbitrary model-generated code.
- Downloadable JSON report and copyable patch text.
- Health endpoint and automated API tests.

## Run locally

Requires Python 3.11+.

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app:app --reload
```

Open http://127.0.0.1:8000.

## Deploy a demo

A Docker-based Render blueprint is included in `render.yaml`. Import this repository in Render and create the service from the blueprint. It deploys in demo-only mode and disables public changes to model credentials. To enable live inference later, add `NEBIUS_API_KEY` and `NEBIUS_MODEL` as private service environment variables in Render, and put the service behind suitable access controls/rate limits before allowing public live inference. Do not switch runtime configuration on for a public service.

## Enable live Nebius inference

1. Obtain access to Nebius Token Factory and confirm that your account can call an NVIDIA Nemotron model.
2. In PatchPilot, open **Model connection**, paste your API key, and enter the exact model ID shown as available in your Token Factory account. The key is held in server memory only until the process stops; it is not saved to `.env` or logged by this app.
3. Select **Live model** and analyze a bug.

Default API base URL: `https://api.tokenfactory.nebius.com/v1`. If Nebius gives your account a different documented endpoint, use that endpoint in the connection panel. Do not commit API keys, share them in screenshots, or place them in frontend JavaScript.

If you don't have access/credits yet, use **Demo mode** to explore the UI. Demo output is illustrative, not an actual model response and not proof that a patch works. A submission to the Nebius x NVIDIA hackathon must use Nebius infrastructure and an NVIDIA open-source model in the actual working project.

## How the verification-first workflow works

1. Describe the observed bug and provide the relevant source code.
2. PatchPilot asks the configured model for a root-cause analysis, minimal unified diff, regression-test proposal, and explicit risks.
3. Review the model output. The app does **not** claim a patch passed tests because it has not executed arbitrary project code.
4. Export the report for review or downstream testing in a separately isolated environment.

## API

- `GET /api/health` — health and connection status.
- `GET /api/config` — safe configuration status (never returns the API key).
- `POST /api/config` — set/clear the in-memory model connection.
- `POST /api/analyze` — analyze a bug using demo mode or the configured model.

## Tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## Security notes

- Intended for local development; do not expose the server publicly without adding authentication, rate limits, CSRF protections, and production hardening.
- Never run untrusted repositories or model-generated commands on the host. A future test runner should use an isolated, resource-limited container.
- API keys are stored in process memory only and are lost when the server restarts.

## Technology

- FastAPI + Uvicorn
- OpenAI Python SDK against Nebius Token Factory's OpenAI-compatible endpoint
- NVIDIA Nemotron model selected by the user from their available model catalog

## License

MIT — see [LICENSE](LICENSE).

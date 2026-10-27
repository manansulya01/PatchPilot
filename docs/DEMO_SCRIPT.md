# PatchPilot — 3-Minute Demo Script

Keep the recording under three minutes. Use a clean browser window and hide secrets.

## 0:00–0:20 — The problem
"AI can suggest code that looks right. But a patch is not proof. PatchPilot separates a repair proposal from verified evidence."

## 0:20–0:45 — The input
Show the checkout bug report and the short Python function. Explain expected versus actual behavior.

## 0:45–1:10 — Show real model usage
Open Model Connection. Show the exact NVIDIA Nemotron model name and that the request is routed through Nebius Token Factory. Never show the API key. Run a live analysis. If live inference is not configured, do not pretend demo mode is a model call. Live mode sends the bug report and source code to Nebius.

## 1:10–2:05 — Inspect the result
Walk through the root-cause hypothesis, proposed diff, patch preflight, skeptical second-pass review, regression-test proposal, assumptions, risks, and SHA-256 input/patch fingerprints. Export the JSON report.

## 2:05–2:35 — Explain verification honestly
Point at "NOT RUN." Explain that the current MVP does not execute arbitrary model-generated code, so it refuses to claim tests passed. If a separately isolated test runner is implemented before recording, demonstrate the original regression test failing and the patched test passing using actual logs.

## 2:35–2:55 — Close
"PatchPilot treats AI-generated fixes as hypotheses. The goal is not more confident code generation — it's a clearer path from a bug report to evidence."

## Recording checklist
- [ ] Live Nebius/NVIDIA model request visibly succeeds.
- [ ] Model ID is visible; secret key is hidden.
- [ ] Video is public and under three minutes.
- [ ] The interface shown is the actual running app.
- [ ] No simulated output is presented as live inference.
- [ ] No test is described as passed unless it was executed.

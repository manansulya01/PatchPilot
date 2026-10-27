# PatchPilot — Devpost submission pack

This is a copy-ready starting point for the Nebius x NVIDIA hackathon. Replace every bracketed field and verify every claim before submitting. Do not claim a successful live model request or a deployed demo until you have confirmed it yourself.

## Project title

PatchPilot — Verification-First AI Debugging

## Tagline

**A generated patch is a hypothesis, not proof.**

## Short description

PatchPilot helps developers investigate bugs, propose minimal code repairs, and inspect risks and regression-test suggestions—while clearly separating AI-generated proposals from evidence that code actually ran.

## Project description

AI coding assistants can produce patches that look convincing but miss the root cause, weaken tests, or introduce regressions. PatchPilot is built around a simple rule: never confuse a plausible fix with a verified fix.

A developer provides a bug report and the relevant source snippet. PatchPilot returns a root-cause hypothesis, a proposed unified diff, a regression-test suggestion, and explicit assumptions and risks. A heuristic patch preflight flags selected risky patterns and malformed or oversized diffs. An optional second pass asks the configured model to challenge the proposal. Exported reports include SHA-256 fingerprints of the submitted input and proposed patch, making the reviewed artifacts easier to identify later.

PatchPilot is deliberately transparent about what it has and has not verified. The current MVP does not execute arbitrary generated code, so test status remains **NOT RUN** unless a real, separately isolated test runner has executed it. A clean heuristic scan is not presented as proof of correctness or security.

The app supports deterministic demo mode for exploration and a live inference path through Nebius Token Factory's OpenAI-compatible API. The live path is intended to use an NVIDIA open-source Nemotron model selected from the account's available catalog. The live model ID, latency, and result should be shown in the demo only after a real request succeeds.

## How Nebius and NVIDIA are used

**Complete this section after a successful real request.**

- **Inference platform:** Nebius Token Factory.
- **NVIDIA model:** [exact model name and ID confirmed in the account].
- **Verified live request:** [date, result, and latency from the preflight or app's connection test].
- **Role in the app:** the configured model analyzes the supplied bug report and code, proposes a minimal patch and regression test, and can perform a separate skeptical review pass.
- **Evidence:** [link to public demo video and/or a redacted screenshot showing model ID and successful request, with credentials hidden].

Do not describe demo mode as model inference. Do not claim that the model's patch passed tests unless you have actual test-run evidence.

## What makes it different

- **Verification status is explicit:** proposals are not mislabeled as passing fixes.
- **Reviewable output:** root-cause hypothesis, unified diff, regression-test proposal, assumptions, and risks appear together.
- **Patch preflight:** heuristic warnings help focus human review, without pretending to be a full security analyzer.
- **Artifact traceability:** SHA-256 fingerprints identify the input and proposed patch in the exported report.
- **Safe default:** no arbitrary model-generated code is executed by the current MVP.

## Built with

- Python and FastAPI
- OpenAI Python SDK using Nebius Token Factory's OpenAI-compatible endpoint
- NVIDIA Nemotron model (fill in the exact model ID after verification)
- HTML, CSS, and JavaScript
- pytest and GitHub Actions

## What we learned

PatchPilot reinforced that a useful AI developer tool must make uncertainty visible. Producing a patch is only one step: developers also need review context, a suggested regression test, traceable artifacts, and an honest account of whether verification actually happened.

**Replace or supplement this paragraph with your real experience** after using the service: note onboarding friction, model availability, API compatibility, measured latency, output quality on your chosen bug, and one thing you would improve in Nebius Token Factory or the model documentation. Do not invent feedback.

## Limitations and next steps

The current MVP does not run generated code. The patch preflight is heuristic and can miss issues or flag safe code. The optional second pass uses the same configured model, so it is not an independent reviewer. Before enabling live inference on a public hosted endpoint, the deployment needs authentication, rate limits, request-size controls, and cost/abuse safeguards. A future test runner should use a disposable, resource-limited sandbox with no secrets and restricted network access.

## Links — fill in before submitting

- **Public working demo:** [actual URL; verify it loads in a private/incognito window]
- **Public source repository:** https://github.com/manansulya01/PatchPilot
- **Public demo video (under 3 minutes):** [YouTube URL; verify visibility is Public]
- **License:** MIT
- **Selected track:** Coding and Agentic Engineering (re-evaluate if the final implementation/track fit changes)

## Final submission checklist

- [ ] A real live request to Nebius Token Factory succeeds using an NVIDIA open-source model.
- [ ] The exact model ID, latency, and actual behavior have been recorded.
- [ ] The demo URL works for a reviewer without logging in, or the event's allowed exception applies.
- [ ] The public YouTube demo is under 3 minutes and shows the actual running app.
- [ ] No API key, token, private source, or other secret appears in the video or repository.
- [ ] README has setup instructions and explains both Nebius and NVIDIA usage.
- [ ] Repository license is present and public.
- [ ] Track, description, links, and required tool feedback are completed in Devpost.
- [ ] Any pre-existing code or concept is accurately disclosed, with hackathon-period changes described honestly.
- [ ] The final description makes no unverified claims about model use, deployment, execution, correctness, or security.

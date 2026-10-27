# PatchPilot — Hackathon Submission Draft

> Update this document with verified facts before submitting. Do not claim a live Nebius/NVIDIA model call until you have run one successfully and captured evidence.

## Track

Coding and Agentic Engineering.

## Short description

PatchPilot is a verification-first debugging workspace that helps developers investigate a bug, request a minimal repair proposal, and review a regression-test suggestion alongside explicit assumptions and risks. Its core principle is simple: a generated patch is a hypothesis, not proof.

## Problem

AI-generated code can look plausible while missing the underlying bug, weakening tests, or introducing regressions. Developers need a clear way to separate a model's proposed repair from evidence that the repair actually works.

## What we built

PatchPilot provides a dark, responsive workspace for a bug report and relevant source snippet. It can return a root-cause hypothesis, a proposed unified diff, a regression-test proposal, and risks/assumptions. The report includes SHA-256 fingerprints for the submitted input and proposed patch, a heuristic patch preflight, and an optional second-pass skeptical review. It explicitly marks verification as NOT RUN because the current MVP does not execute arbitrary generated code. This prevents the product from presenting unverified suggestions as successful repairs.

## Architecture

- FastAPI backend serves the product UI and API.
- OpenAI-compatible client connects to Nebius Token Factory.
- The operator selects the exact NVIDIA Nemotron model ID available to their account.
- A second-pass reviewer can critique the first response using the same configured model; this is a separate pass, not an independent model or proof. A deterministic demo mode allows reviewers to explore the interface without credentials; demo output is clearly labeled as simulated and is not a model call.
- The MVP does not execute model-generated code. A future isolated test runner should use a disposable, resource-limited container.

## NVIDIA / Nebius usage — complete before submission

- [ ] Record the exact NVIDIA open-source model name and model ID used. Suggested starting ID: `nvidia/Nemotron-3_5-Lightning`; verify it is available to your account.
- [ ] Capture evidence of a successful live request through Nebius Token Factory.
- [ ] Describe what Token Factory enabled in the workflow.
- [ ] Record real latency, errors, and relevant model limitations.
- [ ] Confirm the live demo uses Nebius infrastructure and an NVIDIA open-source model.

Current status: integration code exists, but live inference must be configured and tested before these claims can be made.

## Demo URL

Add the actual deployed URL after deploying from the Render blueprint. Do not submit a guessed URL.

## Repository

https://github.com/manansulya01/PatchPilot

## Demo video outline

1. State the problem: code suggestions are not proof.
2. Load the sample bug and source.
3. Show the model connection and exact NVIDIA model, with credentials hidden.
4. Run a live analysis and show the root-cause hypothesis, patch, and regression test.
5. Emphasize that tests are marked NOT RUN unless an actual isolated test runner ran them.
6. End with the product's verification-first principle.

## Significant updates during the submission period

If this repository was empty before work for this hackathon, accurately describe the initial implementation and date. If any code or concept existed before the official submission period, explain which components were pre-existing and which were newly developed. Do not claim all work is new unless that is true.

## Technology feedback

Write this section from actual experience only after testing. Include:
- Onboarding and key setup friction.
- Model availability and documentation clarity.
- API compatibility and request reliability.
- Latency and output quality on the chosen debugging task.
- What went well and what you would improve.

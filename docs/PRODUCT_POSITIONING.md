# Product positioning and differentiation

## The problem PatchPilot targets

PatchPilot is a developer-facing debugging workbench, not a claim that a new patch-generation algorithm outperforms established research systems. It focuses on making the *review of a proposed fix* more inspectable:

1. A structured bug report and relevant source snippet.
2. A model-generated diagnosis, proposed diff, and regression-test suggestion.
3. A heuristic preflight over added diff lines, with explicit warnings and limitations.
4. An optional second call to the same configured model that challenges the first response and proposes missing tests.
5. A downloadable report containing input and patch SHA-256 fingerprints and an explicit verification status.

## What makes the approach useful

- **Review-first UI:** findings, risks, test ideas, and provenance are presented together rather than hidden in raw chat.
- **Challenge pass:** a separate model call is prompted to look for flaws in the proposed patch. It is not a truly independent model and can still agree with an incorrect answer.
- **Preflight signals:** a small deterministic ruleset flags selected risky patterns and malformed/oversized diffs. It is not a complete static analyzer or security boundary.
- **Evidence honesty:** model output, heuristic findings, and actual execution evidence are separate concepts. The current version does not execute user code and therefore never claims a fix passed tests.

## Current limitations

- No repository checkout, AST-level semantic analysis, automated patch application, sandbox, or real test execution.
- No benchmark results demonstrating superiority over published repair agents.
- The same configured model is used for generation and the optional second-pass critique.
- The heuristic rules can miss risky code and can flag harmless code.
- Live inference requires a working Nebius Token Factory account and an available NVIDIA open model.

## Roadmap priority

The most valuable next milestone is a safe, disposable test runner that demonstrates a red-green regression loop with inspectable logs. It should run only in a properly isolated, resource-limited environment, never directly on the web server host. Until that exists, the app should continue to label verification as NOT RUN.

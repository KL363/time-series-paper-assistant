# Changelog

## [2.2.0] - 2026-11-05

- Enforced one stage or core module per reply, progressing only on an explicit user request.
- Ordered stage explanations as motivation, computation, equations, tensor shapes and implementation, with source-backed pseudocode when needed.
- Required stage endings to give key conclusions and genuine open questions, then stop; follow-up questions stay within the current stage.
- Allowed an explicit one-shot complete analysis to bypass stage waits and the default reply budget without forcing a condensed summary.
- Synchronized supporting guidance, examples and the default prompt while preserving paper citations and chat-first output.

## [2.1.0] - 2026-11-03

- Made short, user-paced turns the default: start with an architecture overview, then explain one topic per reply.
- Added a default total reply budget covering prose, code, tables, formulas and references.
- Defined continue, skip and topic-jump behavior without repeated introductions or state files.
- Split code walkthroughs and teaching pseudocode into complete small units while preserving paper references.
- Updated the entrypoint, supporting guidance, bilingual documentation and default prompt to prevent full-paper requests from producing one oversized reply.

## [2.0.0] - 2026-10-23

- Renamed the skill invocation and installation directory to `lingerskill`; the repository name may remain `time-series-paper-auditor`.
- Added explicit-only invocation, including `使用lingerskill给我讲解这篇论文`, with implicit invocation disabled in the client configuration.
- Refocused the default workflow on architecture, data flow, module functions, training and precise paper references.
- Made module-origin analysis distinguish reuse, composition, adaptation, new mechanisms, and data or training contributions.
- Added official-code walkthroughs and teaching pseudocode for missing or inaccessible code, with facts, assumptions and unknowns kept distinct.
- Made chat the default output; notes, cards and state files are no longer generated automatically.
- Moved experiment review, research proposals and file exports to explicitly requested extensions.
- Updated bilingual documentation, examples and validation to reflect the new behavior.

## [1.0.1] - 2026-10-23

- Prepared the first GitHub-ready open-source distribution.
- Added bilingual README, contribution guide, MIT license, `.gitignore`, and validation workflow.
- Declared `MIT` in the Agent Skill metadata.
- Core auditing workflow remains unchanged from 1.0.0.

## [1.0.0] - 2026-10-23

- Initial Agent Skill: stages 00–08 for deep-learning time-series paper analysis.
- Evidence rules, prompt library, note templates and optional PyTorch shape tracing..

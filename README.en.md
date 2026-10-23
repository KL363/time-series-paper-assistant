# Time-Series Paper Auditor

[中文](README.md) | English

**An open-source Agent Skill for auditing deep-learning time-series forecasting papers, from data pipelines and tensor shapes to paper–code alignment, novelty tracing, experiment review, and testable research hypotheses.**

This is not a generic paper summarizer. The goal is to make the technical analysis **traceable, reproducible, and evidence-aware**.

## Workflow

| Stage | Focus |
| --- | --- |
| 00 | Sources, scope and evidence rules |
| 01 | Problem definition and paper positioning |
| 02 | Data pipeline, split protocol and future-information availability |
| 03 | Model graph, equations and tensor-shape tracing |
| 04 | Cross-check paper formulas against actual model `forward()` code |
| 05 | Trace prior modules, adaptations, and novel mechanisms |
| 06 | Audit evaluation protocols, baselines and ablations |
| 07 | Derive falsifiable research hypotheses |
| 08 | Create reusable paper/module/research-idea cards |

Evidence tags: `[P]` paper, `[C-static]` inspected code, `[C-run]` actually executed, `[R]` prior art, `[I]` inference, `[U]` unverified.

## Installation

This repository follows the [Agent Skills specification](https://agentskills.io/specification). Clone the repository into a Skills directory supported by your agent, keeping the directory named `time-series-paper-auditor` so `SKILL.md` is at its root.

```bash
git clone https://github.com/<YOUR-USERNAME>/time-series-paper-auditor.git
```

Replace `<YOUR-USERNAME>` with the repository owner after publication. Installation paths, automatic discovery and plugin ZIP requirements vary by client; not every ChatGPT account or workspace supports uploading custom skills.

## Example prompt

```text
Use time-series-paper-auditor in deep mode to analyze this time-series
forecasting paper. Start with stages 00–03: reconstruct the data pipeline,
model graph, detailed tensor shapes, and information mixing dimensions.
Cite paper/code evidence, distinguish verified facts from inferences,
and preserve unresolved questions for later stages.
```

For detailed Chinese usage instructions, see [`references/user-guide.zh-CN.md`](references/user-guide.zh-CN.md). Prompt examples are in [`references/prompt-library.md`](references/prompt-library.md).

## Local validation

```bash
python -m pip install pyyaml
python scripts/validate_skill.py .
python -m compileall -q scripts
```

The optional PyTorch shape-hook helper in `scripts/trace_shapes.py` requires a trusted PyTorch environment and an already constructed model. Module hooks do not trace every functional tensor operation.

## Contributing and license

Issues and pull requests are welcome; see [CONTRIBUTING.md](CONTRIBUTING.md). Licensed under [MIT](LICENSE). Before publication, ensure you have rights to license every included file. This repository intentionally does not redistribute papers, datasets, model weights or private research data.

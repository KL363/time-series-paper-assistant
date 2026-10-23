# lingerskill

[中文](README.md) | English

**A paper-reading skill for understanding model architecture, data processing, module design and training in deep-learning time-series forecasting papers, with precise pointers back to the paper.**

## Explicit invocation

Provide a paper PDF or accessible link, then ask:

```text
Use lingerskill to explain this paper.
Focus on its architecture, data flow, module functions and module origins.
Point me to the relevant sections, figures and equations.
Use official code when available; otherwise explain preprocessing,
the forward pass and training with clearly labeled teaching pseudocode.
Answer directly in chat.
```

The Chinese trigger is `使用lingerskill给我讲解这篇论文`. In clients that support it, explicitly select the skill with `$lingerskill`.

Ordinary requests to read or summarize a paper do not activate this skill. Follow-up questions about the same paper may continue an explicitly activated session; a new paper requires another explicit invocation. `agents/openai.yaml` sets `policy.allow_implicit_invocation: false`. Natural-language discovery depends on the client, so use `$lingerskill` or its skill picker when needed.

## Reading experience

- Explain the overall computation graph, what each module does, and how modules connect.
- Trace raw data through preprocessing, normalization, patching or frequency transforms when present, batching, the model, predictions and loss. Explain tensor dimensions and the distinction between training and inference.
- Place source pointers beside key explanations: sections, clearly identified PDF page numbering, figure or equation numbers, and code files/functions or line references when available.
- Distinguish direct reuse, composition, adaptation, new mechanisms, and data or training contributions. Separate author claims, prior-work evidence and interpretation.
- Read official code statically along the data-loading → forward → loss/training → prediction path. When code is absent or inaccessible, use teaching pseudocode and mark assumptions and unspecified details.

The default output is a conversation, with no generated Markdown, text, YAML or state files. Running repositories, reproducing experiments and auditing implementation quality are not default tasks. Briefly explain discrepancies that affect understanding; expand into experiment review, research proposals or exports only when explicitly requested.

## Workflow

Stages organize the reading process; they are not a mandatory sequence of answer headings.

| Stage | Focus | Scope |
| --- | --- | --- |
| 00 | Available paper, official code and supporting materials | As needed |
| 01 | Research problem, inputs/outputs and architecture overview | Core |
| 02 | Data processing, flow and tensor meaning | Core |
| 03 | Module design, functions, equations and connections | Core |
| 04 | Static code walkthrough or teaching pseudocode | Core |
| 05 | Module origins and author contributions | Core |
| 06 | Experiments, ablations and evaluation | Explicit request only |
| 07 | Research hypotheses and proposed changes | Explicit request only |
| 08 | Exported notes or cards | Explicit request only |

Evidence tags, used where useful: `[P]` paper, `[C-static]` inspected code, `[C-run]` actually executed code, `[R]` prior work, `[I]` inference, `[U]` unconfirmed. Teaching pseudocode is not presented as the author's implementation, and static inspection is not reported as execution.

See the [Chinese user guide](references/user-guide.zh-CN.md) and [prompt library](references/prompt-library.md).

## Installation

Install the complete project in your client's supported Skills directory, naming the installed folder `lingerskill`. Keep `SKILL.md` and its sibling resource directories together.

```bash
git clone https://github.com/<YOUR-USERNAME>/time-series-paper-auditor.git lingerskill
```

Replace `<YOUR-USERNAME>` with the repository owner; this URL is an installation example. The repository or existing checkout may retain the name `time-series-paper-auditor`; the invocation name and new installation directory are `lingerskill`. Supported paths, discovery and package formats vary by client.

## Local validation

```bash
python -m pip install pyyaml
python scripts/validate_skill.py .
python -m compileall -q scripts
```

The optional `scripts/trace_shapes.py` helper is not part of the default reading workflow. It requires an existing trusted PyTorch model environment and traces module boundaries, not every functional tensor operation.

## Contributing and license

Contributions that improve explanations, source pointers and module-origin analysis are welcome; see [CONTRIBUTING.md](CONTRIBUTING.md). Licensed under [MIT](LICENSE). This repository does not redistribute third-party papers, datasets, model weights or private research data.

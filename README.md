# Time-Series Paper Auditor（时序预测论文深度阅读 Skill）

[English](README.en.md) | 中文

**一个开源的 Agent Skill，用于系统性审读深度学习时序预测论文：从数据管线、模型计算图、Tensor Shape 和 PyTorch `forward()`，延伸到创新性溯源、实验可信度与可证伪研究假设。**

> 本项目不是论文摘要生成器。目标是使论文结论**可定位、计算过程可追踪、实验声称可审计**。

## 能做什么

| 阶段 | 目标 | 主要产物 |
| --- | --- | --- |
| 00 | 建立任务、来源和证据规则 | 来源清单与未解问题 |
| 01 | 论文定位与问题定义 | 研究问题卡 |
| 02 | 复盘数据管线与未来信息边界 | 数据流与泄漏风险表 |
| 03 | 还原模型架构、公式与 Tensor Shape | 模块调用图与逐算子 Shape 表 |
| 04 | 核验论文和实际代码 | 公式—代码映射、运行核验建议 |
| 05 | 追踪模块来源及真正改进之处 | 创新性溯源矩阵 |
| 06 | 审核实验设计与消融证据 | 评测和缺失对照表 |
| 07 | 提炼可证伪的领域研究假设 | 最小实验方案 |
| 08 | 沉淀可复用科研知识卡片 | Paper / Module / Research Idea Cards |

**证据标签：** `[P]` 论文、`[C-static]` 代码静态确认、`[C-run]` 实际运行确认、`[R]` 前作、`[I]` 推断、`[U]` 未验证。AI 不应把推断当成事实，或把静态读代码说成已经运行验证。

## 安装

本项目遵循 [Agent Skills 开放格式](https://agentskills.io/specification)。`SKILL.md` 是入口；`references/`、`assets/`、`scripts/` 是按需使用的补充资源。

### Agent Skills 兼容客户端

将整个项目目录克隆或复制到客户端支持的 Skills 搜索路径，**保留项目文件夹名 `time-series-paper-auditor`**，使 `SKILL.md` 位于其根目录：

```bash
git clone https://github.com/<YOUR-USERNAME>/time-series-paper-auditor.git
```

> 将 `<YOUR-USERNAME>` 换成仓库实际所有者。本仓库公布前，上面的地址仅是安装示例，并非真实链接。不同客户端的自动发现路径和调用方式可能不同，请参考该客户端当前文档。

### ChatGPT / 插件式分发

不同产品对 Skill 和 Plugin 包的安装格式要求可能不同；GitHub 项目源代码**不是**所有插件上传界面可直接使用的 ZIP。若使用针对插件格式打包的 ZIP，请从本项目的 Releases 下载相应发布附件，并阅读对应版本说明。当前是否支持自定义 Skill / Plugin 上传取决于产品、账号及工作区权限。

## 开始使用

上传论文 PDF，尽可能提供附录、官方仓库及具体 commit/tag，然后告诉 AI：

```text
请使用 time-series-paper-auditor，以 deep 模式分析这篇时序预测论文。
优先分析：
1. 原始数据到模型输入的完整管线；
2. 每个模块的真实计算方式与 Tensor Shape；
3. 论文公式与 PyTorch forward 的对应关系；
4. 作者复用、改造或新增了什么机制；
5. 实验是否支持创新声明。
先执行阶段 00–03，保留证据及尚未解决的问题，不要一次输出全部阶段。
```

可选模式：`quick`（初筛）、`deep`（默认精读）、`reproduce`（复现与创新）、`stage`（仅指定阶段）。详细用法见 [`references/user-guide.zh-CN.md`](references/user-guide.zh-CN.md)，可复制的指令见 [`references/prompt-library.md`](references/prompt-library.md)。

## 项目结构

```text
time-series-paper-auditor/
├── SKILL.md                    # Agent Skills 入口
├── references/                 # 各阶段说明、指令库、使用指南
├── assets/                     # 论文卡、模块卡、研究假设、会话状态模板
├── scripts/
│   ├── trace_shapes.py         # 可选：PyTorch 叶子模块 Shape Hooks
│   └── validate_skill.py       # 本项目的轻量结构检查
├── .github/workflows/validate.yml
├── README.md / README.en.md
├── CONTRIBUTING.md
├── CHANGELOG.md
└── LICENSE
```

## 本地验证

```bash
python -m pip install pyyaml
python scripts/validate_skill.py .
python -m compileall -q scripts
```

Shape Hook 用法：

```python
from scripts.trace_shapes import attach_shape_hooks

handles = attach_shape_hooks(model)  # model 是你已经安全加载的 PyTorch 模型
try:
    prediction = model(example_input)
finally:
    for h in handles:
        h.remove()
```

Shape Hook 仅记录 Module 边界；`permute`、`reshape` 等函数式张量操作需要额外断言/日志。不要未经检查直接运行第三方仓库依赖或脚本。

## 局限性和科研规范

- 没有实际阅读论文或代码，就不能声称完成相应的核验。
- 结构分析≠运行复现；统计相关性≠模块工作机制的因果证明。
- 只有相似模块名称，不能证明论文抄袭；创新性需要核实参考文献和具体机制。
- 此仓库不包含任何第三方论文 PDF、数据集、模型权重或私人研究材料。

## 参与贡献

欢迎提交 Issue / Pull Request，尤其欢迎增加时序预测特有的分析检查项、修正张量分析错误和提供**不包含第三方受限材料**的可复现示例。贡献说明见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可证

[MIT License](LICENSE)。在你自己的 GitHub 账号发布前，请确认你有权对其中全部文件采用该许可证；如果希望改用 Apache-2.0 或其他协议，请在发布前统一修改 `LICENSE` 和 `SKILL.md` 的 `license` 字段。

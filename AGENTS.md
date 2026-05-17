# AGENTS.md

Sonic Atlas 开发与研究指南。

## Language Policy

- **英文文档**（`docs/`）为研究工作的源文件（source of truth）
- **中文文档**（`docs/zh/`）为英文文档的翻译版本，供中文阅读参考
- 撰写或修改任何文档时，必须同步更新对应的中文/英文版本
- 研究、实验、代码实现以英文文档为准

## Document Structure

```text
docs/
├── vision.md                              # EN
├── architecture.md                        # EN
├── roadmap.md                             # EN
├── literature/
│   ├── 00_research_plan.md                # EN
│   ├── 01_first_round_review.md           # EN
│   ├── 02_feature_taxonomy.md             # EN
│   └── 03_experiment_protocol.md          # EN
├── foundations/
│   ├── fundamental_analysis.md            # EN
│   ├── 01_discretization_precision.md     # EN
│   ├── 02_phase_perception.md             # EN
│   ├── 03_wave_packets.md                 # EN
│   ├── 04_timbre_characterization.md      # EN
│   └── 05_cnn_feature_extraction.md       # EN
└── zh/                                    # 中文翻译
    ├── vision.md
    ├── architecture.md
    ├── roadmap.md
    ├── literature/
    │   ├── 00_research_plan.md
    │   ├── 01_first_round_review.md
    │   ├── 02_feature_taxonomy.md
    │   └── 03_experiment_protocol.md
    └── foundations/
        ├── fundamental_analysis.md
        ├── 01_discretization_precision.md
        ├── 02_phase_perception.md
        ├── 03_wave_packets.md
        ├── 04_timbre_characterization.md
        └── 05_cnn_feature_extraction.md
```

## Workflow Rules

1. **新建文档**：同时创建英文版（`docs/`）和中文版（`docs/zh/`）
2. **修改文档**：先改英文版，再同步中文版
3. **研究工作**：阅读、引用、实验设计均以英文文档为准
4. **中文文档**：保持与英文版相同的章节结构，代码块和公式不翻译
5. **Foundation 文档**：基础理论文档原为中文，中文版直接复制

## Language Sync Checklist

新建或修改文档时，确保：
- [ ] 英文版路径：`docs/{path}.md`
- [ ] 中文版路径：`docs/zh/{path}.md`
- [ ] 章节结构一致
- [ ] 代码块 / 公式 / 表格数据不翻译
- [ ] 技术术语保留英文（如 latent, embedding, token, onset, centroid 等）

## Repository Structure

```text
sonic-atlas/
├── AGENTS.md
├── README.md
├── docs/                                  # 研究文档（EN + ZH）
├── demos/                                 # 交互式 HTML 演示
├── experiments/                           # 可运行实验
├── data/                                  # 本地数据（gitignored）
└── notebooks/                             # 探索性分析
```

## Current Phase

Phase 2 — Baseline Feature Extraction。详见 [docs/roadmap.md](docs/roadmap.md)。

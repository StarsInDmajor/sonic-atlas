# Architecture

Sonic Atlas 采用 research-to-system 的仓库结构：理论文档、交互演示、可运行实验和数据分层管理。

## Repository Layers

```text
sonic-atlas/
├── docs/          # 研究计划、文献综述、基础理论、路线图
├── demos/         # 交互式 HTML 可视化与概念演示
├── experiments/   # 可运行实验、预计算脚本、原型算法
├── data/          # 本地数据入口（gitignored except .gitkeep）
└── notebooks/     # 探索性分析
```

## Conceptual System

```text
Raw Audio
  ↓
Decomposition Layer
  - STFT / Mel / CQT / CWT
  - Gabor atoms / NMF / K-SVD
  - source separation
  - neural codec tokenization

  ↓
Feature Layer
  - psychoacoustic descriptors
  - pretrained embeddings
  - self-supervised representations
  - generative latents / discrete tokens

  ↓
Validation Layer
  - reconstruction metrics
  - ABX / MUSHRA / subjective labels
  - disentanglement / controllability

  ↓
Creative Layer
  - feature trajectory
  - latent interpolation
  - corpus navigation
  - synthesis parameter mapping
```

## Directory Responsibilities

| Directory | Responsibility |
|---|---|
| `docs/literature/` | 研究计划、literature review、证据矩阵 |
| `docs/foundations/` | 物理声学、心理声学、时频分析、音色、CNN 基础 |
| `demos/foundations/` | 基础概念的交互演示 |
| `demos/creative_features/` | 主线系统的交互原型 |
| `experiments/creative_features/` | 主线实验：baseline features、embedding comparison、latent traversal、creative mapping |
| `experiments/wave_packet_sparse/` | 既有波包稀疏重建实验 |
| `data/raw/` | 原始音频样本（不提交） |
| `data/processed/` | 预处理特征与中间数据（不提交） |
| `data/external/` | 外部下载数据（不提交） |

## Evolution Plan

1. 文献综述稳定后，形成 `docs/literature/02_feature_taxonomy.md`。
2. 实验原型从 `experiments/creative_features/01_baseline_features/` 开始。
3. 成熟实验转化为 `demos/creative_features/` 中的浏览器交互演示。
4. 最终形成一个 feature-space browser：导入声音、提取特征、导航空间、生成创作路径。

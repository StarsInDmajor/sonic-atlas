# Roadmap

## Phase 0 — Foundations Completed

Status: mostly done.

- [x] 听觉离散化精度
- [x] 相位感知
- [x] 波包 / Gabor / CQT / CWT
- [x] 音色 MDS 空间
- [x] CNN 声谱图特征
- [x] 频谱表示参考页
- [x] 第一轮 literature review

## Phase 1 — Feature Taxonomy

Goal: 明确哪些声音特征可作为创作材料。

- [x] 写 `docs/literature/02_feature_taxonomy.md`
- [x] 建立四层特征体系：心理声学、稀疏原子、embedding、latent/token
- [x] 为每类特征定义：可闻性、可解释性、可控性、重建性、创作性
- [x] 写 `docs/literature/03_experiment_protocol.md`，把 taxonomy 转化为 baseline 实验协议

## Phase 2 — Baseline Feature Extraction

Goal: 用可解释特征建立第一个 feature-space browser 原型。

- [x] 实现 baseline feature extraction pipeline (`experiments/creative_features/01_baseline_features/`)
  - [x] `schemas.py` — 统一字段名、常量、feature groups
  - [x] `make_manifest.py` — 扫描语料目录生成 manifest
  - [x] `extract_features.py` — 提取 P0/P1 features
  - [x] `project_features.py` — z-score 归一化 + PCA/UMAP 投影 + kNN 检索
  - [x] `evaluate_features.py` — correlation matrix + category summary + 评估模板
  - [x] `prepare_corpus.py` — 从 ESC-50 / TinySOL 下载并整理语料
- [x] 创建小型声音语料 (60 clips): 20 乐器 + 20 自然声 + 20 城市/物体声
  - 来源: ESC-50 (CC-BY-NC) + TinySOL (CC-BY 4.0) + Philharmonia Orchestra (CC)
  - 乐器: flute, clarinet, oboe, bassoon, alto sax, accordion, violin, cello, trumpet, french horn
  - 自然: rain, thunderstorm, sea waves, fire, crickets, birds, water drops, wind
  - 城市: clock alarm, siren, car horn, engine, train, door, helicopter, typing, glass
- [x] 运行 `extract_features.py` 提取特征 (60/60 成功，79 维)
- [x] 运行 `project_features.py` 生成投影与检索 (4 groups × PCA+UMAP+kNN)
- [ ] 手动听检并填写 evaluation_notes.md
- [ ] 评估特征是否符合直觉标签

Target directory:

```text
experiments/creative_features/01_baseline_features/
```

## Phase 3 — Embedding Comparison

Goal: 比较预训练音频 embedding 的聚类、检索、语义导航能力。

Candidate models:

- PANNs
- AST
- BYOL-A
- AudioMAE
- CLAP
- OpenL3

Target directory:

```text
experiments/creative_features/02_embedding_comparison/
```

## Phase 4 — Latent Traversal and Audibility

Goal: 测试生成式 latent 是否可闻、可控、可创作。

Candidate models:

- DDSP
- RAVE
- EnCodec / DAC
- AudioLDM / CLAP-conditioned generation

Tests:

- latent traversal
- ABX audibility
- semantic rating
- creative usefulness rating

Target directory:

```text
experiments/creative_features/03_latent_traversal/
```

## Phase 5 — Creative Mapping Prototype

Goal: 把特征轨迹转化为音乐结构。

Prototype:

- feature-space browser
- corpus navigation
- latent morphing
- feature trajectory editor
- audio rendering / export

Target directories:

```text
experiments/creative_features/04_creative_mapping/
demos/creative_features/
```

## Phase 6 — Integrated Composition System

Goal: 形成可持续使用的声音创作研究平台。

Capabilities:

1. 导入声音素材库
2. 自动提取多层特征
3. 在 2D/3D 空间中浏览与试听
4. 根据语义或感知坐标检索
5. 生成 feature trajectory
6. 映射到合成、重组或 latent generation
7. 输出声音草图或作品片段

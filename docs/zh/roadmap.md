# 路线图

## Phase 0 — 基础理论（已完成）

状态：基本完成。

- [x] 听觉离散化精度
- [x] 相位感知
- [x] 波包（Wave Packet） / Gabor / CQT / CWT
- [x] 音色 MDS 空间（Multidimensional Scaling，多维尺度分析，将听觉相似性映射为低维几何距离）
- [x] CNN 声谱图特征（CNN，Convolutional Neural Network，卷积神经网络；在声谱图上提取特征的模型）
- [x] 频谱表示参考页
- [x] 第一轮文献综述

## Phase 1 — 特征分类体系

目标：明确哪些声音特征可作为创作材料。

- [x] 写 `docs/literature/02_feature_taxonomy.md`
- [x] 建立四层特征体系：心理声学（Psychoacoustics，研究人耳如何感知声音的学科）、稀疏原子（Sparse Atom）、嵌入（Embedding）、潜变量/标记（Latent/Token）
- [x] 为每类特征定义：可闻性、可解释性、可控性、重建性、创作性
- [x] 写 `docs/literature/03_experiment_protocol.md`，把 taxonomy 转化为 baseline 实验协议

## Phase 2 — 基线特征提取

目标：用可解释特征建立第一个 feature-space browser 原型。

- [x] 实现 baseline feature extraction pipeline (`experiments/creative_features/01_baseline_features/`)
  - [x] `schemas.py` — 统一字段名、常量、feature groups
  - [x] `make_manifest.py` — 扫描语料目录生成 manifest
  - [x] `extract_features.py` — 提取 P0/P1 features
  - [x] `project_features.py` — z-score 归一化（Z-Score Normalization，将数据标准化为均值 0、标准差 1） + PCA（主成分分析，Principal Components Analysis，线性降维） / UMAP（均匀流形近似与投影，Uniform Manifold Approximation and Projection，非线性降维）投影 + kNN（k 近邻检索，k-Nearest Neighbors）检索
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

目标目录：

```text
experiments/creative_features/01_baseline_features/
```

## Phase 3 — 嵌入比较（Embedding Comparison）

目标：比较预训练音频嵌入（Pretrained Audio Embedding，在大规模数据上训练的模型所提取的向量表示）的聚类、检索、语义导航能力。

候选模型：

- PANNs
- AST
- BYOL-A
- AudioMAE
- CLAP
- OpenL3

目标目录：

```text
experiments/creative_features/02_embedding_comparison/
```

## Phase 4 — 潜变量遍历与可闻性（Latent Traversal & Audibility）

目标：测试生成式潜变量（Generative Latent）是否可闻、可控、可创作。

候选模型：

- DDSP（Differentiable Digital Signal Processing，可微数字信号处理，将传统 DSP 与神经网络结合的合成方法）
- RAVE（Realtime Audio Variational autoEncoder，实时音频变分自编码器）
- EnCodec / DAC（Neural Audio Codec，神经音频编解码器）
- AudioLDM / CLAP 条件生成（CLAP，Contrastive Language-Audio Pretraining，音频-文本对比预训练）

测试：

- 潜变量遍历（Latent Traversal，在潜空间中沿特定方向移动以观察声音变化）
- ABX 可闻性测试（ABX Audibility Test）
- 语义评分（Semantic Rating）
- 创作有用性评分（Creative Usefulness Rating）

目标目录：

```text
experiments/creative_features/03_latent_traversal/
```

## Phase 5 — 创作映射原型（Creative Mapping Prototype）

目标：把特征轨迹（Feature Trajectory）转化为音乐结构。

原型功能：

- 特征空间浏览器（Feature-Space Browser）
- 语料库导航（Corpus Navigation）
- 潜变量变形（Latent Morphing，在潜空间中两个声音之间做平滑过渡）
- 特征轨迹编辑器（Feature Trajectory Editor）
- 音频渲染（Audio Rendering） / 导出

目标目录：

```text
experiments/creative_features/04_creative_mapping/
demos/creative_features/
```

## Phase 6 — 集成创作系统

目标：形成可持续使用的声音创作研究平台。

能力：

1. 导入声音素材库
2. 自动提取多层特征
3. 在 2D/3D 空间中浏览与试听
4. 根据语义或感知坐标检索
5. 生成特征轨迹（Feature Trajectory）
6. 映射到合成、重组或潜变量生成（Latent Generation）
7. 输出声音草图或作品片段

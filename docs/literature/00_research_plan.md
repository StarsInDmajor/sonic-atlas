# Research Plan: 基于机器学习声音抽象特征的音乐创作系统

> **课题目标**：通过机器学习方法，从音乐与自然声音中提取抽象声音特征，并将这些特征作为可听、可操作、可组合的音乐创作素材。

---

## 0. 课题定位

本课题关注的问题不是单纯的“音频分类”，也不是单纯的“声音合成”，而是：

> **如何从真实音频中分解、学习、筛选出具有感知意义和创作可操作性的抽象声音特征，并将这些特征转化为音乐创作材料。**

它横跨以下领域：

1. 音频分解与时频表示
2. 音色与声音纹理表征
3. 自监督 / 对比式 / 生成式音频表征学习
4. 心理声学与特征可闻性验证
5. 神经音频合成与 latent-space composition
6. 交互式声音设计与计算机音乐创作

建议将该方向作为 Sonic Atlas 的下一阶段研究模块，暂定名：

> **Creative Feature Lab：基于声音特征的音乐创作实验室**

---

## 1. Research Question

### Primary Question

**如何从音乐与自然声音中提取既具有抽象性、又具有听觉可辨性和创作可操作性的声音特征，并将这些特征转化为可用于音乐创作的素材？**

### Secondary Questions

#### SQ1. 一个正常音频应如何分解？

输入一段真实音频后，应将其分解为哪些层次？

可能层次包括：

1. **波形层**：raw waveform
2. **时频层**：STFT / CQT / CWT / Mel / Gammatone
3. **稀疏原子层**：Gabor atoms / wavelets / matching pursuit
4. **事件层**：onset, transient, sustain, decay, texture
5. **声源层**：source separation / object-level sound event
6. **语义层**：instrument, material, gesture, environment, emotion
7. **潜变量层**：latent embedding from VAE / contrastive learning / diffusion / neural audio codec

#### SQ2. 什么方法能提取更有效的抽象特征？

这里的“有效”至少包含四个标准：

| 标准 | 含义 |
|---|---|
| **重建有效** | 用特征可以较好重建原声音 |
| **分类有效** | 特征能区分乐器、声音类别、演奏技法、材质等 |
| **感知有效** | 特征变化在人耳听感中可察觉、可描述 |
| **创作有效** | 特征可以被控制、组合、变形、映射为音乐参数 |

候选方法包括：

- MFCC / spectral descriptors
- CQT / CWT / Gammatone features
- CNN / CRNN spectrogram embeddings
- self-supervised audio embeddings：wav2vec2, HuBERT, BYOL-A, AudioMAE
- audio-text embeddings：CLAP / LAION-CLAP
- neural codec embeddings：EnCodec, SoundStream, DAC
- generative latent spaces：VAE, DDSP, RAVE, diffusion audio models
- sparse learned dictionaries：K-SVD, NMF, sparse coding, Gabor OMP

#### SQ3. 抽象特征是否是人耳可闻的？

一个机器学习特征可以很有效，但未必可闻。需要区分：

| 类型 | 说明 |
|---|---|
| **可重建但不可解释** | 如 neural codec latent，能还原声音，但单个维度未必可听懂 |
| **可分类但不可操控** | 如分类 CNN embedding，可分辨乐器，但维度没有直接创作意义 |
| **可操控但不自然** | 如某些 VAE latent，插值可听但容易产生伪影 |
| **感知可解释** | 如 spectral centroid、attack time、roughness、inharmonicity |
| **创作可操作** | 如“明亮度”“粗糙度”“颗粒度”“空间感”“金属感”“有机感” |

#### SQ4. 抽象特征如何成为音乐创作素材？

需要从“分析特征”转换为“作曲参数”。可能形式包括：

1. **特征作为控制器**
   - spectral centroid → filter cutoff / brightness
   - onset density → rhythm density
   - roughness → harmonic tension
   - texture entropy → noise ratio / density

2. **特征作为音色坐标**
   - 在 timbre latent space 中移动、插值、聚类、采样。

3. **特征作为生成条件**
   - 用 CLAP text/audio embedding 控制 diffusion / RAVE / DDSP 生成声音。

4. **特征作为素材库索引**
   - 将自然声音或音乐片段嵌入到 latent space，按相似性、情绪、质感、动态检索。

5. **特征作为作曲结构**
   - 用特征轨迹构造音乐时间结构，例如：
     - low roughness → high roughness
     - natural noise → harmonic stable timbre
     - sparse transient → dense texture

---

## 2. Research Scope

### Domain

- Music Information Retrieval (MIR)
- Computational Auditory Scene Analysis
- Audio Representation Learning
- Neural Audio Synthesis
- Sound Design / Computer Music
- Psychoacoustics
- Interactive Music Systems

### Time Range

建议分两层：

1. **Foundational: 1990–2015**
   - MFCC, NMF, sparse coding, sinusoidal modeling, timbre MDS, classic psychoacoustics

2. **Modern ML: 2015–2026**
   - CNN spectrogram, self-supervised audio learning, neural codecs, RAVE, DDSP, CLAP, diffusion audio models

### Methodology Focus

本课题最终应进入实验系统，因此建议采用：

1. 文献调研
2. 方法分类
3. 小规模实验
4. 感知评估
5. 创作原型

### Audio Scope

| 类型 | 示例 | 作用 |
|---|---|---|
| **音乐声音** | 钢琴、吉他、弦乐、鼓、合成器 | 研究音高、音色、起奏、延音 |
| **自然声音** | 风、水、鸟、雨、火、昆虫 | 研究纹理、噪声、事件密度 |
| **城市/物体声音** | 脚步、门、机械、交通 | 研究瞬态、材质、动作 |

---

## 3. Keywords

### English Keywords

| Type | Terms |
|---|---|
| General | audio representation learning, sound feature extraction, timbre representation, audio embeddings |
| Decomposition | STFT, CQT, CWT, wavelet transform, Gabor atoms, matching pursuit, NMF, sparse coding, K-SVD |
| Perception | psychoacoustic features, perceptual audio coding, auditory salience, timbre space, roughness, spectral centroid |
| ML | CNN audio spectrogram, self-supervised audio learning, AudioMAE, BYOL-A, wav2vec, HuBERT, CLAP |
| Neural audio | EnCodec, SoundStream, neural audio codec, RAVE, DDSP, diffusion audio, AudioLDM |
| Composition | interactive sound design, latent space composition, computer music, neural audio synthesis, timbre transfer |
| Evaluation | perceptual evaluation, listening test, MUSHRA, ABX test, controllability, disentanglement |

### 中文关键词

| 类型 | 关键词 |
|---|---|
| 总体 | 音频表征学习，声音特征提取，音色表示，声音嵌入 |
| 分解 | 短时傅里叶变换，恒定Q变换，小波变换，Gabor原子，匹配追踪，非负矩阵分解，稀疏编码 |
| 感知 | 心理声学特征，听觉显著性，音色空间，粗糙度，频谱质心 |
| 机器学习 | 音频CNN，自监督音频学习，音频嵌入，对比学习，音频Transformer |
| 神经音频 | 神经音频编码器，RAVE，DDSP，音频扩散模型，音色迁移 |
| 创作 | 潜空间作曲，交互式声音设计，计算机音乐，生成式音乐 |
| 评估 | 听觉实验，可控性，解耦性，ABX测试，MUSHRA |

### Suggested Categories / Venues

| Source | Categories / Venues |
|---|---|
| arXiv | `cs.SD`, `cs.LG`, `eess.AS`, `cs.MM`, `stat.ML` |
| ACM | Sound and Music Computing, Multimedia Retrieval |
| IEEE | Audio and Acoustic Signal Processing |
| ISMIR | Music Information Retrieval |
| NIME | New Interfaces for Musical Expression |
| ICMC | International Computer Music Conference |
| DAFx | Digital Audio Effects |

---

## 4. Conceptual Pipeline

```text
Raw Audio
  ↓
Preprocessing
  - mono/stereo decision
  - resampling
  - loudness normalization
  - onset segmentation

  ↓
Decomposition Layer
  A. STFT / Mel / CQT / CWT
  B. Gabor atoms / sparse coding
  C. source separation
  D. neural codec tokenization

  ↓
Feature Extraction Layer
  A. handcrafted psychoacoustic descriptors
  B. CNN/Transformer embeddings
  C. self-supervised latent vectors
  D. generative model latents

  ↓
Feature Validation Layer
  A. reconstruction quality
  B. perceptual audibility
  C. disentanglement
  D. controllability

  ↓
Creative Mapping Layer
  A. latent interpolation
  B. feature-to-synthesis control
  C. feature trajectory composition
  D. sample retrieval / recombination

  ↓
Composition System
  - interactive interface
  - generative engine
  - audio rendering
  - listening evaluation
```

---

## 5. Subtopic Decomposition

## Module A — 音频分解方法

### Research Question

正常音频应如何被分解，才能既保留物理信息，又适合后续抽象特征学习？

### Candidate Methods

| 方法 | 优点 | 缺点 | 适合作曲吗？ |
|---|---|---|---|
| STFT | 标准、可逆、易实现 | 固定时频分辨率 | 适合作为基础分析 |
| Mel Spectrogram | 匹配听觉、适合 CNN | 不严格可逆 | 适合作为感知特征 |
| CQT | 音乐音高尺度自然 | 高频时间分辨较差 | 很适合音乐 |
| CWT / Wavelet | 多分辨率，适合瞬态 | 参数选择复杂 | 适合自然声音/纹理 |
| Gabor atoms | 稀疏、事件化 | 字典设计困难 | 很适合作为“声音粒子” |
| NMF | 可分解为谱模板+时间激活 | 线性、局部最优 | 适合循环/纹理 |
| Source separation | 可得声部/声源 | 依赖模型 | 适合 remix 创作 |
| Neural codec | 高质量可重建 token | latent 难解释 | 适合生成模型 |

### Expected Output

- 音频分解方法对照表
- 对不同声音类型的推荐方案
- 同一段音频用 STFT/CQT/CWT/Gabor/NMF 分解并比较稀疏性和可重建性的实验

---

## Module B — 抽象特征提取方法

### Research Question

哪些方法能提取既稳定、可泛化、又具有创作价值的抽象声音特征？

### Feature Families

#### B1. 手工心理声学特征

| 特征 | 听觉意义 | 创作映射 |
|---|---|---|
| spectral centroid | 明亮度 | filter cutoff / orchestration density |
| spectral flux | 变化率 | rhythm / dynamics |
| roughness | 粗糙/张力 | harmonic tension / noise ratio |
| inharmonicity | 金属感/钟声感 | FM index / modal synthesis |
| attack time | 起奏锋利度 | envelope attack / percussion mapping |
| onset density | 事件密度 | rhythmic density |
| spectral flatness | 噪声性 | noise vs tone balance |
| entropy | 纹理复杂度 | texture density |

#### B2. 深度学习 Embedding

| 方法 | 特征类型 | 是否可解释 | 是否适合作曲 |
|---|---|---|---|
| CNN spectrogram embedding | timbre / texture | 中等 | 适合检索和聚类 |
| BYOL-A | general audio embedding | 低-中 | 适合相似性搜索 |
| AudioMAE | masked reconstruction embedding | 低 | 适合聚类/迁移 |
| CLAP | audio-text joint embedding | 中 | 很适合语义控制 |
| EnCodec / DAC latent | codec latent | 低 | 适合生成和重建 |
| RAVE latent | generative latent | 中 | 很适合实时创作 |
| DDSP controls | physical-ish latent | 高 | 很适合可控合成 |

#### B3. 学习型稀疏字典

| 方法 | 抽象单元 | 创作价值 |
|---|---|---|
| K-SVD | 学到的音频原子 | 可作为“声音词汇” |
| NMF | 谱模板 + 激活 | 可作为纹理/声源部件 |
| Sparse coding | 原子激活 | 可作为节奏/事件结构 |
| VQ-VAE / neural codec tokens | 离散声音 token | 可作为音频版“音符” |

### Expected Output

- 特征提取方法 taxonomy
- “可解释性 × 重建性 × 创作性”三轴评价表
- 候选模型 shortlist

---

## Module C — 抽象特征的可闻性

### Research Question

机器学习提取出的 latent feature 是否对应人耳可感知的变化？

### Evaluation Dimensions

| 维度 | 评估问题 | 方法 |
|---|---|---|
| Audibility | 改变该特征，人能听出差异吗？ | ABX / JND 测试 |
| Interpretability | 人能描述变化方向吗？ | 语义标签收集 |
| Disentanglement | 单一特征是否只改变一个听觉属性？ | latent traversal |
| Reconstruction | 特征是否保留足够声音信息？ | SDR, log-spectral distance |
| Perceptual quality | 生成声音自然吗？ | MUSHRA / MOS |
| Compositional value | 变化是否有音乐表达力？ | 专家评分 / 创作案例 |

### Important Distinction

```text
ML feature useful for prediction
≠
Perceptually meaningful feature
≠
Creatively useful feature
```

例如：

- CNN 第三层 embedding 可能分类很好，但难以直接控制。
- CLAP embedding 可语义检索，但空间不一定平滑。
- RAVE latent 可实时控制，但某些维度可能耦合多个听觉属性。
- DDSP 参数可解释性高，但对噪声自然声建模弱。

### Expected Output

- ABX / MUSHRA 实验方案
- latent traversal 听觉测试协议
- 可闻性评价指标表

---

## Module D — 特征到创作素材的映射

### Research Question

如何把抽象声音特征转化为可作曲、可操控、可组织的音乐素材？

### Creative Mapping Types

| 类型 | 说明 | 示例 |
|---|---|---|
| Direct Mapping | 特征直接控制合成参数 | centroid → filter cutoff |
| Latent Interpolation | 在 embedding/latent 空间插值 | bird → flute → noise |
| Feature Trajectory | 将特征变化作为音乐结构 | roughness 从低到高形成张力 |
| Corpus Navigation | 在声音素材库中按特征空间检索 | 找“像水但更金属”的声音 |
| Granular Recomposition | 将原音频拆成片段/粒子后重排 | onset density 控制颗粒密度 |
| Neural Resynthesis | 用 latent 生成新音色 | RAVE / DDSP / AudioLDM |
| Hybrid Scoring | 特征轨迹生成符号音乐参数 | brightness → register; entropy → rhythm |

### Expected Output

- 创作映射类型 taxonomy
- 原型系统设计：feature browser + latent morphing + audio renderer
- 小作品 / sound study 作为 proof-of-concept

---

## 6. Search Strategy

## Phase 1 — Broad Scan

目标：建立领域地图。

### Queries

1. `audio representation learning music creation latent space`
2. `self-supervised audio embeddings music information retrieval`
3. `neural audio synthesis latent space composition RAVE DDSP`
4. `audio feature extraction psychoacoustic descriptors timbre space`
5. `sparse coding dictionary learning audio atoms music`
6. `CLAP audio text embedding sound design retrieval`
7. `neural audio codec tokens music generation EnCodec SoundStream DAC`

### Sources

- arXiv
- ISMIR proceedings
- DAFx proceedings
- NIME / ICMC
- Google Scholar / Semantic Scholar
- GitHub model repos
- Audio ML survey papers

---

## Phase 2 — Focused Literature Review

建议拆成四个独立 literature-review：

### LR1. Audio Decomposition for Creative Use

重点：

- STFT / CQT / CWT
- Matching pursuit / sparse coding
- NMF
- Source separation
- Neural codecs

### LR2. Representation Learning for Timbre and Sound Texture

重点：

- CNN spectrogram embeddings
- BYOL-A / AudioMAE
- CLAP
- timbre transfer
- auditory embeddings

### LR3. Neural Audio Synthesis and Latent Control

重点：

- DDSP
- RAVE
- VAE / VQ-VAE audio
- EnCodec / SoundStream / DAC
- diffusion audio latent space

### LR4. Perceptual and Creative Evaluation

重点：

- ABX / MUSHRA / MOS
- perceptual audio metrics
- disentanglement
- controllability
- creative usability evaluation

---

## Phase 3 — Experimental Prototype Review

筛选 5–8 个可复现实验系统：

| 系统 | 作用 |
|---|---|
| librosa / essentia | 传统音频特征 baseline |
| madmom / librosa onset | 事件分割 |
| OpenL3 / PANNs / AST | 预训练音频 embedding |
| BYOL-A / AudioMAE | 自监督 embedding |
| CLAP | audio-text retrieval |
| EnCodec / DAC | neural codec tokenization |
| DDSP | 可解释控制合成 |
| RAVE | 实时 latent 创作 |

---

## 7. Inclusion / Exclusion Criteria

### Inclusion

纳入满足以下任一条件的研究：

- 能从音频中提取可泛化表示
- 明确处理 timbre / texture / sound event
- 支持重建、变形、生成或检索
- 提供感知评估
- 有可复现代码或公开模型
- 与音乐创作、sound design、MIR 有直接关系

### Exclusion

排除：

- 纯语音识别且与音色/创作无关
- 纯分类但无特征解释或生成用途
- 仅符号音乐（MIDI）生成，不处理音频
- 没有音频输出或无法验证可闻性的 latent 方法
- 纯工程压缩论文，若无 latent 控制或重建接口

---

## 8. Existing Knowledge in Sonic Atlas

| 模块 | 可复用内容 |
|---|---|
| Module 1 | 听觉离散化精度、JND、ERB、采样/量化边界 |
| Module 2 | 相位可闻性、crest factor、CLT、为什么 magnitude spectrogram 通常足够 |
| Module 3 | Gabor atoms、wavelets、matching pursuit、稀疏音频原子 |
| Module 4 | Timbre MDS space、spectral centroid、attack time、spectral irregularity |
| Module 5 | CNN spectrogram embedding、Mel spectrogram、translation equivariance |
| spectral_reference.html | 10种频谱表示的统一对照 |
| wave_packet_demo.html | 真实音频稀疏重建比较，已包含 FFT/Gabor hybrid 初步实验 |

新课题是 Sonic Atlas 的自然下一阶段：

> 从“声音如何被表征”推进到“表征如何成为创作材料”。

---

## 9. Proposed Research Outputs

建议最终输出为新的模块集：

```text
docs/
├── literature/
│   ├── 00_research_plan.md
│   ├── 01_first_round_review.md
│   ├── 02_feature_taxonomy.md
│   └── 03_experiment_protocol.md
├── foundations/
│   └── ... existing foundation reports ...
└── architecture.md

experiments/creative_features/
├── 01_baseline_features/
├── 02_embedding_comparison/
├── 03_latent_traversal/
└── 04_creative_mapping/

demos/creative_features/
├── feature_space_browser.html
├── latent_morphing_demo.html
└── corpus_navigation_demo.html
```

---

## 10. Experimental Roadmap

## Stage 1 — Baseline Feature Extraction

目标：建立传统可解释特征 baseline。

### Input Dataset

- 20 个乐器单音
- 20 个自然声音
- 20 个城市/物体声音

### Features

- spectral centroid
- spectral flux
- spectral flatness
- roughness
- onset density
- attack time
- MFCC mean/std
- CQT chroma
- entropy

### Output

- UMAP/t-SNE 2D feature map
- 聚类结果
- 与主观标签比较

---

## Stage 2 — Deep Embedding Comparison

比较模型：

- CNN on log-mel spectrogram
- OpenL3 / PANNs / AST
- BYOL-A
- CLAP
- EnCodec / DAC latent
- RAVE latent

指标：

| 指标 | 问题 |
|---|---|
| Clustering quality | 同类声音是否聚在一起？ |
| Retrieval quality | 相似声音检索是否合理？ |
| Interpolation quality | 两声音之间是否能平滑 morph？ |
| Reconstruction quality | 能否重建声音？ |
| Interpretability | 维度能否命名？ |
| Controllability | 能否单独改变一个属性？ |

---

## Stage 3 — Perceptual Tests

### Test Types

1. **ABX Test**
   - 改变一个 latent 维度，听者能否分辨？

2. **Semantic Rating**
   - 听者给变化打标签：更亮、更粗糙、更近、更机械、更有机等。

3. **MUSHRA / MOS**
   - 评估生成/重建质量。

4. **Creative Usefulness Rating**
   - 音乐创作者评价：这个变化是否有音乐表达力？

---

## Stage 4 — Composition Prototype

原型功能：

1. 导入音频素材库
2. 自动提取多层特征
3. 在 2D/3D latent space 中浏览声音
4. 选择两个或多个声音进行 morphing
5. 将特征轨迹映射到合成参数
6. 输出可播放音频片段
7. 保存 “feature score” 作为作品草图

---

## 11. Candidate Core Papers / Systems to Investigate

### Classic / Psychoacoustic

- Grey (1977) — Timbre MDS
- McAdams et al. (1995) — Perceptual scaling of timbres
- Zwicker & Fastl — Psychoacoustics
- Serra & Smith — Spectral modeling synthesis

### Sparse / Dictionary

- Mallat & Zhang (1993) — Matching Pursuit
- Aharon, Elad & Bruckstein (2006) — K-SVD
- Virtanen (2007) — Monaural sound source separation by NMF

### Neural / Generative

- Engel et al. (2020) — DDSP
- Caillon & Esling (2021) — RAVE
- Défossez et al. (2022) — EnCodec
- Zeghidour et al. (2021) — SoundStream
- Liu et al. — AudioLDM
- Huang et al. — MusicLM / AudioLM-related works

### Representation Learning

- Cramer et al. (2019) — OpenL3
- Kong et al. — PANNs
- Gong et al. — AST
- Niizumi et al. — BYOL-A
- Huang et al. — AudioMAE
- Wu et al. / LAION — CLAP

---

## 12. Recommended Next Steps

### Step A — 第一轮 Literature Review

优先范围：

> **Audio representation learning and neural audio synthesis for creative sound design**

目标产出：

1. 20 篇候选文献池
2. 8–12 篇核心文献
3. evidence matrix
4. 方法 taxonomy
5. 实验路线

### Step B — 最小实验原型

从最可控的 baseline 开始：

```text
输入音频素材
  → 提取传统心理声学特征
  → UMAP/t-SNE 可视化
  → 特征轨迹映射为合成参数
```

然后再引入深度 embedding。

### Step C — 创作原型设计

开发一个交互式 demo：

```text
Feature Space Browser
  - 上传声音
  - 自动提取特征
  - 投影到 2D 空间
  - 点击点位试听
  - 拖动路径生成 feature trajectory
  - 将 trajectory 映射到合成参数
```

---

## 13. One-Sentence Summary

**本课题旨在建立一个从真实声音中提取抽象、可闻、可控特征，并将其转化为音乐创作材料的机器学习系统，使声音分析不止服务于分类，也服务于作曲、音色设计与声音想象。**

# 研究计划:基于机器学习声音抽象特征的音乐创作系统

> **课题目标**:通过机器学习方法,从音乐与自然声音中提取抽象声音特征,并将这些特征作为可听、可操作、可组合的音乐创作素材。

---

## 0. 课题定位

本课题关注的问题不是单纯的"音频分类",也不是单纯的"声音合成",而是:

> **如何从真实音频中分解、学习、筛选出具有感知意义和创作可操作性的抽象声音特征,并将这些特征转化为音乐创作材料。**

它横跨以下领域:

1. 音频分解(Audio Decomposition)与时频表示(Time-Frequency Representation)
2. 音色(Timbre)与声音纹理(Sound Texture)表征
3. 自监督(Self-Supervised,无需人工标签从数据自身结构学习) / 对比式(Contrastive,通过正负样本对学习相似性) / 生成式(Generative,学习数据分布以生成新样本)音频表征学习
4. 心理声学与特征可闻性验证
5. 神经音频合成(Neural Audio Synthesis,用神经网络直接生成音频)与潜空间作曲(Latent-Space Composition)
6. 交互式声音设计与计算机音乐创作

建议将该方向作为 Sonic Atlas 的下一阶段研究模块,暂定名:

> **Creative Feature Lab:基于声音特征的音乐创作实验室**

---

## 1. 研究问题

### 主要问题

**如何从音乐与自然声音中提取既具有抽象性、又具有听觉可辨性和创作可操作性的声音特征(Feature,对音频的数值化描述),并将这些特征转化为可用于音乐创作的素材?**

### 次要问题

#### SQ1. 一个正常音频应如何分解?

输入一段真实音频后,应将其分解为哪些层次?

可能层次包括:

1. **波形层**:原始波形
2. **时频层**:短时傅里叶变换(STFT,Short-Time Fourier Transform) / 恒定 Q 变换(CQT,Constant-Q Transform) / 连续小波变换(CWT,Continuous Wavelet Transform) / 梅尔频谱(Mel Spectrogram,按人耳感知尺度变换的频谱图) / Gammatone 滤波器组(Gammatone Filterbank,模拟人耳耳蜗的滤波器组)
3. **稀疏原子层**:Gabor 原子(Gabor Atom,局部化的时频高斯波包) / 小波(Wavelet) / 匹配追踪(Matching Pursuit,贪心选取最佳原子的稀疏分解算法)
4. **事件层**:起始点(Onset,声音事件的开始时刻)、瞬态(Transient,短时冲击性信号)、维持(Sustain)、衰减(Decay)、纹理(Texture)
5. **声源层**:声源分离(Source Separation) / 对象级声音事件
6. **语义层**:乐器、材质、手势、环境、情感
7. **潜变量层**(Latent Layer):来自变分自编码器(VAE,Variational Autoencoder) / 对比学习 / 扩散模型(Diffusion Model,通过逐步去噪生成数据的模型) / 神经音频编解码器(Neural Audio Codec)的潜变量嵌入

#### SQ2. 什么方法能提取更有效的抽象特征?

这里的"有效"至少包含四个标准:

| 标准 | 含义 |
|---|---|
| **重建有效** | 用特征可以较好重建原声音 |
| **分类有效** | 特征能区分乐器、声音类别、演奏技法、材质等 |
| **感知有效** | 特征变化在人耳听感中可察觉、可描述 |
| **创作有效** | 特征可以被控制、组合、变形、映射为音乐参数 |

候选方法包括:

- 梅尔频率倒谱系数(MFCC,Mel-Frequency Cepstral Coefficient,频谱包络的倒谱描述) / 频谱描述符(Spectral Descriptor)
- CQT / CWT / Gammatone 特征
- CNN / CRNN 声谱图嵌入(CRNN,卷积循环神经网络)
- 自监督音频嵌入:wav2vec2(基于掩码预测的语音表示模型)、HuBERT(Hidden-Unit BERT,离散单元自监督语音模型)、BYOL-A(Bootstrap Your Own Latent for Audio,无需负样本的音频自监督学习)、AudioMAE(Audio Masked Autoencoder,声谱图掩码自编码器)
- 音频-文本嵌入:CLAP / LAION-CLAP
- 神经编解码器嵌入:EnCodec、SoundStream、DAC(Descript Audio Codec)
- 生成式潜空间(Generative Latent Space):VAE、DDSP(Differentiable Digital Signal Processing,可微数字信号处理,将传统 DSP 与神经网络结合的合成方法)、RAVE(Realtime Audio Variational autoEncoder,实时音频变分自编码器)、扩散音频模型
- 稀疏学习字典:K-SVD(一种学习超完备字典的稀疏编码算法)、NMF(非负矩阵分解,Non-Negative Matrix Factorization)、稀疏编码(Sparse Coding)、Gabor OMP(正交匹配追踪,Orthogonal Matching Pursuit)

#### SQ3. 抽象特征是否是人耳可闻的?

一个机器学习特征可以很有效,但未必可闻。需要区分:

| 类型 | 说明 |
|---|---|
| **可重建但不可解释** | 如 neural codec latent,能还原声音,但单个维度未必可听懂 |
| **可分类但不可操控** | 如分类 CNN embedding,可分辨乐器,但维度没有直接创作意义 |
| **可操控但不自然** | 如某些 VAE latent,插值可听但容易产生伪影 |
| **感知可解释** | 如 spectral centroid、attack time、roughness、inharmonicity |
| **创作可操作** | 如"明亮度""粗糙度""颗粒度""空间感""金属感""有机感" |

#### SQ4. 抽象特征如何成为音乐创作素材?

需要从"分析特征"转换为"作曲参数"。可能形式包括:

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
   - 将自然声音或音乐片段嵌入到 latent space,按相似性、情绪、质感、动态检索。

5. **特征作为作曲结构**
   - 用特征轨迹构造音乐时间结构,例如:
     - low roughness → high roughness
     - natural noise → harmonic stable timbre
     - sparse transient → dense texture

---

## 2. 研究范围

### 领域

- 音乐信息检索(MIR,Music Information Retrieval)
- 计算听觉场景分析(Computational Auditory Scene Analysis)
- 音频表征学习(Audio Representation Learning)
- 神经音频合成(Neural Audio Synthesis)
- 声音设计 / 计算机音乐
- 心理声学(Psychoacoustics)
- 交互式音乐系统(Interactive Music System)

### 时间范围

建议分两层:

1. **基础阶段:1990-2015**
   - MFCC, NMF, sparse coding, sinusoidal modeling, timbre MDS, 经典心理声学

2. **现代机器学习:2015-2026**
   - CNN spectrogram, 自监督音频学习, neural codecs, RAVE, DDSP, CLAP, diffusion audio models

### 方法论重点

本课题最终应进入实验系统,因此建议采用:

1. 文献调研
2. 方法分类
3. 小规模实验
4. 感知评估
5. 创作原型

### 音频范围

| 类型 | 示例 | 作用 |
|---|---|---|
| **音乐声音** | 钢琴、吉他、弦乐、鼓、合成器 | 研究音高、音色、起奏、延音 |
| **自然声音** | 风、水、鸟、雨、火、昆虫 | 研究纹理、噪声、事件密度 |
| **城市/物体声音** | 脚步、门、机械、交通 | 研究瞬态、材质、动作 |

---

## 3. 关键词

### 英文关键词

| 类型 | 关键词 |
|---|---|
| 总体 | audio representation learning（音频表征学习）, sound feature extraction（声音特征提取）, timbre representation（音色表示）, audio embeddings（音频嵌入） |
| 分解 | STFT, CQT, CWT, wavelet transform（小波变换）, Gabor atoms, matching pursuit（匹配追踪）, NMF, sparse coding（稀疏编码）, K-SVD |
| 感知 | psychoacoustic features（心理声学特征）, perceptual audio coding（感知音频编码）, auditory salience（听觉显著性）, timbre space（音色空间）, roughness（粗糙度）, spectral centroid（频谱质心） |
| 机器学习 | CNN audio spectrogram（CNN 声谱图）, self-supervised audio learning（自监督音频学习）, AudioMAE, BYOL-A, wav2vec, HuBERT, CLAP |
| 神经音频 | EnCodec, SoundStream, neural audio codec（神经音频编解码器）, RAVE, DDSP, diffusion audio（扩散音频）, AudioLDM |
| 创作 | interactive sound design（交互式声音设计）, latent space composition（潜空间作曲）, computer music（计算机音乐）, neural audio synthesis（神经音频合成）, timbre transfer（音色迁移） |
| 评估 | perceptual evaluation（感知评估）, listening test（听觉测试）, MUSHRA, ABX test, controllability（可控性）, disentanglement（解耦性） |

### 中文关键词

| 类型 | 关键词 |
|---|---|
| 总体 | 音频表征学习(Audio Representation Learning),声音特征提取,音色表示(Timbre Representation),声音嵌入(Sound Embedding) |
| 分解 | 短时傅里叶变换(STFT),恒定Q变换(CQT),小波变换(CWT),Gabor原子(Gabor Atom,局部化时频高斯波包),匹配追踪(Matching Pursuit),非负矩阵分解(NMF),稀疏编码(Sparse Coding) |
| 感知 | 心理声学特征(Psychoacoustic Feature),听觉显著性(Auditory Salience),音色空间(Timbre Space),粗糙度(Roughness),频谱质心(Spectral Centroid) |
| 机器学习 | 音频CNN(Audio CNN),自监督音频学习(Self-Supervised Audio Learning),音频嵌入(Audio Embedding),对比学习(Contrastive Learning),音频Transformer(Audio Transformer) |
| 神经音频 | 神经音频编码器(Neural Audio Codec),RAVE,DDSP,音频扩散模型(Audio Diffusion Model),音色迁移(Timbre Transfer) |
| 创作 | 潜空间作曲(Latent-Space Composition),交互式声音设计(Interactive Sound Design),计算机音乐(Computer Music),生成式音乐(Generative Music) |
| 评估 | 听觉实验(Listening Test),可控性(Controllability),解耦性(Disentanglement),ABX测试,MUSHRA |

### 推荐学术会议/期刊

| 来源 | 分类 / 会议 |
|---|---|
| arXiv | `cs.SD`, `cs.LG`, `eess.AS`, `cs.MM`, `stat.ML` |
| ACM | Sound and Music Computing, Multimedia Retrieval |
| IEEE | Audio and Acoustic Signal Processing |
| ISMIR | Music Information Retrieval |
| NIME | New Interfaces for Musical Expression |
| ICMC | International Computer Music Conference |
| DAFx | Digital Audio Effects |

---

## 4. 概念管线

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

## 5. 子课题分解

## 模块 A - 音频分解方法

### 研究问题

正常音频应如何被分解,才能既保留物理信息,又适合后续抽象特征学习?

### 候选方法

| 方法 | 优点 | 缺点 | 适合作曲吗? |
|---|---|---|---|
| STFT(短时傅里叶变换) | 标准、可逆、易实现 | 固定时频分辨率 | 适合作为基础分析 |
| Mel 频谱图(梅尔频谱图) | 匹配听觉、适合 CNN | 不严格可逆 | 适合作为感知特征 |
| CQT(恒定Q变换) | 音乐音高尺度自然 | 高频时间分辨较差 | 很适合音乐 |
| CWT / Wavelet(小波变换) | 多分辨率,适合瞬态 | 参数选择复杂 | 适合自然声音/纹理 |
| Gabor atoms(Gabor 原子) | 稀疏、事件化 | 字典设计困难 | 很适合作为"声音粒子" |
| NMF(非负矩阵分解) | 可分解为谱模板+时间激活 | 线性、局部最优 | 适合循环/纹理 |
| Source separation(声源分离) | 可得声部/声源 | 依赖模型 | 适合 remix 创作 |
| Neural codec(神经编解码器) | 高质量可重建 token | latent 难解释 | 适合生成模型 |

### 预期输出

- 音频分解方法对照表
- 对不同声音类型的推荐方案
- 同一段音频用 STFT/CQT/CWT/Gabor/NMF 分解并比较稀疏性和可重建性的实验

---

## 模块 B - 抽象特征提取方法

### 研究问题

哪些方法能提取既稳定、可泛化、又具有创作价值的抽象声音特征?

### 特征家族

#### B1. 手工心理声学特征

| 特征 | 听觉意义 | 创作映射 |
|---|---|---|
| spectral centroid（频谱质心） | 明亮度（Brightness） | filter cutoff / orchestration density |
| spectral flux（频谱通量） | 变化率 | rhythm / dynamics |
| roughness（粗糙度） | 粗糙/张力 | harmonic tension / noise ratio |
| inharmonicity（非谐性） | 金属感/钟声感 | FM index / modal synthesis |
| attack time（起奏时间） | 起奏锋利度 | envelope attack / percussion mapping |
| onset density（起始点密度） | 事件密度 | rhythmic density |
| spectral flatness（频谱平坦度） | 噪声性 | noise vs tone balance |
| entropy（熵） | 纹理复杂度 | texture density |

#### B2. 深度学习嵌入(Deep Learning Embedding)

| 方法 | 特征类型 | 是否可解释 | 是否适合作曲 |
|---|---|---|---|
| CNN 声谱图嵌入(CNN Spectrogram Embedding) | timbre / texture | 中等 | 适合检索和聚类 |
| BYOL-A(Bootstrap Your Own Latent for Audio,无需负样本的音频自监督学习) | general audio embedding | 低-中 | 适合相似性搜索 |
| AudioMAE(Audio Masked Autoencoder,声谱图掩码自编码器) | masked reconstruction embedding | 低 | 适合聚类/迁移 |
| CLAP(Contrastive Language-Audio Pretraining,音频-文本对比预训练) | audio-text joint embedding | 中 | 很适合语义控制 |
| EnCodec / DAC 潜变量(Neural Codec Latent,神经编解码器学到的潜表示) | codec latent | 低 | 适合生成和重建 |
| RAVE 潜变量(RAVE Latent) | generative latent | 中 | 很适合实时创作 |
| DDSP 控制参数(DDSP Controls) | physical-ish latent | 高 | 很适合可控合成 |

#### B3. 学习型稀疏字典(Learned Sparse Dictionary)

| 方法 | 抽象单元 | 创作价值 |
|---|---|---|
| K-SVD | 学到的音频原子(Learned Atom) | 可作为"声音词汇" |
| NMF(非负矩阵分解) | 谱模板(Spectral Template) + 激活(Activation) | 可作为纹理/声源部件 |
| 稀疏编码(Sparse Coding) | 原子激活 | 可作为节奏/事件结构 |
| VQ-VAE / 神经编解码器标记(Neural Codec Token) | 离散声音标记(Discrete Sound Token) | 可作为音频版"音符" |

### 预期输出

- 特征提取方法分类体系
- "可解释性 × 重建性 × 创作性"三轴评价表
- 候选模型短名单

---

## 模块 C - 抽象特征的可闻性

### 研究问题

机器学习提取出的 latent feature 是否对应人耳可感知的变化?

### 评估维度

| 维度 | 评估问题 | 方法 |
|---|---|---|
| 可闻性(Audibility) | 改变该特征,人能听出差异吗? | ABX / JND(最小可觉差,Just Noticeable Difference)测试 |
| 可解释性(Interpretability) | 人能描述变化方向吗? | 语义标签收集 |
| 解耦性(Disentanglement) | 单一特征是否只改变一个听觉属性? | 潜变量遍历(Latent Traversal) |
| 重建性(Reconstructability) | 特征是否保留足够声音信息? | 信号失真比(SDR,Signal-to-Distortion Ratio)、对数频谱距离 |
| 感知质量(Perceptual Quality) | 生成声音自然吗? | MUSHRA / MOS(Mean Opinion Score,平均主观评分) |
| 创作价值(Creative Value) | 变化是否有音乐表达力? | 专家评分 / 创作案例 |

### 重要区分

```text
对预测有用的机器学习特征
≠
有感知意义的特征
≠
对创作有用的特征
```

例如:

- CNN 第三层 embedding 可能分类很好,但难以直接控制。
- CLAP embedding 可语义检索,但空间不一定平滑。
- RAVE latent 可实时控制,但某些维度可能耦合多个听觉属性。
- DDSP 参数可解释性高,但对噪声自然声建模弱。

### 预期输出

- ABX / MUSHRA 实验方案
- latent traversal 听觉测试协议
- 可闻性评价指标表

---

## 模块 D - 特征到创作素材的映射

### 研究问题

如何把抽象声音特征转化为可作曲、可操控、可组织的音乐素材?

### 创作映射类型

| 类型 | 说明 | 示例 |
|---|---|---|
| 直接映射 | 特征直接控制合成参数 | centroid → filter cutoff |
| 潜空间插值 | 在 embedding/latent 空间插值 | bird → flute → noise |
| 特征轨迹 | 将特征变化作为音乐结构 | roughness 从低到高形成张力 |
| 语料库导航 | 在声音素材库中按特征空间检索 | 找"像水但更金属"的声音 |
| 颗粒重组 | 将原音频拆成片段/粒子后重排 | onset density 控制颗粒密度 |
| 神经重合成 | 用 latent 生成新音色 | RAVE / DDSP / AudioLDM |
| 混合记谱 | 特征轨迹生成符号音乐参数 | brightness → register; entropy → rhythm |

### 预期输出

- 创作映射类型分类体系
- 原型系统设计:feature browser + latent morphing + audio renderer
- 小作品 / sound study 作为概念验证

---

## 6. 检索策略

### Phase 1 - 广泛扫描

目标:建立领域地图。

### 检索词

1. `audio representation learning music creation latent space`
2. `self-supervised audio embeddings music information retrieval`
3. `neural audio synthesis latent space composition RAVE DDSP`
4. `audio feature extraction psychoacoustic descriptors timbre space`
5. `sparse coding dictionary learning audio atoms music`
6. `CLAP audio text embedding sound design retrieval`
7. `neural audio codec tokens music generation EnCodec SoundStream DAC`

### 来源

- arXiv
- ISMIR proceedings
- DAFx proceedings
- NIME / ICMC
- Google Scholar / Semantic Scholar
- GitHub model repos
- Audio ML survey papers

---

### Phase 2 - 聚焦文献综述

建议拆成四个独立文献综述:

### LR1. 面向创作的音频分解

重点:

- STFT / CQT / CWT
- Matching pursuit / sparse coding
- NMF
- Source separation
- Neural codecs

### LR2. 音色与声音纹理的表征学习

重点:

- CNN spectrogram embeddings
- BYOL-A / AudioMAE
- CLAP
- timbre transfer
- auditory embeddings

### LR3. 神经音频合成与潜空间控制

重点:

- DDSP
- RAVE
- VAE / VQ-VAE audio
- EnCodec / SoundStream / DAC
- diffusion audio latent space

### LR4. 感知与创作评估

重点:

- ABX / MUSHRA / MOS
- perceptual audio metrics
- disentanglement
- controllability
- creative usability evaluation

---

### Phase 3 - 可复现实验系统筛选

筛选 5-8 个可复现实验系统:

| 系统 | 作用 |
|---|---|
| librosa / essentia(音频特征提取库) | 传统音频特征 baseline |
| madmom / librosa onset | 事件分割(起始点检测) |
| OpenL3 / PANNs / AST(预训练音频嵌入模型) | 预训练音频嵌入(Embedding) |
| BYOL-A / AudioMAE(自监督音频嵌入模型) | 自监督嵌入(Self-Supervised Embedding) |
| CLAP(Contrastive Language-Audio Pretraining) | 音频-文本检索(Audio-Text Retrieval) |
| EnCodec / DAC(神经音频编解码器) | 神经编解码器标记化(Neural Codec Tokenization) |
| DDSP(可微数字信号处理) | 可解释控制合成 |
| RAVE(实时音频变分自编码器) | 实时潜变量创作(Latent Creation) |

---

## 7. 纳入/排除标准

### 纳入

纳入满足以下任一条件的研究:

- 能从音频中提取可泛化表示
- 明确处理 timbre / texture / sound event
- 支持重建、变形、生成或检索
- 提供感知评估
- 有可复现代码或公开模型
- 与音乐创作、sound design、MIR 有直接关系

### 排除

排除:

- 纯语音识别且与音色/创作无关
- 纯分类但无特征解释或生成用途
- 仅符号音乐(MIDI)生成,不处理音频
- 没有音频输出或无法验证可闻性的 latent 方法
- 纯工程压缩论文,若无 latent 控制或重建接口

---

## 8. Sonic Atlas 中的已有知识

| 模块 | 可复用内容 |
|---|---|
| Module 1 | 听觉离散化精度、JND、ERB、采样/量化边界 |
| Module 2 | 相位可闻性、crest factor、CLT、为什么 magnitude spectrogram 通常足够 |
| Module 3 | Gabor atoms、wavelets、matching pursuit、稀疏音频原子 |
| Module 4 | Timbre MDS space、spectral centroid、attack time、spectral irregularity |
| Module 5 | CNN spectrogram embedding、Mel spectrogram、translation equivariance |
| spectral_reference.html | 10种频谱表示的统一对照 |
| wave_packet_demo.html | 真实音频稀疏重建比较,已包含 FFT/Gabor hybrid 初步实验 |

新课题是 Sonic Atlas 的自然下一阶段:

> 从"声音如何被表征"推进到"表征如何成为创作材料"。

---

## 9. 建议研究输出

建议最终输出为新的模块集:

```text
docs/
├── literature/
│   ├── 00_research_plan.md
│   ├── 01_first_round_review.md
│   ├── 02_feature_taxonomy.md
│   └── 03_experiment_protocol.md
├── foundations/
│   └── ... 已有基础报告 ...
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

## 10. 实验路线图

### Stage 1 - 基线特征提取

目标:建立传统可解释特征 baseline。

#### 输入数据集

- 20 个乐器单音
- 20 个自然声音
- 20 个城市/物体声音

#### 特征

- spectral centroid
- spectral flux
- spectral flatness
- roughness
- onset density
- attack time
- MFCC mean/std
- CQT chroma
- entropy

#### 输出

- UMAP/t-SNE 2D feature map
- 聚类结果
- 与主观标签比较

---

### Stage 2 - 深度嵌入比较

比较模型:

- CNN on log-mel 频谱图
- OpenL3 / PANNs / AST
- BYOL-A
- CLAP
- EnCodec / DAC 潜变量
- RAVE 潜变量

指标：

| 指标 | 问题 |
|---|---|
| 聚类质量（Clustering Quality） | 同类声音是否聚在一起？ |
| 检索质量（Retrieval Quality） | 相似声音检索是否合理？ |
| 插值质量（Interpolation Quality） | 两声音之间是否能平滑 morph（变形）？ |
| 重建质量（Reconstruction Quality） | 能否重建声音？ |
| 可解释性（Interpretability） | 维度能否命名？ |
| 可控性（Controllability） | 能否单独改变一个属性？ |

---

### Stage 3 - 感知测试

#### 测试类型

1. **ABX 测试**
   - 改变一个潜变量维度，听者能否分辨？

2. **语义评分（Semantic Rating）**
   - 听者给变化打标签：更亮、更粗糙、更近、更机械、更有机等。

3. **MUSHRA / MOS（平均主观评分，Mean Opinion Score）**
   - 评估生成/重建质量。

4. **创作有用性评分（Creative Usefulness Rating）**
   - 音乐创作者评价：这个变化是否有音乐表达力？

---

### Stage 4 - 创作原型

原型功能:

1. 导入音频素材库
2. 自动提取多层特征
3. 在 2D/3D 潜变量空间（Latent Space）中浏览声音
4. 选择两个或多个声音进行变形（Morphing）
5. 将特征轨迹映射到合成参数
6. 输出可播放音频片段
7. 保存 "特征总谱"（Feature Score）作为作品草图

---

## 11. 候选核心论文/系统

### 经典 / 心理声学

- Grey (1977) - Timbre MDS
- McAdams et al. (1995) - Perceptual scaling of timbres
- Zwicker & Fastl - Psychoacoustics
- Serra & Smith - Spectral modeling synthesis

### 稀疏 / 字典

- Mallat & Zhang (1993) - Matching Pursuit
- Aharon, Elad & Bruckstein (2006) - K-SVD
- Virtanen (2007) - Monaural sound source separation by NMF

### 神经 / 生成

- Engel et al. (2020) - DDSP
- Caillon & Esling (2021) - RAVE
- Défossez et al. (2022) - EnCodec
- Zeghidour et al. (2021) - SoundStream
- Liu et al. - AudioLDM
- Huang et al. - MusicLM / AudioLM-related works

### 表征学习

- Cramer et al. (2019) - OpenL3
- Kong et al. - PANNs
- Gong et al. - AST
- Niizumi et al. - BYOL-A
- Huang et al. - AudioMAE
- Wu et al. / LAION - CLAP

---

## 12. 建议下一步

### Step A - 第一轮文献综述

优先范围:

> **Audio representation learning and neural audio synthesis for creative sound design**

目标产出:

1. 20 篇候选文献池
2. 8-12 篇核心文献
3. evidence matrix
4. 方法分类体系
5. 实验路线

### Step B - 最小实验原型

从最可控的 baseline 开始:

```text
输入音频素材
  → 提取传统心理声学特征
  → UMAP/t-SNE 可视化
  → 特征轨迹映射为合成参数
```

然后再引入深度嵌入（Deep Embedding）。

### Step C — 创作原型设计

开发一个交互式演示：

```text
特征空间浏览器（Feature-Space Browser）
  - 上传声音
  - 自动提取特征
  - 投影到 2D 空间
  - 点击点位试听
  - 拖动路径生成特征轨迹（Feature Trajectory）
  - 将轨迹映射到合成参数
```

---

## 13. 一句话总结

**本课题旨在建立一个从真实声音中提取抽象、可闻、可控特征,并将其转化为音乐创作材料的机器学习系统,使声音分析不止服务于分类,也服务于作曲、音色设计与声音想象。**

# Feature Taxonomy: 面向音乐创作的声音特征分类体系

> **目标**：建立一个面向音乐创作的声音特征分类体系（Feature Taxonomy），说明不同特征如何从音频中提取、如何被人耳感知、是否可解释、是否可控、是否可重建，以及如何转化为创作材料。

---

## 1. 目的与范围

Sonic Atlas 的主线不是只做音频分类，也不是只做声音合成，而是建立一条从真实声音到创作材料的链路：

```text
Audio
  → Decomposition
  → Abstract Feature Extraction
  → Perceptual Validation
  → Creative Mapping
  → Composition System
```

本分类体系的作用是承接第一轮文献综述，并为后续实验提供决策框架：

```text
docs/literature/01_first_round_review.md
  → docs/literature/02_feature_taxonomy.md
  → docs/literature/03_experiment_protocol.md
  → experiments/creative_features/01_baseline_features/
  → demos/creative_features/feature_space_browser.html
```

它回答五个问题：

1. 声音特征可以分成哪些层级？
2. 每类特征的输入、输出和代表方法是什么？
3. 哪些特征是人耳可闻、可解释、可控制的？
4. 哪些特征适合进入第一阶段 baseline 实验？
5. 哪些特征适合后续 embedding comparison、latent traversal、creative mapping？

---

## 2. 设计原则

### 2.1 感知优先于指标

一个特征在模型中有效，不代表它在人耳中有意义。Sonic Atlas 中的特征必须尽量回答：

- 改变它，人能否听出差异？
- 人能否描述变化方向？
- 它是否对应 brightness、roughness、attack、density、metallic、organic 等可交流的听觉概念？

### 2.2 控制优先于新奇

生成新声音不是最终目标。更重要的是：

- 能否沿着一个可理解方向变化？
- 能否单独控制某个听觉属性？
- 能否被组合成 feature trajectory、sound map 或 compositional gesture？

### 2.3 混合表征优于单一潜空间

没有单一表征同时满足所有目标。

```text
Handcrafted descriptors: interpretable + controllable, but weak reconstruction.
Sparse atoms: event-like + recomposable, but limited expressiveness.
Embeddings: strong retrieval/semantics, but weak direct control.
Generative latents/tokens: strong synthesis/reconstruction, but weak interpretability.
```

因此 Sonic Atlas 应采用多层特征栈，而不是追求一个万能潜空间。

### 2.4 创作即评估

一个特征最终是否有价值，不只取决于分类准确率、重建误差或检索指标，还取决于它是否能支撑：

- sound design decision
- corpus navigation
- feature trajectory composition
- latent morphing
- granular recomposition
- sound study / etude / composition sketch

---

## 3. 分类体系总览

Sonic Atlas 将声音特征分为四大家族（Four Families）：

| 家族 | 单位 | 主要作用 | 典型用途 |
|---|---|---|---|
| **A. 心理声学描述符（Psychoacoustic Descriptors）** | 标量（Scalar） / 曲线（Curve） | 可命名、可解释控制 | brightness、roughness、density |
| **B. 稀疏分解（Sparse Decomposition）** | 原子（Atom） / 模板（Template） / 激活（Activation） | 声音粒子、事件、素材重组 | Gabor atoms、NMF、K-SVD |
| **C. 判别式嵌入（Discriminative Embeddings）** | 向量（Vector） | 检索、聚类、语义导航 | PANNs、AST、BYOL-A、CLAP |
| **D. 生成式潜变量/标记（Generative Latents/Tokens）** | 潜变量（Latent） / 离散编码（Discrete Code） | 变形、重合成、生成 | DDSP、RAVE、EnCodec、AudioLDM |

Conceptually:

```text
Raw Audio
  ↓
A. Psychoacoustic descriptors
  - named perceptual controls
  - brightness, roughness, attack, density

  ↓
B. Sparse atoms / templates
  - event-level material
  - Gabor atoms, NMF templates, learned atoms

  ↓
C. Discriminative / semantic embeddings
  - corpus organization
  - similarity, clustering, audio-text retrieval

  ↓
D. Generative latents / tokens
  - resynthesis and transformation
  - RAVE, DDSP, EnCodec, AudioLDM

  ↓
Creative Mapping
  - trajectory, browser, morphing, recomposition, synthesis control
```

---

## 4. 评估维度

每类特征都应按统一维度评价。

| 维度 | 核心问题 | 实际含义 |
|---|---|---|
| **可闻性（Audibility）** | 改变该特征，人耳能否听出差异？ | 是否有明确听觉对应 |
| **可解释性（Interpretability）** | 人能否给它命名？ | brightness、roughness、attack、density 等 |
| **可控性（Controllability）** | 能否独立控制？ | 改一个参数是否主要改变一个听觉属性 |
| **可重建性（Reconstructability）** | 能否帮助重建原声音？ | 是否保留足够信号信息 |
| **语义对齐（Semantic Alignment）** | 是否对应语义标签？ | bird、water、metallic、warm、mechanical 等 |
| **时间分辨率（Temporal Resolution）** | 是否能表达随时间变化？ | clip 标量、frame 曲线、事件序列 |
| **创作可供性（Creative Affordance）** | 是否能直接成为创作材料？ | 能否映射到作曲 / sound design / navigation |
| **计算成本（Computational Cost）** | 提取或生成成本如何？ | 是否适合快速实验和交互 |
| **可复现性（Reproducibility）** | 是否容易复现？ | 是否有成熟库、公开模型、稳定接口 |

建议评分采用 0–3：

| 评分 | 含义 |
|---:|---|
| 0 | 不适用或很弱 |
| 1 | 有一定价值，但不稳定 |
| 2 | 可用，适合实验 |
| 3 | 强，适合作为核心特征 |

---

## 5. 家族 A — 心理声学与手工描述符（Psychoacoustic & Handcrafted Descriptors）

### 5.1 作用

心理声学描述符是第一阶段基线的核心。它们的优势是：

- 可解释（Interpretable）；
- 计算成本低；
- 大多有明确听觉对应；
- 可以直接映射到合成、检索和作曲参数；
- 适合构建第一个特征空间浏览器（Feature-Space Browser）。

缺点是：

- 很难完整重建声音；
- 对高级语义表达较弱；
- 多个听觉属性常常耦合（Coupled），例如 centroid 可能同时受到亮度、噪声、响度、乐器类别影响。

### 5.2 A1. 响度 / 能量

| Feature | Output | Auditory Meaning | Creative Mapping | Priority |
|---|---|---|---|---|
| RMS energy | frame curve / mean / std | signal energy | dynamics, intensity | P0 |
| Loudness proxy | frame curve / mean | perceived intensity | subjective dynamics | P0 |
| Dynamic range | clip scalar | contrast between soft/loud | tension, articulation | P1 |
| Envelope slope | curve / event scalar | gesture shape | swelling, fading, attack profile | P1 |

**Notes**：RMS 不等于 loudness，但可作为第一版 proxy。后续可引入 LUFS、A-weighting、Zwicker loudness 或 perceptual loudness model。

### 5.3 A2. 频谱形状

| Feature | Output | Auditory Meaning | Creative Mapping | Priority |
|---|---|---|---|---|
| Spectral centroid | curve / mean / std | brightness | filter cutoff, register, orchestration brightness | P0 |
| Spectral bandwidth | curve / mean / std | spectral spread | timbral width, diffusion | P0 |
| Spectral rolloff | curve / mean / std | high-frequency boundary | brightness boundary, EQ target | P0 |
| Spectral contrast | curve / mean / std | peak-valley contrast | sharpness, articulation | P1 |
| Spectral flatness | curve / mean / std | noise-like vs tone-like | noise-tone balance | P0 |
| Spectral entropy | curve / mean / std | spectral complexity | texture complexity | P0 |
| Spectral flux | curve / mean / std | spectral change rate | motion, instability, rhythmic activity | P0 |

**Failure modes**：

- 高 centroid 可能表示噪声，也可能表示明亮谐波；
- flatness 高不一定“粗糙”，可能只是宽带噪声；
- rolloff 对响度和预处理敏感；
- flux 会受 transient、vibrato、background noise 同时影响。

### 5.4 A3. 时间 / 事件特征

| Feature | Output | Auditory Meaning | Creative Mapping | Priority |
|---|---|---|---|---|
| Onset density | clip scalar / time window curve | event density | rhythm density, grain density | P0 |
| Attack time | event scalar / clip summary | percussiveness / onset sharpness | envelope attack, articulation | P1 |
| Decay time | event scalar / clip summary | resonance / damping | sustain, tail shape | P2 |
| Transient ratio | scalar / curve | impact proportion | percussive vs sustained balance | P1 |
| Temporal centroid | scalar | energy center in time | gesture position, front-loaded vs back-loaded | P1 |

**Notes**：Temporal features 是 feature trajectory composition 的直接入口。它们不仅描述声音“是什么”，也描述声音“如何发生”。

### 5.5 A4. 音高 / 谐波性

| Feature | Output | Auditory Meaning | Creative Mapping | Priority |
|---|---|---|---|---|
| Fundamental frequency (f0) | curve / summary | pitch | pitch mapping, register | P1 |
| Pitch confidence | curve / mean | pitch stability | stable vs unstable sound | P1 |
| Harmonicity | scalar / curve | tonal vs noisy | harmonic/noise balance | P1 |
| Inharmonicity | scalar / curve | metallic / bell-like quality | FM index, modal synthesis | P1 |
| Chroma | 12-D vector / summary | pitch-class distribution | harmonic color, pitch-space relation | P1 |

**Failure modes**：

- 对自然声、噪声和复合场景，f0 可能不可靠；
- chroma 对非音乐声音意义有限；
- inharmonicity 需要稳定 partial tracking，第一版可暂缓。

### 5.6 A5. 粗糙度 / 不协和 / 纹理

| Feature | Output | Auditory Meaning | Creative Mapping | Priority |
|---|---|---|---|---|
| Roughness | scalar / curve | beating, sensory roughness | tension, instability | P1 |
| Sensory dissonance | scalar / curve | perceptual dissonance | harmonic tension | P2 |
| Modulation energy | curve / summary | vibration / tremor / grain | motion, shimmer, turbulence | P2 |
| Texture entropy | scalar / curve | texture complexity | density, turbulence, organic complexity | P1 |

**Notes**：Roughness 对创作很有价值，但实现依赖模型选择。第一版可以使用简化 roughness estimate，后续再替换为更严谨的 psychoacoustic model。

### 5.7 A6. 倒谱 / 音色概要

| Feature | Output | Auditory Meaning | Creative Mapping | Priority |
|---|---|---|---|---|
| MFCC mean/std | vector | spectral envelope summary | timbre clustering, retrieval | P0 |
| Delta MFCC | vector | envelope change | evolving timbre | P1 |
| Mel-band energy | vector / curve | perceptual-band profile | EQ-like timbre control | P1 |

**Notes**：MFCC 可解释性弱于 centroid/flatness，但非常适合建立 baseline retrieval 和 projection。

### 5.8 家族 A 小结

| 维度 | 评分 | 理由 |
|---|---:|---|
| 可闻性（Audibility） | 3 | 多数描述符有明确听觉对应 |
| 可解释性（Interpretability） | 3 | 可命名、可解释 |
| 可控性（Controllability） | 2–3 | 适合直接映射（Mapping），但属性可能耦合 |
| 可重建性（Reconstructability） | 0–1 | 无法单独重建完整声音 |
| 语义对齐（Semantic Alignment） | 1 | 可支持材质/音色语义，但不是强语义模型 |
| 创作可供性（Creative Affordance） | 3 | 最适合第一阶段创作映射（Creative Mapping）
| Computational Cost | 3 | librosa/scipy 即可实现 |
| Reproducibility | 3 | 成熟、稳定、易复现 |

**Conclusion**：Family A 是 Phase 2 的第一优先级。

---

## 6. 家族 B — 稀疏分解与声音原子（Sparse Decomposition & Sound Atoms）

### 6.1 作用

稀疏分解（Sparse Decomposition）的核心价值不是分类，而是将声音拆成可操作的“粒子”：

```text
audio
  → atoms / templates / activations（原子 / 模板 / 激活）
  → recomposition / rearrangement / texture editing（重组 / 重排 / 纹理编辑）
```

这类方法与现有 `experiments/wave_packet_sparse/` 和 `demos/foundations/wave_packet_demo.html` 直接相关。

### 6.2 B1. STFT / CQT 峰值

| Unit | Meaning | Creative Use |
|---|---|---|
| time-frequency peak | 局部谱峰 | partial editing, peak selection |
| sinusoidal track | 连续谐波轨迹 | tonal resynthesis, pitch/timbre morphing |
| transient component | 短时事件 | attack extraction, percussive rearrangement |

适合：

- pitched instruments；
- partial tracking；
- tonal / harmonic sounds；
- STFT-based visual editing。

限制：

- 对噪声、纹理和复杂混合声音不够自然；
- peak tracking 容易断裂；
- 相位重建和 overlap-add 细节会影响结果。

### 6.3 B2. Gabor 原子 / 匹配追踪

Gabor atom 可以表示为：

```text
atom = (time_center, frequency_center, scale/sigma, amplitude, phase)
```

| Parameter | Meaning | Creative Interpretation |
|---|---|---|
| time center | 事件位置 | when a grain occurs |
| frequency center | 频率中心 | pitch / spectral region |
| scale / sigma | 时间-频率展宽 | short transient vs long tone |
| amplitude | 能量 | event intensity |
| phase | 局部相位 | reconstruction detail |

创作价值：

- 声音粒子；
- sparse score；
- granular recomposition；
- time-frequency material extraction；
- event-level transformation。

限制：

- greedy matching pursuit 计算成本较高；
- fixed dictionary 可能无法匹配真实乐器的非对称 attack/decay；
- 解释性依赖 atom 是否符合听觉事件。

### 6.4 B3. NMF 模板与激活

NMF 将 magnitude spectrogram 分解为：

```text
V ≈ W H

W = spectral templates
H = temporal activations
```

| Component | Meaning | Creative Use |
|---|---|---|
| spectral template | 声音部件 / 音色模板 | learned timbre palette |
| temporal activation | 出现时间 / 强度轨迹 | event pattern / texture rhythm |

适合：

- drum loops；
- repetitive textures；
- monaural source-like separation；
- spectrum-template-based recomposition。

限制：

- 线性 magnitude model 简化过强；
- local minima；
- component 可能不对应真实声源；
- phase reconstruction 仍需额外处理。

### 6.5 B4. K-SVD / 学习字典

K-SVD 和 sparse coding 可以从语料中学习 overcomplete dictionary：

```text
signal patches ≈ dictionary atoms × sparse codes
```

| Unit | Meaning | Creative Use |
|---|---|---|
| learned atom | corpus-specific sound vocabulary | learned grains, timbre units |
| sparse code | atom usage pattern | recomposition score |

适合：

- corpus-specific sound vocabulary；
- natural sound texture units；
- learned audio atoms；
- hybrid symbolic/audio composition。

限制：

- 参数选择复杂；
- 学到的 atom 未必可解释；
- 需要较规范的数据集；
- 重建质量和创作价值需要主观评价。

### 6.6 家族 B 小结

| 维度 | 评分 | 理由 |
|---|---:|---|
| 可闻性（Audibility） | 2 | 原子或分量常对应可闻事件，但不稳定 |
| 可解释性（Interpretability） | 2 | Gabor/NMF 较可解释，学习原子（Learned Atoms）需检查 |
| 可控性（Controllability） | 2 | 可重排、删减、变形，但非总是独立控制 |
| 可重建性（Reconstructability） | 2 | 可部分到较好重建，取决于方法与预算 |
| 语义对齐（Semantic Alignment） | 1 | 通常弱语义，需要标签或嵌入辅助 |
| 创作可供性（Creative Affordance） | 3 | 很适合粒子化、重组、纹理作曲（Texture Composition）
| Computational Cost | 1–2 | 可能比 descriptors 昂贵 |
| Reproducibility | 2 | 方法成熟，但实现细节影响较大 |

**Conclusion**：Family B 应作为 Phase 2–3 的 explainable material extraction 分支，并复用现有 wave packet sparse 实验。

---

## 7. 家族 C — 判别式与语义嵌入（Discriminative & Semantic Embeddings）

### 7.1 作用

嵌入（Embedding）的主要功能是组织声音素材库：

- 语料库组织（Corpus Organization）；
- 相似性搜索（Similarity Search）；
- 聚类（Clustering）；
- 语义导航（Semantic Navigation）；
- 音频-文本检索（Audio-Text Retrieval）；
- 发现意外近邻（Surprising Neighbors）。

但嵌入通常不适合直接作为可控合成参数，因为它们的维度不一定有独立听觉意义。

### 7.2 候选模型

| Model | Type | Strength | Weakness | Phase |
|---|---|---|---|---|
| PANNs | supervised audio tagging | strong general audio embedding | label-biased, not generative | Phase 3 |
| AST | Transformer classifier | strong classification, global context | classification-oriented | Phase 3 |
| BYOL-A | self-supervised | robust general embedding | low interpretability | Phase 3 |
| AudioMAE | masked autoencoding SSL | strong representation | not directly controllable | Phase 3 |
| OpenL3 | audio-visual SSL | environmental / semantic embedding | depends on audiovisual correlations | Phase 3 |
| CLAP | audio-text contrastive | semantic search, text query | semantic similarity may diverge from perceptual similarity | Phase 3 |

### 7.3 三种相似性（Three Kinds of Similarity）

嵌入评估必须区分三种相似性：

```text
声学相似性（Acoustic Similarity） ≠ 语义相似性（Semantic Similarity） ≠ 创作有用性（Creative Usefulness）
```

| 相似性类型 | 问题 | 示例 |
|---|---|---|
| 声学相似性 | 听起来像不像？ | flute 和 whistle 都明亮/有调 |
| 语义相似性 | 标签或意义像不像？ | rain 和 river 都是水 |
| 创作相似性 | 是否能替代或启发创作？ | metallic scrape 作为 cymbal 纹理的替代 |

失败示例：

- 两段声音都很 bright，但一个是 bird，一个是 flute；
- 两段声音语义都是 water，但 rain 和 stream 的纹理差异很大；
- CLAP 可能语义相近，但听感距离并不近；
- classifier embedding 可能按 AudioSet label 聚类，而不是按作曲者关心的质感聚类。

### 7.4 评估方法

| Evaluation | Purpose |
|---|---|
| nearest-neighbor listening | 检查检索结果是否听感合理 |
| category clustering | 检查类别组织能力 |
| descriptor correlation | 检查 embedding dimensions/neighborhoods 是否与 centroid/roughness/density 等相关 |
| robustness tests | pitch shift、time stretch、noise perturbation 后 embedding 是否稳定 |
| text query test | CLAP 是否能按 semantic descriptor 找到素材 |
| composer usefulness rating | 检索结果是否有创作价值 |

### 7.5 家族 C 小结

| 维度 | 评分 | 理由 |
|---|---:|---|
| 可闻性（Audibility） | 1–2 | 邻域可能可闻，单维度通常不可闻 |
| 可解释性（Interpretability） | 1 | 维度难以命名，CLAP 有语义解释优势 |
| 可控性（Controllability） | 1 | 不适合直接控制声音生成 |
| 可重建性（Reconstructability） | 0 | 多数嵌入不能重建音频 |
| 语义对齐（Semantic Alignment） | 2–3 | CLAP/PANNs/AST 强，BYOL-A/AudioMAE 中等 |
| 创作可供性（Creative Affordance） | 2 | 很适合浏览器、检索（Retrieval）、导航（Navigation）
| Computational Cost | 1–2 | 预训练模型成本中等 |
| Reproducibility | 2 | 依赖权重、框架和模型接口 |

**Conclusion**：Family C 是 Phase 3 的核心，主要用于 feature-space browser 的语义导航与相似性检索；它需要与 Family A 的 perceptual descriptors 交叉验证。

---

## 8. 家族 D — 生成式潜变量与音频标记（Generative Latents & Audio Tokens）

### 8.1 作用

生成式特征的关键能力是：

```text
feature / latent / token（特征 / 潜变量 / 标记）
  → audio output（音频输出）
```

它们与判别式嵌入最大区别是：它们通常可以重建或生成音频，因此是潜空间变形（Latent Morphing）、重合成（Resynthesis）和生成式作曲（Generative Composition）的核心。

### 8.2 D1. DDSP 控制参数（DDSP Controls）

DDSP 使用神经网络预测可解释 DSP 控制：

| 控制参数 | 含义 | 创作用途 |
|---|---|---|
| f0（基频） | 音高（Pitch） | 音高轨迹、旋律控制 |
| loudness（响度） | 动态（Dynamics） | 包络和强度 |
| harmonic distribution（谐波分布） | 音色（Timbre） | 谐波色彩 |
| noise filter（噪声滤波器） | 气息 / 噪声分量 | 弓弦噪声、气息、纹理 |

优势：

- 可解释性强；
- 控制明确；
- 与传统合成（Synthesis）语言相容；
- 适合有调 / 准谐波乐器（Quasi-Harmonic Instruments）。

限制：

- 对自然声、城市声、复杂噪声纹理较弱；
- 需要训练或预训练模型；
- 不是通用声学潜变量。

### 8.3 D2. RAVE 潜变量（RAVE Latent）

RAVE 提供实时神经音频合成潜空间（Neural Audio Synthesis Latent Space）。

| 单位 | 含义 | 创作用途 |
|---|---|---|
| 潜向量（Latent Vector） | 学到的音色/纹理状态 | 变形、表演控制 |
| 潜变量遍历（Latent Traversal） | 在潜空间中移动 | 声音变换 |

优势：

- 实时性强；
- 适合表演和声音设计（Sound Design）；
- 可做潜变量插值（Latent Interpolation） / 遍历；
- 对宽泛音色材料有创作吸引力。

限制：

- 潜变量维度纠缠（Entangled Dimensions）；
- 单维变化未必可命名；
- 需要感知验证（Perceptual Validation）；
- 模型训练语料会强烈影响空间结构。

### 8.4 D3. EnCodec / DAC / SoundStream 标记（Tokens）

神经编解码器（Neural Codec）将音频压缩成离散标记（Discrete Token）或残差向量量化编码（Residual Vector Quantization Code）。

| 单位 | 含义 | 创作用途 |
|---|---|---|
| 离散编解码标记（Discrete Codec Token） | 可重建的音频符号 | 标记重组、序列建模 |
| 残差量化层级（Residual Quantizer Level） | 粗到细的细节层 | 抽象/细节控制 |
| 标记序列（Token Sequence） | 后符号音频总谱（Post-Symbolic Audio Score） | 音频语言建模 |

优势：

- 高质量重建；
- 标记作曲（Token Composition）可能性大；
- 可与语言建模（Language Modeling）结合；
- 适合未来“audio score”概念。

限制：

- token 语义不透明；
- 单 token 不一定有可听解释；
- 需要 probing、clustering 或 descriptor alignment 才能用于 human control。

### 8.5 D4. AudioLDM / CLAP 条件潜变量

AudioLDM 等系统使用 CLAP 或文本/音频条件潜变量（Text/Audio-Conditioned Latent）进行生成。

| 单位 | 含义 | 创作用途 |
|---|---|---|
| 文本条件潜变量（Text-Conditioned Latent） | 语义生成状态 | 基于提示的声音设计（Prompt-Based Sound Design） |
| 音频条件潜变量（Audio-Conditioned Latent） | 声音到声音生成 | 变体、风格迁移（Style Transfer） |
| 扩散轨迹（Diffusion Trajectory） | 迭代生成路径 | 受控变换 |

优势：

- 语义控制强；
- 适合声音设计提示（Sound Design Prompt）；
- 能生成复杂声音场景；
- 与基于 CLAP 的浏览器自然衔接。

限制：

- 细粒度可控性（Fine-Grained Controllability）较弱；
- 生成稳定性、版权和数据来源需注意；
- 提示相似性（Prompt Similarity）不等于感知可控性（Perceptual Controllability）。

### 8.6 家族 D 小结

| 维度 | 评分 | 理由 |
|---|---:|---|
| 可闻性（Audibility） | 2–3 | 潜变量/标记变化常可闻，但方向未必清楚 |
| 可解释性（Interpretability） | 1–2 | DDSP 高，RAVE/编解码标记低 |
| 可控性（Controllability） | 2 | 可变形/生成，但维度可能耦合 |
| 可重建性（Reconstructability） | 3 | 这是该类核心优势 |
| 语义对齐（Semantic Alignment） | 1–3 | AudioLDM/CLAP 高，RAVE/编解码标记低 |
| 创作可供性（Creative Affordance） | 3 | 变形、重合成、生成核心 |
| Computational Cost | 0–2 | 依赖模型，通常比 descriptors 昂贵 |
| Reproducibility | 1–2 | 依赖权重、训练语料、GPU、版本 |

**Conclusion**：Family D 是 Phase 4 及之后的核心，不应作为第一阶段 baseline；应在 Family A browser 和 Family C retrieval 稳定后进入 latent traversal。

---

## 9. 跨家族比较（Cross-Family Comparison）

| 家族 | 可闻性 | 可解释性 | 可控性 | 可重建性 | 语义对齐 | 创作用途 | 推荐阶段 |
|---|---:|---:|---:|---:|---:|---|---|
| 心理声学描述符 | 3 | 3 | 3 | 0–1 | 1 | 直接映射、特征轨迹 | Phase 2 |
| 稀疏原子/模板 | 2 | 2 | 2 | 2 | 1 | 重组、声音粒子 | Phase 2–3 |
| 判别式嵌入 | 1–2 | 1 | 1 | 0 | 2–3 | 检索、聚类、导航 | Phase 3 |
| 生成式潜变量/标记 | 2–3 | 1–2 | 2 | 3 | 1–3 | 变形、重合成、生成 | Phase 4 |

实际排序：

```text
1. 从心理声学描述符开始。
2. 添加稀疏分解用于事件/材料提取。
3. 添加嵌入用于语料库规模的导航。
4. 添加生成式潜变量/标记用于变换和合成。
```

---

## 10. 基线实验最小可行特征集（MVP Feature Set）

The first baseline implementation should be deliberately modest. It should produce a reliable feature table and 2D map before introducing heavy ML models.

目标目录：

```text
experiments/creative_features/01_baseline_features/
```

### 10.1 MVP 特征集 v0

| Group | Feature | Output | Priority |
|---|---|---|---|
| Energy | RMS mean/std | scalar pair | P0 |
| Energy | loudness proxy | scalar / curve summary | P0 |
| Spectral | spectral centroid mean/std | scalar pair | P0 |
| Spectral | spectral bandwidth mean/std | scalar pair | P0 |
| Spectral | spectral rolloff mean/std | scalar pair | P0 |
| Spectral | spectral flatness mean/std | scalar pair | P0 |
| Spectral | spectral flux mean/std | scalar pair | P0 |
| Temporal | onset density | scalar | P0 |
| Cepstral | MFCC mean/std | vector | P0 |
| Texture | spectral entropy mean/std | scalar pair | P0 |
| Temporal | attack time estimate | scalar | P1 |
| Harmonic | chroma mean/std | vector | P1 |
| Harmonic | f0 confidence / pitch stability | scalar | P1 |
| Texture | roughness estimate | scalar / curve summary | P1 |

### 10.2 延后特征

| Feature | Reason to Defer |
|---|---|
| full psychoacoustic loudness model | Need model selection and calibration |
| rigorous roughness / dissonance model | Implementation choices affect validity |
| inharmonicity | Requires reliable partial/f0 tracking |
| NMF templates | Better after baseline feature table exists |
| CLAP / PANNs / AST embeddings | Belongs to Phase 3 embedding comparison |
| RAVE / DDSP / EnCodec latents | Belongs to Phase 4 latent traversal |

### 10.3 概念输出 Schema

A baseline feature table should be easy to inspect, project and join with manual labels.

```text
sample_id
file_path
duration
sample_rate
category
manual_tags

rms_mean
rms_std
loudness_proxy_mean
loudness_proxy_std
centroid_mean
centroid_std
bandwidth_mean
bandwidth_std
rolloff_mean
rolloff_std
flatness_mean
flatness_std
flux_mean
flux_std
onset_density
attack_time
entropy_mean
entropy_std
mfcc_01_mean
mfcc_01_std
...
mfcc_13_mean
mfcc_13_std
chroma_01_mean
...
chroma_12_std
```

Suggested later artifacts:

```text
data/processed/baseline_features.csv
data/processed/baseline_projection.json
data/processed/baseline_neighbors.json
```

Because `data/processed/` is intended for generated data, scripts should be reproducible and outputs should not necessarily be committed unless small demo fixtures are intentionally curated.

---

## 11. 特征卡片模板

每个 feature 后续都应可以写成一张 feature card。

```markdown
### Feature Name

| Field | Description |
|---|---|
| Family | Psychoacoustic / Sparse / Embedding / Generative |
| Output Unit | scalar / curve / vector / atom / token |
| Time Scale | frame-level / clip-level / event-level |
| Auditory Correlate | 人耳对应听感 |
| Extraction Method | 如何计算 |
| Normalization | 如何归一化 |
| Creative Mapping | 可映射到什么创作参数 |
| Validation Method | 如何验证可闻性或有用性 |
| Failure Modes | 什么情况下会误导 |
| Experiment Priority | P0 / P1 / P2 |
```

Example:

### Spectral Centroid

| Field | Description |
|---|---|
| Family | Psychoacoustic descriptor |
| Output Unit | frame-level curve, clip-level mean/std |
| Time Scale | frame-level → clip summary |
| Auditory Correlate | brightness |
| Extraction Method | weighted mean of frequency bins |
| Normalization | Hz, optionally log-frequency or z-score across corpus |
| Creative Mapping | filter cutoff, orchestration brightness, register |
| Validation Method | compare with human brightness ratings and nearest-neighbor listening |
| Failure Modes | high centroid may indicate noise rather than harmonic brightness |
| Experiment Priority | P0 |

---

## 12. 特征到创作的映射（Feature-to-Creation Mapping）

分类体系必须最终服务创作。以下是从特征到创作材料的映射类型。

| 映射类型 | 输入特征 | 输出创作材料 | 示例 |
|---|---|---|---|
| 直接参数映射（Direct Parameter Mapping） | centroid, loudness, roughness | 合成控制 | centroid → filter cutoff |
| 轨迹作曲（Trajectory Composition） | 特征曲线 | 音乐形式 | roughness 逐渐增强 |
| 语料库导航（Corpus Navigation） | 描述符 / 嵌入 | 素材选择 | 找“明亮 + 密集”附近的声音 |
| 颗粒重组（Granular Recomposition） | 原子 / 起始点 | 重排纹理 | 按密度重排 Gabor 原子 |
| 潜变量变形（Latent Morphing） | RAVE / DDSP 潜变量 | 生成的变换 | 插值 metal → voice 纹理 |
| 标记编辑（Token Editing） | EnCodec / DAC 编码 | 后符号音频总谱 | 按纹理类别替换标记区域 |
| 混合总谱（Hybrid Scoring） | 特征图 + 手工手势 | 作曲草图 | 在特征空间中绘制路径 |

This suggests the first creative prototype should not start with synthesis. It should start with browsing and hearing feature relationships:

```text
audio corpus
  → baseline descriptors
  → 2D projection
  → nearest neighbors
  → manual listening
  → feature trajectory sketch
```

---

## 13. 开放问题与研究缺口

| Gap | Why It Matters | Follow-up |
|---|---|---|
| Descriptor-feature coupling | Centroid, flatness, loudness, noise and category can be confounded | Correlation matrix + listening checks |
| Human labels missing | Feature usefulness depends on perception | Add manual perceptual tags |
| Embedding vs perception mismatch | CLAP/PANNs may reflect labels more than sound qualities | Cross-check with descriptors and subjective ratings |
| Sparse atom interpretability | Atom parameters may not map cleanly to heard events | Visual + audio atom audition |
| Latent traversal ambiguity | One latent coordinate may affect many attributes | ABX + semantic rating |
| Creative usefulness not standardized | Classification metrics do not measure compositional value | Composer rating / sound studies |
| Dataset scope unclear | Feature behavior depends on corpus | Start with small balanced corpus |

---

## 14. 下一步实验

### Step 1 — Write experiment protocol

Create:

```text
docs/literature/03_experiment_protocol.md
```

It should define:

- dataset size and categories;
- audio preprocessing;
- baseline features;
- normalization;
- projection method;
- nearest-neighbor retrieval;
- manual label format;
- evaluation criteria;
- generated artifacts.

### Step 2 — Implement baseline feature extraction

Target:

```text
experiments/creative_features/01_baseline_features/
```

Minimum implementation:

```text
make_manifest.py
extract_features.py
project_features.py
README.md
```

Expected workflow:

```text
data/raw/small_corpus/
  → manifest.csv
  → baseline_features.csv
  → baseline_projection.json
  → nearest_neighbors.json
```

### Step 3 — Build first feature-space browser

Target:

```text
demos/creative_features/feature_space_browser.html
```

Minimum features:

- display 2D projection;
- color by category or tag;
- click point to inspect feature values;
- optional audio playback if demo audio is available;
- show nearest neighbors;
- support feature-based filtering.

### Step 4 — Prepare embedding comparison

After baseline descriptors are stable, compare:

- PANNs;
- AST;
- BYOL-A;
- AudioMAE;
- OpenL3;
- CLAP.

Evaluation should compare embedding neighborhoods against:

- manual labels;
- descriptor distances;
- subjective listening checks;
- creative usefulness ratings.

---

## 15. 工作结论

1. Sonic Atlas 应采用 **四大家族混合分类体系**: psychoacoustic descriptors, sparse atoms, embeddings, and generative latents/tokens.
2. Phase 2 应从 **P0 手工描述符开始**, 因为它们可解释、可闻、便宜、可复现，且直接对创作映射有用.
3. 稀疏分解应保留为重要分支，因为它暴露了事件化的声音粒子，且与现有波包工作相连接。
4. 嵌入应主要用于检索、聚类和语义导航，而非作为直接可控的合成参数。
5. 生成式潜变量/token 对后续变形和重合成至关重要，但在被视为创作控制之前需要感知验证。
6. 下一步文档应是 `03_experiment_protocol.md`, 随后是基线实现 `experiments/creative_features/01_baseline_features/`.

---

## 参考文献与内部来源

Internal Sonic Atlas documents:

- [`docs/vision.md`](../vision.md)
- [`docs/architecture.md`](../architecture.md)
- [`docs/roadmap.md`](../roadmap.md)
- [`docs/literature/00_research_plan.md`](00_research_plan.md)
- [`docs/literature/01_first_round_review.md`](01_first_round_review.md)
- [`docs/foundations/01_discretization_precision.md`](../foundations/01_discretization_precision.md)
- [`docs/foundations/02_phase_perception.md`](../foundations/02_phase_perception.md)
- [`docs/foundations/03_wave_packets.md`](../foundations/03_wave_packets.md)
- [`docs/foundations/04_timbre_characterization.md`](../foundations/04_timbre_characterization.md)
- [`docs/foundations/05_cnn_feature_extraction.md`](../foundations/05_cnn_feature_extraction.md)

Core systems and papers identified in the first review:

- DDSP — Differentiable Digital Signal Processing
- RAVE — Realtime Audio Variational autoEncoder
- EnCodec — High Fidelity Neural Audio Compression
- SoundStream — End-to-End Neural Audio Codec
- AudioLM / MusicLM — language modeling over audio tokens
- AudioLDM — latent diffusion for text-to-audio generation
- LAION-CLAP — contrastive language-audio pretraining
- AudioMAE — masked autoencoding for audio spectrograms
- BYOL-A — self-supervised audio representation learning
- AST — Audio Spectrogram Transformer
- PANNs — pretrained audio neural networks
- OpenL3 — audiovisual self-supervised audio embeddings
- Matching Pursuit / Gabor atoms
- K-SVD dictionary learning
- NMF monaural source separation

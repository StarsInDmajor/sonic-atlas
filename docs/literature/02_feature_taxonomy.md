# Feature Taxonomy: 面向音乐创作的声音特征分类体系

> **目标**：建立一个面向音乐创作的声音特征分类体系，说明不同特征如何从音频中提取、如何被人耳感知、是否可解释、是否可控、是否可重建，以及如何转化为创作材料。

---

## 1. Purpose and Scope

Sonic Atlas 的主线不是只做音频分类，也不是只做声音合成，而是建立一条从真实声音到创作材料的链路：

```text
Audio
  → Decomposition
  → Abstract Feature Extraction
  → Perceptual Validation
  → Creative Mapping
  → Composition System
```

本 taxonomy 的作用是承接第一轮 literature review，并为后续实验提供决策框架：

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

## 2. Design Principles

### 2.1 Perception before metrics

一个特征在模型中有效，不代表它在人耳中有意义。Sonic Atlas 中的 feature 必须尽量回答：

- 改变它，人能否听出差异？
- 人能否描述变化方向？
- 它是否对应 brightness、roughness、attack、density、metallic、organic 等可交流的听觉概念？

### 2.2 Control before novelty

生成新声音不是最终目标。更重要的是：

- 能否沿着一个可理解方向变化？
- 能否单独控制某个听觉属性？
- 能否被组合成 feature trajectory、sound map 或 compositional gesture？

### 2.3 Hybrid representations over a single latent

没有单一 representation 同时满足所有目标。

```text
Handcrafted descriptors: interpretable + controllable, but weak reconstruction.
Sparse atoms: event-like + recomposable, but limited expressiveness.
Embeddings: strong retrieval/semantics, but weak direct control.
Generative latents/tokens: strong synthesis/reconstruction, but weak interpretability.
```

因此 Sonic Atlas 应采用 multi-layer feature stack，而不是追求一个万能 latent space。

### 2.4 Creation as evaluation

一个 feature 最终是否有价值，不只取决于分类准确率、重建误差或检索指标，还取决于它是否能支撑：

- sound design decision
- corpus navigation
- feature trajectory composition
- latent morphing
- granular recomposition
- sound study / etude / composition sketch

---

## 3. Taxonomy Overview

Sonic Atlas 将声音特征分为四大家族：

| Family | Unit | Main Role | Typical Use |
|---|---|---|---|
| **A. Psychoacoustic descriptors** | scalar / curve | 可命名、可解释控制 | brightness、roughness、density |
| **B. Sparse decomposition** | atom / template / activation | 声音粒子、事件、素材重组 | Gabor atoms、NMF、K-SVD |
| **C. Discriminative embeddings** | vector | 检索、聚类、语义导航 | PANNs、AST、BYOL-A、CLAP |
| **D. Generative latents / tokens** | latent / discrete code | morphing、resynthesis、generation | DDSP、RAVE、EnCodec、AudioLDM |

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

## 4. Evaluation Axes

每类 feature 都应按统一维度评价。

| Axis | Core Question | Practical Interpretation |
|---|---|---|
| **Audibility** | 改变该特征，人耳能否听出差异？ | 是否有明确听觉对应 |
| **Interpretability** | 人能否给它命名？ | brightness、roughness、attack、density 等 |
| **Controllability** | 能否独立控制？ | 改一个参数是否主要改变一个听觉属性 |
| **Reconstructability** | 能否帮助重建原声音？ | 是否保留足够 signal information |
| **Semantic Alignment** | 是否对应语义标签？ | bird、water、metallic、warm、mechanical 等 |
| **Temporal Resolution** | 是否能表达随时间变化？ | clip scalar、frame curve、event sequence |
| **Creative Affordance** | 是否能直接成为创作材料？ | 能否映射到作曲 / sound design / navigation |
| **Computational Cost** | 提取或生成成本如何？ | 是否适合快速实验和交互 |
| **Reproducibility** | 是否容易复现？ | 是否有成熟库、公开模型、稳定接口 |

建议评分采用 0–3：

| Score | Meaning |
|---:|---|
| 0 | 不适用或很弱 |
| 1 | 有一定价值，但不稳定 |
| 2 | 可用，适合实验 |
| 3 | 强，适合作为核心特征 |

---

## 5. Family A — Psychoacoustic and Handcrafted Descriptors

### 5.1 Role

Psychoacoustic descriptors 是第一阶段 baseline 的核心。它们的优势是：

- 可解释；
- 计算成本低；
- 大多有明确听觉对应；
- 可以直接映射到合成、检索和作曲参数；
- 适合构建第一个 feature-space browser。

缺点是：

- 很难完整重建声音；
- 对高级语义表达较弱；
- 多个听觉属性常常耦合，例如 centroid 可能同时受到亮度、噪声、响度、乐器类别影响。

### 5.2 A1. Loudness / Energy

| Feature | Output | Auditory Meaning | Creative Mapping | Priority |
|---|---|---|---|---|
| RMS energy | frame curve / mean / std | signal energy | dynamics, intensity | P0 |
| Loudness proxy | frame curve / mean | perceived intensity | subjective dynamics | P0 |
| Dynamic range | clip scalar | contrast between soft/loud | tension, articulation | P1 |
| Envelope slope | curve / event scalar | gesture shape | swelling, fading, attack profile | P1 |

**Notes**：RMS 不等于 loudness，但可作为第一版 proxy。后续可引入 LUFS、A-weighting、Zwicker loudness 或 perceptual loudness model。

### 5.3 A2. Spectral Shape

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

### 5.4 A3. Temporal / Event Features

| Feature | Output | Auditory Meaning | Creative Mapping | Priority |
|---|---|---|---|---|
| Onset density | clip scalar / time window curve | event density | rhythm density, grain density | P0 |
| Attack time | event scalar / clip summary | percussiveness / onset sharpness | envelope attack, articulation | P1 |
| Decay time | event scalar / clip summary | resonance / damping | sustain, tail shape | P2 |
| Transient ratio | scalar / curve | impact proportion | percussive vs sustained balance | P1 |
| Temporal centroid | scalar | energy center in time | gesture position, front-loaded vs back-loaded | P1 |

**Notes**：Temporal features 是 feature trajectory composition 的直接入口。它们不仅描述声音“是什么”，也描述声音“如何发生”。

### 5.5 A4. Pitch / Harmonicity

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

### 5.6 A5. Roughness / Dissonance / Texture

| Feature | Output | Auditory Meaning | Creative Mapping | Priority |
|---|---|---|---|---|
| Roughness | scalar / curve | beating, sensory roughness | tension, instability | P1 |
| Sensory dissonance | scalar / curve | perceptual dissonance | harmonic tension | P2 |
| Modulation energy | curve / summary | vibration / tremor / grain | motion, shimmer, turbulence | P2 |
| Texture entropy | scalar / curve | texture complexity | density, turbulence, organic complexity | P1 |

**Notes**：Roughness 对创作很有价值，但实现依赖模型选择。第一版可以使用简化 roughness estimate，后续再替换为更严谨的 psychoacoustic model。

### 5.7 A6. Cepstral / Timbre Summary

| Feature | Output | Auditory Meaning | Creative Mapping | Priority |
|---|---|---|---|---|
| MFCC mean/std | vector | spectral envelope summary | timbre clustering, retrieval | P0 |
| Delta MFCC | vector | envelope change | evolving timbre | P1 |
| Mel-band energy | vector / curve | perceptual-band profile | EQ-like timbre control | P1 |

**Notes**：MFCC 可解释性弱于 centroid/flatness，但非常适合建立 baseline retrieval 和 projection。

### 5.8 Family A Summary

| Axis | Score | Rationale |
|---|---:|---|
| Audibility | 3 | 多数 descriptor 有明确听觉对应 |
| Interpretability | 3 | 可命名、可解释 |
| Controllability | 2–3 | 适合直接 mapping，但属性可能耦合 |
| Reconstructability | 0–1 | 无法单独重建完整声音 |
| Semantic Alignment | 1 | 可支持 material/timbre 语义，但不是强语义模型 |
| Creative Affordance | 3 | 最适合第一阶段 creative mapping |
| Computational Cost | 3 | librosa/scipy 即可实现 |
| Reproducibility | 3 | 成熟、稳定、易复现 |

**Conclusion**：Family A 是 Phase 2 的第一优先级。

---

## 6. Family B — Sparse Decomposition and Sound Atoms

### 6.1 Role

Sparse decomposition 的核心价值不是分类，而是将声音拆成可操作的“粒子”：

```text
audio
  → atoms / templates / activations
  → recomposition / rearrangement / texture editing
```

这类方法与现有 `experiments/wave_packet_sparse/` 和 `demos/foundations/wave_packet_demo.html` 直接相关。

### 6.2 B1. STFT / CQT Peaks

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

### 6.3 B2. Gabor Atoms / Matching Pursuit

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

### 6.4 B3. NMF Templates and Activations

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

### 6.5 B4. K-SVD / Learned Dictionary

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

### 6.6 Family B Summary

| Axis | Score | Rationale |
|---|---:|---|
| Audibility | 2 | atom 或 component 常对应可闻事件，但不稳定 |
| Interpretability | 2 | Gabor/NMF 较可解释，learned atoms 需检查 |
| Controllability | 2 | 可重排、删减、变形，但非总是独立控制 |
| Reconstructability | 2 | 可部分到较好重建，取决于方法与预算 |
| Semantic Alignment | 1 | 通常弱语义，需要标签或 embedding 辅助 |
| Creative Affordance | 3 | 很适合粒子化、重组、texture composition |
| Computational Cost | 1–2 | 可能比 descriptors 昂贵 |
| Reproducibility | 2 | 方法成熟，但实现细节影响较大 |

**Conclusion**：Family B 应作为 Phase 2–3 的 explainable material extraction 分支，并复用现有 wave packet sparse 实验。

---

## 7. Family C — Discriminative and Semantic Embeddings

### 7.1 Role

Embedding 的主要功能是组织声音素材库：

- corpus organization；
- similarity search；
- clustering；
- semantic navigation；
- audio-text retrieval；
- finding surprising neighbors。

但 embedding 通常不适合直接作为可控合成参数，因为它们的维度不一定有独立听觉意义。

### 7.2 Candidate Models

| Model | Type | Strength | Weakness | Phase |
|---|---|---|---|---|
| PANNs | supervised audio tagging | strong general audio embedding | label-biased, not generative | Phase 3 |
| AST | Transformer classifier | strong classification, global context | classification-oriented | Phase 3 |
| BYOL-A | self-supervised | robust general embedding | low interpretability | Phase 3 |
| AudioMAE | masked autoencoding SSL | strong representation | not directly controllable | Phase 3 |
| OpenL3 | audio-visual SSL | environmental / semantic embedding | depends on audiovisual correlations | Phase 3 |
| CLAP | audio-text contrastive | semantic search, text query | semantic similarity may diverge from perceptual similarity | Phase 3 |

### 7.3 Three Types of Similarity

Embedding evaluation must distinguish three kinds of similarity:

```text
acoustic similarity ≠ semantic similarity ≠ creative usefulness
```

| Similarity Type | Question | Example |
|---|---|---|
| Acoustic similarity | 听起来像不像？ | flute and whistle both bright/tonal |
| Semantic similarity | 标签或意义像不像？ | rain and river both water |
| Creative similarity | 是否能替代或启发创作？ | metallic scrape as alternative to cymbal texture |

Failure examples：

- 两段声音都很 bright，但一个是 bird，一个是 flute；
- 两段声音语义都是 water，但 rain 和 stream 的纹理差异很大；
- CLAP 可能语义相近，但听感距离并不近；
- classifier embedding 可能按 AudioSet label 聚类，而不是按作曲者关心的质感聚类。

### 7.4 Evaluation Methods

| Evaluation | Purpose |
|---|---|
| nearest-neighbor listening | 检查检索结果是否听感合理 |
| category clustering | 检查类别组织能力 |
| descriptor correlation | 检查 embedding dimensions/neighborhoods 是否与 centroid/roughness/density 等相关 |
| robustness tests | pitch shift、time stretch、noise perturbation 后 embedding 是否稳定 |
| text query test | CLAP 是否能按 semantic descriptor 找到素材 |
| composer usefulness rating | 检索结果是否有创作价值 |

### 7.5 Family C Summary

| Axis | Score | Rationale |
|---|---:|---|
| Audibility | 1–2 | neighborhood 可能可闻，单维度通常不可闻 |
| Interpretability | 1 | 维度难以命名，CLAP 有语义解释优势 |
| Controllability | 1 | 不适合直接控制声音生成 |
| Reconstructability | 0 | 多数 embedding 不能重建音频 |
| Semantic Alignment | 2–3 | CLAP/PANNs/AST 强，BYOL-A/AudioMAE 中等 |
| Creative Affordance | 2 | 很适合 browser、retrieval、navigation |
| Computational Cost | 1–2 | 预训练模型成本中等 |
| Reproducibility | 2 | 依赖权重、框架和模型接口 |

**Conclusion**：Family C 是 Phase 3 的核心，主要用于 feature-space browser 的语义导航与相似性检索；它需要与 Family A 的 perceptual descriptors 交叉验证。

---

## 8. Family D — Generative Latents and Audio Tokens

### 8.1 Role

Generative features 的关键能力是：

```text
feature / latent / token
  → audio output
```

它们与 discriminative embeddings 最大区别是：它们通常可以重建或生成音频，因此是 latent morphing、resynthesis 和 generative composition 的核心。

### 8.2 D1. DDSP Controls

DDSP 使用神经网络预测可解释 DSP 控制：

| Control | Meaning | Creative Use |
|---|---|---|
| f0 | pitch | pitch trajectory, melodic control |
| loudness | dynamics | envelope and intensity |
| harmonic distribution | timbre | harmonic color |
| noise filter | breath / noise component | bow noise, breath, texture |

优势：

- 可解释性强；
- 控制明确；
- 与传统 synthesis 语言相容；
- 适合 pitched / quasi-harmonic instruments。

限制：

- 对自然声、城市声、复杂噪声纹理较弱；
- 需要训练或预训练模型；
- 不是通用声学 latent。

### 8.3 D2. RAVE Latents

RAVE 提供实时 neural audio synthesis latent space。

| Unit | Meaning | Creative Use |
|---|---|---|
| latent vector | learned timbre/texture state | morphing, performance control |
| latent traversal | movement through latent space | sonic transformation |

优势：

- 实时性强；
- 适合表演和 sound design；
- 可做 latent interpolation / traversal；
- 对宽泛音色材料有创作吸引力。

限制：

- latent dimensions entangled；
- 单维变化未必可命名；
- 需要 perceptual validation；
- 模型训练语料会强烈影响空间结构。

### 8.4 D3. EnCodec / DAC / SoundStream Tokens

Neural codec 将音频压缩成离散 token 或 residual vector quantization codes。

| Unit | Meaning | Creative Use |
|---|---|---|
| discrete codec token | reconstructive audio symbol | token recombination, sequence modeling |
| residual quantizer level | coarse-to-fine detail layer | abstraction/detail control |
| token sequence | post-symbolic audio score | audio language modeling |

优势：

- 高质量重建；
- token composition 可能性大；
- 可与 language modeling 结合；
- 适合未来“audio score”概念。

限制：

- token 语义不透明；
- 单 token 不一定有可听解释；
- 需要 probing、clustering 或 descriptor alignment 才能用于 human control。

### 8.5 D4. AudioLDM / CLAP-conditioned Latents

AudioLDM 等系统使用 CLAP 或 text/audio-conditioned latent 进行生成。

| Unit | Meaning | Creative Use |
|---|---|---|
| text-conditioned latent | semantic generation state | prompt-based sound design |
| audio-conditioned latent | sound-to-sound generation | variation, style transfer |
| diffusion trajectory | iterative generation path | controlled transformation |

优势：

- 语义控制强；
- 适合 sound design prompt；
- 能生成复杂声音场景；
- 与 CLAP-based browser 自然衔接。

限制：

- fine-grained controllability 较弱；
- 生成稳定性、版权和数据来源需注意；
- prompt similarity 不等于 perceptual controllability。

### 8.6 Family D Summary

| Axis | Score | Rationale |
|---|---:|---|
| Audibility | 2–3 | latent/token 变化常可闻，但方向未必清楚 |
| Interpretability | 1–2 | DDSP 高，RAVE/codec token 低 |
| Controllability | 2 | 可 morph/generate，但维度可能耦合 |
| Reconstructability | 3 | 这是该类核心优势 |
| Semantic Alignment | 1–3 | AudioLDM/CLAP 高，RAVE/codec token 低 |
| Creative Affordance | 3 | morphing、resynthesis、generation 核心 |
| Computational Cost | 0–2 | 依赖模型，通常比 descriptors 昂贵 |
| Reproducibility | 1–2 | 依赖权重、训练语料、GPU、版本 |

**Conclusion**：Family D 是 Phase 4 及之后的核心，不应作为第一阶段 baseline；应在 Family A browser 和 Family C retrieval 稳定后进入 latent traversal。

---

## 9. Cross-Family Comparison

| Family | Audibility | Interpretability | Controllability | Reconstructability | Semantic Alignment | Creative Use | Recommended Phase |
|---|---:|---:|---:|---:|---:|---|---|
| Psychoacoustic descriptors | 3 | 3 | 3 | 0–1 | 1 | direct mapping, feature trajectory | Phase 2 |
| Sparse atoms / templates | 2 | 2 | 2 | 2 | 1 | recomposition, sound particles | Phase 2–3 |
| Discriminative embeddings | 1–2 | 1 | 1 | 0 | 2–3 | retrieval, clustering, navigation | Phase 3 |
| Generative latents / tokens | 2–3 | 1–2 | 2 | 3 | 1–3 | morphing, resynthesis, generation | Phase 4 |

Practical ordering:

```text
1. Start with psychoacoustic descriptors.
2. Add sparse decomposition for event/material extraction.
3. Add embeddings for corpus-scale navigation.
4. Add generative latents/tokens for transformation and synthesis.
```

---

## 10. Minimum Viable Feature Set for Baseline Experiments

The first baseline implementation should be deliberately modest. It should produce a reliable feature table and 2D map before introducing heavy ML models.

Target directory:

```text
experiments/creative_features/01_baseline_features/
```

### 10.1 MVP Feature Set v0

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

### 10.2 Deferred Features

| Feature | Reason to Defer |
|---|---|
| full psychoacoustic loudness model | Need model selection and calibration |
| rigorous roughness / dissonance model | Implementation choices affect validity |
| inharmonicity | Requires reliable partial/f0 tracking |
| NMF templates | Better after baseline feature table exists |
| CLAP / PANNs / AST embeddings | Belongs to Phase 3 embedding comparison |
| RAVE / DDSP / EnCodec latents | Belongs to Phase 4 latent traversal |

### 10.3 Conceptual Output Schema

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

## 11. Feature Card Template

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

## 12. Feature-to-Creation Mapping

Taxonomy 必须最终服务创作。以下是从 feature 到 creative material 的映射类型。

| Mapping Type | Input Feature | Output Creative Material | Example |
|---|---|---|---|
| Direct parameter mapping | centroid, loudness, roughness | synthesis control | centroid → filter cutoff |
| Trajectory composition | feature curve | musical form | roughness gradually increases |
| Corpus navigation | descriptors / embeddings | sample selection | find sounds near “bright + dense” |
| Granular recomposition | atoms / onsets | rearranged texture | reorder Gabor atoms by density |
| Latent morphing | RAVE / DDSP latent | generated transformation | interpolate metal → voice texture |
| Token editing | EnCodec / DAC codes | post-symbolic audio score | replace token regions by texture class |
| Hybrid scoring | feature map + manual gestures | composition sketch | draw path through feature space |

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

## 13. Open Questions and Research Gaps

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

## 14. Next Experimental Steps

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

## 15. Working Conclusions

1. Sonic Atlas should use a **four-family hybrid taxonomy**: psychoacoustic descriptors, sparse atoms, embeddings, and generative latents/tokens.
2. Phase 2 should start with **P0 handcrafted descriptors**, because they are interpretable, audible, cheap, reproducible and directly useful for creative mapping.
3. Sparse decomposition should remain an important branch because it exposes event-like sound particles and connects to the existing wave packet work.
4. Embeddings should be used primarily for retrieval, clustering and semantic navigation, not as directly controllable synthesis parameters.
5. Generative latents/tokens are essential for later morphing and resynthesis, but require perceptual validation before being treated as creative controls.
6. The immediate next document should be `03_experiment_protocol.md`, followed by the baseline implementation in `experiments/creative_features/01_baseline_features/`.

---

## References and Internal Sources

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

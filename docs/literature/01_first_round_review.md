# Literature Review Round 1: 机器学习声音抽象特征与音乐创作素材

> **研究问题**：如何从音乐与自然声音中提取既抽象、又可闻、可控、可创作的声音特征，并将其作为音乐创作素材？

---

## 1. Search Strategy

### Scope

本轮是第一轮 broad scan + focused screening，目标不是穷尽全部文献，而是建立方法地图、筛选核心论文、明确下一步 deep reading 的优先级。

### Sources

- arXiv API：`cs.SD`, `cs.LG`, `eess.AS`, `cs.MM`
- Tavily Search：用于补充非 arXiv 来源、系统页面、项目页面
- Zotero：个人文献库粗略交叉检查
- OpenViking：已有处理文献交叉检查
- Sonic Atlas existing modules：已有模块 1–5、频谱参考页、波包实验

### Search Queries

- `DDSP Differentiable Digital Signal Processing`
- `RAVE variational autoencoder fast high-quality neural audio synthesis`
- `High Fidelity Neural Audio Compression EnCodec`
- `SoundStream End-to-End Neural Audio Codec`
- `AudioLM language modeling audio generation`
- `MusicLM Generating Music From Text`
- `AudioLDM latent diffusion audio generation CLAP`
- `Large-scale Contrastive Language-Audio Pretraining`
- `Masked Autoencoders that Listen AudioMAE`
- `BYOL for Audio self-supervised representation`
- `PANNs Large-Scale Pretrained Audio Neural Networks`
- `Audio Spectrogram Transformer`
- `K-SVD sparse dictionary learning audio`
- `NMF monaural sound source separation audio`

### Inclusion Criteria

纳入文献需满足至少一项：

1. 提供音频分解、表征学习、latent 或 token 表示；
2. 支持重建、生成、检索、分类或可控合成；
3. 可被映射到声音创作工作流；
4. 与人耳感知、可控性、语义对齐或音色空间相关；
5. 有代码、模型或已被广泛复用。

### Exclusion Criteria

排除：

- 纯语音识别且无创作/音色/声音表示价值；
- 纯分类 benchmark 但没有可复用 embedding 或控制机制；
- 仅符号音乐（MIDI）生成，不处理音频；
- 无法重建、生成、检索或解释的黑盒指标论文。

---

## 2. Candidate Pool

| # | Paper / System | Year | ID / DOI / URL | Source | Core Area | Status |
|---|---|---:|---|---|---|---|
| 1 | DDSP: Differentiable Digital Signal Processing | 2020 | arXiv:2001.04643 | arXiv | 可解释神经音频合成 | Core |
| 2 | RAVE: A variational autoencoder for fast and high-quality neural audio synthesis | 2021 | arXiv:2111.05011 | arXiv | 实时 latent 音频合成 | Core |
| 3 | High Fidelity Neural Audio Compression (EnCodec) | 2022 | arXiv:2210.13438 | arXiv | neural codec / quantized latent | Core |
| 4 | SoundStream: An End-to-End Neural Audio Codec | 2021 | arXiv:2107.03312 | arXiv | neural codec / RVQ tokens | Core |
| 5 | AudioLM: a Language Modeling Approach to Audio Generation | 2022 | arXiv:2209.03143 | arXiv | discrete audio tokens / generation | Core |
| 6 | MusicLM: Generating Music From Text | 2023 | arXiv:2301.11325 | arXiv | text-to-music / semantic conditioning | Core |
| 7 | AudioLDM: Text-to-Audio Generation with Latent Diffusion Models | 2023 | arXiv:2301.12503 | arXiv | CLAP latent diffusion | Core |
| 8 | Large-scale Contrastive Language-Audio Pretraining with Feature Fusion and Keyword-to-Caption Augmentation | 2022 | arXiv:2211.06687 | arXiv | CLAP / audio-text embedding | Core |
| 9 | Human-CLAP: Human-perception-based CLAP | 2025 | arXiv:2506.23553 | arXiv | human alignment / evaluation | Watch |
| 10 | Masked Autoencoders that Listen (AudioMAE) | 2022 | arXiv:2207.06405 | arXiv | self-supervised audio embedding | Core |
| 11 | BYOL for Audio: Self-Supervised Learning for General-Purpose Audio Representation | 2021 | arXiv:2103.06695 | arXiv | SSL audio embedding | Core |
| 12 | Audio Self-supervised Learning: A Survey | 2022 | arXiv:2203.01205 | arXiv | survey | Support |
| 13 | AST: Audio Spectrogram Transformer | 2021 | arXiv:2104.01778 | arXiv | audio Transformer embedding | Core |
| 14 | PANNs: Large-Scale Pretrained Audio Neural Networks for Audio Pattern Recognition | 2019 | arXiv:1912.10211 | arXiv | pretrained audio CNN embedding | Core |
| 15 | OpenL3 / Look, Listen, and Learn More | 2019 | Semantic Scholar / project | Tavily | audiovisual self-supervised embedding | Core |
| 16 | DDSP-SFX: Acoustically-guided sound effects generation | 2023 | arXiv:2309.08060 | arXiv | controllable sound effect generation | Watch |
| 17 | Latent Space Explorations of Singing Voice Synthesis using DDSP | 2021 | arXiv:2103.07197 | arXiv | DDSP latent exploration | Watch |
| 18 | LVNS-RAVE: Diversified audio generation with RAVE and Latent Vector Novelty Search | 2024 | arXiv:2404.14063 | arXiv | latent novelty search / creative generation | Watch |
| 19 | K-SVD: An Algorithm for Designing Overcomplete Dictionaries for Sparse Representation | 2006 | IEEE TSP | Known foundational | learned sparse dictionary | Core foundational |
| 20 | Matching Pursuits with Time-Frequency Dictionaries | 1993 | IEEE TSP | Existing module | Gabor atoms / sparse decomposition | Core foundational |
| 21 | Monaural Sound Source Separation by NMF | 2007 | IEEE TASLP | Known foundational | NMF / source components | Core foundational |
| 22 | Phase-intercept distortion as audio augmentation | 2025 | OV: Krishnan & Condit-Schultz | OV | perceptually invariant augmentation | Support |

---

## 3. Personal Library / Existing Knowledge Cross-Check

### Zotero

Query: `DDSP RAVE EnCodec CLAP AudioMAE BYOL-A PANNs AST`

Result: **No data to display** in the broad Zotero query. This likely means these core audio-ML papers are not yet cataloged under obvious title keywords, or the current query is too broad for Zotero CLI matching.

### OpenViking

Scoped search found an existing processed paper collection:

- `viking://resources/research/inbox/papers/2025-krishnan--KD5M8H5D/`

Relevant contents:

| Resource | Relevance |
|---|---|
| `The_Perception_of_2more_51dbbec1.md` | phase-intercept distortion and perceptual invariance |
| `4._DATA_AUGMENTATION_EXPERIMENT.md` | audio data augmentation for ML |
| `REFERENCES_3.md` | references including source separation, wav2vec2.0, AST, AudioSet, MUSDB18-HQ |
| `4.1._Audio_Classification.md` | audio classification experiment with spectrogram/MFCC context |
| `4.2._Blind_Source_2more_fd44872d.md` | source separation and audio ML metrics |

Implication: Sonic Atlas already has processed context for **phase invariance, audio ML augmentation, source separation, and AST references**, which should be reused in later deep reading.

---

## 4. Extraction Table

| Paper / System | Year | Main Claim | Method | Data / Domain | Key Result | Evidence Strength | Limitation | Relevance |
|---|---:|---|---|---|---|---|---|---|
| DDSP | 2020 | Audio synthesis benefits from combining neural networks with differentiable DSP priors | Autoencoder predicts DSP controls: oscillators, filters, noise, reverb | Musical instruments, monophonic pitched audio | High-fidelity synthesis with fewer parameters than black-box generation | Strong | Best for pitched / quasi-harmonic sources; less suited to arbitrary natural textures | Direct for controllable creative features |
| RAVE | 2021 | VAE can provide fast high-quality latent audio synthesis | Encoder-decoder VAE on raw waveform / spectral losses | General audio, music, timbre models | Real-time generation possible, latent space usable in performance | Strong | Latent dimensions can be entangled and hard to name | Direct for latent composition |
| EnCodec | 2022 | Neural codec learns compact quantized latent tokens with high fidelity | Streaming encoder-decoder + residual vector quantization + adversarial spectral loss | Speech, music, general audio | High-fidelity audio compression at low bitrate | Strong | Tokens are not inherently interpretable | Direct for audio-token composition but needs mapping layer |
| SoundStream | 2021 | End-to-end neural codec can represent speech/music/general audio efficiently | Fully convolutional encoder/decoder + residual vector quantizer | Speech, music, general audio | Efficient compression and reconstruction | Strong | Designed for compression, not creative control | Direct as tokenization substrate |
| AudioLM | 2022 | Audio generation can be cast as language modeling over discrete audio tokens | Semantic tokens + acoustic tokens | Speech and piano/music examples | Long-term consistency and high-quality generation | Strong | Heavy model; controllability mediated by tokens, not direct features | Important for token-based composition |
| MusicLM | 2023 | High-fidelity music can be generated from text descriptions using hierarchical token modeling | Text-conditioned hierarchical sequence-to-sequence over audio tokens | Music | Coherent multi-minute music from text | Strong | Limited fine-grained control; closed models/datasets in many cases | Important for semantic composition but less ideal for low-level feature control |
| AudioLDM | 2023 | CLAP latent + latent diffusion enables text-to-audio generation | Diffusion in latent audio representation conditioned by CLAP | AudioCaps / general audio | Text-to-audio synthesis with lower compute than waveform diffusion | Strong | CLAP alignment may not perfectly match human perception | Direct for semantic sound design |
| LAION-CLAP | 2022 | Audio-text contrastive learning yields joint embedding for retrieval/classification | Audio encoder + text encoder contrastive pretraining, LAION-Audio-630K | Audio-text pairs | General audio-text retrieval/classification | Strong | Embedding is semantic, not necessarily acoustically controllable | Direct for corpus navigation and semantic feature search |
| Human-CLAP | 2025 | CLAPScore may correlate weakly with human subjective evaluation; human-perception alignment is needed | Human-perception-based CLAP objective / evaluation | General audio | Highlights gap between embedding similarity and human judgment | Moderate / emerging | Recent; needs replication | Critical for perceptual validation |
| AudioMAE | 2022 | Masked autoencoding on audio spectrograms learns useful SSL representations | MAE on spectrogram patches with high mask ratio | Audio classification tasks | Competitive SSL audio embeddings | Strong | Good representation, but not necessarily reconstructive in a creative sense | Useful for feature extraction / clustering |
| BYOL-A | 2021 | Bootstrap self-supervision can learn general-purpose audio features without negative samples | Augmentation-based BYOL on audio segments | General audio tasks | Strong transfer performance | Strong | Feature dimensions not interpretable | Useful for general embedding baseline |
| AST | 2021 | Transformer over spectrogram patches improves audio classification via global context | Vision Transformer adapted to spectrograms | AudioSet / speech / sound events | Strong classification performance | Strong | Classification-oriented; no reconstruction | Useful high-level embedding baseline |
| PANNs | 2019 | Large-scale pretrained CNNs provide transferable audio embeddings | CNN trained on large audio tagging dataset | AudioSet-like pattern recognition | Transferable embeddings across audio tasks | Strong | Label-driven semantics; limited generative control | Useful baseline for retrieval/clustering |
| OpenL3 | 2019 | Audio embeddings can be learned from audiovisual correspondence | Self-supervised audiovisual learning | Audio-visual datasets / AudioSet | Competitive deep audio embeddings | Moderate-Strong | Depends on audiovisual correlations; less direct for synthesis | Useful for semantic / environmental sound embedding |
| K-SVD | 2006 | Overcomplete dictionaries can be learned for sparse signal representation | Alternating sparse coding + dictionary update via SVD | General signals | Learns atoms adapted to corpus | Strong foundational | Linear atoms; may need large dictionary for expressive audio | Direct for “sound vocabulary” creation |
| Matching Pursuit | 1993 | Signals can be represented sparsely by greedy selection from time-frequency dictionaries | Gabor / wavelet dictionaries + greedy residual reduction | General signals, audio | Sparse event-like decomposition | Strong foundational | Fixed dictionary may underfit exponential decay / complex textures | Direct for sound-particle composition |
| NMF Source Separation | 2007 | Audio spectrograms can be decomposed into nonnegative spectral templates and activations | NMF on magnitude spectrogram | Monaural mixtures | Interpretable components useful for separation | Strong foundational | Linear additive magnitude model; local minima | Direct for texture/source component extraction |
| Phase-intercept distortion | 2025 | Constant phase shifts can be perceptually invariant yet useful for audio ML augmentation | Phase manipulation + listening test + ML tasks | Music, speech, real-world sounds | Phase augmentation can improve classification/separation metrics | Moderate | Does not directly define creative feature, but constrains what matters perceptually | Support: magnitude features often sufficient |

---

## 5. Methodological Landscape

### 5.1 Four Families of Feature Materials

| Family | Representative Methods | Output Unit | Reconstruction? | Interpretability | Creative Use |
|---|---|---|:---:|:---:|---|
| Psychoacoustic descriptors | centroid, roughness, onset density, flatness, inharmonicity | scalar / trajectory | No | High | Direct mapping to synthesis/composition parameters |
| Sparse decomposition | Gabor MP, K-SVD, NMF | atoms / templates / activations | Partial to full | Medium-High | Sound particles, learned vocabulary, recombination |
| Discriminative embeddings | PANNs, AST, BYOL-A, AudioMAE, OpenL3 | vector embedding | No / weak | Low-Medium | Retrieval, clustering, corpus navigation |
| Generative latents / tokens | DDSP, RAVE, EnCodec, SoundStream, AudioLM, AudioLDM | latent vector / discrete token | Yes | Low-High depending on model | Morphing, resynthesis, generative composition |

### 5.2 Reconstruction-Control Tradeoff

A recurring pattern:

```text
Handcrafted descriptors: interpretable + controllable, but weak reconstruction.
Neural codecs: strong reconstruction, but weak interpretability.
CLAP/AST/PANNs: strong semantics/classification, but weak direct synthesis.
DDSP: interpretable controls, but narrower sound class.
RAVE: creative latent synthesis, but entangled dimensions.
K-SVD/NMF/Gabor: structurally meaningful components, but limited expressiveness unless dictionary is rich.
```

This suggests the project should not choose a single representation. A practical creative system likely needs a **multi-layer representation stack**:

1. low-level psychoacoustic descriptors for named controls;
2. sparse atoms/templates for event-level material;
3. semantic embeddings for search and organization;
4. generative latents/tokens for resynthesis and transformation.

---

## 6. Consensus Findings

### Consensus 1 — Spectrogram-like representations remain central

Almost all successful modern audio systems still rely on spectrogram or spectrogram-derived objectives, even when final models operate on raw waveforms or latents. DDSP uses signal-processing priors; EnCodec uses multi-scale spectrogram adversarial losses; AST/AudioMAE operate directly on spectrogram patches.

**Implication**: Sonic Atlas’s existing spectral_reference and CNN feature modules are a valid foundation.

### Consensus 2 — “Good ML feature” is not the same as “good creative feature”

PANNs, AST, BYOL-A, AudioMAE, and CLAP can produce powerful embeddings for classification, retrieval, and transfer. But their dimensions are not necessarily independently audible or controllable.

**Implication**: every candidate feature must be evaluated along at least three axes: prediction/retrieval quality, perceptual audibility, and creative controllability.

### Consensus 3 — Neural codecs make audio token composition plausible

SoundStream, EnCodec, AudioLM, and MusicLM establish a new paradigm: audio can be represented as discrete token sequences. These tokens can be modeled like language, enabling token-level recombination and generation.

**Implication**: a future system could treat audio tokens as a kind of “post-symbolic score,” but it must add perceptual labels or controls to avoid opaque token editing.

### Consensus 4 — DDSP and RAVE are the most immediately useful creative systems

DDSP provides interpretable controls (pitch, loudness, harmonic distribution, noise filters). RAVE provides real-time high-quality latent morphing. They occupy complementary positions:

- DDSP: lower-dimensional, more interpretable, narrower domain;
- RAVE: broader timbral exploration, less interpretable, performance-friendly.

**Implication**: first prototype should compare DDSP-style controls and RAVE-style latents.

### Consensus 5 — Sparse decomposition remains creatively attractive

Gabor atoms, NMF templates, and K-SVD learned atoms are not state-of-the-art for high-fidelity black-box generation, but they are highly valuable as **compositional units** because they expose discrete events, templates, and activations.

**Implication**: sparse methods should be retained as an “explainable material extraction” branch, not replaced by neural models.

---

## 7. Evidence Gaps

| Gap | Why It Matters | Suggested Follow-up |
|---|---|---|
| Embedding dimensions are rarely perceptually validated | A latent coordinate may not correspond to an audible axis | Latent traversal + ABX listening test |
| Creative usefulness is rarely measured | Classification quality does not imply compositional value | Composer rating / sound study evaluation |
| CLAP similarity may not align with human audio quality | Text-audio similarity can be semantically right but perceptually weak | Include Human-CLAP and subjective ratings |
| Neural codec tokens are opaque | Tokens can reconstruct but not necessarily be composed by humans | Learn token-to-feature probes and cluster tokens |
| DDSP is limited for noisy/natural sounds | Natural sound textures are often non-harmonic | Combine DDSP with noise/texture models or RAVE |
| Sparse dictionaries underfit complex decays unless learned | Fixed Gabor atoms may not match real instrument envelopes | Implement K-SVD / learned dictionary experiment |
| No single representation satisfies all needs | Creative systems need multiple levels | Design hybrid representation stack |

---

## 8. Recommended Core Set for Deep Reading

Priority 1 — immediately relevant:

1. **DDSP** (Engel et al., 2020, arXiv:2001.04643)
2. **RAVE** (Caillon & Esling, 2021, arXiv:2111.05011)
3. **EnCodec** (Défossez et al., 2022, arXiv:2210.13438)
4. **LAION-CLAP** (Wu et al., 2022, arXiv:2211.06687)
5. **AudioLDM** (Liu et al., 2023, arXiv:2301.12503)
6. **AudioMAE** (Huang et al., 2022, arXiv:2207.06405)
7. **BYOL-A** (Niizumi et al., 2021, arXiv:2103.06695)
8. **PANNs** (Kong et al., 2019, arXiv:1912.10211)

Priority 2 — important systems/context:

9. **SoundStream** (Zeghidour et al., 2021, arXiv:2107.03312)
10. **AudioLM** (Borsos et al., 2022, arXiv:2209.03143)
11. **MusicLM** (Agostinelli et al., 2023, arXiv:2301.11325)
12. **AST** (Gong et al., 2021, arXiv:2104.01778)
13. **OpenL3** (Cramer et al., 2019)
14. **Audio SSL Survey** (arXiv:2203.01205)

Priority 3 — foundational / experiment branch:

15. **Matching Pursuit** (Mallat & Zhang, 1993)
16. **K-SVD** (Aharon, Elad & Bruckstein, 2006)
17. **NMF audio source separation** (Virtanen, 2007)
18. **Grey / McAdams timbre MDS** (already covered in module 4)

---

## 9. Proposed Experimental Plan After Review

### Experiment 1 — Feature Baseline Map

Dataset:

- 20 musical sounds
- 20 natural sounds
- 20 object/urban sounds

Features:

- spectral centroid
- flatness
- flux
- roughness
- onset density
- MFCC mean/std
- CQT chroma
- entropy

Output:

- 2D UMAP/t-SNE projection
- cluster labels
- manual perceptual labels
- feature-to-sound retrieval demo

### Experiment 2 — Embedding Comparison

Models:

- PANNs
- AST
- BYOL-A
- AudioMAE
- CLAP
- optional OpenL3

Metrics:

- cluster quality by category/material
- nearest-neighbor retrieval subjective quality
- robustness to pitch/time shift/noise
- alignment with handcrafted psychoacoustic descriptors

### Experiment 3 — Generative Latent Traversal

Models:

- RAVE
- DDSP
- EnCodec / DAC tokenization

Tests:

- latent interpolation
- one-dimensional traversal
- ABX audibility
- semantic rating
- creative usefulness rating

### Experiment 4 — Learned Sound Atoms

Methods:

- fixed Gabor OMP baseline from current wave_packet_demo
- NMF templates
- K-SVD learned atoms

Metrics:

- residual energy
- number of atoms / templates
- perceptual quality
- interpretability of atoms
- recomposition usefulness

---

## 10. Repository Organization Changes

After this review, the repository was reorganized around the main research line: **audio → features → perception → creative materials**.

```text
docs/
├── vision.md
├── architecture.md
├── roadmap.md
├── literature/
│   ├── 00_research_plan.md
│   └── 01_first_round_review.md
└── foundations/
    ├── fundamental_analysis.md
    └── 01–05 foundation reports

demos/
├── foundations/
│   └── existing HTML concept demos
├── references/
│   └── spectral_reference.html
└── creative_features/
    └── future main-line demos

experiments/
├── creative_features/
│   ├── 01_baseline_features/
│   ├── 02_embedding_comparison/
│   ├── 03_latent_traversal/
│   └── 04_creative_mapping/
└── wave_packet_sparse/
    └── previous sparse decomposition scripts
```

Rationale:

- `docs/foundations/` keeps the original five theoretical modules as support for the new main line;
- `docs/literature/` stores research plans, literature reviews, evidence matrices, and future taxonomies;
- `demos/foundations/` keeps polished conceptual HTML demos;
- `demos/creative_features/` is reserved for feature-space browsers and creative interaction prototypes;
- `experiments/creative_features/` becomes the main implementation workspace;
- `experiments/wave_packet_sparse/` preserves previous sparse decomposition experiments without cluttering the root.

---

## 11. References

### Verified arXiv IDs

- Engel, J., Hantrakul, L., Gu, C., & Roberts, A. (2020). **DDSP: Differentiable Digital Signal Processing**. arXiv:2001.04643.
- Caillon, A., & Esling, P. (2021). **RAVE: A variational autoencoder for fast and high-quality neural audio synthesis**. arXiv:2111.05011.
- Défossez, A., Copet, J., Synnaeve, G., et al. (2022). **High Fidelity Neural Audio Compression**. arXiv:2210.13438.
- Zeghidour, N., Luebs, A., Omran, A., et al. (2021). **SoundStream: An End-to-End Neural Audio Codec**. arXiv:2107.03312.
- Borsos, Z., Marinier, R., Vincent, D., et al. (2022). **AudioLM: a Language Modeling Approach to Audio Generation**. arXiv:2209.03143.
- Agostinelli, A., Denk, T. I., Borsos, Z., et al. (2023). **MusicLM: Generating Music From Text**. arXiv:2301.11325.
- Liu, H., Chen, Z., Yuan, Y., et al. (2023). **AudioLDM: Text-to-Audio Generation with Latent Diffusion Models**. arXiv:2301.12503.
- Wu, Y., Chen, K., Zhang, T., et al. (2022). **Large-scale Contrastive Language-Audio Pretraining with Feature Fusion and Keyword-to-Caption Augmentation**. arXiv:2211.06687.
- Huang, P.-Y., Xu, H., Li, J., et al. (2022). **Masked Autoencoders that Listen**. arXiv:2207.06405.
- Niizumi, D., Takeuchi, D., Ohishi, Y., et al. (2021). **BYOL for Audio: Self-Supervised Learning for General-Purpose Audio Representation**. arXiv:2103.06695.
- Gong, Y., Chung, Y.-A., & Glass, J. (2021). **AST: Audio Spectrogram Transformer**. arXiv:2104.01778.
- Kong, Q., Cao, Y., Iqbal, T., et al. (2019). **PANNs: Large-Scale Pretrained Audio Neural Networks for Audio Pattern Recognition**. arXiv:1912.10211.
- Takano, T., Okamoto, Y., Kanamori, Y., & Saito, Y. (2025). **Human-CLAP: Human-perception-based contrastive language-audio pretraining**. arXiv:2506.23553.

### Foundational / Non-arXiv

- Mallat, S., & Zhang, Z. (1993). **Matching pursuits with time-frequency dictionaries**. *IEEE Transactions on Signal Processing*.
- Aharon, M., Elad, M., & Bruckstein, A. (2006). **K-SVD: An Algorithm for Designing Overcomplete Dictionaries for Sparse Representation**. *IEEE Transactions on Signal Processing*.
- Virtanen, T. (2007). **Monaural sound source separation by nonnegative matrix factorization**. *IEEE Transactions on Audio, Speech, and Language Processing*.
- Cramer, J., Wu, H.-H., Salamon, J., & Bello, J. P. (2019). **Look, Listen, and Learn More: Design Choices for Deep Audio Embeddings**.

---

## 12. Next Action Items

1. **Deep read** DDSP, RAVE, EnCodec, CLAP, AudioLDM, AudioMAE, BYOL-A.
2. Build `02_feature_taxonomy.md` from the four-family landscape.
3. Build `03_experiment_protocol.md` for baseline features + embedding comparison.
4. Implement a minimal feature extraction prototype in `experiments/creative_features/01_baseline_features/`.
5. Add future creative interaction demos under `demos/creative_features/`.

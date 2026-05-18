# Sonic Atlas

**通过机器学习方法，从音乐与自然声音中提取抽象声音特征，并将这些特征作为可听、可操作、可组合的音乐创作素材。**

Sonic Atlas 研究声音如何被分解、感知、嵌入、验证与重新组合。它的目标不是只做音频分类或声音合成，而是建立一条从真实声音到创作材料的完整链路：

```text
Audio
  → Decomposition
  → Abstract Feature Extraction
  → Perceptual Validation
  → Creative Mapping
  → Composition System
```

## Core Questions

1. **怎么样分解一个正常音频？**
   - STFT / Mel / CQT / CWT
   - Gabor atoms / NMF / K-SVD
   - source separation
   - neural codec tokenization

2. **用什么方法能提取更有效的抽象特征？**
   - psychoacoustic descriptors
   - CNN / Transformer embeddings
   - self-supervised audio representations
   - CLAP audio-text embeddings
   - DDSP / RAVE / EnCodec / AudioLDM latent spaces

3. **这些抽象特征是否人耳可闻？**
   - JND / ABX / MUSHRA
   - latent traversal
   - semantic rating
   - perceptual controllability

4. **这些特征能否成为音乐创作素材？**
   - feature trajectory composition
   - corpus navigation
   - latent interpolation
   - granular recomposition
   - synthesis parameter mapping

## Repository Structure

```text
.
├── AGENTS.md                          # 开发与研究指南
├── README.md
├── docs/
│   ├── vision.md                      # 项目愿景与核心主张
│   ├── architecture.md                # research-to-system 架构
│   ├── roadmap.md                     # 后续推进路线
│   ├── literature/
│   │   ├── 00_research_plan.md        # 主线研究计划
│   │   ├── 01_first_round_review.md   # 第一轮 literature review
│   │   ├── 02_feature_taxonomy.md     # 面向创作的声音特征分类体系
│   │   └── 03_experiment_protocol.md  # baseline feature extraction 实验协议
│   ├── foundations/                   # 支撑主线的基础理论
│   │   ├── fundamental_analysis.md
│   │   ├── 01_discretization_precision.md
│   │   ├── 02_phase_perception.md
│   │   ├── 03_wave_packets.md
│   │   ├── 04_timbre_characterization.md
│   │   └── 05_cnn_feature_extraction.md
│   └── zh/                            # 中文翻译（镜像 docs/ 结构）
│       ├── vision.md
│       ├── architecture.md
│       ├── roadmap.md
│       ├── literature/
│       └── foundations/
│
├── demos/
│   ├── foundations/                 # 基础概念交互演示
│   │   ├── cqt_wavelet_demo.html
│   │   ├── phase_perception_demo.html
│   │   ├── wave_packet_demo.html
│   │   ├── timbre_demo.html
│   │   └── cnn_feature_demo.html
│   ├── references/
│   │   └── spectral_reference.html
│   └── creative_features/           # 未来主线 demo
│
├── experiments/
│   ├── creative_features/           # 主线实验
│   │   ├── 01_baseline_features/
│   │   ├── 02_embedding_comparison/
│   │   ├── 03_latent_traversal/
│   │   └── 04_creative_mapping/
│   └── wave_packet_sparse/          # 既有波包稀疏重建实验
│
├── data/
│   ├── raw/                         # 原始音频，不提交
│   ├── processed/                   # 预处理数据，不提交
│   └── external/                    # 外部数据，不提交
│
├── notebooks/                       # 探索性分析
├── LICENSE
└── README.md
```

## Language Policy

- **英文文档**（`docs/`）为研究源文件（source of truth）
- **中文文档**（`docs/zh/`）为翻译版本，供中文阅读参考
- 研究、实验、代码实现以英文文档为准
- 详见 [AGENTS.md](AGENTS.md)

## Main Documents

| Document | Purpose |
|---|---|
| [docs/vision.md](docs/vision.md) | 项目愿景：声音特征如何成为创作材料 |
| [docs/architecture.md](docs/architecture.md) | 仓库结构与系统数据流 |
| [docs/roadmap.md](docs/roadmap.md) | 后续实验与系统路线图 |
| [docs/data_sources.md](docs/data_sources.md) | 音源数据集下载链接与获取指南 |
| [docs/literature/00_research_plan.md](docs/literature/00_research_plan.md) | 主线研究计划 |
| [docs/literature/01_first_round_review.md](docs/literature/01_first_round_review.md) | 第一轮 literature review |
| [docs/literature/02_feature_taxonomy.md](docs/literature/02_feature_taxonomy.md) | 面向创作的声音特征分类、评价维度与 baseline feature set |
| [docs/literature/03_experiment_protocol.md](docs/literature/03_experiment_protocol.md) | Baseline feature extraction 实验协议：语料、预处理、特征规格、投影、检索、评估 |

## Foundation Reports

原始五个声音物理/心理声学问题现在作为主线研究的 foundation：

| # | Report | Role in Main Line |
|---|---|---|
| 1 | [离散化精度](docs/foundations/01_discretization_precision.md) | 定义什么声音差异可被人耳分辨 |
| 2 | [相位感知](docs/foundations/02_phase_perception.md) | 解释为什么 magnitude / Mel spectrogram 通常足够 |
| 3 | [波包时频分析](docs/foundations/03_wave_packets.md) | 提供声音粒子、稀疏原子与时频材料思想 |
| 4 | [音色刻画](docs/foundations/04_timbre_characterization.md) | 提供 perceptual timbre space 与音色维度 |
| 5 | [CNN 特征提取](docs/foundations/05_cnn_feature_extraction.md) | 提供深度音频 embedding 的基础 |
| — | [综合报告](docs/foundations/fundamental_analysis.md) | 五个基础问题的一体化综述 |

## Interactive Demos

| Topic | Demo |
|---|---|
| CQT / Wavelet | [demos/foundations/cqt_wavelet_demo.html](demos/foundations/cqt_wavelet_demo.html) |
| Phase Perception | [demos/foundations/phase_perception_demo.html](demos/foundations/phase_perception_demo.html) |
| Wave Packets / Sparse Decomposition | [demos/foundations/wave_packet_demo.html](demos/foundations/wave_packet_demo.html) |
| Timbre Space | [demos/foundations/timbre_demo.html](demos/foundations/timbre_demo.html) |
| CNN Feature Extraction | [demos/foundations/cnn_feature_demo.html](demos/foundations/cnn_feature_demo.html) |
| Spectral Reference | [demos/references/spectral_reference.html](demos/references/spectral_reference.html) |

## Current Method Map

| Representation Family | Methods | Creative Role |
|---|---|---|
| Psychoacoustic descriptors | centroid, roughness, flatness, attack, onset density | 可命名、可控的创作参数 |
| Sparse decomposition | Gabor OMP, K-SVD, NMF | 声音粒子 / learned sound vocabulary |
| Discriminative embeddings | PANNs, AST, BYOL-A, AudioMAE, OpenL3, CLAP | 聚类、检索、语义导航 |
| Generative latents / tokens | DDSP, RAVE, EnCodec, SoundStream, AudioLM, AudioLDM | 变形、重合成、生成式创作 |

## Next Steps

1. 手动听检并填写 `evaluation_notes.md`。
2. 开发 `demos/creative_features/feature_space_browser.html`。
3. 比较 PANNs / AST / BYOL-A / AudioMAE / CLAP embeddings。
4. 测试 DDSP / RAVE / EnCodec latent 的可闻性与可控性。
5. 构建 feature trajectory → composition mapping 原型。

## Relationship to scaler-lab

同目录下的 `scaler-lab` 关注“什么样的音高组合具有新的和声价值”；Sonic Atlas 关注“声音如何被分解、嵌入、感知验证并转化为创作素材”。两者共同构成从调律/音高结构到音色/声音材料的计算音乐研究链条。

## License

MIT License

# Vision

**Sonic Atlas** 的主线是：

> 通过机器学习方法，从音乐与自然声音中提取抽象声音特征，并将这些特征作为可听、可操作、可组合的音乐创作素材。

## Motivation

传统音频分析通常服务于分类、检索、压缩或重建；Sonic Atlas 关注进一步的问题：

1. 声音可以被分解成哪些层次？
2. 机器学习能否从声音中提取抽象但稳定的特征？
3. 这些特征是否对应人耳可闻、可描述的变化？
4. 这些特征能否成为作曲、音色设计和声音想象的材料？

## Core Pipeline

```text
Audio
  → Decomposition
  → Abstract Feature Extraction
  → Perceptual Validation
  → Creative Mapping
  → Composition System
```

## Design Principles

- **Perception before metrics**: 特征不仅要在模型中有效，也必须在人耳中有意义。
- **Control before novelty**: 生成新声音不够，关键是能否控制变化方向。
- **Hybrid representations**: 不追求单一万能 latent，而采用心理声学特征、稀疏原子、深度 embedding、生成式 latent/token 的组合。
- **Creation as evaluation**: 一个特征最终是否有价值，要看它能否支撑声音作品或作曲过程。

## Research Claim

声音特征可以分为四层材料：

| Layer | Unit | Creative Role |
|---|---|---|
| Psychoacoustic descriptors | scalar / curve | 可命名控制参数 |
| Sparse atoms/templates | event / atom / activation | 声音粒子与素材重组 |
| Embeddings | vector / neighborhood | 语义导航与素材检索 |
| Generative latents/tokens | latent / discrete code | 变形、重合成、生成 |

Sonic Atlas 的目标是把这四层统一到一个可实验、可听、可创作的系统中。

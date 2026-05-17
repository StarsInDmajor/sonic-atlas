# 第一轮文献综述:机器学习声音抽象特征与音乐创作素材

> **研究问题**:如何从音乐与自然声音中提取既抽象、又可闻(Audible,人耳可察觉)、可控(Controllable,可独立操纵)、可创作的声音特征,并将其作为音乐创作素材?

---

## 1. 检索策略

### 范围

本轮是第一轮广泛扫描与聚焦筛选,目标不是穷尽全部文献,而是建立方法地图、筛选核心论文、明确下一步深度阅读的优先级。

### 来源

- arXiv API:`cs.SD`, `cs.LG`, `eess.AS`, `cs.MM`
- Tavily Search:用于补充非 arXiv 来源、系统页面、项目页面
- Zotero(个人文献管理工具):个人文献库粗略交叉检查
- OpenViking(知识库管理工具):已有处理文献交叉检查
- Sonic Atlas 已有模块:模块 1-5、频谱参考页、波包实验

### 检索词

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

### 纳入标准

纳入文献需满足至少一项:

1. 提供音频分解、表征学习、latent 或 token 表示;
2. 支持重建、生成、检索、分类或可控合成;
3. 可被映射到声音创作工作流;
4. 与人耳感知、可控性、语义对齐或音色空间相关;
5. 有代码、模型或已被广泛复用。

### 排除标准

排除:

- 纯语音识别且无创作/音色/声音表示价值;
- 纯分类基准测试(Classification Benchmark)但没有可复用嵌入(Embedding)或控制机制;
- 仅符号音乐(MIDI)生成,不处理音频;
- 无法重建、生成、检索或解释的黑盒指标论文。

---

## 2. 候选文献池

| # | 论文 / 系统 | 年份 | ID / DOI / URL | 来源 | 核心领域 | 状态 |
|---|---|---:|---|---|---|---|
| 1 | DDSP: Differentiable Digital Signal Processing | 2020 | arXiv:2001.04643 | arXiv | 可解释神经音频合成(Interpretable Neural Audio Synthesis) | 核心 |
| 2 | RAVE: A variational autoencoder for fast and high-quality neural audio synthesis | 2021 | arXiv:2111.05011 | arXiv | 实时潜变量音频合成(Realtime Latent Audio Synthesis) | 核心 |
| 3 | High Fidelity Neural Audio Compression (EnCodec) | 2022 | arXiv:2210.13438 | arXiv | 神经编解码器(Neural Codec) / 量化潜变量(Quantized Latent) | 核心 |
| 4 | SoundStream: An End-to-End Neural Audio Codec | 2021 | arXiv:2107.03312 | arXiv | 神经编解码器 / 残差向量量化标记(RVQ Token,Residual Vector Quantization) | 核心 |
| 5 | AudioLM: a Language Modeling Approach to Audio Generation | 2022 | arXiv:2209.03143 | arXiv | 离散音频标记(Discrete Audio Token) / 生成 | 核心 |
| 6 | MusicLM: Generating Music From Text | 2023 | arXiv:2301.11325 | arXiv | 文本到音乐生成(Text-to-Music) / 语义条件化(Semantic Conditioning) | 核心 |
| 7 | AudioLDM: Text-to-Audio Generation with Latent Diffusion Models | 2023 | arXiv:2301.12503 | arXiv | CLAP 潜扩散(Latent Diffusion) | 核心 |
| 8 | Large-scale Contrastive Language-Audio Pretraining with Feature Fusion and Keyword-to-Caption Augmentation | 2022 | arXiv:2211.06687 | arXiv | CLAP(音频-文本对比预训练) / 音频-文本嵌入(Audio-Text Embedding) | 核心 |
| 9 | Human-CLAP: Human-perception-based CLAP | 2025 | arXiv:2506.23553 | arXiv | 人类感知对齐(Human Perception Alignment) / 评估 | 观察 |
| 10 | Masked Autoencoders that Listen (AudioMAE) | 2022 | arXiv:2207.06405 | arXiv | 自监督音频嵌入(Self-Supervised Audio Embedding) | 核心 |
| 11 | BYOL for Audio: Self-Supervised Learning for General-Purpose Audio Representation | 2021 | arXiv:2103.06695 | arXiv | 自监督音频嵌入(SSL Audio Embedding) | 核心 |
| 12 | Audio Self-supervised Learning: A Survey | 2022 | arXiv:2203.01205 | arXiv | 综述(Survey) | 支撑 |
| 13 | AST: Audio Spectrogram Transformer | 2021 | arXiv:2104.01778 | arXiv | 音频 Transformer 嵌入(Audio Transformer Embedding) | 核心 |
| 14 | PANNs: Large-Scale Pretrained Audio Neural Networks for Audio Pattern Recognition | 2019 | arXiv:1912.10211 | arXiv | 预训练音频 CNN 嵌入(Pretrained Audio CNN Embedding) | 核心 |
| 15 | OpenL3 / Look, Listen, and Learn More | 2019 | Semantic Scholar / project | Tavily | 视听自监督嵌入(Audiovisual Self-Supervised Embedding) | 核心 |
| 16 | DDSP-SFX: Acoustically-guided sound effects generation | 2023 | arXiv:2309.08060 | arXiv | 可控音效生成(Controllable Sound Effect Generation) | 观察 |
| 17 | Latent Space Explorations of Singing Voice Synthesis using DDSP | 2021 | arXiv:2103.07197 | arXiv | DDSP 潜空间探索(Latent Space Exploration) | 观察 |
| 18 | LVNS-RAVE: Diversified audio generation with RAVE and Latent Vector Novelty Search | 2024 | arXiv:2404.14063 | arXiv | 潜变量新奇搜索(Latent Novelty Search) / 创意生成 | 观察 |
| 19 | K-SVD: An Algorithm for Designing Overcomplete Dictionaries for Sparse Representation | 2006 | IEEE TSP | 已知基础 | 学习型稀疏字典(Learned Sparse Dictionary) | 核心基础 |
| 20 | Matching Pursuits with Time-Frequency Dictionaries | 1993 | IEEE TSP | 已有模块 | Gabor 原子 / 稀疏分解(Sparse Decomposition) | 核心基础 |
| 21 | Monaural Sound Source Separation by NMF | 2007 | IEEE TASLP | 已知基础 | NMF(非负矩阵分解) / 声源分量(Source Components) | 核心基础 |
| 22 | Phase-intercept distortion as audio augmentation | 2025 | OV: Krishnan & Condit-Schultz | OV | 感知不变增强(Perceptually Invariant Augmentation) | 支撑 |

---

## 3. 个人文献库 / 已有知识交叉检查

### Zotero

查询:`DDSP RAVE EnCodec CLAP AudioMAE BYOL-A PANNs AST`

结果:广泛查询**未返回数据**。这可能意味着这些核心音频 ML 论文尚未以明显标题关键词编目,或当前查询对 Zotero CLI 匹配过于宽泛。

### OpenViking

范围搜索找到已有已处理文献集合:

- `viking://resources/research/inbox/papers/2025-krishnan--KD5M8H5D/`

相关内容:

| 资源 | 相关性 |
|---|---|
| `The_Perception_of_2more_51dbbec1.md` | 相位截距失真与感知不变性 |
| `4._DATA_AUGMENTATION_EXPERIMENT.md` | 面向机器学习的音频数据增强 |
| `REFERENCES_3.md` | 参考文献,包括 source separation、wav2vec2.0、AST、AudioSet、MUSDB18-HQ |
| `4.1._Audio_Classification.md` | 使用 spectrogram/MFCC 的音频分类实验 |
| `4.2._Blind_Source_2more_fd44872d.md` | source separation 与音频 ML 指标 |

意义:Sonic Atlas 已有处理过的**相位不变性、音频 ML 增强、source separation 和 AST 参考文献**上下文,应在后续深度阅读中复用。

---

## 4. 提取表

| 论文 / 系统 | 年份 | 主要主张 | 方法 | 数据 / 领域 | 关键结果 | 证据强度 | 局限性 | 相关性 |
|---|---:|---|---|---|---|---|---|---|
| DDSP | 2020 | 音频合成受益于神经网络与可微 DSP 先验的结合 | 自编码器预测 DSP 控制:振荡器、滤波器、噪声、混响 | 乐器、单音有调音频 | 高保真合成,参数少于黑盒生成 | 强 | 最适合有调/准谐波声源;不太适合任意自然纹理 | 直接用于可控创作特征 |
| RAVE | 2021 | VAE 可提供快速高质量潜空间音频合成 | 编码器-解码器 VAE,原始波形 / 频谱损失 | 通用音频、音乐、音色模型 | 可实时生成,潜空间可用于表演 | 强 | 潜空间维度可能纠缠且难以命名 | 直接用于潜空间作曲 |
| EnCodec | 2022 | 神经编解码器学习紧凑量化潜空间 token,保真度高 | 流式编码器-解码器 + 残差向量量化 + 对抗频谱损失 | 语音、音乐、通用音频 | 低比特率下高保真音频压缩 | 强 | token 本身不可解释 | 直接用于音频 token 作曲,但需映射层 |
| SoundStream | 2021 | 端到端神经编解码器可高效表示语音/音乐/通用音频 | 全卷积编码器/解码器 + 残差向量量化器 | 语音、音乐、通用音频 | 高效压缩与重建 | 强 | 为压缩设计,非创作控制 | 直接用作 tokenization 基底 |
| AudioLM | 2022 | 音频生成可视为离散音频 token 上的语言建模 | 语义 token + 声学 token | 语音和钢琴/音乐示例 | 长期一致性和高质量生成 | 强 | 模型庞大;可控性由 token 中介,非直接特征 | 对 token-based 作曲重要 |
| MusicLM | 2023 | 高保真音乐可从文本描述生成,使用层次化 token 建模 | 文本条件层次化序列到序列,基于音频 token | 音乐 | 从文本生成连贯的多分钟音乐 | 强 | 细粒度控制有限;许多模型/数据集不公开 | 对语义作曲重要,但不太适合底层特征控制 |
| AudioLDM | 2023 | CLAP latent + 潜扩散实现文本到音频生成 | 在 CLAP 条件下的潜空间音频表示中进行扩散 | AudioCaps / 通用音频 | 文本到音频合成,计算量低于波形扩散 | 强 | CLAP 对齐可能不完全匹配人类感知 | 直接用于语义声音设计 |
| LAION-CLAP | 2022 | 音频-文本对比学习产生用于检索/分类的联合嵌入 | 音频编码器 + 文本编码器对比预训练,LAION-Audio-630K | 音频-文本对 | 通用音频-文本检索/分类 | 强 | 嵌入是语义的,不一定声学可控 | 直接用于语料库导航和语义特征搜索 |
| Human-CLAP | 2025 | CLAPScore 可能与人类主观评估弱相关;需要人类感知对齐 | 基于人类感知的 CLAP 目标 / 评估 | 通用音频 | 指出嵌入相似性与人类判断之间的差距 | 中等/新兴 | 近期;需要复现 | 对感知验证至关重要 |
| AudioMAE | 2022 | 音频频谱图上的掩码自编码学习有用的 SSL 表示 | 高掩码率的频谱图 patch 上的 MAE | 音频分类任务 | 竞争力的 SSL 音频嵌入 | 强 | 表示良好,但不一定在创作意义上可重建 | 用于特征提取/聚类 |
| BYOL-A | 2021 | Bootstrap 自监督无需负样本即可学习通用音频特征 | 基于增强的 BYOL,应用于音频片段 | 通用音频任务 | 强迁移性能 | 强 | 特征维度不可解释 | 用于通用嵌入基线 |
| AST | 2021 | 频谱图 patch 上的 Transformer 通过全局上下文提升音频分类 | 视觉 Transformer 适配到频谱图 | AudioSet / 语音 / 声音事件 | 强分类性能 | 强 | 面向分类;无重建 | 用作高层嵌入基线 |
| PANNs | 2019 | 大规模预训练 CNN 提供可迁移音频嵌入 | 在大型音频标签数据集上训练的 CNN | AudioSet-like 模式识别 | 跨音频任务的可迁移嵌入 | 强 | 标签驱动语义;生成控制有限 | 用于检索/聚类基线 |
| OpenL3 | 2019 | 音频嵌入可从视听对应关系中学习 | 自监督视听学习 | 视听数据集 / AudioSet | 竞争力的深度音频嵌入 | 中强 | 依赖视听相关性;对合成不太直接 | 用于语义/环境声音嵌入 |
| K-SVD | 2006 | 超完备字典可为稀疏信号表示而学习 | 交替稀疏编码 + SVD 字典更新 | 通用信号 | 学习适配语料的原子 | 强基础 | 线性原子;表达性音频可能需要大字典 | 直接用于"声音词汇"创建 |
| Matching Pursuit | 1993 | 信号可通过贪心选择时频字典进行稀疏表示 | Gabor / 小波字典 + 贪心残差减少 | 通用信号、音频 | 稀疏事件化分解 | 强基础 | 固定字典可能欠拟合指数衰减/复杂纹理 | 直接用于声音粒子作曲 |
| NMF Source Separation | 2007 | 音频频谱图可分解为非负谱模板和激活 | 幅度频谱图上的 NMF | 单声道混合 | 可解释组件有助于分离 | 强基础 | 线性加性幅度模型;局部最优 | 直接用于纹理/声源组件提取 |
| Phase-intercept distortion | 2025 | 恒定相移可感知不变,但对音频 ML 增强有用 | 相位操作 + 听觉测试 + ML 任务 | 音乐、语音、现实世界声音 | 相位增强可改善分类/分离指标 | 中等 | 不直接定义创作特征,但约束了什么在感知上重要 | 支撑:幅度特征通常足够 |

---

## 5. 方法论全景

### 5.1 四类特征材料家族

| 家族 | 代表方法 | 输出单位 | 可重建? | 可解释性 | 创作用途 |
|---|---|---|:---:|:---:|---|
| 心理声学描述符 | centroid, roughness, onset density, flatness, inharmonicity | 标量 / 轨迹 | 否 | 高 | 直接映射到合成/作曲参数 |
| 稀疏分解 | Gabor MP, K-SVD, NMF | 原子 / 模板 / 激活 | 部分到完全 | 中高 | 声音粒子、学习词汇、重组 |
| 判别式嵌入 | PANNs, AST, BYOL-A, AudioMAE, OpenL3 | 向量嵌入 | 否/弱 | 低中 | 检索、聚类、语料库导航 |
| 生成式潜变量/token | DDSP, RAVE, EnCodec, SoundStream, AudioLM, AudioLDM | 潜向量 / 离散 token | 是 | 低到高(取决于模型) | 变形、重合成、生成式作曲 |

### 5.2 重建-控制权衡

一个反复出现的模式:

```text
手工描述符:可解释 + 可控,但重建弱。
神经编解码器:重建强,但可解释性弱。
CLAP/AST/PANNs:语义/分类强,但直接合成弱。
DDSP:控制可解释,但声音类别较窄。
RAVE:创作性潜空间合成,但维度纠缠。
K-SVD/NMF/Gabor:结构上有意义的组件,但除非字典丰富否则表达力有限。
```

这表明项目不应选择单一表示。一个实用的创作系统可能需要**多层表示栈**:

1. 底层心理声学描述符用于命名控制;
2. 稀疏原子/模板用于事件级材料;
3. 语义嵌入用于搜索和组织;
4. 生成式潜变量/token 用于重合成和变换。

---

## 6. 共识发现

### 共识 1 - 类频谱表示仍然核心

几乎所有成功的现代音频系统仍然依赖频谱图或频谱图衍生目标,即使最终模型在原始波形或潜空间上操作。DDSP 使用信号处理先验;EnCodec 使用多尺度频谱图对抗损失;AST/AudioMAE 直接在频谱图 patch 上操作。

**启示**:Sonic Atlas 的现有 spectral_reference 和 CNN 特征模块是有效的基础。

### 共识 2 - "好的 ML 特征"不等于"好的创作特征"

PANNs、AST、BYOL-A、AudioMAE 和 CLAP 可以为分类、检索和迁移产生强大嵌入。但其维度不一定独立可闻或可控。

**启示**:每个候选特征必须沿至少三个轴评估:预测/检索质量、感知可闻性、创作可控性。

### 共识 3 - 神经编解码器使音频 token 作曲变得可行

SoundStream、EnCodec、AudioLM 和 MusicLM 建立了新范式:音频可表示为离散 token 序列。这些 token 可以像语言一样建模,实现 token 级重组和生成。

**启示**:未来系统可将音频 token 视为一种"后符号记谱",但必须添加感知标签或控制以避免不透明的 token 编辑。

### 共识 4 - DDSP 和 RAVE 是最直接有用的创作系统

DDSP 提供可解释控制(音高、响度、谐波分布、噪声滤波器)。RAVE 提供实时高质量潜空间变形。它们占据互补位置:

- DDSP:低维、更可解释、领域较窄;
- RAVE:更广泛的音色探索、不太可解释、适合表演。

**启示**:第一个原型应比较 DDSP 式控制和 RAVE 式潜空间。

### 共识 5 - 稀疏分解在创作上仍然有吸引力

Gabor 原子(Gabor Atom)、NMF 模板(NMF Template)和 K-SVD 学习原子(Learned Atom)不是高保真黑盒生成的最先进方法,但作为**作曲单元**非常有价值,因为它们暴露了离散事件、模板和激活。

**启示**:稀疏方法应作为"可解释材料提取"分支保留,而非被神经模型取代。

---

## 7. 证据缺口

| 缺口 | 为什么重要 | 建议跟进 |
|---|---|---|
| 嵌入维度很少经过感知验证 | 潜空间坐标可能不对应可闻轴 | 潜变量遍历(Latent Traversal) + ABX 听觉测试 |
| 创作有用性很少被测量 | 分类质量不意味着作曲价值 | 作曲家评分 / sound study(声音研究)评估 |
| CLAP 相似性可能不与人类音频质量对齐 | 文本-音频相似性可能语义正确但感知弱 | 包含 Human-CLAP 和主观评分 |
| 神经编解码器标记不透明 | 标记可重建但不一定能被人类作曲 | 学习标记到特征探针(Token-to-Feature Probe)并聚类标记 |
| DDSP 对噪声/自然声音受限 | 自然声音纹理通常非谐波 | 将 DDSP 与噪声/纹理模型或 RAVE 结合 |
| 稀疏字典对复杂衰减欠拟合,除非学习 | 固定 Gabor 原子可能不匹配真实乐器包络 | 实现 K-SVD / 学习字典(Learned Dictionary)实验 |
| 没有单一表示满足所有需求 | 创作系统需要多层 | 设计混合表示栈(Hybrid Representation Stack) |

---

## 8. 推荐深度阅读核心集

优先级 1 - 直接相关:

1. **DDSP** (Engel et al., 2020, arXiv:2001.04643)
2. **RAVE** (Caillon & Esling, 2021, arXiv:2111.05011)
3. **EnCodec** (Défossez et al., 2022, arXiv:2210.13438)
4. **LAION-CLAP** (Wu et al., 2022, arXiv:2211.06687)
5. **AudioLDM** (Liu et al., 2023, arXiv:2301.12503)
6. **AudioMAE** (Huang et al., 2022, arXiv:2207.06405)
7. **BYOL-A** (Niizumi et al., 2021, arXiv:2103.06695)
8. **PANNs** (Kong et al., 2019, arXiv:1912.10211)

优先级 2 - 重要系统/上下文:

9. **SoundStream** (Zeghidour et al., 2021, arXiv:2107.03312)
10. **AudioLM** (Borsos et al., 2022, arXiv:2209.03143)
11. **MusicLM** (Agostinelli et al., 2023, arXiv:2301.11325)
12. **AST** (Gong et al., 2021, arXiv:2104.01778)
13. **OpenL3** (Cramer et al., 2019)
14. **Audio SSL Survey** (arXiv:2203.01205)

优先级 3 - 基础 / 实验分支:

15. **Matching Pursuit** (Mallat & Zhang, 1993)
16. **K-SVD** (Aharon, Elad & Bruckstein, 2006)
17. **NMF audio source separation** (Virtanen, 2007)
18. **Grey / McAdams timbre MDS**(已在模块 4 中涵盖)

---

## 9. 综述后建议实验计划

### 实验 1 - 特征基线地图

数据集:

- 20 个音乐声音
- 20 个自然声音
- 20 个物体/城市声音

特征:

- spectral centroid
- flatness
- flux
- roughness
- onset density
- MFCC mean/std
- CQT chroma
- entropy

输出:

- 2D UMAP/t-SNE 投影
- 聚类标签
- 手动感知标签
- 特征到声音检索演示

### 实验 2 — 嵌入比较（Embedding Comparison）

模型：

- PANNs
- AST
- BYOL-A
- AudioMAE
- CLAP
- 可选 OpenL3

指标：

- 按类别/材质的聚类质量（Clustering Quality）
- 最近邻检索主观质量（Nearest-Neighbor Retrieval Quality）
- 对音高/时间偏移/噪声的鲁棒性（Robustness）
- 与手工心理声学描述符的对齐程度（Alignment）

### 实验 3 — 生成式潜空间遍历（Generative Latent Space Traversal）

模型：

- RAVE
- DDSP
- EnCodec / DAC 标记化（Tokenization）

测试：

- 潜变量插值（Latent Interpolation）
- 单维度遍历（Single-Dimension Traversal）
- ABX 可闻性（Audibility）
- 语义评分（Semantic Rating）
- 创作有用性评分（Creative Usefulness Rating）

### 实验 4 - 学习型声音原子

方法:

- 来自当前 wave_packet_demo 的固定 Gabor OMP 基线
- NMF 模板
- K-SVD 学习原子

指标:

- 残差能量
- 原子/模板数量
- 感知质量
- 原子的可解释性
- 重组有用性

---

## 10. 仓库组织变更

本次综述后,仓库围绕主线研究重组:**音频 → 特征 → 感知 → 创作材料**。

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
    └── 01-05 基础报告

demos/
├── foundations/
│   └── 已有 HTML 概念演示
├── references/
│   └── spectral_reference.html
└── creative_features/
    └── 未来主线演示

experiments/
├── creative_features/
│   ├── 01_baseline_features/
│   ├── 02_embedding_comparison/
│   ├── 03_latent_traversal/
│   └── 04_creative_mapping/
└── wave_packet_sparse/
    └── 既有稀疏分解脚本
```

理由:

- `docs/foundations/` 保留原始五个理论模块作为新主线的支撑;
- `docs/literature/` 存储研究计划、文献综述、证据矩阵和未来分类体系;
- `demos/foundations/` 保留精致的概念 HTML 演示;
- `demos/creative_features/` 预留给 feature-space browser 和创作交互原型;
- `experiments/creative_features/` 成为主要实现工作区;
- `experiments/wave_packet_sparse/` 保留先前稀疏分解实验而不杂乱根目录。

---

## 11. 参考文献

### 已验证 arXiv ID

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

### 基础 / 非 arXiv

- Mallat, S., & Zhang, Z. (1993). **Matching pursuits with time-frequency dictionaries**. *IEEE Transactions on Signal Processing*.
- Aharon, M., Elad, M., & Bruckstein, A. (2006). **K-SVD: An Algorithm for Designing Overcomplete Dictionaries for Sparse Representation**. *IEEE Transactions on Signal Processing*.
- Virtanen, T. (2007). **Monaural sound source separation by nonnegative matrix factorization**. *IEEE Transactions on Audio, Speech, and Language Processing*.
- Cramer, J., Wu, H.-H., Salamon, J., & Bello, J. P. (2019). **Look, Listen, and Learn More: Design Choices for Deep Audio Embeddings**.

---

## 12. 下一步行动项

1. **深度阅读** DDSP、RAVE、EnCodec、CLAP、AudioLDM、AudioMAE、BYOL-A。
2. 从四大家族全景构建 `02_feature_taxonomy.md`。
3. 构建 `03_experiment_protocol.md` 用于 baseline features + embedding comparison。
4. 在 `experiments/creative_features/01_baseline_features/` 中实现最小特征提取原型。
5. 在 `demos/creative_features/` 下添加未来创作交互演示。

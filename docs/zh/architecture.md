# 架构

Sonic Atlas 采用研究到系统（research-to-system）的仓库结构：理论文档、交互演示、可运行实验和数据分层管理。

## 仓库分层

```text
sonic-atlas/
├── docs/          # 研究计划、文献综述、基础理论、路线图
├── demos/         # 交互式 HTML 可视化与概念演示
├── experiments/   # 可运行实验、预计算脚本、原型算法
├── data/          # 本地数据入口（gitignored except .gitkeep）
└── notebooks/     # 探索性分析
```

## 概念系统

```text
Raw Audio
  ↓
Decomposition Layer
  - 短时傅里叶变换（STFT，Short-Time Fourier Transform） / 梅尔频谱（Mel Spectrogram，按人耳感知尺度变换的频谱图） / 恒定 Q 变换（CQT，Constant-Q Transform，对数频率分辨率的时频分析） / 连续小波变换（CWT，Continuous Wavelet Transform）
  - Gabor 原子（Gabor Atom，局部化的时频高斯波包） / 非负矩阵分解（NMF，Non-Negative Matrix Factorization） / K-SVD（一种学习超完备字典的稀疏编码算法）
  - 声源分离（Source Separation）
  - 神经编解码器标记化（Neural Codec Tokenization，用神经网络将音频压缩为离散标记序列）

  ↓
Feature Layer
  - 心理声学描述符（Psychoacoustic Descriptor，基于人耳感知的声学量化指标）
  - 预训练嵌入（Pretrained Embedding，在大规模数据上训练好的模型提取的向量表示）
  - 自监督表示（Self-Supervised Representation，无需人工标签、从数据自身结构学习的特征）
  - 生成式潜变量（Generative Latent） / 离散标记（Discrete Token）

  ↓
Validation Layer
  - 重建指标（Reconstruction Metric）
  - ABX 测试（听者判断 A-B-X 三者中 X 更接近谁的可闻性测试） / MUSHRA（Multiple Stimuli with Hidden Reference and Anchor，多刺激隐藏参考的主观音质评分） / 主观标签
  - 解耦性（Disentanglement，每个潜变量维度只控制一个感知属性） / 可控性（Controllability）

  ↓
Creative Layer
  - 特征轨迹（Feature Trajectory，特征值随时间变化的序列，可作为音乐结构）
  - 潜变量插值（Latent Interpolation，在潜空间两点之间平滑过渡）
  - 语料库导航（Corpus Navigation，按特征空间检索声音素材）
  - 合成参数映射（Synthesis Parameter Mapping，将特征映射到声音合成控制参数）
```

## 目录职责

| 目录 | 职责 |
|---|---|
| `docs/literature/` | 研究计划、文献综述（Literature Review）、证据矩阵 |
| `docs/foundations/` | 物理声学、心理声学、时频分析、音色、CNN 基础 |
| `demos/foundations/` | 基础概念的交互演示 |
| `demos/creative_features/` | 主线系统的交互原型 |
| `experiments/creative_features/` | 主线实验：基线特征（Baseline Features）、嵌入比较（Embedding Comparison）、潜变量遍历（Latent Traversal）、创作映射（Creative Mapping） |
| `experiments/wave_packet_sparse/` | 既有波包稀疏重建实验 |
| `data/raw/` | 原始音频样本（不提交） |
| `data/processed/` | 预处理特征与中间数据（不提交） |
| `data/external/` | 外部下载数据（不提交） |

## 演进计划

1. 文献综述稳定后，形成 `docs/literature/02_feature_taxonomy.md`。
2. 实验原型从 `experiments/creative_features/01_baseline_features/` 开始。
3. 成熟实验转化为 `demos/creative_features/` 中的浏览器交互演示。
4. 最终形成一个特征空间浏览器（Feature-Space Browser）：导入声音、提取特征、导航空间、生成创作路径。

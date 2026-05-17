# 模块二：相位感知——可闻性的百年争论

> **研究问题**：如果成功无损地离散化了一段音乐，改变其相位是否会影响听感？

---

## 1. 历史回顾：从 Ohm 到 Helmholtz 的"相位聋"法则

1843 年，物理学家 Georg Simon Ohm 提出一个大胆假说：**音乐的"品质"（即后来的音色）取决于各谐波的振幅，而与它们之间的相对相位无关。** Helmholtz (1863) 在《论音的感觉》中继承并系统化推广了这一观点，形成所谓 "Ohm-Helmholtz 相位聋法则"。

这一法则的核心直觉：耳蜗近似于 Fourier 分析器——基底膜上不同位置对不同的 Fourier 分量响应，而神经发放率编码每个分量的强度。在这种模型中，相位信息被丢弃。

现代研究已清楚表明：**这一法则作为绝对陈述是错误的**，但其在限定条件下的近似有效性令人惊讶。

---

## 2. 当代实验证据：相位何时可闻

### 2.1 二分量与多分量复合音的相位效应

最早的、也最清晰的可闻相位效应出现在**简单复合音**中：

- **二分量复合音**（基频 + 三次谐波）：相位反转（polarity inversion）引发 **> 99% 置信度的可闻差异**（Cabot et al., 引用自 Lipshitz et al., 1982）
- **多谐波复合音**：改变谐波间相对起始相位 → 改变峰值因子（crest factor）和波形包络 → **可显著影响感知响度和"锋利度"**

这一点并不违反 Ohm 法则的实质——**被感知的是包络变化，而非相位本身**。听觉神经元的相位锁定（对低频纯音）编码的是时间包络，而非抽象相位角。

### 2.2 Lipshitz 等人（1982）的决定性研究

JAES 上最广为引用的系统研究之一，结论直接而严谨：

> 1. Even quite small midrange phase nonlinearities can be audible on **suitably chosen signals**.
> 2. Audibility is far greater on **headphones** than on loudspeakers.
> 3. Simple acoustic signals generated anechoically display clear phase audibility on headphones.
> 4. **On normal music or speech signals phase distortion appears not to be generally audible**, although it was heard with 99% confidence on some recorded vocal material.

使用一阶和二阶单位增益全通滤波器（$f_0$: 100 Hz – 3 kHz，Q: 0.5–2），结论清晰：**人工信号可闻，真实音乐不可闻。**

### 2.3 Deer 等人（1985）的群延迟阈值

从群延迟（group delay）角度重新审查相位失真：

> "a statistically significant perceptual threshold is reached when peak group-delay distortion at 2 kHz is in the neighborhood of **2 ms** (for diotic presentation via earphones)."

但该研究特别强调——**可闻性仅限于耳机回放下的点击测试信号**。在真实音乐的上下文中，此阈值不直接适用。

### 2.4 耳机 vs 扬声器 vs 房间

**耳机回放**的相位可闻性显著高于扬声器（Hansen & Madsen, 1974; Lipshitz et al., 1982）。原因：

1. 去除了房间反射（产生时变梳状滤波）
2. 去除了串扰（左耳听右声道、右耳听左声道）
3. 直接耦合于耳道，消除了头部相关传递函数（HRTF）的相位变换

在扬声器回放中，**房间反射本身引入了自然、持续变化的相位失真**——硬件链中的额外相位失真被对照效应（对比基准的缺失）所"掩蔽"。

---

## 3. 现代最前沿：Cheuk 等人（2025）的相位截距失真研究

arXiv:2506.14571 是截至 2025 年的最新严格实验。研究了一种特殊相位失真——**全局常数相位偏移**（$\theta$ 对所有频率分量施加相同的相移），结论：

> "We thus hypothesized that frequency-independent phase shifting is imperceptible for general audio signals."

人类受试者实验支持这一假说：**除 180° 偏移（极性反转）对极不对称波形有微弱效应外，任意角度的恒定相移不可感知。**

他们进一步将相位截距失真应用于**数据增强**——在音频机器学习训练中随机旋转所有频率分量的相位——获得了改进的分类性能，**间接证实了此操作对人类感知的零影响。**

---

## 4. 综合表：相位操作的感知结果

| 相位操作 | 信号类型 | 感知结果 | 证据强度 |
|---------|---------|:---:|:---:|
| 全局常数相位偏移（θ ≠ 180°） | 任意 | **不可闻** | 强（Cheuk 2025, 受控实验） |
| 全局极性反转（θ = 180°） | 不对称波形（语音元音、管乐） | **弱可闻**——仅耳机、特定信号 | 中等（Lipshitz 1982; Wood效应） |
| 全局极性反转 | 典型音乐 | **几乎不可闻** | 中等 |
| 各谐波相对相位随机化 | 人工多谐波 | **可闻**——包络形状变化 | 强 |
| 各谐波相对相位随机化 | 真实音乐 | **不可闻**（余量极小） | 中等（Lipshitz 1982） |
| 全通滤波器群延迟 ~2 ms | 点击 / 瞬态 | **可闻** | 强（Deer 1985） |
| 全通滤波器群延迟 ~2 ms | 音乐 | **不可闻** | 中等 |
| 双耳间相位差（ITD） | 任意 | **可闻**——但不属于单耳音色 | 强 |

---

## 5. 为什么相位感知如此有限？——神经机制层面的原因

### 5.1 临界带内的相位锁定局限

听觉神经纤维在低频（< 1.5 kHz）对波形特定相位锁定发放——这意味着低频相位信息**进入**了神经系统。然而：

- 在一个临界带内，**多根神经纤维对不同谐波分别锁定**——它们的联合发放率编码的是临界带内的**包络能量**，而非各分量之间的相位差
- 相位关系的信息在汇聚于耳蜗核时可能**丢失在发放率的统计中**

### 5.2 相位信息转换为包络信息

当两个频率相近的分量落在同一临界带内时，它们之间的相位差表现为时间域上的**拍频现象**（beats）——这被听觉系统作为**振幅调制（AM）**检测，而非"相位差"。

当两个分量的频率差超过临界带宽时，它们激活不同的神经纤维群体——此时相位关系在不同临界带的**发放时程**中保留，但听觉系统是否会跨频率通道比较精确相位尚无直接证据。

### 5.3 为什么音乐信号几乎免疫

一个典型的音乐信号包含数千个独立谐波，分布在数十个临界带上。随机的各分量相位打乱所导致的波形包络变化在统计上趋于被**中心极限定理效应**冲淡——大量独立分量的随机相位总和趋向更平滑的高斯分布，包络的峰值因子变化极小。

**换言之，音乐越复杂（谐波越多、同时音符越多），相位失真越不可闻。**

---

## 6. 实用含义

### 6.1 对于数字音频系统

- 线性相位滤波器（FIR）和最小相位滤波器（IIR）之间的选择在**回放**中不可闻（对音乐信号）
- 但**制作**流程中滤波器的相位响应会影响累计处理（如多次均衡器的串联），因相位旋转导致波形峰值增长——此为工程问题，非感知问题
- **无损离散化执行全局相位操作不会破坏听感**

### 6.2 对于音乐信息检索和特征提取

- 使用 **magnitude spectrogram**（丢弃相位）是合理的，由此衍生的 Mel 声谱图、MFCC 等特征完全足够
- 仅相位谱对感知分类无贡献
- 需要信号重建的场景（如音源分离、声码器）才需要保留相位

### 6.3 一个有趣的结论性陈述

> **如果我们成功地将一段音乐"无损离散化"（即在频率和强度上无感知损失地数字化），那么不论我们如何旋转其各频率分量的相位（线性或非线性操作），只要保持振幅不变，在原位的扬声器回放条件下，听众无法区分版本间的差异。**

---

## 参考文献

- Ohm, G. S. (1843). Über die Definition des Tones. *Annalen der Physik*, 135(8), 513-565.
- Helmholtz, H. L. F. (1863). *Die Lehre von den Tonempfindungen*.
- Lipshitz, S. P., Pocock, M., & Vanderkooy, J. (1982). On the audibility of midrange phase distortion in audio systems. *JAES*, 30(9), 580-595.
- Hansen, V., & Madsen, E. R. (1974). On aural phase detection. *JAES*, 22(1), 10-14.
- Deer, J. A., Bloom, P. J., & Preis, D. (1985). Perception of phase distortion in all-pass filters. *JAES*, 33(10), 782-787.
- Cheuk, J., et al. (2025). The Perception of Phase Intercept Distortion and its Application in Data Augmentation. *arXiv:2506.14571*.
- Moore, B. C. J. (2012). *An Introduction to the Psychology of Hearing* (6th ed.). Brill.

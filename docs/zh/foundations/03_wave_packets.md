# 模块三：波包——频率轴的平行维度

> **研究问题**：对于某些音频直接使用频率难以正常描述，是不是可以在频率这个维度平行地引入波包方便量化？

---

## 1. 问题的起源：Fourier 完备但不稀疏

### 1.1 Fourier 分析的根本困境

Fourier 定理保证：任意（满足弱条件的）周期或有限能量信号可以表示为正弦波的加权和。这是物理上**完备**的表征。

但"完备"不等于"有用"——考虑以下两类声音：

| 类型 | Fourier 域的呈现 | 问题 |
|------|-----------------|------|
| 钢琴起奏瞬间（5–20 ms） | 分布在全部 22,050 个 bin 中的宽带能量 | 22,050 维向量描述约 2 ms 中 88 个样本的事件 |
| 稳态长笛中音区 | 集中在基频+谐波的稀疏尖峰 | 描述良好 |
| 钹的击打 | 完全无谐波的噪声连续谱 | 无结构，21,000+ 非零 bin |
| 鸟鸣（快速频率滑音） | 能量在多个 bin 间快速流动 | 单帧分析丢失滑动轨迹 |

**核心矛盾**：Fourier 基是为稳态、定频信号优化的——自然界和音乐中的大多数声音并非此类。

### 1.2 Heisenberg-Gabor 不确定性

Gabor (1946) 给出了这一困境的精确数学边界：

$$\Delta t \cdot \Delta f \geq \frac{1}{4\pi}$$

- $\Delta t$：时间局部化精度（信号"何时"发生的不确定性）
- $\Delta f$：频率局部化精度（信号的"音高"的不确定性）

**无法同时获得极致的时间和频率精度。** 如果你需要一个精确到 1 Hz 的频率分析，你的时间窗至少需要 1 秒——在 1 秒内一个 30 ms 的瞬态事件已经结束了。

---

## 2. 解决方案：Gabor 原子——时频平面上的最优粒子

### 2.1 定义

Gabor (1946) 在其经典论文 *Theory of Communication* 中提出了**时频原子**：

$$\psi_{(t_0, f_0, \sigma)}(t) = e^{-\frac{(t - t_0)^2}{2\sigma^2}} \cdot e^{i 2\pi f_0 (t - t_0)}$$

参数：
- $t_0$：时间中心——原子在"何时"振荡
- $f_0$：频率中心——原子在"什么音高"振荡
- $\sigma$：时间展宽——原子的"粒度"
- 且 Gabor 函数是**唯一达到 Heisenberg 下限的函数族**：$\Delta t \cdot \Delta f = 1/4\pi$（等式！）

### 2.2 Gabor 原子 vs. 正弦波

| 性质 | 正弦波 | Gabor 原子 |
|------|--------|----------|
| 时间局域 | 无限长，无局域性 | 以 $\sigma$ 控制，约 $2\sigma$ 有效宽度 |
| 频率局域 | 完美（单一频率） | 高斯分布，带宽 $\approx 1/(4\pi\sigma)$ |
| 参数数 | 2（频率、复数振幅） | 4（$t_0, f_0, \sigma$, 复数振幅） |
| 表示瞬态 | 需要大量正弦波干涉 | 单一原子即可 |
| 表示稳态纯音 | 天然 | 需要多个宽 $\sigma$ 的原子 |

单个 Gabor 原子就是一个**波包**——在有限时间区间内振荡的"声音粒子"。

---

## 3. 匹配追踪：用波包字典稀疏分解信号

### 3.1 算法思想

Mallat & Zhang (1993) 提出了匹配追踪（Matching Pursuit, MP）：

1. 构造一个过完备字典 $\mathcal{D}$，包含数百万个 Gabor 原子（覆盖所有 $t_0, f_0, \sigma$ 组合）
2. 迭代式地从残余信号中找出相关性最大的原子
3. 减掉该原子的贡献，更新残余
4. 重复 $K$ 次，得到信号 $K$-稀疏近似：

$$s(t) \approx \sum_{k=1}^{K} a_k \cdot \psi_{(t_k, f_k, \sigma_k)}(t)$$

其中每个 $k$ 是一个 **$(t_k, f_k, \sigma_k, a_k)$ 四元组**。

### 3.2 工程实现

**快速多 Gabor 字典匹配追踪**（Průša, Holighaus & Balazs, 2021）：性能比标准 MPTK **提升 3.5–70 倍**。核心技术：

- 在系数域直接更新残余（避免信号域往返）
- 预计算原子间内积并阈值截断——利用 Gabor 原子的局域性，Gram 矩阵的大多数元素接近零
- 多 Gabor 字典内跨字典的交叉 Gram 矩阵同样支持截断
- C 语言实现（LTFAT 工具箱后端），提供 MATLAB/GNU Octave 接口

实验配置：Blackman 窗，$M=512,1024,2048$ 个频率通道，hop size $a=M/4$，3 个字典拼接。在 $M=2048, a=512$ 条件下，加速比达到 **70×**。

**感知匹配追踪**（Chardon, Necciari & Balazs, 2014, *ICASSP*）：将心理声学掩蔽模型直接集成到 MP 分解流程中（Perceptual MP, PMP）。

**字典构造**（5 种窗长）：

| window length (samples) | window length (ms) | FFT size | hop size | 等效 Δf |
|:---:|:---:|:---:|:---:|:---:|
| 128 | 3 | 8192 | 64 | ~27 Hz |
| 256 | 6 | 8192 | 64 | ~13 Hz |
| 512 | 11 | 8192 | 64 | ~7 Hz |
| 1024 | 23 | 8192 | 64 | ~3.5 Hz |
| 2048 | 46 | 8192 | 64 | ~1.7 Hz |

注意：**所有 5 种 σ 对所有频率均可用**——MP 算法在 $(t_0, f_0, \sigma)$ 空间中自由竞争最优原子，不做 σ ∝ 1/f₀ 的显式耦合。

**ERB 尺度的时频掩蔽模型**：掩蔽阈值定义在心理声学 ERB 频率尺度上：

$$\text{ERB}_{\text{num}}(\nu) = 9.265 \ln\!\left(1 + \frac{\nu}{228.8455}\right)$$

其中 $\nu$ 为 Hz。掩蔽模型以 $\Delta F$（ERB 单位）和 $\Delta T$（ms）为坐标，掩蔽强度 $C(\Delta F)$ 和衰减常数 $\lambda(\Delta F)$ 均为 $\Delta F$ 的多项式函数——掩蔽效应在 ERB 尺度上近似平移不变，但在 Hz 尺度上是频率依赖的。

**结果**（80,000 次 MP 迭代后）：PMP 移除了 **35–66%** 的原子（取决于信号类型和掩蔽模型变体），在 PEMO-Q 感知质量评估中保持 > 0.998 的 PSM 分数——"perceptible but not annoying"。

**论文明确指出的后续方向**：用 **ERBLET 变换**（Necciari et al., 2013）替代 Gabor 字典——ERBLET 是一种"感知适配的时频表示"，其时频原子天然在 ERB 尺度上均匀分布，Δf 随 f₀ 自动缩放。换言之，ERBLET 直接内置了恒定 Q 在 ERB 尺度上——这正是在 Gabor 框架中缺失的 σ ∝ 1/f₀ 约束。

### 3.3 σ 与频率依赖性：两种哲学

上述工作揭示了一个深层选择：

| 策略 | 代表 | σ 与 f₀ 的关系 | 感知匹配方式 |
|------|------|:---:|------|
| **多 σ 竞争 + 掩蔽后处理** | Chardon PMP (2014) | 独立（5 种 σ 对全频域可用） | ERB 掩蔽模型后筛 |
| **显式 σ ∝ 1/f₀** | ERBLET, 小波 | 耦合（σ 随 f₀ 自动缩放） | 直接内置在基函数中 |

两者的权衡类似于 STFT vs. 小波之争：多 σ 竞争赋予算法最大自由度（可为低频稳态选宽 σ、为高频瞬态选窄 σ），但字典规模更大、计算更重；显式耦合在字典构建时就注入感知知识，字典更紧凑，但丧失了为"非常规"组合（如低频窄 σ 用于拍频检测）提供原子的灵活性。

当前实践中，**多 Gabor 字典 + 心理声学后处理是主流选择**（自由度高、可证最优），而 **ERBLET / 恒定 Q Gabor 字典代表感知最优的紧致方向**。

### 3.4 音乐信号上的表示效率

Chardon et al. (2014) 在两个真实音乐片段上评测（Bruno Maderna 钢琴协奏曲 3s，Suzanne Vega 歌曲 3s，均为 44.1 kHz）：

| 表示方法 | 活跃系数 | 感知失真 (PEMO-Q PSM) | 原子移除率 |
|---------|:---:|:---:|:---:|
| PCM (44.1 kHz, 3s) | 132,300 样本 | 无（原始） | — |
| 完整 MP (80,000 原子) | 80,000 四元组 | PSM=1.0 / 0.9995 | 0% |
| PMP (频域掩蔽) | ~52,000–54,000 四元组 | PSM=1.0 / 0.9995 | 35–46% |
| PMP (时频掩蔽) | ~40,000–47,000 四元组 | PSM=0.999 / 0.9985 | 40–66% |

> PSM = 1.0 表示感知无差异；> 0.99 表示"perceptible but not annoying"（PEMO-Q 评估标准）。

核心发现：**时频掩蔽模型（同时考虑频率掩蔽和时间掩蔽）比纯频域掩蔽多移除 5–20% 的原子，且保持感知质量 > 0.998。** 这直接验证了波包时频框架在感知压缩上的有效性。

---

## 4. 小波：对数频率的波包族

Kronland-Martinet, Morlet & Grossmann (1987) 首次将小波变换系统地应用于声音信号分析，开创了"听觉时频分析"的方向。他们的关键洞察：小波的**恒定 Q** 特性天然匹配人类听觉。

小波变换的所有分析函数由单一母小波通过**时间平移**和**频率缩放**派生：

$$\psi_{(b, a)}(t) = \frac{1}{\sqrt{a}} \psi\!\left(\frac{t - b}{a}\right)$$

关键特性：

- **恒定 Q**（constant-Q）：$\Delta f / f$ 恒定，带宽与中心频率成正比
- 高频区域的时间分辨率高（适合瞬态），低频区域的频率分辨率高（适合精确音高）
- 此特性**直接匹配人类听觉的对数频率感知和临界带宽**

### 4.1 小波谱（scalogram）

小波变换的模平方 $|W(b, a)|^2$ 构成 **scalogram**——它是 STFT 声谱图的对数频率版本。

与 Mel 声谱图的关键区别：Mel 声谱图仍以固定窗长做 STFT、再在频率轴插值到 Mel 尺度，而**小波变换的内在分析窗自适应于频率**。

> Daubechies (1990): "The wavelet transform, unlike the short-time Fourier transform, treats frequency in a logarithmic way, which is similar to our acoustic perception. This is another argument for the use of wavelets for the analysis and/or synthesis of acoustic signals."

### 4.2 小波与 Gabor MP 的关系

小波可以视为 Gabor 字典的一种**特化**——将原子的 $\sigma$ 与 $f_0$ 显式耦合并限制在一条一维曲线上：

$$\sigma \propto \frac{1}{f_0} \quad \Rightarrow \quad Q = \frac{f_0}{\Delta f} = \text{常数}$$

Gabor MP 的优势在于 $\sigma$ 可以自由选择（对于瞬态，低频处也可用窄 $\sigma$；对于稳态，高频处也可用宽 $\sigma$）；小波的优势在于字典紧凑、计算高效、天然匹配听觉。Chardon et al. (2014) 建议的 ERBLET 变换正是试图在两者之间取得最优——在 ERB 尺度上保持恒定 Q，但仍提供一定的 $\sigma$ 灵活性。

---

## 5. 波包合成：Wickerhauser 的远见

Victor Wickerhauser (1995, IEEE) 提出用**小波包**替代大量正弦振荡器进行声音合成：

- 单个小波包发生器 = 拥有内置频谱包络的"超级振荡器"
- 系数高度稀疏（大多接近零）→ 高效存储
- 可压缩——丢弃小系数仅引入微小误差（对平滑信号）
- 本质上是**声音的"粒子化"合成**——每个声事件对应一个波包，而非持续开动的正弦振荡器

这一思想启发了后续多款实验性声音合成软件，但至今未能取代加性合成和采样合成的工业主流。

---

## 6. 响应原始问题：波包作为频率的平行维度

### 6.1 直接回答

> **是。引入波包维度（$t_0, f_0, \sigma$）不仅在数学上精确，而且解决了纯频率分析的两个根本问题：(1) 表示瞬态事件的不稀疏性；(2) 线性频率轴与对数听觉感知的不匹配。**

### 6.2 Gabor 原子的四维参数空间

在"频率-强度-时间-相位"框架中，Gabor 原子引入了一个新的隐式维度：**时频展宽 $\sigma$**：

| 原始框架 | 扩展框架（波包） |
|---------|----------------|
| 频率 $f$ | 频率中心 $f_0$ |
| 强度 $a$ | 复数振幅 $a_k$（幅度 + 相位） |
| 时间 $t$ | 时间中心 $t_0$ |
| 相位 $\phi$ | 包含在 $a_k$ 的复角中 |
| — | **时频展宽 $\sigma$** ← 新维度 |
| — | 波包形状（Gabor 的 $e^{-t^2/2\sigma^2}$ 仅是特例） |

### 6.3 在 music 具体应用中的合适性

音频描述体系的选择可类比于乐器分析中的表示层级：

| 表示 | 适合 | 不适合 | σ-f₀ 关系 | 感知优化 |
|------|------|--------|:---:|------|
| Fourier（纯正弦） | 稳态持续音、管风琴 | 打击乐、瞬态、噪声 | 无 σ | 无 |
| 短时 Fourier（STFT） | 大多数稳态音乐 | 极快速起奏 | 全局固定 | 无 |
| 小波（对数尺度） | 匹配听觉的频谱分析 | 非恒定 Q 的应用 | **显式 σ ∝ 1/f₀** | 内置（恒定 Q） |
| Gabor MP（波包原子） | 事件级稀疏描述、瞬态检测 | 稳态连续背景 | 自由竞争 | 无（纯 ℓ₂ 驱动） |
| 多 Gabor MP（Průša, 2021） | 多尺度瞬态 + 稳态 | 字典规模大 | 多 σ 自由竞争 | 无 |
| 感知 MP / PMP（Chardon, 2014） | 心理声学最优压缩 | 精密工程测量 | 多 σ 竞争 + ERB 掩蔽后筛 | **后处理（ERB 掩蔽）** |
| ERBLET（Necciari, 2013） | 感知原生的时频分析 | 未在 PMP 中实现 | **σ ∝ 1/ERB(f₀)** | **内置** |

**建议：对于各维度建模，将波包作为频率轴的正交拓展维度。音乐可表示为一个稀疏的 $(t_k, f_k, \sigma_k, a_k)$ 四元组事件序列，而非连续的频率-振幅函数。**

---

## 参考文献

- Gabor, D. (1946). Theory of communication. *Journal of the Institution of Electrical Engineers*, 93(26), 429–457.
- Kronland-Martinet, R., Morlet, J., & Grossmann, A. (1987). Analysis of sound patterns through wavelet transforms. *International Journal of Pattern Recognition and Artificial Intelligence*, 1(2), 273–302.
- Daubechies, I. (1990). The wavelet transform, time-frequency localization and signal analysis. *IEEE Transactions on Information Theory*, 36(5), 961–1005.
- Mallat, S., & Zhang, Z. (1993). Matching pursuits with time-frequency dictionaries. *IEEE Transactions on Signal Processing*, 41(12), 3397–3415.
- Wickerhauser, M. V. (1995). Wavelet packets for sound synthesis. In *An Introduction to Wavelets* (pp. 1–16). IEEE.
- Sturm, B. L., Roads, C., McLeran, A., & Shynk, J. J. (2009). Analysis, visualization, and transformation of audio signals using dictionary-based methods. *Journal of New Music Research*, 38(4), 325–341.
- Necciari, T., Balazs, P., Holighaus, N., & Søndergaard, P. (2013). The ERBlet transform: An auditory-based time-frequency representation with perfect reconstruction. *Proceedings of IEEE ICASSP 2013*, 498–502.
- Chardon, G., Necciari, T., & Balazs, P. (2014). Perceptual matching pursuit with Gabor dictionaries and time-frequency masking. *Proceedings of IEEE ICASSP 2014*, 3132–3136.
- Průša, Z., Holighaus, N., & Balazs, P. (2021). Fast Matching Pursuit with Multi-Gabor Dictionaries. *ACM Transactions on Mathematical Software*, 47(3), Article 24, 1–20.

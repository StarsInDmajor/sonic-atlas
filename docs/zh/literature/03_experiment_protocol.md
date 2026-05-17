# Experiment Protocol: Baseline Feature Extraction and Feature-Space Browser

> **目标**:定义 Sonic Atlas Phase 2 第一条可运行实验链路--从小型声音语料(Corpus)中提取可解释的心理声学(Psychoacoustics)/ 手工描述符(Handcrafted Descriptors),生成特征表(Feature Table)、二维投影(2D Projection)和最近邻检索(Nearest-Neighbor Retrieval),并通过人工听觉检查评估这些特征是否适合作为创作材料。

---

## 1. 目的与范围

本实验协议将 `02_feature_taxonomy.md` 中的四大家族分类体系转化为 Phase 2 的可执行实验方案。它的核心产出是一条完整的、可复现的、从音频文件到创作决策支持的链路:

```text
data/raw/small_corpus/
  → manifest.csv(清单文件,记录所有音频的元数据)
  → audio preprocessing(音频预处理:mono, 22050 Hz, normalize)
  → baseline P0 feature extraction(基线 P0 特征提取)
  → features_raw.csv(原始特征表)
  → z-score normalization(z-score 归一化,将数据标准化为均值 0、标准差 1)
  → features_normalized.csv(归一化特征表)
  → PCA / UMAP 2D projection(PCA 主成分分析 / UMAP 均匀流形近似投影的二维投影)
  → projection_pca.json / projection_umap.json
  → nearest-neighbor retrieval(最近邻检索)
  → neighbors.json
  → manual listening + perceptual tags(人工听检 + 感知标签)
  → evaluation_notes.md
```

**不包含**:

- PANNs / AST / BYOL-A / CLAP 嵌入(Embedding,Phase 3)
- RAVE / DDSP / EnCodec 潜变量遍历(Latent Traversal,Phase 4)
- 复杂心理声学听觉测试(ABX / MUSHRA)
- 大规模数据集训练
- 生成式音频模型

---

## 2. 研究问题

Phase 2 baseline 实验围绕四个问题展开:

### RQ1. 基线描述符（Baseline Descriptors）能否形成直觉上合理的声音空间？

检查：

- 乐器声是否靠近乐器声；
- 自然纹理是否靠近自然纹理；
- 瞬态密集的声音（Transient-Heavy Sounds）是否分布在相近区域；
- 明亮 / 噪声 / 密集的声音是否在局部聚集。

### RQ2. 哪些 handcrafted features 对创作最有解释力?

例如:

- centroid 是否确实对应 brightness?
- flatness / entropy 是否对应 noise / texture complexity?
- onset density 是否对应 rhythmic / granular density?
- MFCC 是否提升 timbre clustering?

### RQ3. 特征空间最近邻（Feature-Space Nearest Neighbors）是否有创作价值？

不是只问“是否同类”，而是问：

- 是否能找到可替代素材？
- 是否能找到听感相近但语义不同的声音？
- 是否能产生创作联想？

### RQ4. Baseline descriptors 的局限在哪里?

需要记录:

- 哪些声音被错误聚类;
- 哪些听感差异没有被捕捉;
- 哪些 feature 受录音响度 / 噪声 / 长度影响过大;
- 哪些需要 embedding 或 sparse decomposition 补充。

---

## 3. 实验总览

| Aspect | Specification |
|---|---|
| Corpus | ~60 clips (20 music + 20 nature + 20 urban_object) |
| Clip duration | 3-10 s (target 5 s) |
| Audio format | WAV / FLAC preferred; MP3 accepted |
| Processing sample rate | 22050 Hz (for baseline descriptors) |
| Feature level | clip-level aggregations of frame-level features |
| Projection | PCA + UMAP |
| Retrieval | k-nearest neighbors (k=5-10) |
| Evaluation | manual listening + perceptual label + correlation analysis |
| Expected time | corpus preparation ~3 h, feature extraction ~1 h, evaluation ~2 h |

---

## 4. 语料设计

### 4.1 类别

| Category ID | Label | Examples | Research Focus |
|---|---|---|---|
| `music` | Musical / instrument sounds | piano, guitar, strings, flute, percussion, synth, voice | pitch, timbre, attack, sustain |
| `nature` | Natural environmental sounds | rain, water, wind, bird, fire, insect, thunder | texture, noise, event density |
| `urban_object` | Urban / object / mechanical sounds | footsteps, door, machine, traffic, metal, glass, typing | transient, material, gesture |

### 4.2 目标分布

```text
60 clips total
├── 20 music
├── 20 nature
└── 20 urban_object
```

Variety within each category is more important than volume. Each category should span a range along at least two perceptual axes (e.g. bright↔dark, tonal↔noisy, sparse↔dense).

### 4.3 子类别与标签示例

**Music subcategories**: piano, guitar, strings, wind, brass, percussion, synth, voice, ensemble

**Nature subcategories**: rain, stream, ocean, wind, bird, insect, fire, thunder, leaves

**Urban/object subcategories**: footsteps, door, machine, traffic, metal impact, glass, typing, bell, siren

**Perceptual tags** (multi-label, human-assigned):

```text
bright / dark
tonal / noisy
smooth / rough
sparse / dense
percussive / sustained
organic / mechanical
stable / evolving
soft / hard
warm / cold
close / distant
```

### 4.4 片段长度规则

| Rule | Value | Rationale |
|---|---|---|
| Target duration | 5 s | Enough for stable clip-level statistics |
| Minimum duration | 3 s | Too short → unstable spectral/temporal estimation |
| Maximum duration | 10 s | Too long → multiple events confound descriptors |
| Long source handling | Record `start_time` / `end_time` in manifest | Sub-clip extraction from longer recordings |

### 4.5 数据来源

Recommended open sources:

| Source | License | Content |
|---|---|---|
| Freesound | CC0 / CC-BY / CC-BY-NC | Wide variety, user-uploaded |
| ESC-50 | CC-BY | Environmental sound classification dataset |
| UrbanSound8K | CC-BY-NC | Urban sounds |
| NSynth (subset) | CC-BY | Musical instrument tones |
| BBC Sound Effects | Various | Professional sound effects |

**Important**: `data/raw/` is gitignored. Only `manifest.csv` and metadata are committed. If curated demo audio is needed for the browser, it should be selected separately from clips with permissive licenses.

---

## 5. 数据布局

```text
data/
├── raw/
│   └── small_corpus/
│       ├── music/
│       │   ├── piano_001.wav
│       │   ├── guitar_001.wav
│       │   └── ...
│       ├── nature/
│       │   ├── rain_001.wav
│       │   └── ...
│       └── urban_object/
│           ├── metal_001.wav
│           └── ...
│
└── processed/
    └── creative_features/
        └── 01_baseline_features/
            ├── manifest.csv
            ├── features_raw.csv
            ├── features_normalized.csv
            ├── feature_stats.json
            ├── missing_features.csv
            ├── projection_pca.json
            ├── projection_umap.json
            ├── neighbors_all.json
            ├── neighbors_timbre.json
            ├── neighbors_texture.json
            ├── correlation_matrix.csv
            ├── category_summary.csv
            └── evaluation_notes.md
```

Code directory:

```text
experiments/creative_features/01_baseline_features/
├── README.md
├── make_manifest.py
├── extract_features.py
├── project_features.py
├── evaluate_features.py
├── schemas.py
└── outputs/               # optional local outputs (gitignored)
```

---

## 6. Manifest Schema

`manifest.csv` is the single source of truth for the corpus.

### 6.1 必须字段

| Field | Type | Required | Description |
|---|---|---:|---|
| `sample_id` | string | yes | Unique ID, e.g. `music_piano_001` |
| `file_path` | string | yes | Relative path from repo root, e.g. `data/raw/small_corpus/music/piano_001.wav` |
| `category` | string | yes | `music` / `nature` / `urban_object` |
| `subcategory` | string | no | e.g. `piano`, `rain`, `metal` |
| `duration` | float | no | Seconds (auto-filled by `make_manifest.py`) |
| `sample_rate` | int | no | Original sample rate (auto-filled) |
| `channels` | int | no | Number of channels (auto-filled) |
| `start_time` | float | no | Sub-clip start in seconds (default 0) |
| `end_time` | float | no | Sub-clip end in seconds (default full length) |
| `source` | string | no | Dataset or recording source |
| `license` | string | no | License / usage terms |
| `manual_tags` | string | no | Semicolon-separated, e.g. `bright;tonal;sustained` |
| `description` | string | no | Free-text description of the sound |
| `notes` | string | no | Any additional notes |

### 6.2 样本 ID 命名规范

```text
{category}_{subcategory}_{sequence}
```

Examples:

```text
music_piano_001
nature_rain_003
urban_object_metal_002
```

Do not use file names as IDs since files may be renamed or reorganized.

---

## 7. 音频预处理协议

### 7.1 加载规则

```text
load audio with librosa or soundfile
convert to mono (average channels if stereo)
resample to 22050 Hz for baseline descriptors
preserve original file on disk unchanged
```

Why 22050 Hz:

- Standard for librosa-based MIR workflows;
- Sufficient for most timbre/texture descriptors (Nyquist = 11025 Hz);
- Fast computation;
- Neural codec / high-frequency analysis will use 44100 / 48000 Hz in later phases.

### 7.2 两种分析视图(Two Analysis Views)

为避免将响度与音色混淆,协议定义两种视图:

| 视图 | 内容 | 用途 |
|---|---|---|
| **原始视图(raw_view)** | 单声道、22050 Hz、未归一化 | RMS、响度代理、起始点密度、振幅特征 |
| **归一化视图(normalized_view)** | 单声道、22050 Hz、峰值归一化(Peak Normalized) | centroid、bandwidth、rolloff、flatness、entropy、MFCC、chroma |

理由:如果所有特征都使用归一化音频,响度信息会丢失。如果所有特征都使用原始音频,录音增益差异会污染音色比较。

### 7.3 归一化方法

```text
normalized_view = audio / max(abs(audio))
```

Peak normalization is simple and stable for the first version. Corpus-level RMS normalization can be added later.

### 7.4 静音处理

| Rule | Behavior |
|---|---|
| Default | Do **not** aggressively trim |
| Optional trim | If leading/trailing silence exceeds 1 s and amplitude < -40 dB relative to peak, apply `librosa.effects.trim(top_db=40)` |
| Metadata | Record whether trim was applied in manifest notes |
| Silence ratio | Compute and store: `silence_ratio = frames_below_threshold / total_frames` |

Why not default trim:

- Silence may be part of the temporal structure;
- But excessive silence distorts RMS, onset density, and duration-dependent features.

### 7.5 标准分析参数

```text
sample_rate        = 22050
n_fft              = 2048
hop_length         = 512
window             = 'hann'
n_mels             = 128
n_mfcc             = 13
roll_percent       = 0.85
fmin               = 0
fmax               = sample_rate / 2  (= 11025)
```

---

## 8. 基线特征集

### 8.1 P0 特征(必须实现)

| Group | Feature | Library / Method | View | Columns |
|---|---|---|---|---|
| Energy | RMS | `librosa.feature.rms` | raw_view | `rms_mean`, `rms_std` |
| Energy | Loudness proxy | RMS in dB SPL, or `librosa.feature.rms` with dB conversion | raw_view | `loudness_proxy_mean`, `loudness_proxy_std` |
| Spectral | Spectral centroid | `librosa.feature.spectral_centroid` | normalized_view | `centroid_mean`, `centroid_std` |
| Spectral | Spectral bandwidth | `librosa.feature.spectral_bandwidth` | normalized_view | `bandwidth_mean`, `bandwidth_std` |
| Spectral | Spectral rolloff | `librosa.feature.spectral_rolloff(roll_percent=0.85)` | normalized_view | `rolloff_mean`, `rolloff_std` |
| Spectral | Spectral flatness | `librosa.feature.spectral_flatness` | normalized_view | `flatness_mean`, `flatness_std` |
| Spectral | Spectral flux | `librosa.onset.onset_strength` | normalized_view | `flux_mean`, `flux_std` |
| Spectral | Spectral entropy | Custom: `-sum(P * log2(P)) / log2(n_bins)` where `P = mag / sum(mag)` | normalized_view | `entropy_mean`, `entropy_std` |
| Temporal | Onset density | `librosa.onset.onset_detect` → count / duration | normalized_view | `onset_density` |
| Cepstral | MFCC | `librosa.feature.mfcc(n_mfcc=13)` | normalized_view | `mfcc_01_mean` ... `mfcc_13_mean`, `mfcc_01_std` ... `mfcc_13_std` |

### 8.2 P1 特征(P0 之后实现)

| Group | Feature | Library / Method | View | Columns |
|---|---|---|---|---|
| Temporal | Attack time | Envelope analysis: time from 10% to 90% of peak amplitude per onset | raw_view | `attack_time` |
| Harmonic | Chroma | `librosa.feature.chroma_stft` | normalized_view | `chroma_01_mean` ... `chroma_12_mean`, `chroma_01_std` ... `chroma_12_std` |
| Harmonic | F0 confidence | `librosa.pyin` or `librosa.yin` | normalized_view | `f0_confidence_mean`, `f0_std` (pitch stability) |
| Texture | Roughness estimate | Simplified: spectral irregularity or beating-based proxy | normalized_view | `roughness_mean`, `roughness_std` |

### 8.3 延后特征

| Feature | Reason to Defer |
|---|---|
| Full psychoacoustic loudness (Zwicker / ITU-R) | Needs model selection and calibration; RMS proxy sufficient for v0 |
| Rigorous roughness / sensory dissonance | Implementation choices affect validity; needs dedicated protocol |
| Inharmonicity | Requires reliable partial / f0 tracking |
| NMF templates | Better after baseline feature table exists; different experiment |
| PANNs / AST / BYOL-A / AudioMAE / CLAP | Phase 3 embedding comparison |
| RAVE / DDSP / EnCodec latents | Phase 4 latent traversal |

---

## 9. 特征计算规格

### 9.1 帧级到片段级聚合

All frame-level features are aggregated to clip-level using:

| Aggregation | Use |
|---|---|
| `mean` | Central tendency |
| `std` | Variability / texture stability |

Optional future aggregations (not in v0):

```text
median, p10, p90, min, max
```

### 9.2 频谱熵定义

```python
# Pseudo-code
S = np.abs(librosa.stft(y, n_fft=n_fft, hop_length=hop_length))
S_mean = S.mean(axis=1)                    # average magnitude spectrum
P = S_mean / (S_mean.sum() + 1e-10)       # normalize to probability
n_bins = len(P)
entropy = -np.sum(P * np.log2(P + 1e-10)) / np.log2(n_bins)
# Range: 0 (pure tone) to 1 (flat / white noise)
```

### 9.3 起奏密度定义

```python
onset_frames = librosa.onset.onset_detect(y=y, sr=sr, hop_length=hop_length)
duration = len(y) / sr
onset_density = len(onset_frames) / duration  # events per second
```

### 9.4 响度代理定义 (v0)

```python
rms = librosa.feature.rms(y=y, hop_length=hop_length)[0]
loudness_proxy_db = 20 * np.log10(rms + 1e-10)
# Aggregate: mean, std of frame-level dB values
```

This is a rough proxy. It does not account for A-weighting, equal-loudness contours, or perceptual loudness models. The protocol explicitly marks this as a placeholder for future refinement.

---

## 10. 特征聚合与归一化

### 10.1 输出特征表

每行 = 一个片段。 Columns = aggregated features + metadata.

```text
sample_id, file_path, category, subcategory, duration, manual_tags,
rms_mean, rms_std, loudness_proxy_mean, loudness_proxy_std,
centroid_mean, centroid_std, bandwidth_mean, bandwidth_std,
rolloff_mean, rolloff_std, flatness_mean, flatness_std,
flux_mean, flux_std, entropy_mean, entropy_std,
onset_density,
mfcc_01_mean, mfcc_01_std, ..., mfcc_13_mean, mfcc_13_std,
attack_time,
chroma_01_mean, ..., chroma_12_std,
f0_confidence_mean, f0_std,
roughness_mean, roughness_std
```

### 10.2 语料库级归一化

Generate two files:

| File | Content |
|---|---|
| `features_raw.csv` | Raw aggregated feature values |
| `features_normalized.csv` | Z-scored: `z = (x - mean) / std` |

### 10.3 特征统计

Save `feature_stats.json` with per-feature statistics:

```json
{
  "centroid_mean": {
    "mean": 2450.3,
    "std": 812.7,
    "min": 380.1,
    "max": 5200.0
  },
  "flatness_mean": {
    "mean": 0.15,
    "std": 0.22,
    "min": 0.001,
    "max": 0.89
  }
}
```

### 10.4 缺失值处理

| Rule | Behavior |
|---|---|
| Inapplicable feature | Write `NaN` |
| Pre-projection imputation | Median imputation per feature column |
| Reporting | Generate `missing_features.csv` listing samples with NaN features |
| Deletion | Do **not** silently delete samples; keep them with NaN and flag |

---

## 11. 投影协议(Projection Protocol)

### 11.1 投影方法

| 方法 | 角色 | 库 |
|---|---|---|
| PCA(主成分分析,Principal Components Analysis) | 确定性线性基线;轴可解释为方差方向 | `sklearn.decomposition.PCA` |
| UMAP(均匀流形近似与投影,Uniform Manifold Approximation and Projection) | 非线性感知图;更适合浏览 | `umap.UMAP` |

t-SNE(t-分布随机邻域嵌入)是可选的。它不是默认选项,因为它非确定性、对困惑度(Perplexity)敏感,且不能很好地保持全局结构。

### 11.2 UMAP 参数(建议 v0)

```python
reducer = umap.UMAP(
    n_components=2,
    n_neighbors=15,
    min_dist=0.1,
    metric='euclidean',
    random_state=42
)
```

### 11.3 投影特征组

Run projection on three feature subsets:

| Group | Features | Purpose |
|---|---|---|
| `all_features` | All normalized P0 features | General similarity map |
| `spectral_features` | centroid, bandwidth, rolloff, flatness, flux, entropy, MFCC | Timbre similarity |
| `temporal_texture` | onset_density, flux, entropy, flatness, rms_std | Texture / event similarity |

This helps answer: which feature group best organizes the corpus for creative navigation?

### 11.4 距离度量

Default: Euclidean distance on z-scored features.

Optional: cosine distance (useful when magnitude is less important than direction).

---

## 12. 相似性与最近邻检索(Similarity & Nearest-Neighbor Retrieval)

### 12.1 检索模式

| 模式 | 特征集 | 创作用途 |
|---|---|---|
| `all_features` | 所有归一化 P0 特征 | 通用"什么声音像这个?" |
| `timbre_features` | centroid, bandwidth, rolloff, flatness, MFCC | "什么音色相似?" |
| `texture_features` | entropy, flatness, flux, onset_density | "什么纹理/密度相似?" |
| `temporal_features` | onset_density, flux, rms_std | "什么事件结构相似?" |

### 12.2 检索参数

```text
k = 5  (default)
k = 10 (for evaluation)
distance_metric = euclidean
feature_set = normalized (z-scored)
```

### 12.3 输出 Schema

`neighbors_all.json` (and similar for other modes):

```json
{
  "music_piano_001": {
    "neighbors": [
      {
        "sample_id": "music_guitar_002",
        "distance": 0.42,
        "rank": 1
      },
      {
        "sample_id": "nature_bird_003",
        "distance": 0.58,
        "rank": 2
      }
    ]
  }
}
```

### 12.4 跨类别邻居分析(Cross-Category Neighbor Analysis)

检索后,计算:

- top-5 近邻中,有多少比例在同一类别?
- 有多少比例共享至少一个感知标签?
- 哪些类别边界最受 / 最不受尊重?
- 哪些跨类别对意外地接近?

---

## 13. 手动听检与标注协议(Manual Listening & Annotation Protocol)

### 13.1 感知标签(每样本)

每个样本应标注多标签感知标签(Perceptual Tags):

| 轴 | 量表 | 标签 |
|---|---|---|
| 亮度(Brightness) | 1-5 | 1 = 很暗,5 = 很亮 |
| 有调 vs 噪声(Tonal vs Noisy) | 1-5 | 1 = 纯有调,5 = 纯噪声 |
| 密度(Density) | 1-5 | 1 = 很稀疏,5 = 很密集 |
| 起奏锋利度(Attack Sharpness) | 1-5 | 1 = 很柔和的起始,5 = 很锋利的起始 |
| 粗糙度(Roughness) | 1-5 | 1 = 很平滑,5 = 很粗糙 |
| 稳定性(Stability) | 1-5 | 1 = 很稳定,5 = 很多变 |
| 有机 vs 机械(Organic vs Mechanical) | 1-5 | 1 = 很有机,5 = 很机械 |

Plus categorical tags:

```text
percussive / sustained / textured / pitched / unpitched / harmonic / inharmonic
```

### 13.2 听检清单(每样本)

| Question | Type | Notes |
|---|---|---|
| What is the main sound source? | free text | |
| Bright or dark? | 1-5 | |
| Tonal or noisy? | 1-5 | |
| Sparse or dense? | 1-5 | |
| Sharp or soft attack? | 1-5 | |
| Obvious pitch? | yes/no | |
| Obvious texture motion? | yes/no | |
| How could this be used in composition? | free text | |

### 13.3 邻居评估(每查询样本)

对每个查询样本,听 top-5 近邻并评分:

| 问题 | 类型 | 备注 |
|---|---|---|
| 它们听起来像吗? | 1-5(声学相似性,Acoustic Similarity) | |
| 它们的意义相似吗? | 1-5(语义相似性,Semantic Similarity) | |
| 你能在作品中用一个替代另一个吗? | 1-5(创作有用性,Creative Usefulness) | |
| 是什么让它们相似 / 不同? | 自由文本 | |
| 哪个近邻最意外但有用? | 自由文本 | |

这直接对应 `02_feature_taxonomy.md` 中的三种相似性类型:

```text
声学相似性(Acoustic Similarity) ≠ 语义相似性(Semantic Similarity) ≠ 创作有用性(Creative Usefulness)
```

---

## 14. 评估标准（Evaluation Criteria）

### 14.1 技术成功

| 标准 | 通过条件 |
|---|---|
| 清单完整性 | 所有有效音频文件均列出 `sample_id` 和 `file_path` |
| 特征提取 | `features_raw.csv` 包含所有有效样本的所有 P0 列 |
| 归一化 | `features_normalized.csv` 已 z-score 归一化；`feature_stats.json` 匹配 |
| 缺失值 | `missing_features.csv` 记录所有 NaN 条目 |
| PCA 投影 | `projection_pca.json` 包含所有样本的 (x, y) |
| UMAP 投影 | `projection_umap.json` 包含所有样本的 (x, y) |
| 最近邻 | 所有检索模式的 JSON 文件完整 |

### 14.2 研究成功

| 标准 | 检查内容 |
|---|---|
| 空间连贯性（Spatial Coherence） | 同类声音是否在投影中聚集？ |
| 特征-标签相关性（Feature-Label Correlation） | centroid 值是否与亮度评分相关？ |
| 特征-标签相关性 | flatness/entropy 值是否与噪声/密集评分相关？ |
| 邻居质量（Neighbor Quality） | 至少 60% 的查询的 top-5 近邻是否感知上合理？ |
| 失败模式（Failure Modes） | 记录至少 5 个描述符失败或误导的案例 |

### 14.3 创作成功

| 标准 | 最低要求 |
|---|---|
| 有趣的邻居对 | 记录至少 5 个意外但有用的邻居对 |
| 可解释的特征轴 | 至少 2 个有清晰感知解释的特征轴 |
| 特征轨迹想法 | 至少 1 个初步特征轨迹作曲草图 |
| 浏览器需求 | 第一个特征空间浏览器的功能清单 |

---

## 15. 生成产物

### 15.1 数据产物

```text
data/processed/creative_features/01_baseline_features/
├── manifest.csv                        # corpus metadata
├── features_raw.csv                    # raw aggregated features
├── features_normalized.csv             # z-scored features
├── feature_stats.json                  # per-feature mean/std/min/max
├── missing_features.csv                # samples with NaN features
├── projection_pca.json                 # PCA 2D coordinates
├── projection_umap.json                # UMAP 2D coordinates
├── neighbors_all.json                  # kNN on all features
├── neighbors_timbre.json               # kNN on timbre features
├── neighbors_texture.json              # kNN on texture features
├── neighbors_temporal.json             # kNN on temporal features
├── correlation_matrix.csv              # feature-feature correlation
├── category_summary.csv                # per-category feature means
└── evaluation_notes.md                 # manual listening evaluation
```

### 15.2 代码产物

```text
experiments/creative_features/01_baseline_features/
├── README.md                           # usage and output documentation
├── make_manifest.py                    # scan data/raw → manifest.csv
├── extract_features.py                 # manifest → features_raw.csv
├── project_features.py                 # features → projections + neighbors
├── evaluate_features.py                # correlation + summary + report
└── schemas.py                          # column names, feature groups, paths
```

### 15.3 投影 JSON Schema

`projection_umap.json` (and `projection_pca.json`):

```json
[
  {
    "sample_id": "music_piano_001",
    "x": 1.234,
    "y": -0.567,
    "category": "music",
    "subcategory": "piano",
    "manual_tags": ["bright", "tonal", "sustained"],
    "file_path": "data/raw/small_corpus/music/piano_001.wav"
  }
]
```

---

## 16. 实现计划

### 16.1 `schemas.py`

Defines constants used across all scripts:

```python
SAMPLE_RATE = 22050
N_FFT = 2048
HOP_LENGTH = 512
N_MFCC = 13
N_CHROMA = 12
ROLL_PERCENT = 0.85
K_NEIGHBORS = 5

P0_FEATURE_COLUMNS = [
    'rms_mean', 'rms_std',
    'loudness_proxy_mean', 'loudness_proxy_std',
    'centroid_mean', 'centroid_std',
    'bandwidth_mean', 'bandwidth_std',
    'rolloff_mean', 'rolloff_std',
    'flatness_mean', 'flatness_std',
    'flux_mean', 'flux_std',
    'entropy_mean', 'entropy_std',
    'onset_density',
] + [f'mfcc_{i:02d}_{agg}' for i in range(1, 14) for agg in ['mean', 'std']]

TIMBRE_FEATURES = ['centroid_mean', 'centroid_std', 'bandwidth_mean', 'bandwidth_std',
                    'rolloff_mean', 'rolloff_std', 'flatness_mean', 'flatness_std'] + \
                   [f'mfcc_{i:02d}_{agg}' for i in range(1, 14) for agg in ['mean', 'std']]

TEXTURE_FEATURES = ['entropy_mean', 'entropy_std', 'flatness_mean', 'flatness_std',
                     'flux_mean', 'flux_std', 'onset_density']

TEMPORAL_FEATURES = ['onset_density', 'flux_mean', 'flux_std', 'rms_std']
```

### 16.2 `make_manifest.py`

Responsibilities:

- Scan `data/raw/small_corpus/` recursively for audio files (`.wav`, `.flac`, `.mp3`, `.ogg`)
- Extract metadata with `soundfile.info` or `librosa.get_duration`
- Derive `sample_id` from `{category}_{subcategory}_{sequence}`
- Output `manifest.csv`

```bash
uv run python experiments/creative_features/01_baseline_features/make_manifest.py \
  --input data/raw/small_corpus \
  --output data/processed/creative_features/01_baseline_features/manifest.csv
```

### 16.3 `extract_features.py`

Responsibilities:

- Read `manifest.csv`
- Load each audio file
- Create `raw_view` and `normalized_view`
- Extract all P0 features (and P1 if enabled)
- Aggregate frame-level → clip-level (mean, std)
- Output `features_raw.csv` and `feature_stats.json`

```bash
uv run python experiments/creative_features/01_baseline_features/extract_features.py \
  --manifest data/processed/creative_features/01_baseline_features/manifest.csv \
  --output-dir data/processed/creative_features/01_baseline_features \
  --enable-p1
```

### 16.4 `project_features.py`

Responsibilities:

- Read `features_raw.csv`
- Z-score normalize → `features_normalized.csv` + `feature_stats.json`
- Median impute NaN
- Run PCA and UMAP on three feature groups
- Run kNN retrieval on four feature groups
- Output projection JSONs and neighbor JSONs

```bash
uv run python experiments/creative_features/01_baseline_features/project_features.py \
  --features data/processed/creative_features/01_baseline_features/features_raw.csv \
  --output-dir data/processed/creative_features/01_baseline_features \
  --k 5
```

### 16.5 `evaluate_features.py`

Responsibilities:

- Read normalized features + manual tags
- Compute feature-feature correlation matrix
- Compute per-category feature summary
- Compute tag-feature correlation (if tags exist)
- Generate `evaluation_notes.md` template
- Output `correlation_matrix.csv` and `category_summary.csv`

```bash
uv run python experiments/creative_features/01_baseline_features/evaluate_features.py \
  --features data/processed/creative_features/01_baseline_features/features_normalized.csv \
  --output-dir data/processed/creative_features/01_baseline_features
```

---

## 17. 可复现性与版本管理(Reproducibility & Versioning)

### 17.1 确定性

| 项目 | 策略 |
|---|---|
| UMAP | `random_state=42` |
| PCA | 确定性(无随机状态) |
| KNN | 确定性(无随机状态) |
| 音频预处理 | 固定 `sr`, `n_fft`, `hop_length` |
| 特征计算 | 使用固定的 librosa 版本;记录 `pip freeze` 或 `uv pip compile` 输出 |

### 17.2 版本管理

- Each run should overwrite outputs in `data/processed/.../01_baseline_features/`
- If experimental parameters change significantly, create a new output directory: `01_baseline_features_v2/`
- Major changes (different corpus, different feature set, different normalization) require a new directory
- Minor changes (bug fixes, column renames) can overwrite in place

### 17.3 文档

`experiments/creative_features/01_baseline_features/README.md` must document:

- How to prepare the corpus
- How to run each script
- What outputs are generated
- What the feature columns mean
- Known limitations

---

## 18. 已知风险与失败模式(Known Risks & Failure Modes)

| 风险 | 影响 | 缓解措施 |
|---|---|---|
| 语料太小/不平衡 | 投影可能被离群值主导 | 目标为平衡的 60 条;后续增加 |
| 录音增益差异 | RMS / 响度代理可能反映录音而非声音 | 能量特征用原始视图,音色特征用归一化视图 |
| 片段中长静音 | 扭曲 RMS、起始点密度、熵 | 计算静音比率;可选裁剪并记录日志 |
| MFCC 主导投影 | MFCC 有 26 维 vs centroid 的 2 维 | 比较有/无 MFCC 的投影 |
| 非线性关系被遗漏 | PCA 可能无法捕捉感知结构 | 使用 UMAP 作为主要浏览投影 |
| 标签在评分者间不可比 | 感知标签是主观的 | 使用 1-5 量表;多评分者时计算评分者间一致性(Inter-Rater Agreement) |
| 特征高度相关 | centroid, bandwidth, rolloff, flatness 可能冗余 | 计算相关矩阵(Correlation Matrix);检查冗余 |
| 自然声不适合音高特征 | chroma, f0 对雨/风可能无意义 | 对非有调声音将音高特征标记为 NaN;在投影中处理 |

---

## 19. 完成标准

Phase 2 baseline is considered complete when:

- [ ] ~60-clip corpus is prepared in `data/raw/small_corpus/`
- [ ] `manifest.csv` is generated with all required fields
- [ ] All P0 features are extracted to `features_raw.csv`
- [ ] `features_normalized.csv` is generated with z-score normalization
- [ ] PCA and UMAP projections are generated for all three feature groups
- [ ] Nearest-neighbor retrieval is generated for all four retrieval modes
- [ ] At least one round of manual listening is completed
- [ ] `evaluation_notes.md` documents findings for RQ1-RQ4
- [ ] `correlation_matrix.csv` reveals feature relationships
- [ ] At least 3 interesting neighbor pairs and 2 interpretable feature axes are identified
- [ ] Failure modes are documented
- [ ] Clear requirements for the first `feature_space_browser.html` are written

---

## 20. 基线之后的下一步

Once Phase 2 baseline is complete:

| Step | Target | Description |
|---|---|---|
| Feature-space browser | `demos/creative_features/feature_space_browser.html` | Interactive 2D map with audio playback and neighbor exploration |
| Embedding comparison | `experiments/creative_features/02_embedding_comparison/` | Compare PANNs / AST / BYOL-A / AudioMAE / CLAP |
| Latent traversal | `experiments/creative_features/03_latent_traversal/` | Test DDSP / RAVE / EnCodec latent audibility |
| Creative mapping | `experiments/creative_features/04_creative_mapping/` | Feature trajectory → synthesis parameter prototype |

---

## 参考文献与内部来源

| Document | Relevance |
|---|---|
| [`02_feature_taxonomy.md`](02_feature_taxonomy.md) | Four-family taxonomy, evaluation axes, MVP feature set |
| [`00_research_plan.md`](00_research_plan.md) | Research questions, experimental roadmap |
| [`01_first_round_review.md`](01_first_round_review.md) | Candidate methods and core papers |
| [`../roadmap.md`](../roadmap.md) | Phase definitions |
| [`../architecture.md`](../architecture.md) | Directory layout and data flow |
| [`../../experiments/creative_features/01_baseline_features/`](../../experiments/creative_features/01_baseline_features/) | Target implementation directory |

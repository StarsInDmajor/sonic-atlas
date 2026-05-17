# Experiment Protocol: Baseline Feature Extraction and Feature-Space Browser

> **目标**：定义 Sonic Atlas Phase 2 第一条可运行实验链路——从小型声音语料中提取可解释的 psychoacoustic / handcrafted descriptors，生成 feature table、2D projection 和 nearest-neighbor retrieval，并通过人工听觉检查评估这些特征是否适合作为创作材料。

---

## 1. Purpose and Scope

本实验协议将 `02_feature_taxonomy.md` 中的四大家族分类体系转化为 Phase 2 的可执行实验方案。它的核心产出是一条完整的、可复现的、从音频文件到创作决策支持的链路：

```text
data/raw/small_corpus/
  → manifest.csv
  → audio preprocessing (mono, 22050 Hz, normalize)
  → baseline P0 feature extraction
  → features_raw.csv
  → z-score normalization
  → features_normalized.csv
  → PCA / UMAP 2D projection
  → projection_pca.json / projection_umap.json
  → nearest-neighbor retrieval
  → neighbors.json
  → manual listening + perceptual tags
  → evaluation_notes.md
```

**不包含**：

- PANNs / AST / BYOL-A / CLAP embedding（Phase 3）
- RAVE / DDSP / EnCodec latent traversal（Phase 4）
- 复杂心理声学 listening test（ABX / MUSHRA）
- 大规模数据集训练
- 生成式音频模型

---

## 2. Research Questions

Phase 2 baseline 实验围绕四个问题展开：

### RQ1. Baseline descriptors 能否形成直觉上合理的声音空间？

检查：

- 乐器声是否靠近乐器声；
- 自然纹理是否靠近自然纹理；
- transient-heavy sounds 是否分布在相近区域；
- bright / noisy / dense sounds 是否在局部聚集。

### RQ2. 哪些 handcrafted features 对创作最有解释力？

例如：

- centroid 是否确实对应 brightness？
- flatness / entropy 是否对应 noise / texture complexity？
- onset density 是否对应 rhythmic / granular density？
- MFCC 是否提升 timbre clustering？

### RQ3. Feature-space nearest neighbors 是否有创作价值？

不是只问"是否同类"，而是问：

- 是否能找到可替代素材？
- 是否能找到听感相近但语义不同的声音？
- 是否能产生创作联想？

### RQ4. Baseline descriptors 的局限在哪里？

需要记录：

- 哪些声音被错误聚类；
- 哪些听感差异没有被捕捉；
- 哪些 feature 受录音响度 / 噪声 / 长度影响过大；
- 哪些需要 embedding 或 sparse decomposition 补充。

---

## 3. Experiment Overview

| Aspect | Specification |
|---|---|
| Corpus | ~60 clips (20 music + 20 nature + 20 urban_object) |
| Clip duration | 3–10 s (target 5 s) |
| Audio format | WAV / FLAC preferred; MP3 accepted |
| Processing sample rate | 22050 Hz (for baseline descriptors) |
| Feature level | clip-level aggregations of frame-level features |
| Projection | PCA + UMAP |
| Retrieval | k-nearest neighbors (k=5–10) |
| Evaluation | manual listening + perceptual label + correlation analysis |
| Expected time | corpus preparation ~3 h, feature extraction ~1 h, evaluation ~2 h |

---

## 4. Corpus Design

### 4.1 Categories

| Category ID | Label | Examples | Research Focus |
|---|---|---|---|
| `music` | Musical / instrument sounds | piano, guitar, strings, flute, percussion, synth, voice | pitch, timbre, attack, sustain |
| `nature` | Natural environmental sounds | rain, water, wind, bird, fire, insect, thunder | texture, noise, event density |
| `urban_object` | Urban / object / mechanical sounds | footsteps, door, machine, traffic, metal, glass, typing | transient, material, gesture |

### 4.2 Target Distribution

```text
60 clips total
├── 20 music
├── 20 nature
└── 20 urban_object
```

Variety within each category is more important than volume. Each category should span a range along at least two perceptual axes (e.g. bright↔dark, tonal↔noisy, sparse↔dense).

### 4.3 Subcategory and Tag Examples

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

### 4.4 Clip Length Rules

| Rule | Value | Rationale |
|---|---|---|
| Target duration | 5 s | Enough for stable clip-level statistics |
| Minimum duration | 3 s | Too short → unstable spectral/temporal estimation |
| Maximum duration | 10 s | Too long → multiple events confound descriptors |
| Long source handling | Record `start_time` / `end_time` in manifest | Sub-clip extraction from longer recordings |

### 4.5 Data Sources

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

## 5. Data Layout

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

### 6.1 Required Fields

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

### 6.2 Sample ID Convention

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

## 7. Audio Preprocessing Protocol

### 7.1 Loading Rules

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

### 7.2 Two Analysis Views

To avoid confounding loudness with timbre, the protocol defines two views:

| View | Content | Use |
|---|---|---|
| **raw_view** | mono, 22050 Hz, un-normalized | RMS, loudness proxy, onset density, amplitude features |
| **normalized_view** | mono, 22050 Hz, peak-normalized (or RMS-normalized to target level) | centroid, bandwidth, rolloff, flatness, entropy, MFCC, chroma |

Rationale: If all features use normalized audio, loudness information is lost. If all features use raw audio, recording gain differences contaminate timbre comparisons.

### 7.3 Normalization Method

```text
normalized_view = audio / max(abs(audio))
```

Peak normalization is simple and stable for the first version. Corpus-level RMS normalization can be added later.

### 7.4 Silence Handling

| Rule | Behavior |
|---|---|
| Default | Do **not** aggressively trim |
| Optional trim | If leading/trailing silence exceeds 1 s and amplitude < -40 dB relative to peak, apply `librosa.effects.trim(top_db=40)` |
| Metadata | Record whether trim was applied in manifest notes |
| Silence ratio | Compute and store: `silence_ratio = frames_below_threshold / total_frames` |

Why not default trim:

- Silence may be part of the temporal structure;
- But excessive silence distorts RMS, onset density, and duration-dependent features.

### 7.5 Standard Analysis Parameters

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

## 8. Baseline Feature Set

### 8.1 P0 Features (Must Implement)

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

### 8.2 P1 Features (Implement After P0)

| Group | Feature | Library / Method | View | Columns |
|---|---|---|---|---|
| Temporal | Attack time | Envelope analysis: time from 10% to 90% of peak amplitude per onset | raw_view | `attack_time` |
| Harmonic | Chroma | `librosa.feature.chroma_stft` | normalized_view | `chroma_01_mean` ... `chroma_12_mean`, `chroma_01_std` ... `chroma_12_std` |
| Harmonic | F0 confidence | `librosa.pyin` or `librosa.yin` | normalized_view | `f0_confidence_mean`, `f0_std` (pitch stability) |
| Texture | Roughness estimate | Simplified: spectral irregularity or beating-based proxy | normalized_view | `roughness_mean`, `roughness_std` |

### 8.3 Deferred Features

| Feature | Reason to Defer |
|---|---|
| Full psychoacoustic loudness (Zwicker / ITU-R) | Needs model selection and calibration; RMS proxy sufficient for v0 |
| Rigorous roughness / sensory dissonance | Implementation choices affect validity; needs dedicated protocol |
| Inharmonicity | Requires reliable partial / f0 tracking |
| NMF templates | Better after baseline feature table exists; different experiment |
| PANNs / AST / BYOL-A / AudioMAE / CLAP | Phase 3 embedding comparison |
| RAVE / DDSP / EnCodec latents | Phase 4 latent traversal |

---

## 9. Feature Computation Specification

### 9.1 Frame-level to Clip-level Aggregation

All frame-level features are aggregated to clip-level using:

| Aggregation | Use |
|---|---|
| `mean` | Central tendency |
| `std` | Variability / texture stability |

Optional future aggregations (not in v0):

```text
median, p10, p90, min, max
```

### 9.2 Spectral Entropy Definition

```python
# Pseudo-code
S = np.abs(librosa.stft(y, n_fft=n_fft, hop_length=hop_length))
S_mean = S.mean(axis=1)                    # average magnitude spectrum
P = S_mean / (S_mean.sum() + 1e-10)       # normalize to probability
n_bins = len(P)
entropy = -np.sum(P * np.log2(P + 1e-10)) / np.log2(n_bins)
# Range: 0 (pure tone) to 1 (flat / white noise)
```

### 9.3 Onset Density Definition

```python
onset_frames = librosa.onset.onset_detect(y=y, sr=sr, hop_length=hop_length)
duration = len(y) / sr
onset_density = len(onset_frames) / duration  # events per second
```

### 9.4 Loudness Proxy Definition (v0)

```python
rms = librosa.feature.rms(y=y, hop_length=hop_length)[0]
loudness_proxy_db = 20 * np.log10(rms + 1e-10)
# Aggregate: mean, std of frame-level dB values
```

This is a rough proxy. It does not account for A-weighting, equal-loudness contours, or perceptual loudness models. The protocol explicitly marks this as a placeholder for future refinement.

---

## 10. Feature Aggregation and Normalization

### 10.1 Output Feature Table

Each row = one clip. Columns = aggregated features + metadata.

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

### 10.2 Corpus-level Normalization

Generate two files:

| File | Content |
|---|---|
| `features_raw.csv` | Raw aggregated feature values |
| `features_normalized.csv` | Z-scored: `z = (x - mean) / std` |

### 10.3 Feature Stats

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

### 10.4 Missing Value Handling

| Rule | Behavior |
|---|---|
| Inapplicable feature | Write `NaN` |
| Pre-projection imputation | Median imputation per feature column |
| Reporting | Generate `missing_features.csv` listing samples with NaN features |
| Deletion | Do **not** silently delete samples; keep them with NaN and flag |

---

## 11. Projection Protocol

### 11.1 Projection Methods

| Method | Role | Library |
|---|---|---|
| PCA | Deterministic linear baseline; axis interpretable as variance directions | `sklearn.decomposition.PCA` |
| UMAP | Nonlinear perceptual map; better for browsing | `umap.UMAP` |

t-SNE is optional. It is not the default because it is non-deterministic, sensitive to perplexity, and does not preserve global structure well.

### 11.2 UMAP Parameters (suggested v0)

```python
reducer = umap.UMAP(
    n_components=2,
    n_neighbors=15,
    min_dist=0.1,
    metric='euclidean',
    random_state=42
)
```

### 11.3 Feature Groups for Projection

Run projection on three feature subsets:

| Group | Features | Purpose |
|---|---|---|
| `all_features` | All normalized P0 features | General similarity map |
| `spectral_features` | centroid, bandwidth, rolloff, flatness, flux, entropy, MFCC | Timbre similarity |
| `temporal_texture` | onset_density, flux, entropy, flatness, rms_std | Texture / event similarity |

This helps answer: which feature group best organizes the corpus for creative navigation?

### 11.4 Distance Metric

Default: Euclidean distance on z-scored features.

Optional: cosine distance (useful when magnitude is less important than direction).

---

## 12. Similarity and Nearest-Neighbor Retrieval

### 12.1 Retrieval Modes

| Mode | Feature Set | Creative Use |
|---|---|---|
| `all_features` | All normalized P0 features | General "what sounds like this?" |
| `timbre_features` | centroid, bandwidth, rolloff, flatness, MFCC | "What has similar timbre?" |
| `texture_features` | entropy, flatness, flux, onset_density | "What has similar texture / density?" |
| `temporal_features` | onset_density, flux, rms_std | "What has similar event structure?" |

### 12.2 Retrieval Parameters

```text
k = 5  (default)
k = 10 (for evaluation)
distance_metric = euclidean
feature_set = normalized (z-scored)
```

### 12.3 Output Schema

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

### 12.4 Cross-Category Neighbor Analysis

After retrieval, compute:

- What fraction of top-5 neighbors are in the same category?
- What fraction share at least one perceptual tag?
- Which category boundaries are most / least respected?
- Which cross-category pairs are surprisingly close?

---

## 13. Manual Listening and Labeling Protocol

### 13.1 Perceptual Tags (per sample)

Each sample should be labeled with multi-label perceptual tags:

| Axis | Scale | Labels |
|---|---|---|
| Brightness | 1–5 | 1 = very dark, 5 = very bright |
| Tonal vs Noisy | 1–5 | 1 = pure tonal, 5 = pure noise |
| Density | 1–5 | 1 = very sparse, 5 = very dense |
| Attack sharpness | 1–5 | 1 = very soft onset, 5 = very sharp |
| Roughness | 1–5 | 1 = very smooth, 5 = very rough |
| Stability | 1–5 | 1 = very stable, 5 = very evolving |
| Organic vs Mechanical | 1–5 | 1 = very organic, 5 = very mechanical |

Plus categorical tags:

```text
percussive / sustained / textured / pitched / unpitched / harmonic / inharmonic
```

### 13.2 Listening Checklist (per sample)

| Question | Type | Notes |
|---|---|---|
| What is the main sound source? | free text | |
| Bright or dark? | 1–5 | |
| Tonal or noisy? | 1–5 | |
| Sparse or dense? | 1–5 | |
| Sharp or soft attack? | 1–5 | |
| Obvious pitch? | yes/no | |
| Obvious texture motion? | yes/no | |
| How could this be used in composition? | free text | |

### 13.3 Neighbor Evaluation (per query sample)

For each query sample, listen to top-5 neighbors and rate:

| Question | Type | Notes |
|---|---|---|
| Do they sound similar? | 1–5 (acoustic similarity) | |
| Do they mean similar things? | 1–5 (semantic similarity) | |
| Could you substitute one for another in a piece? | 1–5 (creative usefulness) | |
| What makes them similar / different? | free text | |
| Which neighbor is most surprising but useful? | free text | |

This directly maps to the three similarity types from `02_feature_taxonomy.md`:

```text
acoustic similarity ≠ semantic similarity ≠ creative usefulness
```

---

## 14. Evaluation Criteria

### 14.1 Technical Success

| Criterion | Pass Condition |
|---|---|
| Manifest completeness | All valid audio files listed with `sample_id` and `file_path` |
| Feature extraction | `features_raw.csv` has all P0 columns for all valid samples |
| Normalization | `features_normalized.csv` is z-scored; `feature_stats.json` matches |
| Missing values | `missing_features.csv` accounts for all NaN entries |
| PCA projection | `projection_pca.json` has all samples with (x, y) |
| UMAP projection | `projection_umap.json` has all samples with (x, y) |
| Nearest neighbors | All retrieval mode JSONs are complete |

### 14.2 Research Success

| Criterion | What to Check |
|---|---|
| Spatial coherence | Do same-category sounds cluster in projection? |
| Feature-label correlation | Do centroid values correlate with brightness ratings? |
| Feature-label correlation | Do flatness/entropy values correlate with noisy/dense ratings? |
| Neighbor quality | Are top-5 neighbors perceptually reasonable for at least 60% of queries? |
| Failure modes | Document at least 5 cases where descriptors fail or mislead |

### 14.3 Creative Success

| Criterion | Minimum |
|---|---|
| Interesting neighbor pairs | At least 5 surprising-but-useful neighbor pairs documented |
| Interpretable feature axes | At least 2 feature axes with clear perceptual interpretation |
| Feature trajectory idea | At least 1 preliminary feature trajectory composition sketch |
| Browser requirements | Clear list of what the first feature-space browser should do |

---

## 15. Generated Artifacts

### 15.1 Data Artifacts

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

### 15.2 Code Artifacts

```text
experiments/creative_features/01_baseline_features/
├── README.md                           # usage and output documentation
├── make_manifest.py                    # scan data/raw → manifest.csv
├── extract_features.py                 # manifest → features_raw.csv
├── project_features.py                 # features → projections + neighbors
├── evaluate_features.py                # correlation + summary + report
└── schemas.py                          # column names, feature groups, paths
```

### 15.3 Projection JSON Schema

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

## 16. Implementation Plan

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

## 17. Reproducibility and Versioning

### 17.1 Determinism

| Item | Policy |
|---|---|
| UMAP | `random_state=42` |
| PCA | Deterministic (no random state) |
| KNN | Deterministic (no random state) |
| Audio preprocessing | Fixed `sr`, `n_fft`, `hop_length` |
| Feature computation | Use fixed librosa version; record `pip freeze` or `uv pip compile` output |

### 17.2 Versioning

- Each run should overwrite outputs in `data/processed/.../01_baseline_features/`
- If experimental parameters change significantly, create a new output directory: `01_baseline_features_v2/`
- Major changes (different corpus, different feature set, different normalization) require a new directory
- Minor changes (bug fixes, column renames) can overwrite in place

### 17.3 Documentation

`experiments/creative_features/01_baseline_features/README.md` must document:

- How to prepare the corpus
- How to run each script
- What outputs are generated
- What the feature columns mean
- Known limitations

---

## 18. Known Risks and Failure Modes

| Risk | Impact | Mitigation |
|---|---|---|
| Corpus too small / unbalanced | Projections may be dominated by outliers | Aim for balanced 60 clips; increase later |
| Recording gain differences | RMS / loudness proxy may reflect recording, not sound | Use raw_view for energy, normalized_view for timbre |
| Long silence in clips | Distorts RMS, onset density, entropy | Compute silence ratio; optional trim with logging |
| MFCC dominates projection | MFCC has 26 dimensions vs 2 for centroid | Compare projection with and without MFCC |
| Nonlinear relationships missed | PCA may not capture perceptual structure | Use UMAP as primary browsing projection |
| Tags not comparable across raters | Perceptual labels are subjective | Use 1–5 scales; compute inter-rater agreement if multiple raters |
| Features correlate heavily | centroid, bandwidth, rolloff, flatness may be redundant | Compute correlation matrix; check for redundancy |
| Natural sounds poorly described by pitch features | chroma, f0 may be meaningless for rain/wind | Mark pitch features as NaN for non-pitched sounds; handle in projection |

---

## 19. Completion Criteria

Phase 2 baseline is considered complete when:

- [ ] ~60-clip corpus is prepared in `data/raw/small_corpus/`
- [ ] `manifest.csv` is generated with all required fields
- [ ] All P0 features are extracted to `features_raw.csv`
- [ ] `features_normalized.csv` is generated with z-score normalization
- [ ] PCA and UMAP projections are generated for all three feature groups
- [ ] Nearest-neighbor retrieval is generated for all four retrieval modes
- [ ] At least one round of manual listening is completed
- [ ] `evaluation_notes.md` documents findings for RQ1–RQ4
- [ ] `correlation_matrix.csv` reveals feature relationships
- [ ] At least 3 interesting neighbor pairs and 2 interpretable feature axes are identified
- [ ] Failure modes are documented
- [ ] Clear requirements for the first `feature_space_browser.html` are written

---

## 20. Next Steps After Baseline

Once Phase 2 baseline is complete:

| Step | Target | Description |
|---|---|---|
| Feature-space browser | `demos/creative_features/feature_space_browser.html` | Interactive 2D map with audio playback and neighbor exploration |
| Embedding comparison | `experiments/creative_features/02_embedding_comparison/` | Compare PANNs / AST / BYOL-A / AudioMAE / CLAP |
| Latent traversal | `experiments/creative_features/03_latent_traversal/` | Test DDSP / RAVE / EnCodec latent audibility |
| Creative mapping | `experiments/creative_features/04_creative_mapping/` | Feature trajectory → synthesis parameter prototype |

---

## References and Internal Sources

| Document | Relevance |
|---|---|
| [`02_feature_taxonomy.md`](02_feature_taxonomy.md) | Four-family taxonomy, evaluation axes, MVP feature set |
| [`00_research_plan.md`](00_research_plan.md) | Research questions, experimental roadmap |
| [`01_first_round_review.md`](01_first_round_review.md) | Candidate methods and core papers |
| [`../roadmap.md`](../roadmap.md) | Phase definitions |
| [`../architecture.md`](../architecture.md) | Directory layout and data flow |
| [`../../experiments/creative_features/01_baseline_features/`](../../experiments/creative_features/01_baseline_features/) | Target implementation directory |

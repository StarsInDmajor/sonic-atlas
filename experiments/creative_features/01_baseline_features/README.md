# 01_baseline_features

Phase 2 baseline feature extraction experiment for Sonic Atlas.

Extracts psychoacoustic / handcrafted descriptors from a small audio corpus,
generates 2D projections, and computes nearest-neighbor retrieval.

## Pipeline

```text
data/raw/small_corpus/
  → manifest.csv           (make_manifest.py)
  → features_raw.csv       (extract_features.py)
  → features_normalized.csv (project_features.py)
  → projection_pca.json    (project_features.py)
  → projection_umap.json   (project_features.py)
  → neighbors.json         (project_features.py)
  → correlation_matrix.csv (evaluate_features.py)
  → evaluation_notes.md    (evaluate_features.py)
```

## Prerequisites

Python environment with:

- librosa
- numpy
- scipy
- scikit-learn
- umap-learn
- pandas
- soundfile
- matplotlib (optional, for plotting)

All available in the project's direnv-managed nix environment.

## Corpus

The small corpus contains 55 audio clips:

| Category | Count | Subcategories | Source |
|---|---:|---|---|
| music | 15 | flute, clarinet, oboe, bassoon, alto_saxophone, accordion | TinySOL (CC-BY 4.0) |
| nature | 20 | rain, thunderstorm, sea_waves, crackling_fire, crickets, chirping_birds, water_drops, wind | ESC-50 (CC-BY-NC) |
| urban_object | 20 | clock_alarm, siren, car_horn, engine, train, door_wood_creaks, helicopter, typing, glass_breaking | ESC-50 (CC-BY-NC) |

### Data sources

- **ESC-50**: Environmental Sound Classification dataset, 2000 clips across 50 categories.
  GitHub: https://github.com/karolpiczak/ESC-50
- **TinySOL**: Isolated musical notes from 14 instruments, recorded at IRCAM.
  Zenodo: https://zenodo.org/records/3685331

## Pipeline

```text
# 1. Prepare corpus (download + organize)
prepare_corpus.py

# 2. Generate manifest
make_manifest.py

# 3. Extract features
extract_features.py

# 4. Project + retrieve
project_features.py

# 5. Evaluate
evaluate_features.py
```

## Step 1: Prepare Corpus

Download and organize audio samples from ESC-50 and TinySOL:

```bash
# Prerequisites: ESC-50 at /tmp/ESC-50, TinySOL at /tmp/TinySOL_full
# (see prepare_corpus.py for download instructions)

uv run python experiments/creative_features/01_baseline_features/prepare_corpus.py \
  --esc50 /tmp/ESC-50 \
  --tinysol /tmp/TinySOL_full
```

This copies selected samples to `data/raw/small_corpus/` and generates `manifest.csv`.

## Step 2: Generate Manifest

If corpus is already prepared, regenerate manifest:

```bash
uv run python experiments/creative_features/01_baseline_features/make_manifest.py \
  --input data/raw/small_corpus \
  --output data/processed/creative_features/01_baseline_features/manifest.csv
```

## Step 3: Extract Features

```bash
# P0 features only (default):
uv run python experiments/creative_features/01_baseline_features/extract_features.py \
  --manifest data/processed/creative_features/01_baseline_features/manifest.csv \
  --output-dir data/processed/creative_features/01_baseline_features

# With P1 features (attack_time, chroma, f0, roughness):
uv run python experiments/creative_features/01_baseline_features/extract_features.py \
  --manifest data/processed/creative_features/01_baseline_features/manifest.csv \
  --output-dir data/processed/creative_features/01_baseline_features \
  --enable-p1
```

## Step 4: Project and Retrieve

```bash
uv run python experiments/creative_features/01_baseline_features/project_features.py \
  --features data/processed/creative_features/01_baseline_features/features_raw.csv \
  --output-dir data/processed/creative_features/01_baseline_features \
  --k 5
```

Generates:

- `features_normalized.csv` — z-scored features
- `feature_stats.json` — per-feature mean/std/min/max
- `projection_pca.json` / `projection_umap.json` — 2D coordinates
- `projection_pca_{group}.json` / `projection_umap_{group}.json` — per feature group
- `neighbors.json` / `neighbors_{group}.json` — kNN retrieval

Feature groups: `all`, `timbre`, `texture`, `temporal`.

## Step 5: Evaluate

```bash
uv run python experiments/creative_features/01_baseline_features/evaluate_features.py \
  --features data/processed/creative_features/01_baseline_features/features_normalized.csv \
  --output-dir data/processed/creative_features/01_baseline_features
```

Generates:

- `correlation_matrix.csv` — feature-feature Pearson correlation
- `category_summary.csv` — per-category feature means/stds
- `tag_feature_summary.csv` — per-tag feature means (if manual_tags exist)
- `evaluation_notes.md` — template for RQ1–RQ4 evaluation

## Feature Set

### P0 (Must Implement)

| Group | Features |
|---|---|
| Energy | rms_mean/std, loudness_proxy_mean/std |
| Spectral | centroid_mean/std, bandwidth_mean/std, rolloff_mean/std, flatness_mean/std, flux_mean/std, entropy_mean/std |
| Temporal | onset_density |
| Cepstral | mfcc_01_mean/std ... mfcc_13_mean/std |

### P1 (Optional)

| Group | Features |
|---|---|
| Temporal | attack_time |
| Harmonic | chroma_01_mean/std ... chroma_12_mean/std, f0_confidence_mean, f0_std |
| Texture | roughness_mean/std |

## Output Files

| File | Description |
|---|---|
| `manifest.csv` | Corpus metadata: sample_id, file_path, category, subcategory, duration, tags |
| `features_raw.csv` | Raw aggregated feature values |
| `features_normalized.csv` | Z-scored features |
| `feature_stats.json` | Per-feature statistics (mean, std, min, max, nan_count) |
| `missing_features.csv` | Samples with NaN feature values |
| `projection_pca.json` | PCA 2D projection (all features) |
| `projection_umap.json` | UMAP 2D projection (all features) |
| `projection_{method}_{group}.json` | Projection per feature group |
| `neighbors.json` | kNN retrieval (all features) |
| `neighbors_{group}.json` | kNN retrieval per feature group |
| `correlation_matrix.csv` | Feature-feature correlation |
| `category_summary.csv` | Per-category feature means |
| `tag_feature_summary.csv` | Per-tag feature means |
| `evaluation_notes.md` | Evaluation template |

## References

- [Feature Taxonomy](../../../docs/literature/02_feature_taxonomy.md)
- [Experiment Protocol](../../../docs/literature/03_experiment_protocol.md)
- [Research Plan](../../../docs/literature/00_research_plan.md)

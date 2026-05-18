# Data Sources

Sound corpus acquisition guide for Sonic Atlas. The full corpus contains ~54,000 audio clips (16 GB) from six sources. Audio files are **not** tracked in Git — use this guide to download and rebuild the corpus.

## Quick Start

```bash
# 1. Download all sources into a staging directory
mkdir -p /tmp/sonic-atlas-sources

# 2. Build the corpus
uv run python experiments/build_corpus.py \
  --output data/corpus \
  --source-dir /tmp/sonic-atlas-sources \
  --sources ESC-50 TinySOL Philharmonia FSD50K LibriSpeech synthetic
```

## Sources

### 1. FSD50K

| Field | Value |
|---|---|
| Content | 51,197 Freesound clips, human-annotated, 200 categories |
| Used in corpus | 43,515 clips |
| License | CC-BY |
| Paper | Eduardo Fonseca et al., "FSD50K: An Open Dataset of Human-Labeled Sound Events" (arXiv 2010.14761) |

**Download**

1. Visit <https://zenodo.org/record/4060432>
2. Download `FSD50K.dev_audio.zip` and `FSD50K.eval_audio.zip`
3. Download `FSD50K.ground_truth.zip` (contains labels)
4. Extract so the directory structure is:
   ```
   /tmp/sonic-atlas-sources/FSD50K/
   ├── FSD50K.dev_audio/    # 40,966 clips
   ├── FSD50K.eval_audio/   # 10,231 clips
   └── ground_truth/        # labels
   ```

> **Note**: Requires Zenodo account. Total ~23 GB compressed.

### 2. Philharmonia Orchestra

| Field | Value |
|---|---|
| Content | Professional orchestral single-note samples (brass, strings, guitar) |
| Used in corpus | 6,669 clips |
| License | Creative Commons (CC) |
| Source | Philharmonia Orchestra, London |

**Download**

```bash
# The samples are available as individual MP3/WAV files from:
# https://www.philharmonia.co.uk/explore/sound-samples

# Recommended: use a batch downloader or mirror
mkdir -p /tmp/sonic-atlas-sources/philharmonia
# Expected directory structure:
# philharmonia/
# ├── Brass/Brass/{trumpet,french horn,trombone,tuba}/
# ├── Strings/Strings/{violin,viola,cello,double bass,guitar}/
# └── ...
```

1. Visit <https://www.philharmonia.co.uk/explore/sound-samples>
2. Navigate to each instrument page
3. Download all sample MP3 files per instrument
4. Arrange into the directory structure shown above

### 3. TinySOL

| Field | Value |
|---|---|
| Content | 2,940 isolated orchestral instrument notes (winds + accordion) |
| Used in corpus | 752 clips |
| License | CC-BY 4.0 |
| Paper | Gómez-García et al., "TinySOL: A Tiny Dataset of Solo Instrument Notes" (ISMIR 2019 Late-Breaking Demo) |

**Download**

1. Visit <https://zenodo.org/record/3685367>
2. Download `TinySOL.tar.gz` (~500 MB)
3. Extract to:
   ```
   /tmp/sonic-atlas-sources/TinySOL2020/
   ├── Flute/
   ├── Clarinet_Bb/
   ├── Oboe/
   ├── Bassoon/
   ├── Sax_Alto/
   └── Accordion/
   ```

### 4. LibriSpeech

| Field | Value |
|---|---|
| Content | Read English speech from audiobooks |
| Used in corpus | 2,703 clips (clean subset) |
| License | CC-BY 4.0 |
| Paper | Vassil Panayotov et al., "Librispeech: An ASR Corpus Based on Public Domain Audio Books" (ICASSP 2015) |

**Download**

```bash
cd /tmp/sonic-atlas-sources

# Download the clean training set (100-hour subset is sufficient)
wget https://www.openslr.org/resources/12/train-clean-100.tar.gz
tar xzf train-clean-100.tar.gz

# Expected structure:
# LibriSpeech/
# ├── train-clean-100/
# │   └── {speaker_id}/{chapter_id}/*.flac
```

Source: <https://www.openslr.org/12>

### 5. ESC-50

| Field | Value |
|---|---|
| Content | 2,000 environmental sound clips, 50 categories |
| Used in corpus | 653 clips |
| License | CC-BY-NC (non-commercial) |
| Paper | Karol J. Piczak, "ESC: Dataset for Environmental Sound Classification" (ACM MM 2015) |

**Download**

1. Visit <https://github.com/karolpiczak/ESC-50>
2. Download the dataset:
   ```bash
   cd /tmp/sonic-atlas-sources
   wget https://github.com/karoldvl/ESC-50/archive/master.zip
   unzip master.zip
   mv ESC-50-master ESC-50
   ```
3. Expected structure:
   ```
   ESC-50/
   ├── audio/       # 2,000 WAV files
   └── meta/        # esc50.csv
   ```

### 6. Synthetic

| Field | Value |
|---|---|
| Content | 24 generated audio files (noise + sine sweeps) |
| Used in corpus | 24 clips |
| License | Public Domain |

**No download needed** — `build_corpus.py` generates these automatically when `--sources synthetic` is specified:

- `texture/noise/` — 15 files: white, pink, brown noise (5 variants each)
- `texture/tone/` — 9 files: sine sweep C2→C7 at 3 speeds × 3 durations

## Partial Rebuild

To rebuild only specific sources:

```bash
uv run python experiments/build_corpus.py \
  --output data/corpus \
  --source-dir /tmp/sonic-atlas-sources \
  --sources ESC-50 TinySOL
```

The script will skip sources not present in `--source-dir` with a warning.

## License Summary

| Source | License | Commercial use |
|---|---|---|
| FSD50K | CC-BY | ✅ (with attribution) |
| Philharmonia | CC | ✅ |
| TinySOL | CC-BY 4.0 | ✅ (with attribution) |
| LibriSpeech | CC-BY 4.0 | ✅ (with attribution) |
| ESC-50 | CC-BY-NC | ❌ |
| Synthetic | Public Domain | ✅ |

> **Note**: 653 ESC-50 clips carry a CC-BY-NC restriction. Remove or replace them for commercial applications.

## Rebuilding on Another Machine

The complete corpus is maintained on `betelgeuse`:

```bash
rsync -az betelgeuse:~/sonic-atlas/data/corpus/ data/corpus/
```

Or rebuild from scratch using the steps above — the manifests (`data/corpus_fsd50k/manifest.csv`, etc.) in this repo provide the full index.

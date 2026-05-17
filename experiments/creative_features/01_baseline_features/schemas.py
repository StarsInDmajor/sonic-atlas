"""
Sonic Atlas — Baseline Feature Extraction
==========================================
Unified schemas, constants, and column definitions used across all scripts.
"""

from pathlib import Path

# ── Audio Processing Parameters ──────────────────────────────────────────────
SAMPLE_RATE = 22050
N_FFT = 2048
HOP_LENGTH = 512
WINDOW = "hann"
N_MELS = 128
N_MFCC = 13
N_CHROMA = 12
ROLL_PERCENT = 0.85
FMIN = 0
FMAX = SAMPLE_RATE // 2  # 11025

# ── Retrieval ────────────────────────────────────────────────────────────────
K_NEIGHBORS = 5

# ── File Extensions ──────────────────────────────────────────────────────────
AUDIO_EXTENSIONS = {".wav", ".flac", ".mp3", ".ogg", ".aiff", ".aif"}

# ── Category IDs ─────────────────────────────────────────────────────────────
CATEGORIES = ("music", "nature", "urban_object")

# ── Paths (relative to repo root) ────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_RAW_DIR = REPO_ROOT / "data" / "raw" / "small_corpus"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "data" / "processed" / "creative_features" / "01_baseline_features"

# ── Manifest Columns ─────────────────────────────────────────────────────────
MANIFEST_COLUMNS = [
    "sample_id",
    "file_path",
    "category",
    "subcategory",
    "duration",
    "sample_rate",
    "channels",
    "start_time",
    "end_time",
    "source",
    "license",
    "manual_tags",
    "description",
    "notes",
]

MANIFEST_REQUIRED = ["sample_id", "file_path", "category"]

# ── P0 Feature Columns (Must Implement) ─────────────────────────────────────
P0_SCALAR_FEATURES = [
    "rms_mean",
    "rms_std",
    "loudness_proxy_mean",
    "loudness_proxy_std",
    "centroid_mean",
    "centroid_std",
    "bandwidth_mean",
    "bandwidth_std",
    "rolloff_mean",
    "rolloff_std",
    "flatness_mean",
    "flatness_std",
    "flux_mean",
    "flux_std",
    "entropy_mean",
    "entropy_std",
    "onset_density",
]

P0_MFCC_FEATURES = [
    f"mfcc_{i:02d}_{agg}" for i in range(1, N_MFCC + 1) for agg in ("mean", "std")
]

P0_FEATURE_COLUMNS = P0_SCALAR_FEATURES + P0_MFCC_FEATURES

# ── P1 Feature Columns (Implement After P0) ─────────────────────────────────
P1_SCALAR_FEATURES = [
    "attack_time",
    "f0_confidence_mean",
    "f0_std",
    "roughness_mean",
    "roughness_std",
]

P1_CHROMA_FEATURES = [
    f"chroma_{i:02d}_{agg}" for i in range(1, N_CHROMA + 1) for agg in ("mean", "std")
]

P1_FEATURE_COLUMNS = P1_SCALAR_FEATURES + P1_CHROMA_FEATURES

# ── All Feature Columns ─────────────────────────────────────────────────────
ALL_FEATURE_COLUMNS = P0_FEATURE_COLUMNS + P1_FEATURE_COLUMNS

# ── Feature Groups (for projection / retrieval) ─────────────────────────────
TIMBRE_FEATURES = [
    "centroid_mean",
    "centroid_std",
    "bandwidth_mean",
    "bandwidth_std",
    "rolloff_mean",
    "rolloff_std",
    "flatness_mean",
    "flatness_std",
] + [f"mfcc_{i:02d}_{agg}" for i in range(1, N_MFCC + 1) for agg in ("mean", "std")]

TEXTURE_FEATURES = [
    "entropy_mean",
    "entropy_std",
    "flatness_mean",
    "flatness_std",
    "flux_mean",
    "flux_std",
    "onset_density",
]

TEMPORAL_FEATURES = [
    "onset_density",
    "flux_mean",
    "flux_std",
    "rms_std",
]

# Mapping from mode name to column list
FEATURE_GROUPS = {
    "all": P0_FEATURE_COLUMNS,
    "timbre": TIMBRE_FEATURES,
    "texture": TEXTURE_FEATURES,
    "temporal": TEMPORAL_FEATURES,
}

# ── Metadata Columns (non-feature, carried through for joins) ────────────────
METADATA_COLUMNS = [
    "sample_id",
    "file_path",
    "category",
    "subcategory",
    "manual_tags",
    "description",
    "duration",
]

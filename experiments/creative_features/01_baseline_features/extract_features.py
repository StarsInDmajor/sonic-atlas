"""
extract_features.py
===================
Read manifest.csv, extract P0 (and optional P1) features from each audio file.

Usage:
    uv run python experiments/creative_features/01_baseline_features/extract_features.py \
        --manifest data/processed/creative_features/01_baseline_features/manifest.csv \
        --output-dir data/processed/creative_features/01_baseline_features

    # With P1 features enabled:
    uv run python experiments/creative_features/01_baseline_features/extract_features.py \
        --manifest data/processed/creative_features/01_baseline_features/manifest.csv \
        --output-dir data/processed/creative_features/01_baseline_features \
        --enable-p1
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import librosa
import numpy as np
import pandas as pd

from schemas import (
    ALL_FEATURE_COLUMNS,
    DEFAULT_OUTPUT_DIR,
    FMAX,
    FMIN,
    HOP_LENGTH,
    N_CHROMA,
    N_FFT,
    N_MELS,
    N_MFCC,
    P0_FEATURE_COLUMNS,
    P1_FEATURE_COLUMNS,
    ROLL_PERCENT,
    SAMPLE_RATE,
    WINDOW,
)


# ── Helper: Two Analysis Views ───────────────────────────────────────────────


def load_audio_views(filepath: str, sr: int = SAMPLE_RATE) -> tuple[np.ndarray, np.ndarray]:
    """
    Load audio and return two views:
    - raw_view: mono, resampled, un-normalized
    - normalized_view: mono, resampled, peak-normalized
    """
    y, _ = librosa.load(filepath, sr=sr, mono=True)

    if len(y) == 0:
        raise ValueError(f"Empty audio: {filepath}")

    raw_view = y.copy()

    peak = np.max(np.abs(y))
    if peak > 0:
        normalized_view = y / peak
    else:
        normalized_view = y.copy()

    return raw_view, normalized_view


# ── Feature Extraction Functions ─────────────────────────────────────────────


def extract_rms(y: np.ndarray, sr: int, hop_length: int) -> tuple[float, float]:
    """RMS energy (raw_view)."""
    rms = librosa.feature.rms(y=y, hop_length=hop_length)[0]
    return float(np.mean(rms)), float(np.std(rms))


def extract_loudness_proxy(y: np.ndarray, sr: int, hop_length: int) -> tuple[float, float]:
    """Loudness proxy in dB (raw_view)."""
    rms = librosa.feature.rms(y=y, hop_length=hop_length)[0]
    rms_db = 20.0 * np.log10(rms + 1e-10)
    return float(np.mean(rms_db)), float(np.std(rms_db))


def extract_centroid(y: np.ndarray, sr: int, n_fft: int, hop_length: int) -> tuple[float, float]:
    """Spectral centroid in Hz (normalized_view)."""
    centroid = librosa.feature.spectral_centroid(
        y=y, sr=sr, n_fft=n_fft, hop_length=hop_length
    )[0]
    return float(np.mean(centroid)), float(np.std(centroid))


def extract_bandwidth(y: np.ndarray, sr: int, n_fft: int, hop_length: int) -> tuple[float, float]:
    """Spectral bandwidth in Hz (normalized_view)."""
    bw = librosa.feature.spectral_bandwidth(
        y=y, sr=sr, n_fft=n_fft, hop_length=hop_length
    )[0]
    return float(np.mean(bw)), float(np.std(bw))


def extract_rolloff(y: np.ndarray, sr: int, n_fft: int, hop_length: int) -> tuple[float, float]:
    """Spectral rolloff in Hz (normalized_view)."""
    rolloff = librosa.feature.spectral_rolloff(
        y=y, sr=sr, n_fft=n_fft, hop_length=hop_length, roll_percent=ROLL_PERCENT
    )[0]
    return float(np.mean(rolloff)), float(np.std(rolloff))


def extract_flatness(y: np.ndarray, sr: int, n_fft: int, hop_length: int) -> tuple[float, float]:
    """Spectral flatness (normalized_view)."""
    flatness = librosa.feature.spectral_flatness(
        y=y, n_fft=n_fft, hop_length=hop_length
    )[0]
    return float(np.mean(flatness)), float(np.std(flatness))


def extract_flux(y: np.ndarray, sr: int, n_fft: int, hop_length: int) -> tuple[float, float]:
    """Spectral flux via onset strength (normalized_view)."""
    flux = librosa.onset.onset_strength(
        y=y, sr=sr, n_fft=n_fft, hop_length=hop_length
    )
    return float(np.mean(flux)), float(np.std(flux))


def extract_entropy(y: np.ndarray, sr: int, n_fft: int, hop_length: int) -> tuple[float, float]:
    """
    Spectral entropy (normalized_view).
    Entropy of the mean magnitude spectrum, normalized to [0, 1].
    """
    S = np.abs(librosa.stft(y, n_fft=n_fft, hop_length=hop_length))
    S_mean = S.mean(axis=1)

    total = S_mean.sum()
    if total < 1e-10:
        return 0.0, 0.0

    P = S_mean / total
    n_bins = len(P)
    entropy = -np.sum(P * np.log2(P + 1e-10)) / np.log2(n_bins)
    return float(entropy), 0.0  # entropy is a single value per clip


def extract_onset_density(y: np.ndarray, sr: int, hop_length: int) -> float:
    """Onset density: events per second (normalized_view)."""
    onsets = librosa.onset.onset_detect(y=y, sr=sr, hop_length=hop_length, units="frames")
    duration = len(y) / sr
    if duration <= 0:
        return 0.0
    return float(len(onsets) / duration)


def extract_mfcc(y: np.ndarray, sr: int, n_fft: int, hop_length: int, n_mfcc: int) -> list[float]:
    """MFCC mean and std (normalized_view). Returns 2 * n_mfcc values."""
    mfcc = librosa.feature.mfcc(
        y=y, sr=sr, n_fft=n_fft, hop_length=hop_length, n_mfcc=n_mfcc
    )
    result = []
    for i in range(n_mfcc):
        result.append(float(np.mean(mfcc[i])))
        result.append(float(np.std(mfcc[i])))
    return result


# ── P1 Features ──────────────────────────────────────────────────────────────


def extract_attack_time(y: np.ndarray, sr: int, hop_length: int) -> float:
    """
    Estimate attack time: time from 10% to 90% of peak amplitude.
    Returns median attack time across detected onsets.
    """
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr, hop_length=hop_length, units="frames")
    if len(onset_frames) == 0:
        return np.nan

    rms = librosa.feature.rms(y=y, hop_length=hop_length)[0]
    if len(rms) == 0:
        return np.nan

    attack_times = []
    for frame in onset_frames:
        if frame >= len(rms):
            continue
        peak_val = rms[frame]
        threshold_10 = 0.1 * peak_val
        threshold_90 = 0.9 * peak_val

        # Search backward for 10% point
        start_frame = frame
        for f in range(frame, -1, -1):
            if rms[f] <= threshold_10:
                start_frame = f
                break

        # Search forward for 90% point (should be at or near onset)
        end_frame = frame
        for f in range(frame, min(len(rms), frame + 20)):
            if rms[f] >= threshold_90:
                end_frame = f
                break

        dt = (end_frame - start_frame) * hop_length / sr
        if dt > 0:
            attack_times.append(dt)

    if not attack_times:
        return np.nan

    return float(np.median(attack_times))


def extract_f0_confidence(y: np.ndarray, sr: int, hop_length: int) -> tuple[float, float]:
    """F0 confidence and pitch stability via pyin (normalized_view)."""
    try:
        f0, voiced_flag, voiced_prob = librosa.pyin(
            y, fmin=librosa.note_to_hz("C2"), fmax=librosa.note_to_hz("C7"),
            sr=sr, hop_length=hop_length
        )
    except Exception:
        return np.nan, np.nan

    # Filter out unvoiced frames
    valid = ~np.isnan(f0)
    if valid.sum() < 3:
        return 0.0, np.nan

    f0_valid = f0[valid]
    confidence = float(np.mean(voiced_prob[valid]))
    stability = float(np.std(f0_valid) / (np.mean(f0_valid) + 1e-10))  # CoV
    return confidence, stability


def extract_chroma(y: np.ndarray, sr: int, n_fft: int, hop_length: int) -> list[float]:
    """Chroma features mean and std (normalized_view). Returns 2 * 12 values."""
    chroma = librosa.feature.chroma_stft(
        y=y, sr=sr, n_fft=n_fft, hop_length=hop_length
    )
    result = []
    for i in range(N_CHROMA):
        result.append(float(np.mean(chroma[i])))
        result.append(float(np.std(chroma[i])))
    return result


def extract_roughness(y: np.ndarray, sr: int, n_fft: int, hop_length: int) -> tuple[float, float]:
    """
    Simplified roughness estimate via spectral irregularity.
    Defined as: sum(|S[k] - 0.5*(S[k-1] + S[k+1])|) / sum(S[k])
    This is a proxy, not a psychoacoustic roughness model.
    """
    S = np.abs(librosa.stft(y, n_fft=n_fft, hop_length=hop_length))
    S_mean = S.mean(axis=1)

    if S_mean.sum() < 1e-10:
        return 0.0, 0.0

    irregularity = np.zeros(len(S_mean))
    for k in range(1, len(S_mean) - 1):
        irregularity[k] = abs(S_mean[k] - 0.5 * (S_mean[k - 1] + S_mean[k + 1]))

    ratio = float(np.sum(irregularity) / (np.sum(S_mean) + 1e-10))
    return ratio, 0.0


# ── Main Extraction ──────────────────────────────────────────────────────────


def extract_features_for_clip(
    filepath: str,
    enable_p1: bool = False,
) -> dict[str, float]:
    """Extract all P0 (and optionally P1) features for a single audio file."""
    raw_view, normalized_view = load_audio_views(filepath, sr=SAMPLE_RATE)

    features: dict[str, float] = {}

    # ── P0 Features ──────────────────────────────────────────────────────
    # Energy (raw_view)
    features["rms_mean"], features["rms_std"] = extract_rms(raw_view, SAMPLE_RATE, HOP_LENGTH)
    features["loudness_proxy_mean"], features["loudness_proxy_std"] = extract_loudness_proxy(
        raw_view, SAMPLE_RATE, HOP_LENGTH
    )

    # Spectral shape (normalized_view)
    features["centroid_mean"], features["centroid_std"] = extract_centroid(
        normalized_view, SAMPLE_RATE, N_FFT, HOP_LENGTH
    )
    features["bandwidth_mean"], features["bandwidth_std"] = extract_bandwidth(
        normalized_view, SAMPLE_RATE, N_FFT, HOP_LENGTH
    )
    features["rolloff_mean"], features["rolloff_std"] = extract_rolloff(
        normalized_view, SAMPLE_RATE, N_FFT, HOP_LENGTH
    )
    features["flatness_mean"], features["flatness_std"] = extract_flatness(
        normalized_view, SAMPLE_RATE, N_FFT, HOP_LENGTH
    )
    features["flux_mean"], features["flux_std"] = extract_flux(
        normalized_view, SAMPLE_RATE, N_FFT, HOP_LENGTH
    )
    features["entropy_mean"], features["entropy_std"] = extract_entropy(
        normalized_view, SAMPLE_RATE, N_FFT, HOP_LENGTH
    )

    # Temporal (normalized_view)
    features["onset_density"] = extract_onset_density(normalized_view, SAMPLE_RATE, HOP_LENGTH)

    # Cepstral (normalized_view)
    mfcc_values = extract_mfcc(normalized_view, SAMPLE_RATE, N_FFT, HOP_LENGTH, N_MFCC)
    for i, val in enumerate(mfcc_values):
        agg = "mean" if i % 2 == 0 else "std"
        col = f"mfcc_{(i // 2) + 1:02d}_{agg}"
        features[col] = val

    # ── P1 Features ──────────────────────────────────────────────────────
    if enable_p1:
        features["attack_time"] = extract_attack_time(raw_view, SAMPLE_RATE, HOP_LENGTH)

        chroma_values = extract_chroma(normalized_view, SAMPLE_RATE, N_FFT, HOP_LENGTH)
        for i, val in enumerate(chroma_values):
            agg = "mean" if i % 2 == 0 else "std"
            col = f"chroma_{(i // 2) + 1:02d}_{agg}"
            features[col] = val

        f0_conf, f0_stab = extract_f0_confidence(normalized_view, SAMPLE_RATE, HOP_LENGTH)
        features["f0_confidence_mean"] = f0_conf
        features["f0_std"] = f0_stab

        rough_mean, rough_std = extract_roughness(normalized_view, SAMPLE_RATE, N_FFT, HOP_LENGTH)
        features["roughness_mean"] = rough_mean
        features["roughness_std"] = rough_std

    return features


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract baseline audio features from manifest")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_OUTPUT_DIR / "manifest.csv")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--enable-p1", action="store_true", help="Also extract P1 features")
    args = parser.parse_args()

    if not args.manifest.exists():
        print(f"ERROR: manifest not found: {args.manifest}", file=sys.stderr)
        sys.exit(1)

    # Determine feature columns
    feature_columns = P0_FEATURE_COLUMNS if not args.enable_p1 else P0_FEATURE_COLUMNS + P1_FEATURE_COLUMNS

    # Read manifest
    manifest = pd.read_csv(args.manifest)
    print(f"Loaded manifest with {len(manifest)} entries")

    # Extract features
    results: list[dict] = []
    errors: list[str] = []
    t0 = time.time()

    for idx, row in manifest.iterrows():
        sample_id = row["sample_id"]
        file_path = row["file_path"]

        # Resolve path relative to repo root
        from schemas import REPO_ROOT

        filepath = REPO_ROOT / file_path
        if not filepath.exists():
            print(f"  SKIP {sample_id}: file not found ({filepath})")
            errors.append(sample_id)
            continue

        try:
            features = extract_features_for_clip(str(filepath), enable_p1=args.enable_p1)
            result = {
                "sample_id": sample_id,
                "file_path": file_path,
                "category": row.get("category", ""),
                "subcategory": row.get("subcategory", ""),
                "duration": row.get("duration", ""),
                "manual_tags": row.get("manual_tags", ""),
                "description": row.get("description", ""),
            }
            result.update(features)
            results.append(result)
            elapsed = time.time() - t0
            print(f"  [{idx + 1}/{len(manifest)}] {sample_id} OK  ({elapsed:.1f}s)")
        except Exception as e:
            print(f"  [{idx + 1}/{len(manifest)}] {sample_id} ERROR: {e}", file=sys.stderr)
            errors.append(sample_id)

    if not results:
        print("ERROR: no features extracted.", file=sys.stderr)
        sys.exit(1)

    # Build DataFrame
    df = pd.DataFrame(results)

    # Ensure all feature columns exist (fill missing with NaN)
    for col in feature_columns:
        if col not in df.columns:
            df[col] = np.nan

    # Reorder columns: metadata first, then features in defined order
    metadata_cols = ["sample_id", "file_path", "category", "subcategory", "duration", "manual_tags", "description"]
    ordered_cols = [c for c in metadata_cols if c in df.columns] + feature_columns
    df = df[[c for c in ordered_cols if c in df.columns]]

    # Write features_raw.csv
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output_path = args.output_dir / "features_raw.csv"
    df.to_csv(output_path, index=False, float_format="%.6f")
    print(f"\nWrote {len(df)} rows × {len(df.columns)} columns to {output_path}")

    # Compute and save feature_stats.json
    feature_cols_in_df = [c for c in feature_columns if c in df.columns]
    stats = {}
    for col in feature_cols_in_df:
        vals = pd.to_numeric(df[col], errors="coerce")
        stats[col] = {
            "mean": float(vals.mean()) if not vals.isna().all() else None,
            "std": float(vals.std()) if not vals.isna().all() else None,
            "min": float(vals.min()) if not vals.isna().all() else None,
            "max": float(vals.max()) if not vals.isna().all() else None,
            "nan_count": int(vals.isna().sum()),
        }

    stats_path = args.output_dir / "feature_stats.json"
    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=2)
    print(f"Wrote feature stats to {stats_path}")

    # Report missing features
    nan_cols = [col for col in feature_cols_in_df if df[col].isna().any()]
    if nan_cols:
        missing_path = args.output_dir / "missing_features.csv"
        missing_rows = []
        for _, r in df.iterrows():
            nan_feats = [col for col in feature_cols_in_df if pd.isna(r.get(col))]
            if nan_feats:
                missing_rows.append({"sample_id": r["sample_id"], "missing_features": ";".join(nan_feats)})
        pd.DataFrame(missing_rows).to_csv(missing_path, index=False)
        print(f"WARNING: {len(nan_cols)} feature columns have NaN values → {missing_path}")

    # Summary
    elapsed_total = time.time() - t0
    print(f"\nDone in {elapsed_total:.1f}s")
    print(f"  Extracted: {len(results)}")
    print(f"  Errors:    {len(errors)}")
    if errors:
        print(f"  Failed IDs: {', '.join(errors)}")


if __name__ == "__main__":
    main()

"""
project_features.py
===================
Read features_raw.csv, normalize, project (PCA + UMAP), and compute kNN retrieval.

Usage:
    uv run python experiments/creative_features/01_baseline_features/project_features.py \
        --features data/processed/creative_features/01_baseline_features/features_raw.csv \
        --output-dir data/processed/creative_features/01_baseline_features \
        --k 5
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.neighbors import NearestNeighbors

from schemas import (
    DEFAULT_OUTPUT_DIR,
    FEATURE_GROUPS,
    K_NEIGHBORS,
    METADATA_COLUMNS,
    P0_FEATURE_COLUMNS,
)


def z_score_normalize(
    df: pd.DataFrame, feature_columns: list[str]
) -> tuple[pd.DataFrame, dict]:
    """Z-score normalize feature columns. Returns normalized df and stats."""
    stats = {}
    df_norm = df.copy()

    for col in feature_columns:
        if col not in df.columns:
            continue
        vals = pd.to_numeric(df[col], errors="coerce")
        mean = float(vals.mean())
        std = float(vals.std())
        if std < 1e-10:
            # Constant feature — zero it out to avoid division issues
            df_norm[col] = 0.0
            stats[col] = {"mean": mean, "std": 0.0, "min": float(vals.min()), "max": float(vals.max())}
        else:
            df_norm[col] = (vals - mean) / std
            stats[col] = {"mean": mean, "std": std, "min": float(vals.min()), "max": float(vals.max())}

    return df_norm, stats


def impute_nan(df: pd.DataFrame, feature_columns: list[str]) -> pd.DataFrame:
    """Median-impute NaN values in feature columns."""
    cols = [c for c in feature_columns if c in df.columns]
    if not cols:
        return df

    imputer = SimpleImputer(strategy="median")
    df[cols] = imputer.fit_transform(df[cols])
    return df


def run_pca(features: np.ndarray, n_components: int = 2) -> np.ndarray:
    """Run PCA and return projected coordinates."""
    pca = PCA(n_components=n_components, random_state=None)
    coords = pca.fit_transform(features)
    return coords


def run_umap(features: np.ndarray, n_components: int = 2, random_state: int = 42) -> np.ndarray:
    """Run UMAP and return projected coordinates."""
    import umap

    reducer = umap.UMAP(
        n_components=n_components,
        n_neighbors=min(15, len(features) - 1),
        min_dist=0.1,
        metric="euclidean",
        random_state=random_state,
    )
    coords = reducer.fit_transform(features)
    return coords


def compute_neighbors(
    features: np.ndarray,
    sample_ids: list[str],
    k: int = K_NEIGHBORS,
) -> dict:
    """Compute k-nearest neighbors for each sample."""
    k_actual = min(k + 1, len(features))  # +1 because self is included
    nn = NearestNeighbors(n_neighbors=k_actual, metric="euclidean")
    nn.fit(features)
    distances, indices = nn.kneighbors(features)

    result = {}
    for i, sid in enumerate(sample_ids):
        neighbors = []
        for rank, (dist, j) in enumerate(zip(distances[i], indices[i])):
            if j == i:
                continue  # skip self
            neighbors.append({
                "sample_id": sample_ids[j],
                "distance": float(dist),
                "rank": rank,
            })
            if len(neighbors) >= k:
                break
        result[sid] = {"neighbors": neighbors}

    return result


def build_projection_json(
    df: pd.DataFrame,
    coords: np.ndarray,
    x_label: str = "x",
    y_label: str = "y",
) -> list[dict]:
    """Build projection output JSON."""
    items = []
    for i, (_, row) in enumerate(df.iterrows()):
        item = {
            "sample_id": row.get("sample_id", ""),
            x_label: round(float(coords[i, 0]), 6),
            y_label: round(float(coords[i, 1]), 6),
            "category": row.get("category", ""),
            "subcategory": row.get("subcategory", ""),
        }
        # Parse manual_tags if present
        tags_raw = row.get("manual_tags", "")
        if isinstance(tags_raw, str) and tags_raw.strip():
            item["manual_tags"] = [t.strip() for t in tags_raw.split(";") if t.strip()]
        else:
            item["manual_tags"] = []

        if "file_path" in row:
            item["file_path"] = row["file_path"]

        items.append(item)
    return items


def save_json(data, path: Path) -> None:
    """Save data to JSON file."""
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  → {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize features, project, and compute kNN")
    parser.add_argument("--features", type=Path, default=DEFAULT_OUTPUT_DIR / "features_raw.csv")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--k", type=int, default=K_NEIGHBORS, help="Number of nearest neighbors")
    parser.add_argument("--umap-seed", type=int, default=42, help="UMAP random state")
    args = parser.parse_args()

    if not args.features.exists():
        print(f"ERROR: features file not found: {args.features}", file=sys.stderr)
        sys.exit(1)

    # Load features
    df = pd.read_csv(args.features)
    print(f"Loaded {len(df)} samples × {len(df.columns)} columns")

    # Identify available feature columns
    available_features = [c for c in P0_FEATURE_COLUMNS if c in df.columns]
    if not available_features:
        print("ERROR: no P0 feature columns found in features file.", file=sys.stderr)
        sys.exit(1)

    print(f"P0 features available: {len(available_features)}")

    # ── Step 1: Impute NaN ───────────────────────────────────────────────
    df = impute_nan(df, available_features)

    # ── Step 2: Z-score normalize ────────────────────────────────────────
    print("\nNormalizing features...")
    df_norm, stats = z_score_normalize(df, available_features)

    # Write features_normalized.csv
    args.output_dir.mkdir(parents=True, exist_ok=True)
    norm_path = args.output_dir / "features_normalized.csv"
    norm_cols = [c for c in METADATA_COLUMNS if c in df_norm.columns] + available_features
    df_norm[[c for c in norm_cols if c in df_norm.columns]].to_csv(norm_path, index=False, float_format="%.6f")
    print(f"  → {norm_path}")

    # Write feature_stats.json
    stats_path = args.output_dir / "feature_stats.json"
    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=2)
    print(f"  → {stats_path}")

    # ── Step 3: Projection + Neighbors ───────────────────────────────────
    sample_ids = df_norm["sample_id"].tolist()
    t0 = time.time()

    for group_name, group_cols in FEATURE_GROUPS.items():
        available = [c for c in group_cols if c in df_norm.columns]
        if len(available) < 2:
            print(f"\nSkipping group '{group_name}': only {len(available)} features available")
            continue

        print(f"\n─── Feature group: {group_name} ({len(available)} features) ───")
        X = df_norm[available].values.astype(np.float64)

        # PCA
        print("  Running PCA...")
        pca_coords = run_pca(X, n_components=2)
        pca_json = build_projection_json(df_norm, pca_coords)
        save_json(pca_json, args.output_dir / f"projection_pca_{group_name}.json")

        # UMAP
        print("  Running UMAP...")
        try:
            umap_coords = run_umap(X, n_components=2, random_state=args.umap_seed)
            umap_json = build_projection_json(df_norm, umap_coords)
            save_json(umap_json, args.output_dir / f"projection_umap_{group_name}.json")
        except Exception as e:
            print(f"  UMAP failed: {e}", file=sys.stderr)

        # Neighbors
        print(f"  Computing k={args.k} nearest neighbors...")
        neighbors = compute_neighbors(X, sample_ids, k=args.k)
        save_json(neighbors, args.output_dir / f"neighbors_{group_name}.json")

    # ── Step 4: Also save "all" projection as default aliases ────────────
    # Copy projection_umap_all.json → projection_umap.json (and PCA)
    for method in ("pca", "umap"):
        src = args.output_dir / f"projection_{method}_all.json"
        dst = args.output_dir / f"projection_{method}.json"
        if src.exists() and not dst.exists():
            dst.write_text(src.read_text())
            print(f"\n  Copied {src.name} → {dst.name}")

    src = args.output_dir / "neighbors_all.json"
    if src.exists():
        dst = args.output_dir / "neighbors.json"
        if not dst.exists():
            dst.write_text(src.read_text())
            print(f"  Copied {src.name} → {dst.name}")

    elapsed = time.time() - t0
    print(f"\nDone in {elapsed:.1f}s")


if __name__ == "__main__":
    main()

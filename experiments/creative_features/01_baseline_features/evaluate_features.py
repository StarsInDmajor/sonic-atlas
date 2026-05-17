"""
evaluate_features.py
====================
Compute correlation matrix, category summary, and generate evaluation template.

Usage:
    uv run python experiments/creative_features/01_baseline_features/evaluate_features.py \
        --features data/processed/creative_features/01_baseline_features/features_normalized.csv \
        --output-dir data/processed/creative_features/01_baseline_features
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from schemas import DEFAULT_OUTPUT_DIR, P0_FEATURE_COLUMNS


def compute_correlation_matrix(df: pd.DataFrame, feature_columns: list[str]) -> pd.DataFrame:
    """Compute Pearson correlation matrix for feature columns."""
    available = [c for c in feature_columns if c in df.columns]
    if not available:
        return pd.DataFrame()

    df_features = df[available].apply(pd.to_numeric, errors="coerce")
    return df_features.corr()


def compute_category_summary(df: pd.DataFrame, feature_columns: list[str]) -> pd.DataFrame:
    """Compute per-category feature means and stds."""
    available = [c for c in feature_columns if c in df.columns]
    if not available or "category" not in df.columns:
        return pd.DataFrame()

    df_features = df[["category"] + available].copy()
    for col in available:
        df_features[col] = pd.to_numeric(df_features[col], errors="coerce")

    summary = df_features.groupby("category").agg(["mean", "std", "count"])
    # Flatten MultiIndex columns
    summary.columns = [f"{col}_{agg}" for col, agg in summary.columns]
    return summary.reset_index()


def compute_tag_feature_correlation(
    df: pd.DataFrame, feature_columns: list[str]
) -> pd.DataFrame | None:
    """
    If manual_tags exist, compute mean feature values per tag.
    Returns a DataFrame with rows=tags, columns=feature means.
    """
    if "manual_tags" not in df.columns:
        return None

    available = [c for c in feature_columns if c in df.columns]
    if not available:
        return None

    # Parse tags
    tag_rows = []
    for _, row in df.iterrows():
        tags_raw = row.get("manual_tags", "")
        if isinstance(tags_raw, str) and tags_raw.strip():
            tags = [t.strip() for t in tags_raw.split(";") if t.strip()]
        else:
            tags = []
        for tag in tags:
            entry = {"tag": tag}
            for col in available:
                entry[col] = pd.to_numeric(row.get(col), errors="coerce")
            tag_rows.append(entry)

    if not tag_rows:
        return None

    df_tags = pd.DataFrame(tag_rows)
    tag_summary = df_tags.groupby("tag").mean(numeric_only=True)

    # Only keep tags with at least 2 samples
    tag_counts = df_tags["tag"].value_counts()
    valid_tags = tag_counts[tag_counts >= 2].index
    tag_summary = tag_summary.loc[tag_summary.index.isin(valid_tags)]

    if tag_summary.empty:
        return None

    return tag_summary.reset_index()


def generate_evaluation_template(df: pd.DataFrame, output_dir: Path) -> None:
    """Generate evaluation_notes.md template."""
    categories = df["category"].unique().tolist() if "category" in df.columns else []
    n = len(df)

    template = f"""# Baseline Feature Evaluation Notes

> Auto-generated template. Fill in observations after manual listening.

## Corpus Summary

- Total samples: {n}
- Categories: {', '.join(categories)}

## RQ1: Does the feature space form an intuitively reasonable sound space?

### Observations from PCA projection

<!-- 
Describe what you see:
- Do same-category sounds cluster?
- Are there clear or fuzzy boundaries?
- Which categories overlap?
-->

### Observations from UMAP projection

<!-- 
Describe what you see:
- Are clusters tighter or looser than PCA?
- Do new subclusters emerge?
- Which sounds are outliers?
-->

## RQ2: Which features have the most explanatory power?

### Correlation matrix observations

<!-- 
Look at correlation_matrix.csv:
- Which features are highly correlated (r > 0.7)?
- Are there redundant features?
- Which features are independent?
-->

### Tag-feature relationships

<!-- 
If tag-feature correlations were computed:
- Do brightness tags correlate with centroid?
- Do density tags correlate with onset_density or entropy?
- Do tonal/noisy tags correlate with flatness?
-->

## RQ3: Do nearest neighbors have creative value?

### Interesting neighbor pairs

<!-- Document at least 5 surprising-but-useful pairs -->

| Query | Neighbor | Distance | Why interesting? |
|---|---|---|---|
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |

### Cross-category neighbors

<!-- 
Which cross-category pairs are surprisingly close?
What does this tell us about feature similarity vs semantic similarity?
-->

## RQ4: What are the limitations of baseline descriptors?

### Failure cases

<!-- Document at least 5 cases where descriptors fail or mislead -->

| Sample | Expected | Actual | What went wrong |
|---|---|---|---|
| | | | |
| | | | |
| | | | |
| | | | |
| | | | |

### Features that need refinement

<!-- 
Which features need better implementations?
Which features are missing entirely?
What should Phase 3 embeddings capture that descriptors cannot?
-->

## Creative Insights

### Interpretable feature axes

<!-- Name at least 2 feature axes with clear perceptual meaning -->

1. **Axis name**: features involved, what you hear when moving along it
2. **Axis name**: features involved, what you hear when moving along it

### Feature trajectory ideas

<!-- Describe at least 1 preliminary feature trajectory composition sketch -->

### Requirements for feature-space browser

<!-- What should the first interactive browser do? -->

- [ ] 2D map display (UMAP)
- [ ] Color by category
- [ ] Click to inspect feature values
- [ ] Audio playback
- [ ] Nearest-neighbor highlights
- [ ] Feature filter / search
- [ ] Other: ___

## Next Steps

- [ ] Document interesting neighbor pairs
- [ ] Identify redundant features
- [ ] Plan embedding comparison (Phase 3)
- [ ] Design first feature-space browser
"""

    path = output_dir / "evaluation_notes.md"
    path.write_text(template)
    print(f"  → {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate features: correlation, summary, template")
    parser.add_argument("--features", type=Path, default=DEFAULT_OUTPUT_DIR / "features_normalized.csv")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    if not args.features.exists():
        print(f"ERROR: features file not found: {args.features}", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(args.features)
    print(f"Loaded {len(df)} samples")

    available_features = [c for c in P0_FEATURE_COLUMNS if c in df.columns]
    print(f"P0 features available: {len(available_features)}")

    args.output_dir.mkdir(parents=True, exist_ok=True)

    # ── Correlation Matrix ───────────────────────────────────────────────
    print("\nComputing correlation matrix...")
    corr = compute_correlation_matrix(df, available_features)
    if not corr.empty:
        corr_path = args.output_dir / "correlation_matrix.csv"
        corr.to_csv(corr_path, float_format="%.4f")
        print(f"  → {corr_path}")

    # ── Category Summary ─────────────────────────────────────────────────
    print("Computing category summary...")
    cat_summary = compute_category_summary(df, available_features)
    if not cat_summary.empty:
        cat_path = args.output_dir / "category_summary.csv"
        cat_summary.to_csv(cat_path, index=False, float_format="%.4f")
        print(f"  → {cat_path}")

    # ── Tag-Feature Correlation ──────────────────────────────────────────
    print("Computing tag-feature correlation...")
    tag_corr = compute_tag_feature_correlation(df, available_features)
    if tag_corr is not None:
        tag_path = args.output_dir / "tag_feature_summary.csv"
        tag_corr.to_csv(tag_path, index=False, float_format="%.4f")
        print(f"  → {tag_path}")
    else:
        print("  (no manual tags found or insufficient samples per tag)")

    # ── Evaluation Template ──────────────────────────────────────────────
    print("Generating evaluation template...")
    generate_evaluation_template(df, args.output_dir)

    print("\nDone.")


if __name__ == "__main__":
    main()

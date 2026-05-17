"""
make_manifest.py
================
Scan `data/raw/small_corpus/` and generate `manifest.csv`.

Usage:
    uv run python experiments/creative_features/01_baseline_features/make_manifest.py \
        --input data/raw/small_corpus \
        --output data/processed/creative_features/01_baseline_features/manifest.csv

Directory structure expected:
    data/raw/small_corpus/
    ├── music/
    │   ├── piano_001.wav
    │   └── ...
    ├── nature/
    │   ├── rain_001.wav
    │   └── ...
    └── urban_object/
        ├── metal_001.wav
        └── ...
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import soundfile as sf

from schemas import AUDIO_EXTENSIONS, CATEGORIES, DEFAULT_RAW_DIR, DEFAULT_OUTPUT_DIR, MANIFEST_COLUMNS, REPO_ROOT


def derive_sample_id(category: str, subcategory: str, sequence: int) -> str:
    """Generate sample_id: {category}_{subcategory}_{sequence:03d}"""
    return f"{category}_{subcategory}_{sequence:03d}"


def infer_subcategory(filepath: Path, category_dir: Path, category: str = "") -> str:
    """
    Infer subcategory from parent directory name or filename stem.

    Priority:
    1. If file is in a subdirectory under category/, use that directory name
    2. Otherwise use the filename stem before the first underscore/number
    """
    relative = filepath.relative_to(category_dir)
    parts = relative.parts

    if len(parts) > 1:
        # File is in a subdirectory: music/piano/001.wav → subcategory = "piano"
        return parts[-2]

    # File directly in category dir: piano_001.wav → subcategory = "piano"
    stem = filepath.stem
    # Remove trailing _digits pattern: music_accordion_001 → accordion
    import re
    match = re.match(r"(?:[a-z]+_)*?([a-z_]+?)_\d+$", stem)
    if match:
        candidate = match.group(1)
        # Remove category prefix if present: "music_accordion" → "accordion"
        prefix = category + "_"
        if candidate.startswith(prefix):
            candidate = candidate[len(prefix):]
        if candidate and candidate != category:
            return candidate
    # Fallback: use category as subcategory
    return category


def scan_audio_files(input_dir: Path) -> list[dict]:
    """Recursively scan for audio files and build manifest rows."""
    rows: list[dict] = []
    category_counters: dict[str, dict[str, int]] = {cat: {} for cat in CATEGORIES}

    for category in CATEGORIES:
        category_dir = input_dir / category
        if not category_dir.is_dir():
            print(f"WARNING: category directory not found: {category_dir}", file=sys.stderr)
            continue

        for filepath in sorted(category_dir.rglob("*")):
            if not filepath.is_file():
                continue
            if filepath.suffix.lower() not in AUDIO_EXTENSIONS:
                continue

            # Get audio info
            try:
                info = sf.info(str(filepath))
                duration = info.duration
                sample_rate = info.samplerate
                channels = info.channels
            except Exception as e:
                print(f"WARNING: cannot read {filepath}: {e}", file=sys.stderr)
                continue

            # Derive subcategory and sample_id
            subcategory = infer_subcategory(filepath, category_dir, category)
            counter_key = subcategory
            if counter_key not in category_counters[category]:
                category_counters[category][counter_key] = 0
            category_counters[category][counter_key] += 1
            sequence = category_counters[category][counter_key]

            sample_id = derive_sample_id(category, subcategory, sequence)
            # Path relative to repo root (REPO_ROOT)
            file_path = str(filepath.relative_to(REPO_ROOT))

            rows.append(
                {
                    "sample_id": sample_id,
                    "file_path": file_path,
                    "category": category,
                    "subcategory": subcategory,
                    "duration": f"{duration:.3f}",
                    "sample_rate": sample_rate,
                    "channels": channels,
                    "start_time": 0,
                    "end_time": "",
                    "source": "",
                    "license": "",
                    "manual_tags": "",
                    "description": "",
                    "notes": "",
                }
            )

    return rows


def write_manifest(rows: list[dict], output_path: Path) -> None:
    """Write manifest to CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=MANIFEST_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({col: row.get(col, "") for col in MANIFEST_COLUMNS})

    print(f"Wrote {len(rows)} entries to {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan corpus directory and generate manifest.csv")
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_RAW_DIR,
        help="Root corpus directory containing category subdirectories",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_DIR / "manifest.csv",
        help="Output manifest CSV path",
    )
    args = parser.parse_args()

    if not args.input.is_dir():
        print(f"ERROR: input directory does not exist: {args.input}", file=sys.stderr)
        print(f"  Create it and add audio files organized as:", file=sys.stderr)
        print(f"    {args.input}/music/*.wav", file=sys.stderr)
        print(f"    {args.input}/nature/*.wav", file=sys.stderr)
        print(f"    {args.input}/urban_object/*.wav", file=sys.stderr)
        sys.exit(1)

    rows = scan_audio_files(args.input)
    if not rows:
        print("ERROR: no audio files found. Check directory structure.", file=sys.stderr)
        sys.exit(1)

    write_manifest(rows, args.output)

    # Summary
    categories_found = {}
    for row in rows:
        cat = row["category"]
        categories_found[cat] = categories_found.get(cat, 0) + 1

    print("\nCorpus summary:")
    for cat in CATEGORIES:
        count = categories_found.get(cat, 0)
        status = "OK" if count >= 15 else "LOW" if count > 0 else "MISSING"
        print(f"  {cat:15s}: {count:3d} clips  [{status}]")
    print(f"  {'TOTAL':15s}: {len(rows):3d} clips")


if __name__ == "__main__":
    main()

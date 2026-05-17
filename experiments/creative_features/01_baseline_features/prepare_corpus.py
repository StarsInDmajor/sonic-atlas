"""
prepare_corpus.py
=================
Select and organize audio samples from ESC-50 and TinySOL into data/raw/small_corpus/.

Usage:
    uv run python experiments/creative_features/01_baseline_features/prepare_corpus.py \
        --esc50 /tmp/ESC-50 \
        --tinysol /tmp/TinySOL \
        --output data/raw/small_corpus \
        --manifest data/processed/creative_features/01_baseline_features/manifest.csv

Selection criteria:
    - ESC-50: ~20 nature + ~20 urban_object clips (5s each, WAV)
    - TinySOL: ~20 instrument single notes across 8 instruments
"""

from __future__ import annotations

import argparse
import csv
import shutil
import sys
from pathlib import Path

from schemas import AUDIO_EXTENSIONS, DEFAULT_OUTPUT_DIR, DEFAULT_RAW_DIR, MANIFEST_COLUMNS

# ── ESC-50 Selection ─────────────────────────────────────────────────────────
# ESC-50 categories: https://github.com/karolpiczak/ESC-50#dataset
# We pick categories that map cleanly to our nature / urban_object classes.

ESC50_NATURE = {
    # category_name: (esc50_label, target_count)
    "rain": ("rain", 3),
    "thunderstorm": ("thunderstorm", 2),
    "sea_waves": ("sea_waves", 3),
    "crackling_fire": ("crackling_fire", 2),
    "crickets": ("crickets", 2),
    "chirping_birds": ("chirping_birds", 3),
    "water_drops": ("water_drops", 2),
    "wind": ("wind", 3),
}

ESC50_URBAN = {
    "clock_alarm": ("clock_alarm", 2),
    "siren": ("siren", 3),
    "car_horn": ("car_horn", 2),
    "engine": ("engine", 3),
    "train": ("train", 2),
    "door_wood_creaks": ("door_wood_creaks", 2),
    "helicopter": ("helicopter", 2),
    "typing": ("keyboard_typing", 2),
    "glass_breaking": ("glass_breaking", 2),
}

# TinySOL actually available (partial download: Winds + Keyboards only)
TINYSOL_INSTRUMENTS = {
    # instrument_dir: (target_count, subcategory)
    "Flute": (3, "flute"),
    "Clarinet_Bb": (3, "clarinet"),
    "Oboe": (2, "oboe"),
    "Bassoon": (2, "bassoon"),
    "Sax_Alto": (2, "alto_saxophone"),
    "Accordion": (3, "accordion"),
}

# ── ESC-50 helpers ───────────────────────────────────────────────────────────


def parse_esc50_meta(esc50_dir: Path) -> list[dict]:
    """Parse ESC-50 metadata CSV."""
    meta_path = esc50_dir / "meta" / "esc50.csv"
    if not meta_path.exists():
        raise FileNotFoundError(f"ESC-50 metadata not found: {meta_path}")

    rows = []
    with open(meta_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def select_esc50_samples(esc50_dir: Path, category_map: dict, target_class: str) -> list[dict]:
    """Select ESC-50 samples for a given category mapping."""
    meta = parse_esc50_meta(esc50_dir)
    audio_dir = esc50_dir / "audio"

    selected = []
    for subcategory, (esc50_label, target_count) in category_map.items():
        # Find matching samples
        candidates = [row for row in meta if row.get("category", "").strip() == esc50_label]

        if not candidates:
            print(f"  WARNING: no ESC-50 samples found for category '{esc50_label}'")
            continue

        # Prefer fold 1 for reproducibility, take up to target_count
        fold1 = [c for c in candidates if c.get("fold") == "1"]
        pool = fold1 if len(fold1) >= target_count else candidates
        picked = pool[:target_count]

        for i, row in enumerate(picked):
            filename = row["filename"]
            src = audio_dir / filename
            if not src.exists():
                print(f"  WARNING: file not found: {src}")
                continue

            sample_id = f"{target_class}_{subcategory}_{i + 1:03d}"
            selected.append({
                "sample_id": sample_id,
                "source_path": str(src),
                "category": target_class,
                "subcategory": subcategory,
                "esc50_category": esc50_label,
                "filename": filename,
            })

    return selected


# ── TinySOL helpers ──────────────────────────────────────────────────────────


def find_tinysol_dir(tinysol_root: Path) -> Path:
    """Find the actual WAV directory inside TinySOL extraction."""
    candidates = [
        tinysol_root / "TinySOL2020",
        tinysol_root / "TinySOL" / "TinySOL2020",
        tinysol_root / "WAV",
        tinysol_root,
    ]
    for c in candidates:
        if c.is_dir() and any(c.rglob("*.wav")):
            return c
    return tinysol_root


def parse_tinysol_filename(filepath: Path) -> dict | None:
    """
    Parse TinySOL filename convention.
    Format: {InstrumentCode}-{Technique}-{Pitch}-{Dynamic}-{Instance}.wav
    Example: TpC-ord-C4-mf-1a.wav
    """
    stem = filepath.stem
    parts = stem.split("-")
    if len(parts) < 4:
        return None

    return {
        "instrument_code": parts[0],
        "technique": parts[1],
        "pitch": parts[2],
        "dynamic": parts[3],
        "instance": parts[4] if len(parts) > 4 else "",
    }


def select_tinysol_samples(tinysol_root: Path, instrument_map: dict) -> list[dict]:
    """Select TinySOL samples for chosen instruments."""
    sol_dir = find_tinysol_dir(tinysol_root)

    selected = []
    for inst_dir_name, (target_count, subcategory) in instrument_map.items():
        # Find the instrument directory
        candidates = []
        for family_dir in sol_dir.iterdir():
            if not family_dir.is_dir():
                continue
            inst_dir = family_dir / inst_dir_name / "ordinario"
            if inst_dir.is_dir():
                candidates.extend(sorted(inst_dir.glob("*.wav")))

        if not candidates:
            print(f"  WARNING: no TinySOL samples found for '{inst_dir_name}'")
            continue

        # Prefer mf dynamic, then ff, then pp
        mf = [c for c in candidates if "-mf-" in c.stem]
        ff = [c for c in candidates if "-ff-" in c.stem]
        pp = [c for c in candidates if "-pp-" in c.stem]
        pool = mf if len(mf) >= target_count else (ff if len(ff) >= target_count else candidates)

        # Sort by pitch for variety, pick evenly spaced
        pool_sorted = sorted(pool, key=lambda p: p.stem)
        step = max(1, len(pool_sorted) // target_count)
        picked = [pool_sorted[i * step] for i in range(min(target_count, len(pool_sorted)))]

        for i, src in enumerate(picked):
            info = parse_tinysol_filename(src)
            sample_id = f"music_{subcategory}_{i + 1:03d}"
            selected.append({
                "sample_id": sample_id,
                "source_path": str(src),
                "category": "music",
                "subcategory": subcategory,
                "tinysol_instrument": inst_dir_name,
                "pitch": info["pitch"] if info else "",
                "dynamic": info["dynamic"] if info else "",
                "filename": src.name,
            })

    return selected


# ── Copy and organize ────────────────────────────────────────────────────────


def copy_samples(samples: list[dict], output_dir: Path, repo_root: Path) -> list[dict]:
    """Copy selected samples to output directory and return manifest rows."""
    manifest_rows = []

    for sample in samples:
        src = Path(sample["source_path"])
        category = sample["category"]
        subcategory = sample["subcategory"]
        sample_id = sample["sample_id"]

        # Destination: output_dir/category/subcategory_sampleid.wav
        dest_dir = output_dir / category
        dest_dir.mkdir(parents=True, exist_ok=True)

        dest_filename = f"{sample_id}{src.suffix}"
        dest = dest_dir / dest_filename

        shutil.copy2(src, dest)

        # Build manifest row
        manifest_rows.append({
            "sample_id": sample_id,
            "file_path": str(dest.relative_to(repo_root)),
            "category": category,
            "subcategory": subcategory,
            "duration": "",
            "sample_rate": "",
            "channels": "",
            "start_time": 0,
            "end_time": "",
            "source": sample.get("esc50_category", "") or sample.get("tinysol_instrument", ""),
            "license": "CC-BY 4.0" if category == "music" else "CC-BY-NC (ESC-50)",
            "manual_tags": "",
            "description": f"{subcategory} - {sample.get('pitch', '')} {sample.get('dynamic', '')}".strip(" -"),
            "notes": f"source: {src.name}",
        })

    return manifest_rows


def write_manifest(rows: list[dict], output_path: Path) -> None:
    """Write manifest CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=MANIFEST_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({col: row.get(col, "") for col in MANIFEST_COLUMNS})
    print(f"\nWrote manifest: {output_path} ({len(rows)} entries)")


# ── Main ─────────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare small_corpus from ESC-50 and TinySOL")
    parser.add_argument("--esc50", type=Path, default=Path("/tmp/ESC-50"), help="ESC-50 root directory")
    parser.add_argument("--tinysol", type=Path, default=Path("/tmp/TinySOL_full"), help="TinySOL root directory")
    parser.add_argument("--output", type=Path, default=DEFAULT_RAW_DIR, help="Output corpus directory")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_OUTPUT_DIR / "manifest.csv", help="Output manifest")
    parser.add_argument("--dry-run", action="store_true", help="Print plan without copying")
    args = parser.parse_args()

    print("=" * 60)
    print("Sonic Atlas — Corpus Preparation")
    print("=" * 60)

    # ── ESC-50 ───────────────────────────────────────────────────────────
    print("\n── ESC-50: Nature sounds ──")
    if not args.esc50.is_dir():
        print(f"  ERROR: ESC-50 directory not found: {args.esc50}")
        sys.exit(1)

    nature_samples = select_esc50_samples(args.esc50, ESC50_NATURE, "nature")
    print(f"  Selected: {len(nature_samples)} nature samples")
    for s in nature_samples:
        print(f"    {s['sample_id']:30s} ← {s['filename']}")

    print("\n── ESC-50: Urban/object sounds ──")
    urban_samples = select_esc50_samples(args.esc50, ESC50_URBAN, "urban_object")
    print(f"  Selected: {len(urban_samples)} urban_object samples")
    for s in urban_samples:
        print(f"    {s['sample_id']:30s} ← {s['filename']}")

    # ── TinySOL ──────────────────────────────────────────────────────────
    print("\n── TinySOL: Musical instrument sounds ──")
    if not args.tinysol.is_dir():
        print(f"  ERROR: TinySOL directory not found: {args.tinysol}")
        sys.exit(1)

    music_samples = select_tinysol_samples(args.tinysol, TINYSOL_INSTRUMENTS)
    print(f"  Selected: {len(music_samples)} music samples")
    for s in music_samples:
        print(f"    {s['sample_id']:30s} ← {s['filename']}  ({s.get('pitch', '')} {s.get('dynamic', '')})")

    # ── Summary ──────────────────────────────────────────────────────────
    all_samples = nature_samples + urban_samples + music_samples
    print(f"\n{'=' * 60}")
    print(f"Total: {len(all_samples)} samples")
    print(f"  music:        {len(music_samples)}")
    print(f"  nature:       {len(nature_samples)}")
    print(f"  urban_object: {len(urban_samples)}")

    if args.dry_run:
        print("\n[DRY RUN] No files copied.")
        return

    # ── Copy ─────────────────────────────────────────────────────────────
    print(f"\nCopying to {args.output} ...")
    from schemas import REPO_ROOT
    manifest_rows = copy_samples(all_samples, args.output, REPO_ROOT)
    print(f"Copied {len(manifest_rows)} files")

    # ── Write manifest ───────────────────────────────────────────────────
    write_manifest(manifest_rows, args.manifest)

    # ── Verify ───────────────────────────────────────────────────────────
    print(f"\nVerification:")
    for cat in ("music", "nature", "urban_object"):
        cat_dir = args.output / cat
        if cat_dir.is_dir():
            count = len(list(cat_dir.glob("*")))
            print(f"  {cat:15s}: {count:3d} files  ✓")
        else:
            print(f"  {cat:15s}: MISSING  ✗")


if __name__ == "__main__":
    main()

"""
build_corpus.py
===============
Scan all available sound sources, standardize to WAV 22050Hz mono,
organize into corpus directory, and generate manifest.csv.

Usage:
    uv run python experiments/build_corpus.py \
        --output data/corpus \
        --manifest data/corpus/manifest.csv \
        --sources ESC-50 TinySOL Philharmonia

Sources are searched in /tmp by default. Override with --source-dir.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import sys
import tempfile
from pathlib import Path

import librosa
import numpy as np
import soundfile as sf

# ── Constants ────────────────────────────────────────────────────────────────

TARGET_SR = 22050
TARGET_CHANNELS = 1
TARGET_FORMAT = "WAV"
TARGET_SUBTYPE = "PCM_16"

MANIFEST_COLUMNS = [
    "sample_id", "file_path", "category", "subcategory", "instrument",
    "tags", "duration", "sample_rate", "source", "source_id",
    "license", "pitch", "dynamic", "technique", "description",
]

# ── Taxonomy mapping ─────────────────────────────────────────────────────────

# Maps instrument/source names to (category, subcategory, instrument)
INSTRUMENT_TAXONOMY = {
    # TinySOL winds
    "Flute": ("music", "woodwind", "flute"),
    "Clarinet_Bb": ("music", "woodwind", "clarinet"),
    "Oboe": ("music", "woodwind", "oboe"),
    "Bassoon": ("music", "woodwind", "bassoon"),
    "Sax_Alto": ("music", "woodwind", "alto_saxophone"),
    # TinySOL keyboards
    "Accordion": ("music", "keyboard", "accordion"),
    # Philharmonia brass
    "trumpet": ("music", "brass", "trumpet"),
    "french horn": ("music", "brass", "french_horn"),
    "trombone": ("music", "brass", "trombone"),
    "tuba": ("music", "brass", "tuba"),
    # Philharmonia strings
    "violin": ("music", "string_bowed", "violin"),
    "viola": ("music", "string_bowed", "viola"),
    "cello": ("music", "string_bowed", "cello"),
    "double bass": ("music", "string_bowed", "double_bass"),
    "guitar": ("music", "string_plucked", "guitar"),
    "mandolin": ("music", "string_plucked", "mandolin"),
    "banjo": ("music", "string_plucked", "banjo"),
    # Additional keyboard
    "piano": ("music", "keyboard", "piano"),
    "harpsichord": ("music", "keyboard", "harpsichord"),
    "organ": ("music", "keyboard", "organ"),
}

# ESC-50 category → our taxonomy
ESC50_TAXONOMY = {
    # Nature
    "rain": ("nature", "weather", "rain"),
    "thunderstorm": ("nature", "weather", "thunderstorm"),
    "wind": ("nature", "weather", "wind"),
    "sea_waves": ("nature", "water", "sea_waves"),
    "pouring_water": ("nature", "water", "pouring"),
    "water_drops": ("nature", "water", "drops"),
    "stream": ("nature", "water", "stream"),
    "chirping_birds": ("nature", "animal", "bird"),
    "crowing_rooster": ("nature", "animal", "bird"),
    "crying_baby": ("nature", "human", "baby"),
    "frog": ("nature", "animal", "frog"),
    "crickets": ("nature", "animal", "insect"),
    "insects": ("nature", "animal", "insect"),
    "hen": ("nature", "animal", "bird"),
    "cow": ("nature", "animal", "mammal"),
    "pig": ("nature", "animal", "mammal"),
    "sheep": ("nature", "animal", "mammal"),
    "cat": ("nature", "animal", "mammal"),
    "dog": ("nature", "animal", "mammal"),
    "crackling_fire": ("nature", "fire", "crackling"),
    "breathing": ("nature", "human", "breathing"),
    "coughing": ("nature", "human", "coughing"),
    "sneezing": ("nature", "human", "sneezing"),
    "snoring": ("nature", "human", "snoring"),
    "clapping": ("nature", "human", "clapping"),
    "laughing": ("nature", "human", "laughing"),
    "crying": ("nature", "human", "crying"),
    # Urban
    "siren": ("urban", "alarm", "siren"),
    "car_horn": ("urban", "alarm", "car_horn"),
    "engine": ("urban", "machine", "engine"),
    "train": ("urban", "transport", "train"),
    "airplane": ("urban", "transport", "airplane"),
    "helicopter": ("urban", "transport", "helicopter"),
    "bus": ("urban", "transport", "bus"),
    "motorcycle": ("urban", "transport", "motorcycle"),
    "bicycle": ("urban", "transport", "bicycle"),
    "clock_alarm": ("urban", "alarm", "clock"),
    "clock_tick": ("urban", "domestic", "clock"),
    "door_wood_creaks": ("urban", "impact", "door"),
    "door_wood_knock": ("urban", "impact", "door"),
    "glass_breaking": ("urban", "impact", "glass"),
    "can_opening": ("urban", "domestic", "can"),
    "vacuum_cleaner": ("urban", "domestic", "vacuum"),
    "washing_machine": ("urban", "domestic", "washing"),
    "toilet_flush": ("urban", "domestic", "toilet"),
    "keyboard_typing": ("urban", "human", "typing"),
    "mouse_click": ("urban", "human", "click"),
    "footsteps": ("urban", "human", "footsteps"),
    "brushing_teeth": ("urban", "domestic", "brushing"),
    "drinking_sipping": ("urban", "human", "drinking"),
    "hand_saw": ("urban", "machine", "saw"),
    "chainsaw": ("urban", "machine", "chainsaw"),
    "fireworks": ("urban", "alarm", "fireworks"),
    "church_bells": ("urban", "alarm", "bell"),
    "crow": ("nature", "animal", "bird"),
}

# ── Helpers ──────────────────────────────────────────────────────────────────


def convert_to_standard(src: Path, dst: Path) -> dict | None:
    """Convert audio file to standard WAV format. Returns metadata or None on failure."""
    try:
        y, sr = librosa.load(str(src), sr=TARGET_SR, mono=True)
        duration = len(y) / sr

        # Skip very short clips (< 0.5s)
        if duration < 0.5:
            return None

        dst.parent.mkdir(parents=True, exist_ok=True)
        sf.write(str(dst), y, sr, format=TARGET_FORMAT, subtype=TARGET_SUBTYPE)

        return {
            "duration": round(duration, 3),
            "sample_rate": sr,
        }
    except Exception as e:
        print(f"    WARNING: failed to convert {src.name}: {e}")
        return None


def parse_tinysol_filename(filepath: Path) -> dict:
    """Parse TinySOL filename: {Code}-{Technique}-{Pitch}-{Dynamic}-{Instance}.wav"""
    stem = filepath.stem
    parts = stem.split("-")
    if len(parts) >= 4:
        return {
            "pitch": parts[2],
            "dynamic": parts[3],
            "technique": parts[1],
            "instance": parts[4] if len(parts) > 4 else "",
        }
    return {"pitch": "", "dynamic": "", "technique": "", "instance": ""}


def parse_philharmonia_filename(filepath: Path) -> dict:
    """Parse Philharmonia filename patterns."""
    stem = filepath.stem
    parts = stem.split("_")
    result = {"pitch": "", "dynamic": "", "technique": "normal", "duration_label": ""}

    if len(parts) >= 2:
        # Pattern: instrument_pitch_duration_dynamic_technique
        # e.g. trumpet_C5_1_forte_normal or violin_A4_long_piano_mute
        result["pitch"] = parts[1] if len(parts) > 1 else ""
        if len(parts) > 2:
            result["duration_label"] = parts[2]
        if len(parts) > 3:
            result["dynamic"] = parts[3]
        if len(parts) > 4:
            result["technique"] = parts[4]

    return result


# ── Source scanners ──────────────────────────────────────────────────────────


def scan_esc50(source_dir: Path, repo_root: Path, corpus_dir: Path) -> list[dict]:
    """Scan ESC-50 and return manifest rows."""
    esc50_dir = source_dir / "ESC-50"
    if not esc50_dir.is_dir():
        print(f"  ESC-50 not found at {esc50_dir}")
        return []

    meta_path = esc50_dir / "meta" / "esc50.csv"
    audio_dir = esc50_dir / "audio"

    if not meta_path.exists():
        print(f"  ESC-50 metadata not found: {meta_path}")
        return []

    with open(meta_path) as f:
        meta = list(csv.DictReader(f))

    rows = []
    counters: dict[str, int] = {}

    for entry in meta:
        category_name = entry.get("category", "").strip()
        if category_name not in ESC50_TAXONOMY:
            continue

        cat, subcat, instrument = ESC50_TAXONOMY[category_name]
        key = f"{cat}_{subcat}_{instrument}"
        counters[key] = counters.get(key, 0) + 1
        seq = counters[key]

        sample_id = f"{cat}_{subcat}_{instrument}_{seq:04d}"
        src_file = audio_dir / entry["filename"]

        if not src_file.exists():
            continue

        dest = corpus_dir / cat / subcat / f"{sample_id}.wav"
        meta_info = convert_to_standard(src_file, dest)
        if meta_info is None:
            continue

        rel_path = str(dest.relative_to(repo_root))
        rows.append({
            "sample_id": sample_id,
            "file_path": rel_path,
            "category": cat,
            "subcategory": subcat,
            "instrument": instrument,
            "tags": "",
            "duration": meta_info["duration"],
            "sample_rate": meta_info["sample_rate"],
            "source": "ESC-50",
            "source_id": entry["filename"],
            "license": "CC-BY-NC",
            "pitch": "",
            "dynamic": "",
            "technique": "",
            "description": f"{category_name} from ESC-50 fold {entry.get('fold','')}",
        })

    return rows


def scan_tinysol(source_dir: Path, repo_root: Path, corpus_dir: Path) -> list[dict]:
    """Scan TinySOL and return manifest rows."""
    tinysol_dir = source_dir / "TinySOL" / "TinySOL2020"
    if not tinysol_dir.is_dir():
        tinysol_dir = source_dir / "TinySOL_full" / "TinySOL2020"
    if not tinysol_dir.is_dir():
        tinysol_dir = source_dir / "TinySOL2020"
    if not tinysol_dir.is_dir():
        print(f"  TinySOL not found under {source_dir}")
        return []

    rows = []
    counters: dict[str, int] = {}

    for family_dir in sorted(tinysol_dir.iterdir()):
        if not family_dir.is_dir():
            continue
        for inst_dir in sorted(family_dir.iterdir()):
            if not inst_dir.is_dir():
                continue
            inst_name = inst_dir.name
            if inst_name not in INSTRUMENT_TAXONOMY:
                print(f"  SKIP TinySOL instrument: {inst_name}")
                continue

            cat, subcat, instrument = INSTRUMENT_TAXONOMY[inst_name]

            # Find WAV files in ordinario/ or directly
            ord_dir = inst_dir / "ordinario"
            wav_files = sorted((ord_dir if ord_dir.is_dir() else inst_dir).glob("*.wav"))

            for src_file in wav_files:
                key = f"{cat}_{subcat}_{instrument}"
                counters[key] = counters.get(key, 0) + 1
                seq = counters[key]

                sample_id = f"{cat}_{subcat}_{instrument}_{seq:04d}"
                dest = corpus_dir / cat / subcat / f"{sample_id}.wav"
                meta_info = convert_to_standard(src_file, dest)
                if meta_info is None:
                    continue

                sol_info = parse_tinysol_filename(src_file)
                rel_path = str(dest.relative_to(repo_root))

                tags = []
                if sol_info["dynamic"]:
                    tags.append(sol_info["dynamic"])
                if sol_info["technique"] and sol_info["technique"] != "ord":
                    tags.append(sol_info["technique"])

                rows.append({
                    "sample_id": sample_id,
                    "file_path": rel_path,
                    "category": cat,
                    "subcategory": subcat,
                    "instrument": instrument,
                    "tags": ";".join(tags),
                    "duration": meta_info["duration"],
                    "sample_rate": meta_info["sample_rate"],
                    "source": "TinySOL",
                    "source_id": src_file.name,
                    "license": "CC-BY 4.0",
                    "pitch": sol_info["pitch"],
                    "dynamic": sol_info["dynamic"],
                    "technique": sol_info["technique"],
                    "description": f"{instrument} {sol_info['pitch']} {sol_info['dynamic']}",
                })

    return rows


def scan_philharmonia(source_dir: Path, repo_root: Path, corpus_dir: Path) -> list[dict]:
    """Scan Philharmonia Orchestra samples and return manifest rows."""
    phil_dir = source_dir / "philharmonia"
    if not phil_dir.is_dir():
        print(f"  Philharmonia not found at {phil_dir}")
        return []

    rows = []
    counters: dict[str, int] = {}

    for family_dir in sorted(phil_dir.iterdir()):
        if not family_dir.is_dir():
            continue
        # Navigate: philharmonia/Brass/Brass/trumpet/ or philharmonia/Strings/Strings/violin/
        inner = family_dir / family_dir.name
        search_dir = inner if inner.is_dir() else family_dir

        for inst_dir in sorted(search_dir.iterdir()):
            if not inst_dir.is_dir():
                continue
            inst_name = inst_dir.name.lower()

            # Find matching taxonomy
            taxonomy_key = None
            for tk in INSTRUMENT_TAXONOMY:
                if tk.lower() == inst_name:
                    taxonomy_key = tk
                    break

            if taxonomy_key is None:
                print(f"  SKIP Philharmonia instrument: {inst_name}")
                continue

            cat, subcat, instrument = INSTRUMENT_TAXONOMY[taxonomy_key]

            # Collect all audio files
            audio_files = sorted(
                list(inst_dir.glob("*.mp3")) + list(inst_dir.glob("*.wav"))
            )

            for src_file in audio_files:
                key = f"{cat}_{subcat}_{instrument}"
                counters[key] = counters.get(key, 0) + 1
                seq = counters[key]

                sample_id = f"{cat}_{subcat}_{instrument}_{seq:04d}"
                dest = corpus_dir / cat / subcat / f"{sample_id}.wav"
                meta_info = convert_to_standard(src_file, dest)
                if meta_info is None:
                    continue

                ph_info = parse_philharmonia_filename(src_file)
                rel_path = str(dest.relative_to(repo_root))

                tags = []
                if ph_info["dynamic"]:
                    tags.append(ph_info["dynamic"])
                if ph_info["technique"] and ph_info["technique"] != "normal":
                    tags.append(ph_info["technique"])

                rows.append({
                    "sample_id": sample_id,
                    "file_path": rel_path,
                    "category": cat,
                    "subcategory": subcat,
                    "instrument": instrument,
                    "tags": ";".join(tags),
                    "duration": meta_info["duration"],
                    "sample_rate": meta_info["sample_rate"],
                    "source": "Philharmonia",
                    "source_id": src_file.name,
                    "license": "CC",
                    "pitch": ph_info["pitch"],
                    "dynamic": ph_info["dynamic"],
                    "technique": ph_info["technique"],
                    "description": f"{instrument} {ph_info['pitch']} {ph_info['dynamic']} {ph_info['technique']}",
                })

    return rows


# FSD50K label → our taxonomy
FSD50K_TAXONOMY = {
    # Music - keyboard
    "Piano": ("music", "keyboard", "piano"),
    "Organ": ("music", "keyboard", "organ"),
    "Synthesizer": ("music", "electronic", "synthesizer"),
    "Sampler": ("music", "electronic", "sampler"),
    # Music - percussion
    "Drum": ("music", "percussion", "drum"),
    "Drum_kit": ("music", "percussion", "drum_kit"),
    "Snare_drum": ("music", "percussion", "snare_drum"),
    "Bass_drum": ("music", "percussion", "bass_drum"),
    "Cymbal": ("music", "percussion", "cymbal"),
    "Crash_cymbal": ("music", "percussion", "cymbal"),
    "Hi-hat": ("music", "percussion", "hihat"),
    "Gong": ("music", "percussion", "gong"),
    "Cowbell": ("music", "percussion", "cowbell"),
    "Marimba_and_xylophone": ("music", "percussion", "marimba"),
    "Mallet_percussion": ("music", "percussion", "mallet"),
    "Percussion": ("music", "percussion", "percussion"),
    "Tabla": ("music", "percussion", "tabla"),
    "Timpani": ("music", "percussion", "timpani"),
    "Steel_guitar": ("music", "string_plucked", "steel_guitar"),
    # Music - strings
    "Bass_guitar": ("music", "string_plucked", "bass_guitar"),
    "Guitar": ("music", "string_plucked", "guitar"),
    "Acoustic_guitar": ("music", "string_plucked", "guitar"),
    "Electric_guitar": ("music", "string_plucked", "electric_guitar"),
    "Violin_fiddle": ("music", "string_bowed", "violin"),
    "String_section": ("music", "string_bowed", "ensemble"),
    # Music - wind
    "Harmonica": ("music", "woodwind", "harmonica"),
    "Saxophone": ("music", "woodwind", "saxophone"),
    "Trumpet": ("music", "brass", "trumpet"),
    "Trombone": ("music", "brass", "trombone"),
    # Music - voice
    "Singing": ("music", "voice", "singing"),
    "Female_singing": ("music", "voice", "female_singing"),
    "Male_singing": ("music", "voice", "male_singing"),
    "Choir": ("music", "voice", "choir"),
    "Yodeling": ("music", "voice", "yodeling"),
    "Rapping": ("music", "voice", "rapping"),
    "Humming": ("music", "voice", "humming"),
    # Nature
    "Wind": ("nature", "weather", "wind"),
    "Rain": ("nature", "weather", "rain"),
    "Thunder": ("nature", "weather", "thunder"),
    "Water": ("nature", "water", "water"),
    "Stream": ("nature", "water", "stream"),
    "Ocean": ("nature", "water", "ocean"),
    "Bird": ("nature", "animal", "bird"),
    "Bird_vocalization_and_bird_calling": ("nature", "animal", "bird"),
    "Insect": ("nature", "animal", "insect"),
    "Frog": ("nature", "animal", "frog"),
    "Cat": ("nature", "animal", "mammal"),
    "Dog": ("nature", "animal", "mammal"),
    "Livestock_and_farm_animals": ("nature", "animal", "mammal"),
    "Wild_animals": ("nature", "animal", "mammal"),
    "Crackling_fire": ("nature", "fire", "crackling"),
    "Fire": ("nature", "fire", "fire"),
    # Urban
    "Siren": ("urban", "alarm", "siren"),
    "Alarm": ("urban", "alarm", "alarm"),
    "Alarm_clock": ("urban", "alarm", "clock"),
    "Doorbell": ("urban", "alarm", "doorbell"),
    "Bicycle_bell": ("urban", "alarm", "bicycle_bell"),
    "Church_bell": ("urban", "alarm", "church_bell"),
    "Bell": ("urban", "alarm", "bell"),
    "Car_horn": ("urban", "alarm", "car_horn"),
    "Vehicle_horn_and_car_horn_and_honking": ("urban", "alarm", "car_horn"),
    "Engine": ("urban", "machine", "engine"),
    "Motor_vehicle_(road)": ("urban", "transport", "car"),
    "Train": ("urban", "transport", "train"),
    "Aircraft": ("urban", "transport", "aircraft"),
    "Helicopter": ("urban", "transport", "helicopter"),
    "Skateboard": ("urban", "transport", "skateboard"),
    "Bus": ("urban", "transport", "bus"),
    "Door": ("urban", "impact", "door"),
    "Glass": ("urban", "impact", "glass"),
    "Coin_(dropping)": ("urban", "impact", "coin"),
    "Typing": ("urban", "human", "typing"),
    "Keyboard_typing": ("urban", "human", "typing"),
    "Clapping": ("urban", "human", "clapping"),
    "Footsteps": ("urban", "human", "footsteps"),
    "Laughter": ("nature", "human", "laughing"),
    "Crying_and_sobbing": ("nature", "human", "crying"),
    "Cough": ("nature", "human", "coughing"),
    "Sneeze": ("nature", "human", "sneezing"),
    "Breathing": ("nature", "human", "breathing"),
    "Snoring": ("nature", "human", "snoring"),
    "Speech": ("nature", "human", "speech"),
    "Human_voice": ("nature", "human", "voice"),
    "Male_speech_and_man_speaking": ("nature", "human", "speech_male"),
    "Female_speech_and_woman_speaking": ("nature", "human", "speech_female"),
    "Child_speech_and_kid_speaking": ("nature", "human", "speech_child"),
    "Conversation": ("nature", "human", "conversation"),
    "Shout": ("nature", "human", "shout"),
    "Bark": ("nature", "animal", "dog"),
    "Chirp_and_tweet": ("nature", "animal", "bird"),
    "Crow": ("nature", "animal", "bird"),
    "Owl": ("nature", "animal", "bird"),
    "Neigh_and_howling": ("nature", "animal", "mammal"),
    "Moo": ("nature", "animal", "mammal"),
    "Pig": ("nature", "animal", "mammal"),
    "Sheep": ("nature", "animal", "mammal"),
    "Chicken_and_rooster": ("nature", "animal", "bird"),
    "Duck": ("nature", "animal", "bird"),
    "Buzz": ("nature", "animal", "insect"),
    "Fly_and_housefly": ("nature", "animal", "insect"),
    "Mosquito": ("nature", "animal", "insect"),
    "Bee_and_wasp": ("nature", "animal", "insect"),
    "Cricket": ("nature", "animal", "insect"),
    "Tools": ("urban", "machine", "tools"),
    "Hammer": ("urban", "machine", "hammer"),
    "Sawing": ("urban", "machine", "saw"),
    "Filing_(rasp)": ("urban", "machine", "file"),
    "Vacuum_cleaner": ("urban", "domestic", "vacuum"),
    "Hair_dryer": ("urban", "domestic", "hair_dryer"),
    "Toilet_flush": ("urban", "domestic", "toilet"),
    "Running_water": ("urban", "domestic", "water"),
    "Dishes_and_pots_and_pans": ("urban", "domestic", "dishes"),
    "Microwave_oven": ("urban", "domestic", "microwave"),
    "Blender": ("urban", "domestic", "blender"),
    "Drawer_open_or_close": ("urban", "impact", "drawer"),
    "Tap": ("urban", "impact", "tap"),
    "Knock": ("urban", "impact", "knock"),
    "Slam": ("urban", "impact", "slam"),
    "Smash_and_crash": ("urban", "impact", "crash"),
    "Crackle": ("nature", "fire", "crackle"),
    "Thunderstorm": ("nature", "weather", "thunderstorm"),
    "Drip": ("nature", "water", "drip"),
    "Splash_and_splatter": ("nature", "water", "splash"),
    "Pour": ("nature", "water", "pour"),
    "Gurgling": ("nature", "water", "gurgle"),
    "Steam": ("nature", "water", "steam"),
    "Wind_noise_and_microphone_wind": ("nature", "weather", "wind"),
    "Waves_and_surf": ("nature", "water", "ocean"),
    "Raindrop": ("nature", "weather", "rain"),
    "Smoke_detector_and_smoke_alarm": ("urban", "alarm", "smoke_detector"),
    "Squeak": ("urban", "impact", "squeak"),
    "Scrape": ("urban", "impact", "scrape"),
    "Rattle": ("urban", "impact", "rattle"),
    "Whoosh_and_swoosh_and_swish": ("nature", "texture", "whoosh"),
    "Thump_and_thud": ("urban", "impact", "thud"),
    "Tick": ("urban", "domestic", "tick"),
    "Tick-tock": ("urban", "domestic", "clock"),
    "Mechanical_fan": ("urban", "machine", "fan"),
    "Air_conditioning": ("urban", "machine", "ac"),
    "Printer": ("urban", "machine", "printer"),
    "Computer_noise": ("urban", "machine", "computer"),
    "Television": ("urban", "domestic", "television"),
    "Radio": ("urban", "domestic", "radio"),
    "Burst_and_pop": ("urban", "impact", "burst"),
    "Explosion": ("urban", "impact", "explosion"),
    "Gunshot_and_gunfire": ("urban", "impact", "gunshot"),
    "Music": ("music", "electronic", "music"),
    "Musical_instrument": ("music", "electronic", "instrument"),
    "Bowed_string_instrument": ("music", "string_bowed", "bowed_strings"),
    "Plucked_string_instrument": ("music", "string_plucked", "plucked_strings"),
    "Tapping": ("music", "percussion", "tapping"),
    "Strum": ("music", "string_plucked", "strum"),
    # More human sounds
    "Chatter": ("nature", "human", "chatter"),
    "Walk_and_footsteps": ("urban", "human", "footsteps"),
    "Applause": ("nature", "human", "applause"),
    "Screaming": ("nature", "human", "screaming"),
    "Whistling": ("nature", "human", "whistling"),
    "Sigh": ("nature", "human", "sigh"),
    "Gasp": ("nature", "human", "gasp"),
    "Groan": ("nature", "human", "groan"),
    "Grunt": ("nature", "human", "grunt"),
    "Yell": ("nature", "human", "yell"),
    "Babble": ("nature", "human", "babble"),
    "Whispering": ("nature", "human", "whisper"),
    # More urban/domestic
    "Cutlery_and_silverware": ("urban", "domestic", "cutlery"),
    "Shatter": ("urban", "impact", "shatter"),
    "Writing": ("urban", "human", "writing"),
    "Crack": ("urban", "impact", "crack"),
    "Crushing": ("urban", "impact", "crushing"),
    "Bouncing": ("urban", "impact", "bouncing"),
    "Wobble": ("urban", "impact", "wobble"),
    "Jingle_and_bell": ("urban", "alarm", "jingle"),
    "Chime": ("urban", "alarm", "chime"),
    "Buzzer": ("urban", "alarm", "buzzer"),
    "Beep_and_bleep": ("urban", "alarm", "beep"),
    "Ding": ("urban", "alarm", "ding"),
    "Frying": ("urban", "domestic", "frying"),
    "Shuffling_cards": ("urban", "domestic", "cards"),
    "Scissors": ("urban", "domestic", "scissors"),
    "Rub": ("urban", "impact", "rub"),
    "Scratch": ("urban", "impact", "scratch"),
    "Squish": ("urban", "impact", "squish"),
    "Splash_and_splatter": ("nature", "water", "splash"),
    "Fill_(liquid)": ("nature", "water", "fill"),
    "Drip": ("nature", "water", "drip"),
    "Spray": ("nature", "water", "spray"),
    "Plop": ("nature", "water", "plop"),
    "Accelerating_and_revving_and_vroom": ("urban", "machine", "revving"),
    "Shuffling_cards": ("urban", "domestic", "cards"),
    "Zipper_(clothing)": ("urban", "domestic", "zipper"),
    "Fart": ("nature", "human", "fart"),
    "Burping_and_eructation": ("nature", "human", "burping"),
    "Wheeze": ("nature", "human", "wheeze"),
}


def scan_fsd50k(source_dir: Path, repo_root: Path, corpus_dir: Path) -> list[dict]:
    """Scan FSD50K eval audio and return manifest rows."""
    # Check multiple possible locations
    fsd_dir = None
    for candidate in [
        source_dir / "FSD50K_hf",           # HuggingFace download
        source_dir / "FSD50K.eval_audio",    # Zenodo zip extracted
    ]:
        if candidate.is_dir() and any(candidate.glob("*.wav")):
            fsd_dir = candidate
            break

    if fsd_dir is None:
        # Try extracting from zip
        zip_path = source_dir / "FSD50K.eval_audio.zip"
        if zip_path.exists():
            print(f"  Extracting {zip_path}...")
            import zipfile
            with zipfile.ZipFile(zip_path, 'r') as z:
                z.extractall(source_dir)
            fsd_dir = source_dir / "FSD50K.eval_audio"
        else:
            print(f"  FSD50K not found. Looked in: FSD50K_hf/, FSD50K.eval_audio/, FSD50K.eval_audio.zip")
            return []

    # Load ground truth
    gt_path = source_dir / "FSD50K.ground_truth" / "eval.csv"
    if not gt_path.exists():
        gt_zip = source_dir / "FSD50K.gt.zip"
        if gt_zip.exists():
            import zipfile
            with zipfile.ZipFile(gt_zip, 'r') as z:
                z.extractall(source_dir)
    if not gt_path.exists():
        print(f"  FSD50K ground truth not found at {gt_path}")
        return []

    with open(gt_path) as f:
        gt_rows = list(csv.DictReader(f))

    # Build filename → labels lookup
    file_labels = {}
    for row in gt_rows:
        fname = row["fname"]
        labels = [l.strip() for l in row["labels"].split(",")]
        file_labels[fname] = labels

    rows = []
    counters: dict[str, int] = {}
    processed = 0
    skipped = 0

    # Process each audio file
    for audio_file in sorted(fsd_dir.glob("*.wav")):
        fname = audio_file.stem  # e.g. "37199"
        labels = file_labels.get(fname, [])

        # Find the best matching taxonomy entry
        best_match = None
        for label in labels:
            if label in FSD50K_TAXONOMY:
                best_match = label
                break

        if best_match is None:
            skipped += 1
            continue

        cat, subcat, instrument = FSD50K_TAXONOMY[best_match]
        key = f"{cat}_{subcat}_{instrument}"
        counters[key] = counters.get(key, 0) + 1
        seq = counters[key]

        sample_id = f"{cat}_{subcat}_{instrument}_{seq:04d}"
        dest = corpus_dir / cat / subcat / f"{sample_id}.wav"
        meta_info = convert_to_standard(audio_file, dest)
        if meta_info is None:
            skipped += 1
            continue

        rel_path = str(dest.relative_to(repo_root))
        processed += 1

        rows.append({
            "sample_id": sample_id,
            "file_path": rel_path,
            "category": cat,
            "subcategory": subcat,
            "instrument": instrument,
            "tags": ";".join(labels),
            "duration": meta_info["duration"],
            "sample_rate": meta_info["sample_rate"],
            "source": "FSD50K",
            "source_id": audio_file.name,
            "license": "CC-BY",
            "pitch": "",
            "dynamic": "",
            "technique": "",
            "description": f"{instrument} from FSD50K ({best_match})",
        })

    print(f"  Processed: {processed}, Skipped (no match): {skipped}")
    return rows


def scan_librispeech(source_dir: Path, repo_root: Path, corpus_dir: Path) -> list[dict]:
    """Scan LibriSpeech dev-clean for voice/speech samples."""
    ls_dir = source_dir / "LibriSpeech" / "dev-clean"
    if not ls_dir.is_dir():
        # Try tar.gz
        tar_path = source_dir / "dev-clean.tar.gz"
        if not tar_path.exists():
            tar_path = source_dir / "librispeech" / "dev-clean.tar.gz"
        if tar_path.exists():
            print(f"  Extracting {tar_path}...")
            import tarfile
            with tarfile.open(tar_path, 'r:gz') as t:
                t.extractall(source_dir)
        else:
            print(f"  LibriSpeech not found at {ls_dir}")
            return []

    rows = []
    counters: dict[str, int] = {}

    # Navigate: dev-clean/{speaker_id}/{chapter_id}/{speaker_id}-{chapter_id}-{utterance_id}.flac
    for speaker_dir in sorted(ls_dir.iterdir()):
        if not speaker_dir.is_dir():
            continue
        for chapter_dir in sorted(speaker_dir.iterdir()):
            if not chapter_dir.is_dir():
                continue
            for audio_file in sorted(chapter_dir.glob("*.flac")):
                key = "nature_human_speech"
                counters[key] = counters.get(key, 0) + 1
                seq = counters[key]

                sample_id = f"nature_human_speech_{seq:04d}"
                dest = corpus_dir / "nature" / "human" / f"{sample_id}.wav"
                meta_info = convert_to_standard(audio_file, dest)
                if meta_info is None:
                    continue

                rel_path = str(dest.relative_to(repo_root))
                rows.append({
                    "sample_id": sample_id,
                    "file_path": rel_path,
                    "category": "nature",
                    "subcategory": "human",
                    "instrument": "speech",
                    "tags": "speech;clean;read",
                    "duration": meta_info["duration"],
                    "sample_rate": meta_info["sample_rate"],
                    "source": "LibriSpeech",
                    "source_id": audio_file.name,
                    "license": "CC-BY 4.0",
                    "pitch": "",
                    "dynamic": "",
                    "technique": "",
                    "description": f"clean speech from LibriSpeech {speaker_dir.name}-{chapter_dir.name}",
                })

    return rows


def generate_synthetic(repo_root: Path, corpus_dir: Path) -> list[dict]:
    """Generate synthetic textures (noise, tones) and return manifest rows."""
    rows = []
    sr = TARGET_SR

    # Noise types
    noise_types = {
        "white": lambda n: np.random.randn(n),
        "pink": lambda n: _pink_noise(n),
        "brown": lambda n: _brown_noise(n),
    }

    for noise_name, noise_fn in noise_types.items():
        for i in range(5):  # 5 variants each, 3-8 seconds
            dur = 3.0 + np.random.rand() * 5.0
            n_samples = int(dur * sr)
            y = noise_fn(n_samples)
            # Normalize
            y = y / (np.max(np.abs(y)) + 1e-10) * 0.9

            sample_id = f"texture_noise_{noise_name}_{i + 1:04d}"
            dest = corpus_dir / "texture" / "noise" / f"{sample_id}.wav"
            dest.parent.mkdir(parents=True, exist_ok=True)
            sf.write(str(dest), y, sr, format=TARGET_FORMAT, subtype=TARGET_SUBTYPE)

            rel_path = str(dest.relative_to(repo_root))
            rows.append({
                "sample_id": sample_id,
                "file_path": rel_path,
                "category": "texture",
                "subcategory": "noise",
                "instrument": noise_name,
                "tags": f"noise;{noise_name}",
                "duration": round(dur, 3),
                "sample_rate": sr,
                "source": "synthetic",
                "source_id": "",
                "license": "public_domain",
                "pitch": "",
                "dynamic": "",
                "technique": "",
                "description": f"{noise_name} noise",
            })

    # Tones (sine sweep across pitches)
    for midi_note in range(36, 85, 6):  # C2 to C7, every 6 semitones
        freq = 440.0 * 2 ** ((midi_note - 69) / 12.0)
        dur = 3.0
        t = np.linspace(0, dur, int(sr * dur), endpoint=False)
        y = 0.8 * np.sin(2 * np.pi * freq * t)
        # Fade in/out
        fade = int(0.05 * sr)
        y[:fade] *= np.linspace(0, 1, fade)
        y[-fade:] *= np.linspace(1, 0, fade)

        note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        note_name = note_names[midi_note % 12] + str(midi_note // 12 - 1)

        sample_id = f"texture_tone_sine_{note_name}_{midi_note:03d}"
        dest = corpus_dir / "texture" / "tone" / f"{sample_id}.wav"
        dest.parent.mkdir(parents=True, exist_ok=True)
        sf.write(str(dest), y, sr, format=TARGET_FORMAT, subtype=TARGET_SUBTYPE)

        rel_path = str(dest.relative_to(repo_root))
        rows.append({
            "sample_id": sample_id,
            "file_path": rel_path,
            "category": "texture",
            "subcategory": "tone",
            "instrument": "sine",
            "tags": "tone;sine;tonal",
            "duration": round(dur, 3),
            "sample_rate": sr,
            "source": "synthetic",
            "source_id": "",
            "license": "public_domain",
            "pitch": note_name,
            "dynamic": "",
            "technique": "",
            "description": f"sine tone {note_name} ({freq:.1f} Hz)",
        })

    return rows


def _pink_noise(n: int) -> np.ndarray:
    """Generate pink noise using Voss-McCartney algorithm."""
    rows_count = 16
    white = np.random.randn(rows_count, n)
    pink = np.cumsum(white, axis=1)
    return pink.sum(axis=0) / rows_count


def _brown_noise(n: int) -> np.ndarray:
    """Generate brown noise (integrated white noise)."""
    white = np.random.randn(n)
    return np.cumsum(white) / np.sqrt(n)


# ── Main ─────────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(description="Build standardized sound corpus")
    parser.add_argument("--output", type=Path, default=Path("data/corpus"))
    parser.add_argument("--manifest", type=Path, default=None)
    parser.add_argument("--source-dir", type=Path, default=Path("/tmp"))
    parser.add_argument("--sources", nargs="+", default=["ESC-50", "TinySOL", "Philharmonia", "synthetic"],
                        help="Sources to scan: ESC-50, TinySOL, Philharmonia, FSD50K, LibriSpeech, synthetic")
    parser.add_argument("--repo-root", type=Path, default=None)
    args = parser.parse_args()

    repo_root = args.repo_root or Path.cwd()
    corpus_dir = (repo_root / args.output).resolve()
    manifest_path = args.manifest or (corpus_dir / "manifest.csv")

    print("=" * 60)
    print("Sonic Atlas — Build Corpus")
    print("=" * 60)
    print(f"  Source dir: {args.source_dir}")
    print(f"  Output:     {corpus_dir}")
    print(f"  Manifest:   {manifest_path}")
    print(f"  Sources:    {', '.join(args.sources)}")

    all_rows = []

    # ── Scan each source ────────────────────────────────────────────────
    if "ESC-50" in args.sources:
        print("\n── Scanning ESC-50 ──")
        rows = scan_esc50(args.source_dir, repo_root, corpus_dir)
        print(f"  Processed: {len(rows)} clips")
        all_rows.extend(rows)

    if "TinySOL" in args.sources:
        print("\n── Scanning TinySOL ──")
        rows = scan_tinysol(args.source_dir, repo_root, corpus_dir)
        print(f"  Processed: {len(rows)} clips")
        all_rows.extend(rows)

    if "Philharmonia" in args.sources:
        print("\n── Scanning Philharmonia ──")
        rows = scan_philharmonia(args.source_dir, repo_root, corpus_dir)
        print(f"  Processed: {len(rows)} clips")
        all_rows.extend(rows)

    if "FSD50K" in args.sources:
        print("\n── Scanning FSD50K ──")
        rows = scan_fsd50k(args.source_dir, repo_root, corpus_dir)
        print(f"  Processed: {len(rows)} clips")
        all_rows.extend(rows)

    if "LibriSpeech" in args.sources:
        print("\n── Scanning LibriSpeech ──")
        rows = scan_librispeech(args.source_dir, repo_root, corpus_dir)
        print(f"  Processed: {len(rows)} clips")
        all_rows.extend(rows)

    if "synthetic" in args.sources:
        print("\n── Generating synthetic textures ──")
        rows = generate_synthetic(repo_root, corpus_dir)
        print(f"  Generated: {len(rows)} clips")
        all_rows.extend(rows)

    # ── Write manifest ──────────────────────────────────────────────────
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(manifest_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=MANIFEST_COLUMNS)
        writer.writeheader()
        for row in all_rows:
            writer.writerow({col: row.get(col, "") for col in MANIFEST_COLUMNS})

    print(f"\n{'=' * 60}")
    print(f"Manifest written: {manifest_path} ({len(all_rows)} entries)")

    # ── Summary ─────────────────────────────────────────────────────────
    cats = {}
    for row in all_rows:
        cat = row["category"]
        subcat = row["subcategory"]
        cats.setdefault(cat, {}).setdefault(subcat, 0)
        cats[cat][subcat] += 1

    print(f"\nCorpus summary:")
    total = 0
    for cat in sorted(cats):
        cat_total = sum(cats[cat].values())
        total += cat_total
        print(f"  {cat:15s} {cat_total:5d}")
        for subcat in sorted(cats[cat]):
            print(f"    {subcat:13s} {cats[cat][subcat]:5d}")
    print(f"  {'TOTAL':15s} {total:5d}")

    # Estimate size
    total_size = sum(
        (repo_root / row["file_path"]).stat().st_size
        for row in all_rows
        if (repo_root / row["file_path"]).exists()
    )
    print(f"\nEstimated corpus size: {total_size / 1024 / 1024:.1f} MB")


if __name__ == "__main__":
    main()

import os
import json
import argparse
from datetime import datetime, timedelta
import shutil

# -----------------------------
# CLI argument
# -----------------------------
ap = argparse.ArgumentParser(description="Generate sample baselines and changesets")
ap.add_argument("--wipe-cache", action="store_true", help="Wipe the cache folder before generating samples")
args = ap.parse_args()

CACHE_DIR = "cache"

# -----------------------------
# Wipe cache if requested
# -----------------------------
if args.wipe_cache and os.path.exists(CACHE_DIR):
    shutil.rmtree(CACHE_DIR)

# Create cache folder if it does not exist
os.makedirs(CACHE_DIR, exist_ok=True)

# Create component subfolder
component = "MyComponent"
component_dir = os.path.join(CACHE_DIR, component)
os.makedirs(component_dir, exist_ok=True)

# -----------------------------
# Helper to write JSON
# -----------------------------
def write_json(filename, obj):
    with open(os.path.join(component_dir, filename), "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)

# -----------------------------
# Baselines with creation dates
# -----------------------------
base_date = datetime(2020, 1, 15, 10, 0, 0)
def d(days):
    return (base_date + timedelta(days=days)).isoformat() + "Z"

baselines = {
    "baselines": [
        {"uuid": "bl1",   "name": "1.0.0",                "creation_date": d(0)},
        {"uuid": "bl1r",  "name": "1.0.0-rerelease",      "creation_date": d(30)},
        {"uuid": "bl2",   "name": "1.1.0",                "creation_date": d(120)},
        {"uuid": "bl3a",  "name": "1.1.1-hotfix-A",       "creation_date": d(150)},
        {"uuid": "bl3b",  "name": "1.1.1-hotfix-B",       "creation_date": d(160)},
        {"uuid": "bl4",   "name": "2.0.0",                "creation_date": d(365)},
        {"uuid": "bl5x",  "name": "2.1.0-feature-X",      "creation_date": d(420)},
        {"uuid": "bl5y",  "name": "2.1.0-feature-Y",      "creation_date": d(430)},
        {"uuid": "bl5z",  "name": "2.1.0-feature-Z",      "creation_date": d(440)},
        {"uuid": "bl_b1", "name": "banana-1.0.0",         "creation_date": d(40)},
        {"uuid": "bl_b2", "name": "banana-1.1.0",         "creation_date": d(90)},
        {"uuid": "bl_b3", "name": "banana-1.2.0",         "creation_date": d(140)},
        {"uuid": "bl_a1", "name": "apple-2.0.0",          "creation_date": d(380)},
        {"uuid": "bl_a2", "name": "apple-2.0.1",          "creation_date": d(395)},
        {"uuid": "bl_a22", "name": "apple-2.0.2",          "creation_date": d(398)},
        {"uuid": "bl_a3", "name": "apple-2.1.0",          "creation_date": d(410)},
        {"uuid": "bl_a4", "name": "apple-3.0.0",          "creation_date": d(470)},
        {"uuid": "bl6",   "name": "2.2.0-merge",          "creation_date": d(480)},
        {"uuid": "bl7",   "name": "2.2.0-rebaseline",     "creation_date": d(520)},
        {"uuid": "bl8a",  "name": "2.3.0-hotfix-A",       "creation_date": d(560)},
        {"uuid": "bl8b",  "name": "2.3.0-hotfix-B",       "creation_date": d(565)},
        {"uuid": "bl9",   "name": "2.4.0-final-merge",    "creation_date": d(610)}
    ]
}

# Write baselines as a list to match lscm output format
# The lscm output is a JSON list with a single object containing the "baselines" key.
write_json("baselines.json", [baselines])

# -----------------------------
# Changesets JSONs (keys match baseline IDs)
# -----------------------------
cs_sets = {
    "bl1_2020": ["cs1","cs2"],
    "bl1r_2021": ["cs1","cs2"],
    "bl2_2021": ["cs1","cs2","cs3"],
    "bl3a_2021": ["cs1","cs2","cs4"],
    "bl3b_2021": ["cs1","cs2","cs4"],
    "bl4_2022": ["cs1","cs2","cs3","cs4"],
    "bl5x_2022": ["cs1","cs2","cs3","cs4","cs5"],
    "bl5y_2022": ["cs1","cs2","cs3","cs4","cs6"],
    "bl5z_2022": ["cs1","cs2","cs3","cs4","cs6","cs6_2"],
    "bl6_2022": ["cs1","cs2","cs3","cs4","cs5","cs6"],
    "bl7_2023": ["cs1","cs2","cs3","cs4","cs5","cs6"],
    "bl8a_2023": ["cs1","cs2","cs3","cs4","cs5","cs6","cs7"],
    "bl8b_2023": ["cs1","cs2","cs3","cs4","cs5","cs6","cs8"],
    "bl9_2024": ["cs1","cs2","cs3","cs4","cs5","cs6","cs7","cs8"],

    "bl_b1_2021": ["cs1","cs2","cs10"],
    "bl_b2_2021": ["cs1","cs2","cs10","cs11"],
    "bl_b3_2021": ["cs1","cs2","cs10","cs11","cs12"],

    "bl_a1_2022": ["cs1","cs2","cs3","cs4","cs20"],
    "bl_a2_2022": ["cs1","cs2","cs3","cs4","cs20","cs23"],
    "bl_a22_2022": ["cs1","cs2","cs3","cs4","cs20","cs23","cs22"],
    "bl_a3_2022": ["cs1","cs2","cs3","cs4","cs20","cs21"],
    "bl_a4_2022": ["cs1","cs2","cs3","cs4","cs20","cs21","cs22","cs23"],
}

# Write changesets JSON files
for name, cs in cs_sets.items():
    write_json(f"cs_{name}.json", {"changes": [{"uuid": c, "name": c} for c in cs]})

print(f"Cache updated: {len(baselines['baselines'])} baselines and {len(cs_sets)} changesets files.")

# Note: lscm outputs baselines as a JSON list with a single object
#       containing the "baselines" array. We wrote the sample
#       generator to match that format (a list containing the dict).

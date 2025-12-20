import os, json, zipfile

# Create cache folder
os.makedirs("cache", exist_ok=True)

# Helper to write JSON
def write_json(filename, obj):
    with open(os.path.join("cache", filename), "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)

# Baselines
baselines = {
    "baselines": [
        {"id": "bl1", "name": "1.0.0"},
        {"id": "bl1r", "name": "1.0.0-rerelease"},
        {"id": "bl2", "name": "1.1.0"},
        {"id": "bl3a", "name": "1.1.1-hotfix-A"},
        {"id": "bl3b", "name": "1.1.1-hotfix-B"},
        {"id": "bl4", "name": "2.0.0"},
        {"id": "bl5x", "name": "2.1.0-feature-X"},
        {"id": "bl5y", "name": "2.1.0-feature-Y"},
        {"id": "bl6", "name": "2.2.0-merge"},
        {"id": "bl7", "name": "2.2.0-rebaseline"},
        {"id": "bl8a", "name": "2.3.0-hotfix-A"},
        {"id": "bl8b", "name": "2.3.0-hotfix-B"},
        {"id": "bl9", "name": "2.4.0-final-merge"}
    ]
}
write_json("baselines_MyComponent.json", baselines)

# Changesets
cs_sets = {
    "bl1_2020": ["cs1","cs2"],
    "bl1r_2021": ["cs1","cs2"],
    "bl2_2021": ["cs1","cs2","cs3"],
    "bl3a_2021": ["cs1","cs2","cs4"],
    "bl3b_2021": ["cs1","cs2","cs4"],
    "bl4_2022": ["cs1","cs2","cs3","cs5"],
    "bl5x_2022": ["cs1","cs2","cs3","cs5","cs6"],
    "bl5y_2022": ["cs1","cs2","cs3","cs5","cs7"],
    "bl6_2022": ["cs1","cs2","cs3","cs5","cs6"],
    "bl7_2023": ["cs1","cs2","cs3","cs5","cs6"],
    "bl8a_2023": ["cs1","cs2","cs3","cs5","cs6","cs8"],
    "bl8b_2023": ["cs1","cs2","cs3","cs5","cs6","cs9"],
    "bl9_2024": ["cs1","cs2","cs3","cs4","cs5","cs6","cs8","cs9"]
}

for name, cs in cs_sets.items():
    write_json(f"cs_{name}.json", {"changeSets": [{"id": c, "name": c} for c in cs]})

# Create the zip
with zipfile.ZipFile("baseline_demo_all_permutations_samples.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for root, _, files in os.walk("cache"):
        for f in files:
            z.write(os.path.join(root, f), arcname=os.path.join("cache", f))

print("ZIP created: baseline_demo_all_permutations_samples.zip")

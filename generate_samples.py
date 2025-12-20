import os, json, zipfile

# -----------------------
# Helper
# -----------------------
os.makedirs("cache", exist_ok=True)
def write_json(filename, obj):
    with open(os.path.join("cache", filename), "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)

# -----------------------
# Baselines JSON
# -----------------------
baselines = {
    "baselines": [
        # Original mainline & side-branches
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
        {"id": "bl9", "name": "2.4.0-final-merge"},

        # Fruit branches derived from mainline
        {"id": "banana-1", "name": "banana-1.0.0"},  # from 1.0.0
        {"id": "banana-1.1", "name": "banana-1.1.0"}, # node 2

        {"id": "apple-2", "name": "apple-2.0.0"},    # from 2.0.0
        {"id": "apple-2.0.1", "name": "apple-2.0.1"},# merges later
        {"id": "apple-2.1", "name": "apple-2.1.0"},  # split
        {"id": "apple-3", "name": "apple-3.0.0"}     # split merge
    ]
}
write_json("baselines_MyComponent.json", baselines)

# -----------------------
# Changesets JSONs
# -----------------------
cs_sets = {
    # Original baselines
    "bl1_2020": ["cs1","cs2"],
    "bl1r_2021": ["cs1","cs2"],
    "bl2_2021": ["cs1","cs2","cs3"],
    "bl3a_2021": ["cs1","cs2","cs4"],
    "bl3b_2021": ["cs1","cs2","cs4"],
    "bl4_2022": ["cs3","cs4"],  # mainline 2.0.0
    "bl5x_2022": ["cs3","cs4","cs5"],
    "bl5y_2022": ["cs3","cs4","cs6"],
    "bl6_2022": ["cs3","cs4","cs5","cs6"],
    "bl7_2023": ["cs3","cs4","cs5","cs6"],
    "bl8a_2023": ["cs3","cs4","cs5","cs6","cs7"],
    "bl8b_2023": ["cs3","cs4","cs5","cs6","cs8"],
    "bl9_2024": ["cs3","cs4","cs5","cs6","cs7","cs8"],

    # Fruit branch: banana
    "banana-1_2021": ["cs1","cs2","cs10"],       # derived from 1.0.0
    "banana-1.1_2021": ["cs1","cs2","cs10","cs11"], # successor

    # Fruit branch: apple splits & merges
    "apple-2_2022": ["cs3","cs4","cs20"],             # successor of mainline 2.0.0
    "apple-2.0.1_2022": ["cs3","cs4","cs20","cs23"], # successor of apple-2.0.0
    "apple-2.1_2022": ["cs3","cs4","cs20","cs21"],   # split branch, successor of apple-2.0.0
    "apple-3_2022": ["cs3","cs4","cs20","cs21","cs22","cs23"], # merges apple-2.0.1 & apple-2.1.0

}

# Write changesets JSON files
for name, cs in cs_sets.items():
    write_json(f"cs_{name}.json", {"changeSets": [{"id": c, "name": c} for c in cs]})

# -----------------------
# Create ZIP of cache
# -----------------------
zip_filename = "baseline_demo_fruit_corrected.zip"
with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as z:
    for root, _, files in os.walk("cache"):
        for f in files:
            z.write(os.path.join(root, f), arcname=os.path.join("cache", f))

print(f"ZIP created: {zip_filename}")
print("Cache updated: original branches preserved + fruit branches with correct successors/merges.")

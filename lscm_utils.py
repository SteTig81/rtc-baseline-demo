
import subprocess
import json
import os
import logging
import datetime

logger = logging.getLogger(__name__)

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def run_lscm(args, cache_file=None):
    if cache_file and os.path.exists(cache_file):
        logger.info(f"Using cache {cache_file}")
        with open(cache_file, "r", encoding="utf-8") as f:
            return json.load(f)

    logger.info("Running lscm " + " ".join(args))
    result = subprocess.run(["lscm"] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    data = json.loads(result.stdout)

    if cache_file:
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    return data

def list_baselines(server, component):
    component_dir = os.path.join(CACHE_DIR, component)
    os.makedirs(component_dir, exist_ok=True)
    cache_file = os.path.join(component_dir, "baselines.json")
    data = run_lscm(["list", "baselines", "-r", server, "-C", component, "-m", "all", "-j"], cache_file)
    # data is now a list: [ { "baselines": [...] } ]
    if isinstance(data, list) and data:
        return data[0].get("baselines", [])
    return []

def list_changesets_yearly(server, component, baseline_id, start_year=2020):
    """
    Load changesets for a baseline, aggregated by year.
    Raises an exception if no changesets are found.
    """
    now = datetime.datetime.utcnow().year
    all_cs = []
    component_dir = os.path.join(CACHE_DIR, component)
    os.makedirs(component_dir, exist_ok=True)

    for year in range(start_year, now + 1):
        since = f"{year}-01-01"
        until = f"{year + 1}-01-01"
        cache_file = os.path.join(component_dir, f"cs_{baseline_id}_{year}.json")
        if os.path.exists(cache_file):
            with open(cache_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                all_cs.extend(data.get("changes", []))
        else:
            # If not cached, run lscm
            data = run_lscm(["list", "changesets", "-r", server, "-C", component, "-b", baseline_id, "--created-after", since, "--created-before", until, "-m", "all", "-j"], cache_file)
            all_cs.extend(data.get("changes", []))

    if not all_cs:
        raise ValueError(f"No changesets found for baseline '{baseline_id}' from year {start_year} to {now}!")

    return all_cs


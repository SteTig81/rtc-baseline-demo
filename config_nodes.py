import hashlib
import logging

logger = logging.getLogger(__name__)

def cfg_id(cs_ids):
    h = hashlib.sha1("".join(sorted(cs_ids)).encode())
    return "cfg_" + h.hexdigest()[:12]

def build_config_nodes(baselines):
    nodes = {}

    for bl in baselines:
        cs_json = bl["changesets_json"]
        cs_ids = sorted(cs["id"] for cs in cs_json)
        cid = cfg_id(cs_ids)

        if cid not in nodes:
            nodes[cid] = {
                "id": cid,
                "bl_count": 0,
                "cs_count": len(cs_json),
                "baselines": [],
                "changesets": cs_json
            }

        # Copy the baseline without 'changesets_json'
        bl_copy = {k: v for k, v in bl.items() if k != "changesets_json"}

        nodes[cid]["baselines"].append(bl_copy)
        nodes[cid]["bl_count"] += 1

    # Sort baselines in each node by creation_date (earliest first)
    for node in nodes.values():
        node["baselines"].sort(key=lambda b: b.get("creation_date", "9999-12-31"))

    return list(nodes.values())

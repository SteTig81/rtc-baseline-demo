
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

        nodes[cid]["baselines"].append(bl)
        nodes[cid]["bl_count"] += 1

    return list(nodes.values())

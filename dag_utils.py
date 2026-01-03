from collections import defaultdict
from itertools import combinations
import logging

logger = logging.getLogger(__name__)

def build_dag_edges(nodes):
    edges = defaultdict(list)
    for a, b in combinations(nodes, 2):
        sa = {c["uuid"] for c in a["changesets"]}
        sb = {c["uuid"] for c in b["changesets"]}
        if sa < sb:
            edges[a["id"]].append(b["id"])
        elif sb < sa:
            edges[b["id"]].append(a["id"])
    return edges

def remove_transitive_edges(edges):
    """
    Removes transitive edges from a DAG.
    If A -> B and A -> C and B -> C, then A -> C is removed.
    """
    reduced = {src: set(dsts) for src, dsts in edges.items()}
    nodes = list(reduced.keys())

    for src in nodes:
        direct = set(reduced.get(src, []))
        for mid in list(direct):
            for dst in reduced.get(mid, []):
                if dst in direct:
                    reduced[src].discard(dst)

    return {k: sorted(v) for k, v in reduced.items() if v}

def assign_predecessors(nodes, edges):
    node_map = {n["id"]: n for n in nodes}
    for n in nodes:
        preds = []
        for src, dsts in edges.items():
            if n["id"] in dsts:
                preds.append(node_map[src])
        # Sort predecessors by cs_count descending
        preds.sort(key=lambda x: x["cs_count"], reverse=True)
        n["predecessors"] = [p["id"] for p in preds]

def compute_root_distance(nodes):
    """Compute root_distance for each node in the DAG."""
    node_map = {n["id"]: n for n in nodes}

    # Initialize all distances as None
    for n in nodes:
        n["root_distance"] = None

    # Start with root nodes (no predecessors)
    queue = [n for n in nodes if not n.get("predecessors")]
    for n in queue:
        n["root_distance"] = 0

    # BFS traversal to assign distances
    while queue:
        current = queue.pop(0)
        cur_dist = current["root_distance"]
        # Find nodes for which current is a predecessor
        for n in nodes:
            if current["id"] in n.get("predecessors", []):
                if n["root_distance"] is None or n["root_distance"] < cur_dist + 1:
                    n["root_distance"] = cur_dist + 1
                    queue.append(n)

def compute_mainline(nodes):
    """
    Compute mainline nodes using root_distance.
    The mainline follows the longest path from any root to a leaf.
    Works for multiple partial trees.
    """
    node_map = {n["id"]: n for n in nodes}

    # Initialize
    for n in nodes:
        n["mainline"] = False

    # Find leaves (nodes with largest root_distance)
    max_distance = max(n["root_distance"] for n in nodes if n["root_distance"] is not None)
    leaves = [n for n in nodes if n["root_distance"] == max_distance]

    for leaf in leaves:
        cur = leaf
        while cur:
            cur["mainline"] = True
            if not cur.get("predecessors"):
                break
            preds = [node_map[p] for p in cur["predecessors"]]
            # Choose predecessor with largest root_distance, tie-breaker cs_count
            cur = max(preds, key=lambda x: (x["root_distance"], x["cs_count"]))


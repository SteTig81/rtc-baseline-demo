
from collections import defaultdict
from itertools import combinations
import logging

logger = logging.getLogger(__name__)

def build_dag_edges(nodes):
    edges = defaultdict(list)
    for a, b in combinations(nodes, 2):
        sa = {c["id"] for c in a["changesets"]}
        sb = {c["id"] for c in b["changesets"]}
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
        preds.sort(key=lambda x: x["cs_count"], reverse=True)
        n["predecessors"] = [p["id"] for p in preds]

def compute_mainline(nodes):
    node_map = {n["id"]: n for n in nodes}
    dp = {}

    ordered = sorted(nodes, key=lambda n: n["cs_count"])
    for n in ordered:
        if not n["predecessors"]:
            dp[n["id"]] = (1, n["cs_count"], None)
        else:
            best = max(
                ((dp[p][0], dp[p][1], p) for p in n["predecessors"] if p in dp),
                key=lambda x: (x[0], x[1])
            )
            dp[n["id"]] = (best[0] + 1, best[1] + n["cs_count"], best[2])

    leaf = max(dp.items(), key=lambda x: (x[1][0], x[1][1]))[0]
    cur = leaf
    while cur:
        node_map[cur]["mainline"] = True
        cur = dp[cur][2]

    for n in nodes:
        n.setdefault("mainline", False)

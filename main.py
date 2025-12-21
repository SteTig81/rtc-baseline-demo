
import argparse
import logging
from lscm_utils import list_baselines, list_changesets_yearly
from config_nodes import build_config_nodes
from dag_utils import build_dag_edges, remove_transitive_edges, assign_predecessors, compute_root_distance, compute_mainline
from export_graph import export_graph

logging.basicConfig(level=logging.INFO)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", required=True)
    ap.add_argument("--output", default="baseline_history.json")
    args = ap.parse_args()

    baselines = list_baselines(args.component)
    for bl in baselines:
        bl["changesets_json"] = list_changesets_yearly(bl["id"])

    nodes = build_config_nodes(baselines)
    edges = remove_transitive_edges(build_dag_edges(nodes))
    assign_predecessors(nodes, edges)
    compute_root_distance(nodes)
    compute_mainline(nodes)
    export_graph(nodes, edges, args.output)

if __name__ == "__main__":
    main()

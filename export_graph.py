
import json
import logging

logger = logging.getLogger(__name__)

def export_graph(nodes, edges, filename):
    links = [{"source": s, "target": t} for s, ts in edges.items() for t in ts]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump({"nodes": nodes, "links": links}, f, indent=2)

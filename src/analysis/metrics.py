from __future__ import annotations

import math
from collections import defaultdict

import networkx as nx
import numpy as np
from scipy.spatial import Delaunay, QhullError


def _geometry(records):
    if not records:
        return {"cell_count": 0, "area": 0.0, "center_x": 0.0, "center_y": 0.0,
                "expanse": 0.0, "sparsity": 0.0}
    weights = np.array([math.pi * float(r["R"]) ** 2 for r in records])
    positions = np.array([[r["x"], r["y"]] for r in records], dtype=float)
    total_area = float(weights.sum())
    center = (weights[:, None] * positions).sum(axis=0) / total_area if total_area else np.zeros(2)
    distances = np.linalg.norm(positions - center, axis=1) + np.array([r["R"] for r in records])
    expanse = float(distances.max()) if len(distances) else 0.0
    sparsity = float(math.pi * expanse**2 / total_area) if total_area else 0.0
    return {"cell_count": len(records), "area": total_area,
            "center_x": float(center[0]), "center_y": float(center[1]),
            "expanse": expanse, "sparsity": sparsity}


def build_spatial_graph(records):
    graph = nx.Graph()
    for record in records:
        graph.add_node(int(record["cell_id"]), record=record)
    if len(records) < 3:
        if len(records) == 2:
            graph.add_edge(int(records[0]["cell_id"]), int(records[1]["cell_id"]))
        return graph
    positions = np.array([[r["x"], r["y"]] for r in records], dtype=float)
    try:
        triangulation = Delaunay(positions)
    except QhullError:
        return graph
    for simplex in triangulation.simplices:
        for i in range(3):
            for j in range(i + 1, 3):
                graph.add_edge(int(records[simplex[i]]["cell_id"]), int(records[simplex[j]]["cell_id"]))
    return graph


def build_lineage_graph(records):
    graph = nx.DiGraph()
    ids = {int(r["cell_id"]) for r in records}
    graph.add_nodes_from(ids)
    for record in records:
        parent_id = record.get("parent_id")
        if parent_id is not None and int(parent_id) in ids:
            graph.add_edge(int(parent_id), int(record["cell_id"]))
    return graph


def calculate_connectivity(records):
    spatial = build_spatial_graph(records)
    lineage = build_lineage_graph(records)
    lineage_edges = {tuple(sorted(edge)) for edge in lineage.edges}
    spatial_edges = {tuple(sorted(edge)) for edge in spatial.edges}
    return len(lineage_edges & spatial_edges) / len(lineage_edges) if lineage_edges else 0.0


def subcolony_components(records):
    spatial = build_spatial_graph(records)
    groups = defaultdict(list)
    for record in records:
        if record.get("subcolony_id") is not None:
            groups[int(record["subcolony_id"])].append(int(record["cell_id"]))
    result = {}
    for subcolony_id, ids in groups.items():
        subgraph = spatial.subgraph(ids)
        result[subcolony_id] = {
            "cell_count": len(ids),
            "connected_components": nx.number_connected_components(subgraph),
        }
    return result


def calculate_snapshot_metrics(records):
    geometry = _geometry(records)
    subcolonies = subcolony_components(records) if records else {}
    return {
        "time": float(records[0]["time"]) if records else 0.0,
        **geometry,
        "connectivity": calculate_connectivity(records) if records else 0.0,
        "subcolonies": len(subcolonies),
        "largest_subcolony": max((v["cell_count"] for v in subcolonies.values()), default=0),
        "component_count": sum(v["connected_components"] for v in subcolonies.values()),
    }


def calculate_all_metrics(snapshot_records):
    by_time = defaultdict(list)
    for record in snapshot_records:
        by_time[float(record["time"])].append(record)
    return [calculate_snapshot_metrics(by_time[t]) for t in sorted(by_time)]


def birth_location_metrics(snapshot_records, births):
    if not snapshot_records:
        return []
    final_time = max(float(row["time"]) for row in snapshot_records)
    final = calculate_snapshot_metrics([row for row in snapshot_records if float(row["time"]) == final_time])
    center = np.array([final["center_x"], final["center_y"]])
    expanse = final["expanse"] or 1.0
    return [{**birth, "normalized_birth_location": float(
        np.linalg.norm(np.array([birth["birth_x"], birth["birth_y"]]) - center) / expanse
    )} for birth in births]

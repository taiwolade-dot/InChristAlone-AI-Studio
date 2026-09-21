def prepare_graph_visualization(graph):

    nodes = []
    edges = []

    seen_nodes = set()

    for item in graph:

        source = item.get("source")
        target = item.get("target")

        if source and source not in seen_nodes:
            nodes.append(
                {
                    "id": source,
                    "label": source
                }
            )
            seen_nodes.add(source)

        if target and target not in seen_nodes:
            nodes.append(
                {
                    "id": target,
                    "label": target
                }
            )
            seen_nodes.add(target)

        edges.append(
            {
                "from": source,
                "to": target,
                "label": item.get(
                    "relationship",
                    "related"
                )
            }
        )

    return {
        "nodes": nodes,
        "edges": edges,
        "node_count": len(nodes),
        "edge_count": len(edges)
    }

from dataclasses import dataclass


@dataclass
class GraphNode:

    name: str
    node_type: str

    file: str

    metadata: dict
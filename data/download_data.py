import osmnx as ox
import numpy as np
import json


class Logger:

    def __init__(self, m_log: bool) -> None:
        self.m_log = m_log
    
    def log(self, message: str) -> None:
        if self.m_log:
            print(message)

logger = Logger(True)


def graph_from_place(place: str = "Rio de Janeiro") -> any:
    logger.log("Downloading data")
    return ox.graph_from_place(place, simplify=False, truncate_by_edge=True, network_type="drive")

def add_travel_time_to_graph(graph: any) -> None:
    logger.log("Adding travel time")
    graph = ox.speed.add_edge_speeds(graph)
    graph = ox.speed.add_edge_travel_times(graph)

def make_dict_from_graph(graph: any) -> dict:
    nodes = []
    edges = []

    new_ids = {}

    logger.log("Adding nodes")
    # Add nodes
    for node_original_id in graph.nodes:

        node = graph.nodes[node_original_id]
        new_ids[node_original_id] = len(nodes) # Assign new id to nodes

        lat = node["y"]
        lng = node["x"]
        street_count = node["street_count"]

        nodes.append((lat, lng, street_count))
    logger.log(f"Added {len(nodes)} nodes")
    
    logger.log("Adding edges")
    # Add edges
    for edge_key in graph.edges:

        edge_info = graph.edges[edge_key]

        first_node_new_id = new_ids[edge_key[0]]
        second_node_new_id = new_ids[edge_key[1]]

        street_name = edge_info.get("name", None)
        street_travel_time = edge_info.get("travel_time", None)
        street_length = edge_info.get("length", None)
        street_oneway = edge_info.get("oneway", None)
        street_reversed = edge_info.get("reversed", None)
        street_lanes = edge_info.get("lanes", None)


        cleaned_edge = (
            first_node_new_id,
            second_node_new_id,
            street_name, 
            street_travel_time, 
            street_length, 
            street_oneway, 
            street_reversed, 
            street_lanes
        )
        check_edge_attribute_types(cleaned_edge)


        edges.append(cleaned_edge)
    logger.log(f"Added {len(edges)} edges")
    
    return {"nodes": nodes, "edges": edges}

def check_edge_attribute_types(cleaned_edge: tuple) -> None:
    """
    Print warning if any attribute with wrong type
    """

    types = [
        ("street_name", str),
        ("street_travel_time", float),
        ("street_length", np.float64),
        ("street_oneway", bool),
        ("street_reversed", bool),
        ("street_lanes", str)
    ]

    for attr_idx in range(2, len(types) + 2): # First two attributes are node ids
        attr_name, attr_correct_type = types[attr_idx - 2]
        attr_actual_type = type(cleaned_edge[attr_idx])

        if not isinstance(cleaned_edge[attr_idx], attr_correct_type):
            if cleaned_edge[attr_idx] is None:
                continue
            print(f"Warning: attribute '{attr_name}' of edge ({cleaned_edge[0]}, {cleaned_edge[1]}) not of type {attr_correct_type}, but {attr_actual_type} instead")

def make_json_from_dict(graph: dict, path: str) -> None:
    logger.log("Dumping to json")
    with open(path + ".json", "w", encoding="utf8") as file:
        json.dump(graph, file)


if __name__ == "__main__":
    place = "Rio de Janeiro"
    g = graph_from_place(place)
    add_travel_time_to_graph(g)
    a = make_dict_from_graph(g)
    make_json_from_dict(a, place)
    logger.log("Done")
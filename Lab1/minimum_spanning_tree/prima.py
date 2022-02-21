import os
import random
import time
from itertools import combinations, groupby

import firebase_admin
import networkx as nx
from firebase_admin import credentials, firestore
from tqdm import tqdm

import tree


def gnp_random_connected_graph(num_of_nodes: int,
                               completeness: float,
                               draw: bool = False) -> nx.Graph:
    edges = combinations(range(num_of_nodes), 2)
    graph = nx.Graph()
    graph.add_nodes_from(range(num_of_nodes))

    for _, node_edges in groupby(edges, key=lambda x: x[0]):
        node_edges = list(node_edges)
        random_edge = random.choice(node_edges)
        graph.add_edge(*random_edge)
        for e in node_edges:
            if random.random() < completeness:
                graph.add_edge(*e)

    for (u, v, w) in graph.edges(data=True):
        w['weight'] = random.randint(0, 500)

    return graph


def get_firebase(algorithm):
    cred = credentials.Certificate('firebase_token.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db.collection('dm_lab09').document(algorithm)


def main(algorithm):
    doc = get_firebase(algorithm)
    for nodes in tqdm(range(1, 752, 10)):
        time_taken = 0
        for i in range(100):
            graph = gnp_random_connected_graph(nodes, 0.9, False)

            start = time.perf_counter()
            tree.minimum_spanning_tree(graph, algorithm=algorithm)
            end = time.perf_counter()

            time_taken += end - start

        doc.update({
            str(nodes): (time_taken / 100)
        })


if __name__ == '__main__':
    main(os.getenv('algorithm'))

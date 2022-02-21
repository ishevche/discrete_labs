import heapq

import networkx as nx


def minimum_spanning_tree(graph: nx.Graph, algorithm):
    if algorithm == 'prima':
        prima(graph)
    else:
        kruskal(graph)


def calculate(graph: nx.Graph):
    ans = 0
    edges = graph.edges(data=True)
    for _, _, data in edges:
        ans += data['weight']
    return ans


def kruskal(graph):
    def get_root_parent(ver: int) -> int:
        if ver == parents[ver]:
            return ver
        return get_root_parent(parents[ver])

    answer_tree = nx.Graph()
    answer_tree.add_nodes_from(range(len(graph)))
    edges = list(graph.edges(data=True))
    edges.sort(key=lambda x: x[2]['weight'])
    parents = [-1] * len(graph)
    size = [1] * len(graph)
    for u in graph.nodes():
        parents[u] = u
    for u, v, data in edges:
        u_parent = get_root_parent(u)
        v_parent = get_root_parent(v)
        if u_parent == v_parent:
            continue
        if size[u_parent] < size[v_parent]:
            u_parent, v_parent = v_parent, u_parent
        parents[v_parent] = u_parent
        size[u_parent] += size[v_parent]
        answer_tree.add_edge(u, v, **data)
    return answer_tree


def prima(graph):
    queue = []

    graph_edges = [[] for _ in range(len(graph))]
    for idx, (u, v, data) in enumerate(graph.edges(data=True)):
        graph_edges[u] += [(data['weight'], idx, v, u)]
        graph_edges[v] += [(data['weight'], idx, u, v)]
    edge_used = [False] * len(graph.edges())
    node_used = [False] * len(graph)

    nodes_got = 1
    nodes_to_get = len(graph)
    answer_graph = nx.Graph()
    answer_graph.add_node(0)
    for edge in graph_edges[0]:
        heapq.heappush(queue, edge)
        edge_used[edge[1]] = True
    node_used[0] = True

    while nodes_got < nodes_to_get:
        edge = heapq.heappop(queue)
        if node_used[edge[2]] and node_used[edge[3]]:
            continue
        if node_used[edge[2]]:
            node_used[edge[3]] = True
            nodes_got += 1
            answer_graph.add_edge(edge[2], edge[3], weight=edge[0])
            for u_edge in graph_edges[edge[3]]:
                if not node_used[u_edge[2]]:
                    heapq.heappush(queue, u_edge)
        else:
            node_used[edge[2]] = True
            nodes_got += 1
            answer_graph.add_edge(edge[2], edge[3], weight=edge[0])
            for u_edge in graph_edges[edge[2]]:
                if not node_used[u_edge[2]]:
                    heapq.heappush(queue, u_edge)

    return answer_graph

import matplotlib.pyplot as plt
import networkx as nx
import random

def grow_compact_square_island(n_nodes, seed=(0, 0)):
    G = nx.Graph()
    G.add_node(seed)

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    frontier = set(
        (seed[0] + dx, seed[1] + dy)
        for dx, dy in directions
    )

    while len(G) < n_nodes:
        # compute weights = number of occupied neighbors
        candidates = list(frontier)
        weights = []

        for x, y in candidates:
            w = sum(
                (x + dx, y + dy) in G
                for dx, dy in directions
            )
            weights.append((w + 1) ** 2)  # +1 avoids zero probability

        new_node = random.choices(candidates, weights=weights, k=1)[0]
        frontier.remove(new_node)

        G.add_node(new_node)

        for dx, dy in directions:
            nbr = (new_node[0] + dx, new_node[1] + dy)
            if nbr in G:
                G.add_edge(new_node, nbr)
            else:
                frontier.add(nbr)

    return G

def prune_degree_one_nodes(G):
    G = G.copy()  # don’t destroy original graph

    while True:
        leaves = [n for n, d in G.degree() if d == 1]
        if not leaves:
            break
        G.remove_nodes_from(leaves)

    return G

G = grow_compact_square_island(500)

G = prune_degree_one_nodes(G)

pos = {node: node for node in G.nodes()}  # (x, y) positions

plt.figure(figsize=(6, 6))
nx.draw(
    G,
    pos=pos,
    node_size=30,
    node_color="black",
    edge_color="gray",
    with_labels=False
)
plt.axis("equal")
plt.show()

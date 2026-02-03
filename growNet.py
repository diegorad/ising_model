import matplotlib.pyplot as plt
import networkx as nx
import random
import sys
from tools import *

def prune_degree_one_nodes(G):
	G = G.copy()  # don’t destroy original graph

	while True:
		leaves = [n for n, d in G.degree() if d == 1]
		if not leaves:
			break
		G.remove_nodes_from(leaves)

	return G

#################
size = 250
ratio = 0.35
S = {0: 1, 1: 4}
replacement = 0.15
#################

#Argument parsing
while sys.argv:
	if sys.argv[0] == "--ratio":
		ratio = float(sys.argv[1])
		sys.argv = sys.argv[1:]
	if sys.argv[0] == "--size":
		size = int(sys.argv[1])
		sys.argv = sys.argv[1:]
	if sys.argv[0] == "--S_0":
		S[0] = int(sys.argv[1])
		sys.argv = sys.argv[1:]
	if sys.argv[0] == "--S_1":
		S[1] = int(sys.argv[1])
		sys.argv = sys.argv[1:]
	if sys.argv[0] == "--replacement":
		replacement = float(sys.argv[1])
		sys.argv = sys.argv[1:]
	
	sys.argv = sys.argv[1:]
		
G = nx.Graph()
G.add_node((0,0), type=0, spin=S[0])

N = {0: int(ratio * size)}
N[1] = size-N[0]
n_nodes = N[0]+N[1]

directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

frontier = set(
	(dx, dy)
	for dx, dy in directions
)

i = 1
while len(G) < n_nodes:
	# compute weights = number of occupied neighbors
	candidates = list(frontier)
	weights = []

	for x, y in candidates:
		w = sum(
			(x + dx, y + dy) in G
			for dx, dy in directions
		)
		weights.append((w + 1) ** 3)  # +1 avoids zero probability

	new_node = random.choices(candidates, weights=weights, k=1)[0]
	frontier.remove(new_node)

	if(i<N[0]):
		if(random.random()<replacement):
			n_type=1
		else:
			n_type=0
	else:
		if(random.random()<replacement):
			n_type=0
		else:
			n_type=1
		
	G.add_node(new_node, type=n_type, spin=S[n_type])
	i = i+1

	for dx, dy in directions:
		nbr = (new_node[0] + dx, new_node[1] + dy)
		if nbr in G:
			G.add_edge(new_node, nbr)
		else:
			frontier.add(nbr)

G = prune_degree_one_nodes(G)

real_N = 	{
			0: len(select_nodes(G.nodes(data=True), 0)),
			1: len(select_nodes(G.nodes(data=True), 1))
			}
print(f"N[0] = {real_N[0]}, N[1] = {real_N[1]}")
print(f"Ratio = {round(real_N[0]/(real_N[0]+real_N[1]),2)}")

pos = {node: {'pos': node} for node in G.nodes()}  # (x, y) positions
nx.set_node_attributes(G, pos)

#Name nodes by index
mapping = {node: i for i, node in enumerate(G.nodes())}
H = nx.relabel_nodes(G, mapping)

#Export net.dat
print("Exporting node data to net.dat")
nodeList = [(item[0], item[1]['type'], item[1]['spin']) for item in H.nodes(data=True)]
with open("nodes.dat", "w") as f:
    f.write(''.join(str(len(H.nodes()))+ '\n'))
    for item in nodeList:
        i, t ,s = item
        f.write(''.join(str(i) + ' ' + str(t) + ' ' + str(s)))
        f.write('\n')
        
#Export neighbor list
print("Exporting neighbors list to neighbors.dat")
with open("neighbors.dat", "w") as f:
	for node in H.nodes():
		neighbors = [node for node in H.adj[node]]
		
		#Fill for C array
		while len(neighbors) < 4:
			neighbors.append(-1)
			
		for neighbor in neighbors:
			f.write(''.join(str(neighbor)+' '))
		f.write('\n')

color_map = {
	0: "black",
	1: "red"
}

node_colors = [color_map[H.nodes[n]['type']] for n in H.nodes()]
coords = {node: H.nodes[node]['pos'] for node in H.nodes()}

plt.figure(figsize=(6, 6))
nx.draw(
	H,
	pos=coords,
	node_size=30,
	node_color=node_colors,
	edge_color="gray",
	with_labels=False
)
plt.axis("equal")
plt.show()

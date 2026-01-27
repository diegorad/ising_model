import networkx as nx
import random
import sys
from tools import *

#Defaults
size = 50
ratio = 0.1
periodic = False

S_0 = 2
S_1 = 1

#Argument parsing
while sys.argv:
	if sys.argv[0] == "--ratio":
		ratio = float(sys.argv[1])
		sys.argv = sys.argv[1:]
	if sys.argv[0] == "--size":
		size = int(sys.argv[1])
		sys.argv = sys.argv[1:]
	if sys.argv[0] == "--S_0":
		S_0 = int(sys.argv[1])
		sys.argv = sys.argv[1:]
	if sys.argv[0] == "--S_1":
		S_1 = int(sys.argv[1])
		sys.argv = sys.argv[1:]
	if sys.argv[0] == "--periodic":
		periodic = True
		
	sys.argv = sys.argv[1:]

#Here S corresponds to S/2
S = {0: S_0,	#Spin of species 0
	 1: S_1 	#Spin of species 1
	 }

#Print info
print(f"Size: {size}")
print(f"Percentage elements: {{0: {ratio}, 1: {1-ratio}}}")
print(f"Spin: {S}")
print(f"Periodic: {periodic}")

#Calculate and populate allowed projections
S_z = {0: [], 1: []}
for i in [0, 1]:
	for j in range(S[i] + 1):
		S_z[i].append(-S[i] + 2*j)

H = nx.grid_2d_graph(size, size, periodic=periodic)

#Name nodes by index
mapping = {node: i for i, node in enumerate(H.nodes())}

G = nx.relabel_nodes(H, mapping)

#Assing type to nodes accordin to ratio
N = len(G.nodes())
Na = int(ratio * N)
Nb = N - Na

numberOfNodes = {}
numberOfNodes[0] = int(ratio * N/(1+ratio))
numberOfNodes[1] = N-numberOfNodes[0]

randomSequence = randomSequence(Na, Nb, 0, 1)

node_data = {}
for index, node in enumerate(G.nodes()):
    attr = randomSequence[index]
    node_data[node] = {'type': attr}

nx.set_node_attributes(G, node_data)

#Define spins of the two species at random
for i in [0,1]:
#	randomSequence = [S_z[i][random.randrange(S[i] + 1)] for _ in range(numberOfNodes[i])]

	node_data = {}
	for index, node in enumerate(select_nodes(G.nodes(data=True), i)):
		attr = S[i]
		node_data[node] = {'spin': attr}
	
	nx.set_node_attributes(G, node_data)

##Export net.edgelist
#print("Exporting edgelist to net.edgelist")
#nx.write_edgelist(G, "net.edgelist", data=False)

#Export net.dat
print("Exporting node data to net.dat")
nodeList = [(item[0], item[1]['type'], item[1]['spin']) for item in G.nodes(data=True)]
with open("nodes.dat", "w") as f:
    f.write(''.join(str(len(G.nodes()))+ '\n'))
    for item in nodeList:
        i, t ,s = item
        f.write(''.join(str(i) + ' ' + str(t) + ' ' + str(s)))
        f.write('\n')
     
#Export neighbor list
print("Exporting neighbors list to neighbors.dat")
with open("neighbors.dat", "w") as f:
	for node in range(N):
		neighbors = [node for node in G.adj[node]]
		
		#Fill for C array
		while len(neighbors) < 4:
			neighbors.append(-1)
			
		for neighbor in neighbors:
			f.write(''.join(str(neighbor)+' '))
		f.write('\n')


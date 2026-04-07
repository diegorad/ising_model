#!/usr/bin/env python3

import networkx as nx
import matplotlib.pyplot as plt
import random
import sys
import math
from tools import *

###################
size = 50
ratio = 0.5
periodic = False
show = False
layers = 5
network_type = 'random'
replacement = 0

S_0 = 4
S_1 = 1
###################

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
    if sys.argv[0] == "--show":
        show = True
    if sys.argv[0] == "--layers":
        layers = int(sys.argv[1])
        sys.argv = sys.argv[1:]
    if sys.argv[0] == "--replacement":
        replacement = float(sys.argv[1])
        sys.argv = sys.argv[1:]
    if sys.argv[0] == "--type":
        network_type = sys.argv[1]
        sys.argv = sys.argv[1:]
        
    sys.argv = sys.argv[1:]

#Here S corresponds to S/2
S = {0: S_0,    #Spin of species 0
     1: S_1     #Spin of species 1
     }

#Calculate and populate allowed projections
S_z = {0: [], 1: []}
for i in [0, 1]:
    for j in range(S[i] + 1):
        S_z[i].append(-S[i] + 2*j)

H = nx.grid_2d_graph(size, size, periodic=periodic)

#Coordinates
pos = {node: {'pos': node} for node in H.nodes()}  # (x, y) positions
nx.set_node_attributes(H, pos)

#Name nodes by index
mapping = {node: i for i, node in enumerate(H.nodes())}
G = nx.relabel_nodes(H, mapping)

N = len(G.nodes())

if(network_type == 'random' or network_type == 'snn'):
    neighbors_lenght = 4
    
    #Assing type to nodes according to ratio
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

if(network_type == 'snn'):
    neighbors_lenght = 8
    G.clear_edges()
    
    for node in G.nodes():
        x, y = G.nodes[node]['pos']

        # distance to nearest neighbors
        for i in G.nodes():
            x_i, y_i = G.nodes[i]['pos']
            dist = math.sqrt(pow(x - x_i, 2) + pow(y - y_i, 2))
            if(dist != 0 and dist <= 1.42):
                G.add_edge(node, i)

if(network_type == 'shell'):
    for node in G.nodes():
        x, y = G.nodes[node]['pos']

        # distance to nearest boundary
        dist_to_edge = min(
            x,
            size-1- x,
            y,
            size-1-y
        )

        if dist_to_edge < layers:
            G.nodes[node]['type'] = 1
        else:
            G.nodes[node]['type'] = 0
        
    #Replacement    
    for node in G.nodes():
        if(random.random()<replacement):
            current_type = G.nodes[node]['type']
            #Not gate
            replaced_type = 1 if current_type == 0 else 0
            G.nodes[node]['type'] = replaced_type

if(network_type == 'triangle'):
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        
        if y >= x:
            G.nodes[node]['type'] = 1
        else:
            G.nodes[node]['type'] = 0

#Populate spin attribute
for i in [0,1]:
#    randomSequence = [S_z[i][random.randrange(S[i] + 1)] for _ in range(numberOfNodes[i])]

    node_data = {}
    for index, node in enumerate(select_nodes(G.nodes(data=True), i)):
        attr = S[i]
        node_data[node] = {'spin': attr}
    
    nx.set_node_attributes(G, node_data)

#Print info
real_N =     {
            0: len(select_nodes(G.nodes(data=True), 0)),
            1: len(select_nodes(G.nodes(data=True), 1))
            }
            
print(f"\nSize: {size}")
print(f"Spin: {S}")
print(f"Percentage elements: {{0: {round(real_N[0]/N, 3)}, 1: {round(real_N[1]/N, 3)}}}")
print(f"Ratio: {round(real_N[0]/(real_N[0]+real_N[1]),2)}")
print(f"Periodic: {periodic}\n")

#Export nodes.dat
print("Exporting node data to nodes.dat")
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
    #Array dimension
    f.write(''.join(str(len(G.nodes())) + ' ' + str(neighbors_lenght) + '\n'))
    
    for node in range(N):
        neighbors = [node for node in G.adj[node]]
        
        #Fill for C array
        while len(neighbors) < neighbors_lenght:
            neighbors.append(-1)
        
        for neighbor in neighbors:
            f.write(''.join(str(neighbor)+' '))    
        f.write('\n')
#    print(counter)
    
if(show):
    color_map = {
        0: "black",
        1: "red"
    }

    node_colors = [color_map[G.nodes[n]['type']] for n in G.nodes()]
    coords = {node: G.nodes[node]['pos'] for node in G.nodes()}

    plt.figure(figsize=(6, 6))
    nx.draw(
        G,
        pos=coords,
        node_size=30,
        node_color=node_colors,
        edge_color="gray",
        with_labels=False
    )
    plt.axis("equal")
    plt.show()

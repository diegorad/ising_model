import random

def randomSequence(lenght_1, lenght_2, kind_1, kind_2):
    seq = [0 for i in range(lenght_1)]
    seq = seq + ([1 for i in range(lenght_2)])
    random.shuffle(seq)

    nodeTypes = [kind_1, kind_2]
    return [nodeTypes[i] for i in seq]

def select_nodes(nodeList, attr):
    selected_nodes = [index for index, val in nodeList if val['type'] == attr]  
    return selected_nodes

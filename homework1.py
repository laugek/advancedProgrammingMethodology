####################################################
### PACKAGES
#####################################################

from random import *
import math

####################################################
### CLASSES
#####################################################

# The graph is represented by 1 standard list called 'graph' which contains
# n number of:
    # adjacency lists (class AdjList ), which points to a start node (1st neighbor)
    # all nodes (class Node) has 4 atributes:
            # Node number
            # capacity
            # Pointer to next
            # flow

class Node(object):
    def __init__(self, number = None, capacity = None, pointer = None, flow = 0):
        self.number = number
        self.capacity = capacity
        self.pointer = pointer
        self.flow = flow

    def set_pointer(self, new_next):
        self.pointer = new_next

    def set_flow(self, new_flow):
        self.flow = new_flow

    def set_capacity(self, new_capacity):
        self.capacity = new_capacity

    def get_flow(self):
        return self.flow

    def get_number(self):
        return self.number

    def get_capacity(self):
        return self.capacity

    def get_pointer(self):
        return self.pointer


class AdjList(object):
    # list for just one node now
    def __init__(self, start_node=None):
        self.start_node = start_node

    def set_start(self, new_node):
        self.start_node = new_node

    def get_start(self):
        return self.start_node

    def insert(self, number = None, capacity = None, pointer = None, flow = 0):
        new_node = Node(number, capacity, pointer, flow)
        new_node.set_pointer(self.start_node)
        self.start_node = new_node

    ### FOR TESTING ADJ LIST
    def find_neighbor(self):
        current = self.start_node
        count = 0
        outFlow = 0
        print("node number / capacity / flow:")
        while current:
            print(current.get_number(), "/", current.get_capacity(), "/", current.get_flow())
            outFlow += current.get_flow()
            current = current.get_pointer()
            count += 1
        print("total number of neighbors:", count)
        print("total flow to neighbors:", outFlow)
        return count

    def search(self, number):
        current = self.start_node
        while current:
            if current.get_number() == number:
                return current
            current = current.get_pointer()

####################################################
### FUNCTIONS
#####################################################

### building the graph with adj list
def buildGraph(input_file):
    graph = []
    with open( input_file , 'rt') as in_file:
        #for idx1, line in enumerate(in_file):
        for idx1, line in enumerate(in_file):
            graph.append(AdjList())
            line=line.split()
            for idx2, capacity in enumerate(line):
                if (capacity != '-1'):
                    #print(idx2, capacity)
                    graph[idx1].insert(idx2, capacity)
    return graph


### bread first search to find all paths between to vertices
def allPathBFS(graph, start, target):
    # if it is same from beginning...
    if start == target:
        print("start is target")
        return(None, "Nan")
    # initialize
    visited = set() # create set (unique) node numbers that have been visited
    pathcapacity = []
    que = []
    que.append([start]) # que is set to start to begin with
    pathcapacity = []
    pathcapacity.append([0]) # keeps track of all capacitys in the path
    allPath = []
    while que:
        # remove path from que and extend this path from last element
        path = que.pop(0)
        w = pathcapacity.pop(0)
        nodeNumber = path[-1] # take the last element of the path
        visited.add(nodeNumber) # add this node to list of visited nodes
        #finidng neighbors of the node
        current = graph[nodeNumber].start_node
        while current:
            next_path = list(path)
            next_path.append(current.get_number())
            next_w = list(w)
            next_w.append(current.get_capacity())
            if current.get_number() == target:
                length = len(next_path)
                next_w.pop(0) # need this because otherwise i'll have a zero capacity
                allPath.append([next_path, length, next_w])
            if current.get_number() not in visited and current.get_number() != target:
                que.append(next_path)
                pathcapacity.append(next_w)
            current = current.get_pointer()
    return allPath, visited
    # if we never find it...
    print("Target not found")
    return(None, "Nan")


### edmonds-karps algorithm
def edka(graph, source, sink):
    maxFlow = 0 # initialize to zero
    all_paths, visited = allPathBFS(graph, source, sink) # get all paths from source to sink
    for path in all_paths: # itterate over them starting with the sortest
        val = setMinCap(graph, path) # set all edges flow to minimum capacity in path
        maxFlow += val # add this to max flow
    return maxFlow

# set the flow to minimum capacity in a path
def setMinCap(graph, path):
    cap = [] # initialize with zero
    # find the minimum capacity
    numberOfNodesInPath = int(path[1])
    for i in range(0, numberOfNodesInPath-1):
        #finding the numbers of the nodes
        fromNodeNumber = path[0][i]
        toNodeNumber = path[0][i+1]
        # serach for the edge
        toNode = graph[fromNodeNumber].search(toNodeNumber)
        # append the remaining capacity to the cap vector
        flow = float(toNode.get_flow())
        capacity = float(toNode.get_capacity())
        cap.append(capacity-flow)
    # determine the minimum value
    min_val = min(cap)
    # set flow to minimum remaining capacity in all edges
    for i in range(0,int(numberOfNodesInPath-1)):
        fromNodeNumber = path[0][i]
        toNodeNumber = path[0][i+1]
        toNode = graph[fromNodeNumber].search(toNodeNumber)
        toNode.set_flow(toNode.get_flow() + min_val)
        # set the capacity in the other direction = 0
        fromNode = graph[toNodeNumber].search(fromNodeNumber)
        fromNode.set_capacity(0)
    return min_val

## create the residual graph..
def resGraph(graph):
    resGraph = []
    for idx, adjlist in enumerate(graph): # for all adjlists in the graph
        resGraph.append(AdjList())
        current = adjlist.get_start()
        while current:
            match = math.isclose(float(current.get_flow()), float(current.get_capacity()), rel_tol=0.1)
            if match == False or current.get_capacity() == 0:
                resGraph[idx].insert(current.get_number(), current.get_capacity(), None, current.get_flow())
            # go to next
            current = current.get_pointer()
    return resGraph

# find the seperation set between two  sets S and T
def findSepSet(S,T):
    minCut = []
    minCutFlow = 0
    for fromNodeNumber in S:
        for toNodeNumber in T:
            node = None
            node = graph1[fromNodeNumber].search(toNodeNumber)
            if node != None:
                minCut.append([ fromNodeNumber, toNodeNumber ])
                minCutFlow+= node.get_flow()
    return minCut, minCutFlow



####################################################
######################## EXCERCISES
####################################################

####################################################
###  ex2 A
#####################################################
print(".......... Ex2 A ......................\n")
 ### build the graph
graph1 = buildGraph('graph.txt')
# ### BSF
print("\n\tFINDING SHORTEST PATH USING BFS:")
# definint source and target for rest of excercises
source = 0
target = 149
print("Source / Target:", source, "/", target)
all_path11, visited11 = allPathBFS(graph1, source, target)
print("Shortest path:", all_path11[0][0])
print("Length of path:", all_path11[0][1])
print("Capacity of edges:", all_path11[0][2])
#
#
# ####################################################
# ###  ex2 B
# #####################################################
print("\n\n.......... Ex2 B ......................\n")
print("\tFINDING ALL PATHS USING BFS:")
print("Source / Target:", source, "/", target)
maxFlow = edka(graph1, source, target)
print("Maximum flow found:", maxFlow)
# use find_neighbor to display the flow if all edges away from source
print("Neighbors of sourcenode:")
graph1[source].find_neighbor()

####################################################
###  ex2 C
#####################################################
print("\n\n.......... Ex2 C ......................\n")
print("\tFINDING MIN CUT USING RESIDUAL GRAPH:")
# 1) First find the residual graph
resGraph = resGraph(graph1)
print("We consider the residual graph. Nodes with no remaining capacity has been removed.")
print("Example: source nodes neighbors in residual graph is reduced")
resGraph[source].find_neighbor()
# 2) Then we run BFS to on residual graph to find nodes that are reachable from
# the source node. This is our set S
all_paths, S = allPathBFS(resGraph, source, target)
print("\nNumber of reachable nodes from source in residual graph:", len(S))
# 3) find the T set
allNodes = set()
for i in range(0,200):
    allNodes.add(i)
T = allNodes.difference(S)
# 4) Find connecting edges between S and T, which is the minimum cut
minCut, minCutFlow = findSepSet(S, T)
print("Flow of min cut:", minCutFlow)
print("Min cut:", minCut)
print("The flow of the min cut should be equal to the max flow:", maxFlow)

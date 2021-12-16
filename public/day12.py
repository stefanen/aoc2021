# Python3 Program to print BFS traversal
# from a given source vertex. BFS(int s)
# traverses vertices reachable from s.
from collections import defaultdict
 
# This class represents a directed graph
# using adjacency list representation
class Graph:
 
    # Constructor
    def __init__(self):
 
        # default dictionary to store graph
        self.graph = defaultdict(list)
 
    # function to add an edge to graph
    def addEdge(self,u,v):
        self.graph[u].append(v)

 
    # A function used by DFS
    def DFSUtil(self, v, parents, my_list, item):
 
        # Mark the current node as visited
        # and print it
        new_parents=parents.copy()
        new_parents.append(v)
        if v == "end":
            print(new_parents)
 
        # Recur for all the vertices
        # adjacent to this vertex
        found=False
        for neighbour in self.graph[v]:

            if  (neighbour in ['start','end'] and new_parents.count(neighbour)<1) \
            or (neighbour in [item] and new_parents.count(neighbour)<2) \
            or (neighbour in my_list and new_parents.count(neighbour)<1) \
            or (neighbour.isupper()):
                found=True
                self.DFSUtil(neighbour, new_parents, my_list, item)


    #if not found:
        #    print(parents)
 
    # The function to do DFS traversal. It uses
    # recursive DFSUtil()
    def DFS(self, v, my_list, item):
 
        # Create a set to store visited vertices
        parents=[] 
        # Call the recursive helper function
        # to print DFS traversal
        self.DFSUtil(v, parents, my_list, item)








    # Function to print a BFS of graph
    def BFS(self, s):
 
        # Mark all the vertices as not visited
        print(self.graph)
        visited=defaultdict()
        visited["start"]=False
        visited["A"]=False
        visited["c"]=False
        visited["b"]=False
        visited["d"]=False
        visited["end"]=False
 
        # Create a queue for BFS
        queue = []
 
        # Mark the source node as
        # visited and enqueue it
        queue.append(s)
        visited[s] = True
 
        while queue:
 
            # Dequeue a vertex from
            # queue and print it
            s = queue.pop(0)
            print (s, end = " ")
 
            # Get all adjacent vertices of the
            # dequeued vertex s. If a adjacent
            # has not been visited, then mark it
            # visited and enqueue it
            for i in self.graph[s]:
                if visited[i] == False:
                    queue.append(i)
                    visited[i] = True
 
# Driver code
 
# Create a graph given in
# the above diagram

g=Graph()

g.addEdge("end", "MY")
g.addEdge("MY", "xc")
g.addEdge("ho", "NF")
g.addEdge("start", "ho")
g.addEdge("NF", "xc")
g.addEdge("NF", "yf")
g.addEdge("end", "yf")
g.addEdge("xc", "TP")
g.addEdge("MY", "qo")
g.addEdge("yf", "TP")
g.addEdge("dc", "NF")
g.addEdge("dc", "xc")
g.addEdge("start", "dc")
g.addEdge("yf", "MY")
g.addEdge("MY", "ho")
g.addEdge("EM", "uh")
g.addEdge("xc", "yf")
g.addEdge("ho", "dc")
g.addEdge("uh", "NF")
g.addEdge("yf", "ho")
g.addEdge("end", "uh")
g.addEdge("start", "NF")

g.addEdge("MY", "end")
g.addEdge("xc", "MY")
g.addEdge("NF", "ho")
g.addEdge("ho", "start")
g.addEdge("xc", "NF")
g.addEdge("yf", "NF")
g.addEdge("yf", "end")
g.addEdge("TP", "xc")
g.addEdge("qo", "MY")
g.addEdge("TP", "yf")
g.addEdge("NF", "dc")
g.addEdge("xc", "dc")
g.addEdge("dc", "start")
g.addEdge("MY", "yf")
g.addEdge("ho", "MY")
g.addEdge("uh", "EM")
g.addEdge("yf", "xc")
g.addEdge("dc", "ho")
g.addEdge("NF", "uh")
g.addEdge("ho", "yf")
g.addEdge("uh", "end")
g.addEdge("NF", "start")


#
#g.addEdge("fs", "end")
#g.addEdge("he", "DX")
#g.addEdge("fs", "he")
#g.addEdge("start", "DX")
#g.addEdge("pj", "DX")
#g.addEdge("end", "zg")
#g.addEdge("zg", "sl")
#g.addEdge("zg", "pj")
#g.addEdge("pj", "he")
#g.addEdge("RW", "he")
#g.addEdge("fs", "DX")
#g.addEdge("pj", "RW")
#g.addEdge("zg", "RW")
#g.addEdge("start", "pj")
#g.addEdge("he", "WI")
#g.addEdge("zg", "he")
#g.addEdge("pj", "fs")
#g.addEdge("start", "RW")
#
#g.addEdge("end", "fs")
#g.addEdge("DX", "he")
#g.addEdge("he", "fs")
#g.addEdge("DX", "start")
#g.addEdge("DX", "pj")
#g.addEdge("zg", "end")
#g.addEdge("sl", "zg")
#g.addEdge("pj", "zg")
#g.addEdge("he", "pj")
#g.addEdge("he", "RW")
#g.addEdge("DX", "fs")
#g.addEdge("RW", "pj")
#g.addEdge("RW", "zg")
#g.addEdge("pj", "start")
#g.addEdge("WI", "he")
#g.addEdge("he", "zg")
#g.addEdge("fs", "pj")
#g.addEdge("RW", "start")
#


#fs he pj zg sl




small_list=['uh','yf','ho','dc','xc','qo'] 
#small_list=['fs','he','pj','zg','sl'] 
#item='fs'
for item in small_list:
    g.DFS("start",small_list, item)
 
# This code is contributed by Neelam Yadav

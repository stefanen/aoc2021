import sys
import re
from collections import defaultdict
import itertools
import functools
from collections import Counter
import copy
import numpy as np
from scipy.spatial.transform import Rotation as R

class Node:
    def __init__(self,value, parent):
        self.value=value
        self.parent=parent

    def print_s(self):
        res=[self.value]
        n=self.parent
        while n is not None:
            res.append(n.value)
            n=n.parent
        return res


# using adjacency list representation
class Graph:
 
    # Constructor
    def __init__(self,root):
 
        # default dictionary to store graph
        self.graph = defaultdict(list)
        self.root=root
 
    # function to add an edge to graph
    def addEdge(self,u,v):
        u=Node(u,None)
        v=Node(v,None)
        self.graph[u.value].append(v)
        self.graph[v.value].append(u)


    # Function to print a BFS of graph
    def BFS(self, v):
 
        # Mark all the vertices as not visited
        #print(self.graph)
        visited=defaultdict(lambda: False)
 
        # Create a queue for BFS
        queue = []
 
        # Mark the source node as
        # visited and enqueue it
        s=self.root
        queue.append(s)
        visited[s.value] = True
 
        res={}
        while queue:
 
            # Dequeue a vertex from
            # queue and print it
            s = queue.pop(0)
            res[s.value]=s.print_s()
 
            # Get all adjacent vertices of the
            # dequeued vertex s. If a adjacent
            # has not been visited, then mark it
            # visited and enqueue it
            for i in self.graph[s.value]:
                #print(i)
                if visited[i.value] == False:
                    i.parent=s
                    queue.append(i)
                    #print ("adding to queue", s.print_s(),i.print_s())

                    visited[i.value] = True
        return res

def rotate(x,up_dir,rot):
    v=copy.deepcopy(x)
    if up_dir=="-z":
        v[0],v[1],v[2]=-1*v[1],-1*v[0],-1*v[2]
    elif up_dir=="+x":
        v[0],v[1],v[2]=v[2],v[0],v[1]
    elif up_dir=="-x":
        v[0],v[1],v[2]=-1*v[2],-1*v[1],-1*v[0]
    elif up_dir=="+y":
        v[0],v[1],v[2]=v[1],v[2],v[0]
    elif up_dir=="-y":
        v[0],v[1],v[2]=-1*v[0],-1*v[2],-1*v[1]

    curr=0
    while curr<rot:
        v[0],v[1]=v[1],-1*v[0]
        curr+=1
        #print(v)
    return v
    ##print(v)

def det_orientation(v1,v2):
    for f in ["+z","-z","+x","-x","+y","-y"]:
        for r in [0,1,2,3]:
            if rotate(v1,f,r)==v2:
                return (f,r)



input = open(0).read().strip()
scanners={}
for line in input.split('\n'):
    m = re.search('--- scanner (.+?) ---', line)
    if m:
        found = m.group(1)
        #print(found)
        current_scanner=int(found)
        scanners[current_scanner]=[]
    elif line != "":
        scanners[current_scanner].append([int(e) for e in line.split(",")])

#print(scanners)

def compare_scanners(i,j):
    best_score=0
    for f in ["+z","-z","+x","-x","+y","-y"]:
        for r in [0,1,2,3]:
            my_counter = Counter()
            for beacon in scanners[j]:
                beacon=rotate(beacon,f,r)
                for other_beacon in scanners[i]:
                    #print("found")
                    #my_counter[','.join([str(z[1]-z[0]) for z in zip(beacon,other_beacon)])]+=1
                    my_counter[tuple([z[1]-z[0] for z in zip(beacon,other_beacon)])]+=1
            if best_score<my_counter.most_common(1)[0][1]: 
                best_candidate=list(my_counter.most_common(1)[0][0])
                best_score=my_counter.most_common(1)[0][1]
                best_orientation=(f,r)
    if best_score<12:
        return None
    return (best_candidate, best_orientation, best_score)

g=Graph(Node(0,None))
for xm,ym in list(itertools.combinations(scanners.keys(), 2)):
    if compare_scanners(xm,ym) is not None:
        g.addEdge(xm,ym)

def transform(src, res):
    result=[]
    for b in src:
        beacon=copy.deepcopy(b)
        beacon=rotate(beacon,res[1][0],res[1][1])
        translation=res[0]
        beacon[0]+=translation[0]
        beacon[1]+=translation[1]
        beacon[2]+=translation[2]
        result.append(beacon)
    return result

sc_coords=[]
for sc,path in g.BFS(0).items():
    beacon_list=[]
    if sc==0:
        sc_coords.append([0,0,0])
    else:
        #print(path)
        res=[[0,0,0]]
        for x,y in zip(path,path[1:]):
            conv=compare_scanners(y,x)
            res=transform(res,conv)
        sc_coords.append(res[0])
#print(sc_coords)

max_d=0
for xm,ym in list(itertools.combinations(sc_coords, 2)):
    max_d=max(max_d,abs(xm[0]-ym[0])+abs(xm[1]-ym[1])+abs(xm[2]-ym[2]))
print(max_d)

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



expected=[[-892,524,684],
[-876,649,763],
[-838,591,734],
[-789,900,-551],
[-739,-1745,668],
[-706,-3180,-659],
[-697,-3072,-689],
[-689,845,-530],
[-687,-1600,576],
[-661,-816,-575],
[-654,-3158,-753],
[-635,-1737,486],
[-631,-672,1502],
[-624,-1620,1868],
[-620,-3212,371],
[-618,-824,-621],
[-612,-1695,1788],
[-601,-1648,-643],
[-584,868,-557],
[-537,-823,-458],
[-532,-1715,1894],
[-518,-1681,-600],
[-499,-1607,-770],
[-485,-357,347],
[-470,-3283,303],
[-456,-621,1527],
[-447,-329,318],
[-430,-3130,366],
[-413,-627,1469],
[-345,-311,381],
[-36,-1284,1171],
[-27,-1108,-65],
[7,-33,-71],
[12,-2351,-103],
[26,-1119,1091],
[346,-2985,342],
[366,-3059,397],
[377,-2827,367],
[390,-675,-793],
[396,-1931,-563],
[404,-588,-901],
[408,-1815,803],
[423,-701,434],
[432,-2009,850],
[443,580,662],
[455,729,728],
[456,-540,1869],
[459,-707,401],
[465,-695,1988],
[474,580,667],
[496,-1584,1900],
[497,-1838,-617],
[527,-524,1933],
[528,-643,409],
[534,-1912,768],
[544,-627,-890],
[553,345,-567],
[564,392,-477],
[568,-2007,-577],
[605,-1665,1952],
[612,-1593,1893],
[630,319,-379],
[686,-3108,-505],
[776,-3184,-501],
[846,-3110,-434],
[1135,-1161,1235],
[1243,-1093,1063],
[1660,-552,429],
[1693,-557,386],
[1735,-437,1738],
[1749,-1800,1813],
[1772,-405,1572],
[1776,-675,371],
[1779,-442,1789],
[1780,-1548,337],
[1786,-1538,337],
[1847,-1591,415],
[1889,-1729,1762],
[1994,-1805,1792]]


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
                #print(beacon)
#                translation=[68,-1246,-43]
#                beacon[0]+=translation[0]
#                beacon[1]+=translation[1]
#                beacon[2]+=translation[2]
#                translation=[88, 113, -1104]
#                beacon[0]+=translation[0]
#                beacon[1]+=translation[1]
#                beacon[2]+=translation[2]


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
#    print(best_candidate)
#    print(best_score)
#    print(best_orientation)
    #print(rotate(best_candidate,best_orientation[0],best_orientation[1]))

g=Graph(Node(0,None))
for xm,ym in list(itertools.combinations(scanners.keys(), 2)):
    if compare_scanners(xm,ym) is not None:
        g.addEdge(xm,ym)
    #print(xm,ym,compare_scanners(xm,ym))



#res0_1=compare_scanners(0,1)
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



#g.addEdge(0, 1)
#g.addEdge(1, 3)
#g.addEdge(1, 4)
#g.addEdge(2, 4)


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

    #print("\n".join([str(i) for i in beacon_list]))
    #print("¤"+str(sc))
 
print(sc_coords)

for xm,ym in list(itertools.combinations(sc_coords, 2)):
    print(abs(xm[0]-ym[0])+abs(xm[1]-ym[1])+abs(xm[2]-ym[2]))
sys.exit()


print("\n".join([str(i) for i in scanners[0]]))
print("¤")
print("\n".join([str(i) for i in transform(scanners[1],res0_1)
    ]))

print("¤")
res1_4=compare_scanners(1,4)
print("\n".join([str(i) for i in transform(transform(scanners[4],res1_4),res0_1)
    ]))

print("¤")
res1_3=compare_scanners(1,3)
print("\n".join([str(i) for i in transform(transform(scanners[3],res1_3),res0_1)
    ]))

print("¤")
res4_2=compare_scanners(4,2)
print("\n".join([str(i) for i in transform(transform(transform(scanners[2],res4_2),res1_4),res0_1)
    ]))

for i in transform(transform(transform(scanners[2],res4_2),res1_4),res0_1):
	if i not in expected:
		print("not found")





sys.exit()

d1_0=res[0]
o1_0=res[1]
res=compare_scanners(1,4)
if res is not None:
    print([z[1]+z[0] for z in zip(d1_0,rotate(res[0],o1_0[0],o1_0[1]))])



#for b in scanners[4]:
#    beacon=copy.deepcopy(b)
#    beacon=rotate(beacon,res[1][0],res[1][1])
#    translation=res[0]
#    beacon[0]+=translation[0]
#    beacon[1]+=translation[1]
#    beacon[2]+=translation[2]
#    print(beacon)





#compare_scanners(4,1)
#compare_scanners(1,4)

#print(scanners[1])



A=[1,2,3]
print(rotate(A,"-z",1))


o=det_orientation([-1,-1,1],[1,-1,1])
assert rotate([-2,-2,2],o[0],o[1])==[2,-2,2]
sys.exit()

print(rotate(A,"+z",0))
print(rotate(A,"+z",1))
print(rotate(A,"+z",2))
print(rotate(A,"+z",3))

print(rotate(A,"-z",0))
print(rotate(A,"-z",1))
print(rotate(A,"-z",2))
print(rotate(A,"-z",3))

print(rotate(A,"+x",0))
print(rotate(A,"+x",1))
print(rotate(A,"+x",2))
print(rotate(A,"+x",3))

print(rotate(A,"-x",0))
print(rotate(A,"-x",1))
print(rotate(A,"-x",2))
print(rotate(A,"-x",3))

print(rotate(A,"+y",0))
print(rotate(A,"+y",1))
print(rotate(A,"+y",2))
print(rotate(A,"+y",3))

print(rotate(A,"-y",0))
print(rotate(A,"-y",1))
print(rotate(A,"-y",2))
print(rotate(A,"-y",3))



#vec = [1,1,1]
#
#rotation_degrees = 90
#rotation_radians = np.radians(rotation_degrees)
#rotation_axis = np.array([0, 0, 1])
#
#rotation_vector = rotation_radians * rotation_axis
#rotation = R.from_rotvec(rotation_vector)
#rotated_vec = rotation.apply(vec)
#
#print(rotated_vec)

import sys
import networkx as nx
import itertools
 
# Driver program
#g = Graph(9)
#g.graph = [[0, 4, 0, 0, 0, 0, 0, 8, 0],
#           [4, 0, 8, 0, 0, 0, 0, 11, 0],
#           [0, 8, 0, 7, 0, 4, 0, 0, 2],
#           [0, 0, 7, 0, 9, 14, 0, 0, 0],
#           [0, 0, 0, 9, 0, 10, 0, 0, 0],
#           [0, 0, 4, 14, 10, 0, 2, 0, 0],
#           [0, 0, 0, 0, 0, 2, 0, 1, 6],
#           [8, 11, 0, 0, 0, 0, 1, 0, 7],
#           [0, 0, 2, 0, 0, 0, 6, 7, 0]
#           ]


g = nx.DiGraph()
input = open(0).read().strip()
matrix=[[int(c) for c in list(line)] for line in [e for e in input.split('\n')]]

matrix=[list(itertools.chain.from_iterable([row, 
    list(map(lambda x:(x+1) if x+1<10 else x-8, row)),
    list(map(lambda x:(x+2) if x+2<10 else x-7, row)),
    list(map(lambda x:(x+3) if x+3<10 else x-6, row)),
    list(map(lambda x:(x+4) if x+4<10 else x-5, row))
    ])) for row in [e for e in matrix]]


new_matrix=[[-1 for c in range(len(matrix)*5)] for line in [e for e in range(len(matrix)*5)]]

for i in range(0,len(matrix)):
    for j in range(0,len(matrix[0])):
        x=matrix[i][j]
        new_matrix[i][j]=x
        new_matrix[i+len(matrix)][j]=(x+1) if x+1<10 else x-8
        new_matrix[i+2*len(matrix)][j]=(x+2) if x+2<10 else x-7
        new_matrix[i+3*len(matrix)][j]=(x+3) if x+3<10 else x-6
        new_matrix[i+4*len(matrix)][j]=(x+4) if x+4<10 else x-5

#print(new_matrix)
#print(new_matrix[49][49])
#print(new_matrix[51][51])
#sys.exit()

matrix=new_matrix

for i in range(0,len(matrix)):
    for j in range(0,len(matrix[0])):
        neighbour_candidates=[(i-1,j),(i+1,j),(i,j-1),(i,j+1)]
        for n in neighbour_candidates:
            if 0<=n[0]<len(matrix) and 0<=n[1]<len(matrix[0]):
                #x=1
#                if f'{i}_{j}' == "2_3":
#                    print(n, matrix[n[0]][n[1]])
                g.add_edge(f'{i}_{j}', f'{n[0]}_{n[1]}')
                g[f'{i}_{j}'][f'{n[0]}_{n[1]}']['weight'] = matrix[n[0]][n[1]]


print(matrix)

#print(g["2_3"]["2_4"]['weight'])
#g["0_0"]["0_1"]['weight'] = 3

shortest_path=nx.shortest_path(g,"0_0",f'{len(matrix)-1}_{len(matrix)-1}',"weight")
print(shortest_path)
sum=0
previous_edge=shortest_path[0]
tmp=matrix[0][0]
for edge in shortest_path:
    x=int(edge.split("_")[0])
    y=int(edge.split("_")[1])
    sum+=matrix[x][y]
    matrix[x][y]=" "
    print(edge, previous_edge)

    old_x=int(previous_edge.split("_")[0])
    old_y=int(previous_edge.split("_")[1])

    if old_y<y:
        print("Y-move")
    elif old_x<x:
        print("X-move")
    elif old_y>y:
        print("NY-move")
    elif old_x>x:
        print("NX-move")
    else:
        print("U-move")

    previous_edge=edge
    #print(sum)
print(sum-tmp)

for row in matrix:
    print(''.join([str(x) for x in row]))



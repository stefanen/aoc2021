from itertools import chain
import collections
import sys
from collections import Counter
 

#input = open('small.txt').read().strip()
input = open(0).read().strip()
matrix=[[int(c) for c in list(line)] for line in [e for e in input.split('\n')]]

rows = len(matrix)
columns = len(matrix[0])

def print_p(i):
#    print(matrix)
#    if i%10>0:
#        return
    print(f'')
    print(f'')
    for i in range(0,rows):
        print(matrix[i])

sum=0
days=300
for i in range(0,days):
    print_p(i)
    #counts=dict(sum(map(Counter, matrix), Counter()))
    #print(chain(*matrix))
    #counts=dict(Counter(chain(*matrix)))
    #print(sorted(list(counts.values()),reverse=True))



    for i in range(0,rows):
        for j in range(0,columns):
            matrix[i][j]+=1
        
    found=True
    while found:
        found=False
        for i in range(0,rows):
            for j in range(0,columns):
                if matrix[i][j]>9:
                    found=True
                    matrix[i][j]=-999
                    neighbour_candidates=[(i-1,j),(i+1,j),(i,j-1),(i,j+1),(i-1,j-1),(i+1,j+1),(i-1,j+1),(i+1,j-1)]
                    for n in neighbour_candidates:
                        if 0<=n[0]<len(matrix) and 0<=n[1]<len(matrix[0]):
                            matrix[n[0]][n[1]]+=1
                    #spread

    for i in range(0,rows):
        for j in range(0,columns):
            if matrix[i][j]<0:
                sum+=1
                matrix[i][j]=0


print(sum)

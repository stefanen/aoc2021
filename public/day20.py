import sys
import networkx as nx
import itertools
import copy
from collections import Counter

input = open(0).read().strip()

t=list(input.split('\n')[0])

print(t)

lines=[e for e in input.split('\n')[2:]]

padding=54
for i in range(0,padding):
    lines.insert(0,''.join(['.'*len(lines[0])]))
    lines.append(''.join(['.'*len(lines[0])]))

#print(lines)
matrix=[list('.'*padding)+[str(c) for c in list(line)]+list('.')*padding for line in lines]
#print(matrix)


def conv_char(i,j,b):
    global matrix
    if i<0 or j<0 or i>=len(matrix) or j>=len(matrix[0]):
        return "0" if b else "1"
    if matrix[i][j]=='.' :
        return "0"
    return "1"

count=0
while count < 50:
    new_matrix=copy.deepcopy(matrix)
    print(new_matrix)
    for i in range(0,len(matrix)):
        for j in range(0,len(matrix[0])):
            binary_s=conv_char(i-1,j-1,count%2==0)+ \
                    conv_char(i-1,j,count%2==0)+ \
                    conv_char(i-1,j+1,count%2==0)+ \
                    conv_char(i,j-1,count%2==0)+ \
                    conv_char(i,j,count%2==0)+ \
                    conv_char(i,j+1,count%2==0)+ \
                    conv_char(i+1,j-1,count%2==0)+ \
                    conv_char(i+1,j,count%2==0)+ \
                    conv_char(i+1,j+1,count%2==0)
            index=int(binary_s
                    ,2)

            #print(binary_s,index, t[index])
            new_matrix[i][j]=t[index]
    count+=1
    matrix=new_matrix

print(dict(sum(map(Counter, new_matrix), Counter())))


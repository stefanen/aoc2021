from itertools import chain
import collections
import sys
from collections import Counter 

#input = open('small.txt').read().strip()


sys.setrecursionlimit(100000)

input = open('9-4096-4.in').read().strip()
groups=[[0 for c in list(line)] for line in [e for e in input.split('\n')]]
matrix=[[int(c) for c in list(line)] for line in [e for e in input.split('\n')]]

rows = len(matrix)
columns = len(matrix[0])

def visit_all_neighbours(i,j,group):
    if i>0 and groups[i-1][j]==0 and matrix[i-1][j]!=9:
        groups[i-1][j]=group
        visit_all_neighbours(i-1,j,group)
    if i+1<rows and groups[i+1][j]==0 and matrix[i+1][j]!=9:
        groups[i+1][j]=group
        visit_all_neighbours(i+1,j,group)
    if j>0 and groups[i][j-1]==0 and matrix[i][j-1]!=9:
        groups[i][j-1]=group
        visit_all_neighbours(i,j-1,group)
    if j+1<columns and groups[i][j+1]==0 and matrix[i][j+1]!=9:
        groups[i][j+1]=group
        visit_all_neighbours(i,j+1,group)


    #print(f'{i} {j}')

current_group=0
for i in range(0,rows):
    prev=float('inf')
#    print(i)
    for j in range(0,columns):
        if groups[i][j]!=0 or matrix[i][j]==9:
            continue
        current_group=current_group+1
        groups[i][j]=current_group
        visit_all_neighbours(i,j, current_group)

#        neighbours=[matrix[i-1][j] if i>0 else float('inf'),matrix[i+1][j] if i+1<rows else float('inf'),matrix[i][j-1] if j>0 else float('inf'),matrix[i][j+1] if j+1<columns else float('inf')]
#        #print(neighbours)
#        if matrix[i][j]<min(neighbours):
#            sum=sum+matrix[i][j]+1
        #print(min(neighbours))
        #print(matrix[i][j])

res=sorted(list(Counter([item for sublist in groups for item in sublist if item>0]).values()),reverse=True)

print(res[0]*res[1]*res[2])

#row_index=0
#for line in lines:
#    print(line)
#    row_index=row_index+1
#
#print(lines[row_index-1])












#print(144*a_6(256+5)+39*a_6(256+4)+45*a_6(256+3)+34*a_6(256+2)+38*a_6(256+1))




#o = 0
#prev = float('inf')
#
##prev = float(2)
##print(f'test{prev}')
##print(list(zip(l, l[1:], l[2:])))
##1/0
#for a,b,c in zip(l, l[1:], l[2:]):
#        tmp = a+b+c
#        if tmp > prev:
#                o += 1
#        prev = tmp
#
#print(o)

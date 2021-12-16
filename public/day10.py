from itertools import chain
import collections
import sys
 

#input = open('small.txt').read().strip()
input = open('../input_d_10.txt').read().strip()
matrix=[[int(c) for c in list(line)] for line in [e for e in input.split('\n')]]

rows = len(matrix)
columns = len(matrix[0])

sum=0
for i in range(0,rows):
    for j in range(0,columns):
        print(matrix[i][j])

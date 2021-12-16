from itertools import chain
import collections
import sys
 

#input = open('small.txt').read().strip()
input = open('../input_d_9.txt').read().strip()
matrix=[[int(c) for c in list(line)] for line in [e for e in input.split('\n')]]

rows = len(matrix)
columns = len(matrix[0])

sum=0
for i in range(0,rows):
    prev=float('inf')
    for j in range(0,columns):
        neighbours=[matrix[i-1][j] if i>0 else float('inf'),matrix[i+1][j] if i+1<rows else float('inf'),matrix[i][j-1] if j>0 else float('inf'),matrix[i][j+1] if j+1<columns else float('inf')]
        #print(neighbours)
        if matrix[i][j]<min(neighbours):
            sum=sum+matrix[i][j]+1
        #print(min(neighbours))
        #print(matrix[i][j])

print(sum)
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

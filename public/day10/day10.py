from itertools import chain
import collections
import sys
 

#input = open('small.txt').read().strip()
input = open('../input_d_10.txt').read().strip()

closers= {
        "[": "]",
        "(": ")",
        "<": ">",
        "{": "}"
        }

openers= {
        "]": "[",
        ")": "(",
        ">": "<",
        "}": "{"
        }

score2= {
        "]": 57,
        ")": 3,
        ">": 25137,
        "}": 1197
        }

score= {
        "]": 2,
        ")": 1,
        ">": 4,
        "}": 3
        }

sum=0
for line in [e for e in input.split('\n')]:
    stack = []
    local=0
    for char in list(line):
        if char in list("[({<"):
            stack.append(char)
        if char in list("])}>"):
            curr=stack.pop()
            if curr!=openers[char]:
                stack=[]
                break;

    if len(stack)==0:
        continue

    for i in reversed(stack):
        curr=closers[i]
        local=local*5+score[curr]
    print(local)


#print(sum)


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

import sys
import itertools
import functools

#input = open(0).read().strip()


x=7
y=2

p_x=0
p_y=0

y_quit=-96


#3297
#print(0,0)
for x in range(27,28):
    for y in range (2,3):
        y_max=0
        curr_y=0
        hit=False
        for n in range(1,999999999999):
            x_n=n
            if x_n>x:
                x_n=x
            prev_y=curr_y
            curr_x=int(x_n*(2*x-x_n+1)/2)
            curr_y=int(n*(2*y-n+1)/2)
            y_max=max(curr_y,y_max)
            print(curr_x,curr_y)
            if 288<=curr_x<=330 and -96<=curr_y<=-50:
                hit=True
            #print(prev_y, curr_y)
            if curr_y < y_quit:
                #print(prev_y, hit, y)
                #if 288<=curr_x<=330:
                #    print(x)
                if hit:
                    print(y_max, x,y)
                #print(hit)
                break

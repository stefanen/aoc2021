import termplotlib as tpl
import numpy as np
import sys

lines = open(0).read().strip().split('\n')
#lines=lines[:3]

#lines is ['0,0', '0,1', '0,2']

##need help making this segment shorter
#x=[]
#y=[]
#for item in lines:
#    x_0,y_0=item.split(',')
#    x.append(x_0)
#    y.append(y_0)
#    #print(item)
#    #print(x)
#    #print(y)
#
#x= [int(i) for i in x]
#y= [int(i) for i in y]


#print([line.split(',') for line in lines])
#print(map(int,line.split(',')) for line in lines)
#print(*(map(int,line.split(',')) for line in lines))
#print(zip((map(int, line.split(',')) for line in lines)))
#print(zip(*(map(int, line.split(',')) for line in lines)))

x, y = zip(*(map(int, line.split(',')) for line in lines))
#x, y = zip(*( line.split(',') for line in lines))
#x, y = zip(*(map(lambda x: x+x,line.split(',')) for line in lines))

#x is [0,0,0]
#y is [0,1,2]

##


#x,y = [item.split(',') for item in lines]
print(x)
print(y)
#sys.exit()
#x=[1,2,3]
#y=[3,4,2]
fig = tpl.figure()
fig.plot(x, y, width=40, height=10, plot_command="plot '-' w points")
fig.show()

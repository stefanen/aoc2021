import sys
import networkx as nx
import itertools
import copy
import re
from collections import Counter

input = open(0).read().strip()


lines=[e for e in input.split('\n')]
lines=lines[:20]
cuboids=[]
for line in lines:
    #on x=-35..17,y=-28..24,z=-43..2
    print(line)
    #m = re.search('(on|off) x=-35..17,y=-28..24,z=-43..2', line)
    m = re.search('(on|off) x=([0-9-]*)\.\.([0-9-]*),y=([0-9-]*)\.\.([0-9-]*),z=([0-9-]*)\.\.([0-9-]*)', line)
    (status,x_min,x_max,y_min,y_max,z_min,z_max) =  (m.group(1),int(m.group(2)),int(m.group(3)),int(m.group(4)),int(m.group(5)),int(m.group(6)),int(m.group(7)))
    cuboids.append((status,x_min,x_max,y_min,y_max,z_min,z_max))

def contains(cube, cuboid):
    if cuboid[1]<=cube[0]<=cuboid[2] and cuboid[3]<=cube[1]<=cuboid[4] and cuboid[5]<=cube[2]<=cuboid[6]:
        return True
    return False

def volume(cuboid):
    return (cuboid[2]-cuboid[1]+1)*(cuboid[4]-cuboid[3]+1)*(cuboid[6]-cuboid[5]+1)


def volume_all_intersections_of_size(cuboid,other_cuboids,k):
    res=0
    for c in itertools.combinations(other_cuboids,k):
        res+=volume_intersection(list(c)+[cuboid])
    return res

def volume_intersection(cuboids):
    #print(cuboids)
    (min_x,max_x,min_y,max_y,min_z,max_z)=(float('-inf'),float('inf'),float('-inf'),float('inf'),float('-inf'),float('inf'))
    for cuboid in cuboids:
        min_x=max(min_x,cuboid[1])
        min_y=max(min_y,cuboid[3])
        min_z=max(min_z,cuboid[5])
        max_x=min(max_x,cuboid[2])
        max_y=min(max_y,cuboid[4])
        max_z=min(max_z,cuboid[6])
    #print((min_x,max_x,min_y,max_y,min_z,max_z))
    if min_x>max_x or min_y>max_y or min_z>max_z:
        return 0
    return (max_x-min_x+1)*(max_y-min_y+1)*(max_z-min_z+1)


def uniq_count(cuboid,remaining_cuboids):
    if len(remaining_cuboids)==0:
        return volume(cuboid)

    res=volume(cuboid)
    for i in range(0,len(remaining_cuboids)):
        print(1000+i)
        res=res+((-1) if i%2==0 else 1)*volume_all_intersections_of_size(cuboid,remaining_cuboids,i+1)
        #print(res)
    return res


#print(cuboids[1:3])
#print(volume_intersection(cuboids))
#print(uniq_count(cuboids[3],[]))
#print(uniq_count(cuboids[1],cuboids[2:]))
#print(uniq_count(cuboids[0],cuboids[1:]))

sum=0
for i in range(0,len(cuboids)):
    print(i)
    cuboid=cuboids[i]
    if cuboid[0]=='on':
        sum+=uniq_count(cuboids[i],cuboids[i+1:])
    
print(sum)
#
sys.exit()

all_x_endpoints=set()
all_y_endpoints=set()
all_z_endpoints=set()
for cuboid in cuboids:
    all_x_endpoints.add(cuboid[1])
    all_x_endpoints.add(cuboid[2])
    all_y_endpoints.add(cuboid[3])
    all_y_endpoints.add(cuboid[4])
    all_z_endpoints.add(cuboid[5])
    all_z_endpoints.add(cuboid[6])

all_x_endpoints=sorted(list(all_x_endpoints))
all_y_endpoints=sorted(list(all_y_endpoints))
all_z_endpoints=sorted(list(all_z_endpoints))
print(all_x_endpoints, all_y_endpoints, all_z_endpoints)
print(all_z_endpoints)


#print(cuboids)
on_count=0
x_idx=0
#for x in range(all_x_endpoints[0],all_x_endpoints[-1]+1):
    
print(len(all_x_endpoints))
print(len(all_y_endpoints))
print(len(all_z_endpoints))
while x_idx < len(all_x_endpoints):
    print(x_idx)
    x=all_x_endpoints[x_idx]
    x_count=1
    y_idx=0
    #for y in range(all_y_endpoints[0],all_y_endpoints[-1]+1):
    while y_idx < len(all_y_endpoints):
        print(y_idx)
        y=all_y_endpoints[y_idx]
        y_count=1
        z_idx=0
        while z_idx < len(all_z_endpoints):
            z=all_z_endpoints[z_idx]
            z_count=1
            for cuboid in reversed(cuboids):
                #print(cuboid)
                if contains((x,y,z),cuboid):
                    if cuboid[0]=="on":
                        on_count+=(z_count*y_count*x_count)
                    break
            #interior
            z=all_z_endpoints[z_idx]+1
            if z_idx==len(all_z_endpoints)-1:
                z_count=0
            else:
                z_count=all_z_endpoints[z_idx+1]-all_z_endpoints[z_idx]-1
            #print(z, z_count)
            for cuboid in reversed(cuboids):
                #print(cuboid)
                if contains((x,y,z),cuboid):
                    if cuboid[0]=="on":
                        on_count+=(z_count*y_count*x_count)
                    break
            z_idx+=1


        #interior
        y=all_y_endpoints[y_idx]+1
        if y_idx==len(all_y_endpoints)-1:
            y_count=0
        else:
            y_count=all_y_endpoints[y_idx+1]-all_y_endpoints[y_idx]-1
        y_idx+=1
        z_idx=0
        while z_idx < len(all_z_endpoints):
            z=all_z_endpoints[z_idx]
            z_count=1
            for cuboid in reversed(cuboids):
                #print(cuboid)
                if contains((x,y,z),cuboid):
                    if cuboid[0]=="on":
                        on_count+=(z_count*y_count*x_count)
                    break
            #interior
            z=all_z_endpoints[z_idx]+1
            if z_idx==len(all_z_endpoints)-1:
                z_count=0
            else:
                z_count=all_z_endpoints[z_idx+1]-all_z_endpoints[z_idx]-1
            #print(z, z_count)
            for cuboid in reversed(cuboids):
                #print(cuboid)
                if contains((x,y,z),cuboid):
                    if cuboid[0]=="on":
                        on_count+=(z_count*y_count*x_count)
                    break
            z_idx+=1

    x=all_x_endpoints[x_idx]+1
    if x_idx==len(all_x_endpoints)-1:
        x_count=0
    else:
        x_count=all_x_endpoints[x_idx+1]-all_x_endpoints[x_idx]-1
    
    y_idx=0
    #for y in range(all_y_endpoints[0],all_y_endpoints[-1]+1):
    while y_idx < len(all_y_endpoints):
        y=all_y_endpoints[y_idx]
        y_count=1
        z_idx=0
        while z_idx < len(all_z_endpoints):
            z=all_z_endpoints[z_idx]
            z_count=1
            for cuboid in reversed(cuboids):
                #print(cuboid)
                if contains((x,y,z),cuboid):
                    if cuboid[0]=="on":
                        on_count+=(z_count*y_count*x_count)
                    break
            #interior
            z=all_z_endpoints[z_idx]+1
            if z_idx==len(all_z_endpoints)-1:
                z_count=0
            else:
                z_count=all_z_endpoints[z_idx+1]-all_z_endpoints[z_idx]-1
            #print(z, z_count)
            for cuboid in reversed(cuboids):
                #print(cuboid)
                if contains((x,y,z),cuboid):
                    if cuboid[0]=="on":
                        on_count+=(z_count*y_count*x_count)
                    break
            z_idx+=1


        #interior
        y=all_y_endpoints[y_idx]+1
        if y_idx==len(all_y_endpoints)-1:
            y_count=0
        else:
            y_count=all_y_endpoints[y_idx+1]-all_y_endpoints[y_idx]-1
        y_idx+=1
        z_idx=0
        while z_idx < len(all_z_endpoints):
            z=all_z_endpoints[z_idx]
            z_count=1
            for cuboid in reversed(cuboids):
                #print(cuboid)
                if contains((x,y,z),cuboid):
                    if cuboid[0]=="on":
                        on_count+=(z_count*y_count*x_count)
                    break
            #interior
            z=all_z_endpoints[z_idx]+1
            if z_idx==len(all_z_endpoints)-1:
                z_count=0
            else:
                z_count=all_z_endpoints[z_idx+1]-all_z_endpoints[z_idx]-1
            #print(z, z_count)
            for cuboid in reversed(cuboids):
                #print(cuboid)
                if contains((x,y,z),cuboid):
                    if cuboid[0]=="on":
                        on_count+=(z_count*y_count*x_count)
                    break
            z_idx+=1

    x_idx+=1

print(on_count)


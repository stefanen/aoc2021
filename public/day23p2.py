import re
import sys
import networkx as nx
from collections import Counter
import itertools
from collections import defaultdict
import copy

COST={"A":1,"B":10,"C":100,"D":1000}

class Tile:
    def __init__(self,type,position,values):
        self.type=type
        self.position=position
        self.values=values
   
    def get_move_tile_src_index(self):
        #get last non-empty
        for t in reversed(list(enumerate(self.values))):
            if t[1]!=".":
                return t[0]

    def get_move_tile_dst_index(self):
        #get first empty
        for t in enumerate(self.values):
            #print(t)
            if t[1]==".":
                return t[0]
    
    def get_top_value(self):
        return next((x for x in reversed(self.values) if x!='.'), None)
    
    def get_bot_empty(self):
        return next((x for x in self.values if x=='.'), None)

    def to_string(self):
        return f'[{self.type} {self.position} {",".join(self.values)}]'
        #return f'[{self.type} {self.values}]'
    
    def to_string_short(self):
        #return f'[{self.type} {self.capacity} {self.position}]'
        return f'{",".join(self.values)}'
    
    
    def equals(self,other):
        return self.position==other.position

def get_cost(src,dst):
    cost=abs(src.position-dst.position)
    if src.type!="W":
        cost+=len(src.values)-src.get_move_tile_src_index()
    if dst.type!="W":
        cost+=len(dst.values)-dst.get_move_tile_dst_index()
    cost=cost*COST.get(src.get_top_value())
    return cost


class State:
    def __init__(self):
        self.tiles=[]

        tile=Tile("W",1,['.'])
        self.tiles.append(tile)

        tile=Tile("W",2,['.'])
        self.tiles.append(tile)
        
        tile=Tile("A",3,['D','C'])
        self.tiles.append(tile)
        
        tile=Tile("W",4,['.'])
        self.tiles.append(tile)
        
        tile=Tile("B",5,['A','C'])
        self.tiles.append(tile)
        
        tile=Tile("W",6,['.'])
        self.tiles.append(tile)

        tile=Tile("C",7,['B','B'])
        self.tiles.append(tile)
        
        tile=Tile("W",8,['.'])
        self.tiles.append(tile)

        tile=Tile("D",9,['A','D'])
        self.tiles.append(tile)
        
        tile=Tile("W",10,['.'])
        self.tiles.append(tile)

        tile=Tile("W",11,['.'])
        self.tiles.append(tile)

    def set_state(self,state_str):
        i=0
        for value in state_str.split("_"):
            self.tiles[i].values=value.split(",")
            i+=1


    #def __copy__(self):
        #cls = self.__class__
        #result = cls.__new__(cls)
        #result.tiles=[1,2,3,4,5,6,7,8,9,10,11]
        #result.set_state(self.to_string())
        #result.tiles
        #result.tiles
        #return result

    def get_legal_moves(self,force_src=-1):
        res=[]
        #print("A")
        for src in self.tiles:
            #print("S")
            if src.get_top_value() is None:
                continue #Nothing to move
            if force_src>-1:
                if src.position!=force_src:
                    continue #Prune1
            for dst in self.tiles:
                if dst.equals(src):
                    continue#Rule-no 0 length moves
                if dst.get_bot_empty() is None:
                    continue#Rule-destination tile is full
                if src.type=='W' and dst.type=='W':
                    continue#Rule-is-locked-until-can-go-home
                if dst.type!='W' and src.get_top_value()!=dst.type:
                    continue#Rule, this type of animal doesn't live in that destination-bucket
#                if src.type!='W' and src.get_top_value()=="D" and src.position!=9 and (dst.position>9 or dst.position<src.position):
#                    continue
                if dst.type!='W' :
                    dst_values=set(dst.values)
                    dst_values.discard(src.get_top_value())
                    dst_values.discard(".")
                    if len(dst_values)!=0:
                        continue#Rule, that animal won't share home with other types of animals.
                if src.type!='W' and src.values[0] != ".":
                    src_values=set(src.values)
                    src_values.discard(src.type)
                    src_values.discard(".")
                    #print(src_values)
                    if len(src_values)==0:
                        continue#Prevent loops. no sense in moving away from a perfectly arranged home-bucket.
                collision=False
                for tile in self.tiles:
                    if tile.type=='W' and tile.get_top_value() is not None and min(dst.position,src.position)<tile.position<max(dst.position,src.position):
                        collision=True
                if collision:
                    continue#Collisions not allowed
                cost=get_cost(src,dst)
                #new_state=copy.deepcopy(self)
                new_state=State()
                new_state.set_state(self.to_string())
                for tile in new_state.tiles:
                    if tile.equals(src):
                        tile.values[src.get_move_tile_src_index()]="."
                    if tile.equals(dst):
                        tile.values[dst.get_move_tile_dst_index()]=src.get_top_value()
                #print(new_state.to_string())
                res.append((cost, new_state,dst.type))
        for cand in res:
            if cand[2]!="W" and True:
                #Prune2: forced move
                return [(cand[0],cand[1],cand[2])]
        return res

    def to_string(self):
        return '_'.join([tile.to_string_short() for tile in self.tiles])

    def to_string_big(self):
        return ''.join(["=" for tile in self.tiles]) + "\n" +\
                ''.join([tile.values[0] if tile.type=="W" else "." for tile in self.tiles]) + "\n" +\
                ''.join([tile.values[-1] if tile.type!="W" else "#" for tile in self.tiles]) + "\n" +\
                ''.join([tile.values[-2] if tile.type!="W" else "#" for tile in self.tiles]) + "\n" +\
                ''.join([tile.values[-3] if tile.type!="W" and len(tile.values)>2 else "#" for tile in self.tiles]) + "\n" +\
                ''.join([tile.values[-4] if tile.type!="W" and len(tile.values)>2 else "#" for tile in self.tiles]) 

def do_all_moves(state_str):
    global g
    global debug
    global seen
    sum=0
    if seen[state_str]>0:
        return 0
    state=State()
    state.set_state(state_str)
    if debug<4:
        next_states=state.get_legal_moves(7)
    else:
        next_states=state.get_legal_moves(-1)

    #print(next_states)

    seen[state_str]+=1
    debug+=1
    for cost,next_state_str,move_type in next_states:
        #print(next_state.to_string())
        g.add_edge(state_str, next_state_str)
        g[state_str][next_state_str]['weight'] = cost
        #print(state.to_string(), next_state.to_string(), cost)
        do_all_moves(next_state_str)
    #print(len(g.nodes(True)))



init_state=State()

#start_string="._._D,D,D,C_._A,B,C,C_._B,A,B,B_._A,C,A,D_._."
start_string_test="._._A,A_._C,C_._B,B_._D,D_._."
start_string_part1="._._D,C_._A,C_._B,B_._A,D_._."
start_string_part2="._._D,D,D,C_._A,B,C,C_._B,A,B,B_._A,C,A,D_._."
start_string=start_string_part2

target_string_part1="._._A,A_._B,B_._C,C_._D,D_._."
target_string_part2="._._A,A,A,A_._B,B,B,B_._C,C,C,C_._D,D,D,D_._."
target_string=target_string_part2

#start_string=re.sub(r'[^D,_]','.',start_string)
#target_string=re.sub(r'[^D,_]','.',target_string)

init_state.set_state(start_string)

print(init_state.to_string())
print(init_state.to_string_big())

#Globals:
debug=0
seen=defaultdict(int)
g = nx.DiGraph()

do_all_moves(init_state)
print(f'Finised creating weighted graph, took {debug} recursive steps nodes={len(g.nodes(True))} edges={len(g.edges)}')

shortest_path=nx.shortest_path(g,start_string,target_string,"weight")
shortest_path_length=nx.shortest_path_length(g,start_string,target_string,"weight")
#print(shortest_path)
state=State()
prev_state=None
counter=Counter()
animated_path=[]
for state_str in shortest_path:
    state.set_state(state_str)
    if prev_state is not None:
        for p in prev_state.tiles:
            for s in state.tiles:
                if s.equals(p):
                    if s.values != p.values:
                        if p.type=="W" :
                            if p.values[-1]==".":
                                dst=p
                            else:
                                src=p
                        else:
                            if p.values[0]==".":
                                dst=p
                            elif s.values[0]==".":
                                src=p
                            elif p.get_move_tile_src_index()<s.get_move_tile_src_index():
                                dst=p
                            else:
                                src=p
        counter[src.get_top_value()]+=get_cost(src,dst)
    prev_state=copy.deepcopy(state)
    animated_path.append(state.to_string_big())

line0=""
line1=""
line2=""
line3=""
line4=""
line5=""
for idx,path in enumerate(animated_path):
    line0+=path.split("\n")[0]+"  "
    line1+=path.split("\n")[1]+"  "
    line2+=path.split("\n")[2]+"  "
    line3+=path.split("\n")[3]+"  "
    line4+=path.split("\n")[4]+"  "
    line5+=path.split("\n")[5]+"  "

    if idx%5==0:
        print(line0)
        print(line1)
        print(line2)
        print(line3)
        print(line4)
        print(line5)
        line0=""
        line1=""
        line2=""
        line3=""
        line4=""
        line5=""

print(line0)
print(line1)
print(line2)
print(line3)
print(line4)
print(line5)


print(f'shortest path printed above has cost {shortest_path_length}')
print(f'{counter}')


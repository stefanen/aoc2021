import sys
import networkx as nx
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

    def get_legal_moves(self):
        res=[]
        for src in self.tiles:
            if src.get_top_value() is None:
                continue
            for dst in self.tiles:
                if dst.equals(src):
                    continue
                if dst.get_bot_empty() is None:
                    continue
                if src.type=='W' and dst.type=='W':
                    continue
                if dst.type!='W' and src.get_top_value()!=dst.type:
                    continue
                if dst.type!='W' :
                    dst_values=set(dst.values)
                    dst_values.discard(src.get_top_value())
                    dst_values.discard(".")
                    if len(dst_values)!=0:
                        continue
                if src.type!='W' :
                    src_values=set(src.values)
                    src_values.discard(src.type)
                    src_values.discard(".")
                    #print(src_values)
                    if len(src_values)==0:
                        continue
                collision=False
                for tile in self.tiles:
                    if tile.type=='W' and tile.get_top_value() is not None and min(dst.position,src.position)<tile.position<max(dst.position,src.position):
                        collision=True
                if collision:
                    continue
                cost=abs(src.position-dst.position)
                if src.type!="W":
                    cost+=len(src.values)-src.get_move_tile_src_index()
                if dst.type!="W":
                    cost+=len(dst.values)-dst.get_move_tile_dst_index()
                cost=cost*COST.get(src.get_top_value())
                new_state=copy.deepcopy(self)
                for tile in new_state.tiles:
                    if tile.equals(src):
                        tile.values[src.get_move_tile_src_index()]="."
                    if tile.equals(dst):
                        tile.values[dst.get_move_tile_dst_index()]=src.get_top_value()

                res.append((cost, new_state,dst.type))
        for cand in res:
            if cand[2]!="W":
                #forced move
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

debug=0
seen=defaultdict(int)
def do_all_moves(state):
    global g
    global debug
    global seen
    next_states=state.get_legal_moves()
    sum=0
    if seen[state.to_string()]>0:
        return 0
    seen[state.to_string()]+=1
    for cost,next_state,move_type in next_states:

        debug+=1
        g.add_edge(state.to_string(), next_state.to_string())
        g[state.to_string()][next_state.to_string()]['weight'] = cost
        #print(state.to_string(), next_state.to_string(), cost)
        sum+=cost+do_all_moves(next_state)
    #print(len(g.nodes(True)))
    return sum



init_state=State()

#start_string="._._D,D,D,C_._A,B,C,C_._B,A,B,B_._A,C,A,D_._."
start_string_test="._._A,A_._C,C_._B,B_._D,D_._."
start_string_part1="._._D,C_._A,C_._B,B_._A,D_._."
start_string_part2="._._D,D,D,C_._A,B,C,C_._B,A,B,B_._A,C,A,D_._."
start_string=start_string_part2

target_string_part1="._._A,A_._B,B_._C,C_._D,D_._."
target_string_part2="._._A,A,A,A_._B,B,B,B_._C,C,C,C_._D,D,D,D_._."
target_string=target_string_part2
init_state.set_state(start_string)

print(init_state.to_string())
print(init_state.to_string_big())
g = nx.DiGraph()
do_all_moves(init_state)
print(f'Finised creating weighted graph, took {debug} recursive steps')

shortest_path=nx.shortest_path(g,start_string,target_string,"weight")
shortest_path_length=nx.shortest_path_length(g,start_string,target_string,"weight")
print(shortest_path)
state=State()
for state_str in shortest_path:
    state.set_state(state_str)
    print(state.to_string_big())
print(f'shortest path printed above has cost {shortest_path_length}')


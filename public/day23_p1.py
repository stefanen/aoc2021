import sys
import networkx as nx
import itertools
from collections import defaultdict
import copy
 
# Driver program
#g = Graph(9)
#g.graph = [[0, 4, 0, 0, 0, 0, 0, 8, 0],
#           [4, 0, 8, 0, 0, 0, 0, 11, 0],
#           [0, 8, 0, 7, 0, 4, 0, 0, 2],
#           [0, 0, 7, 0, 9, 14, 0, 0, 0],
#           [0, 0, 0, 9, 0, 10, 0, 0, 0],
#           [0, 0, 4, 14, 10, 0, 2, 0, 0],
#           [0, 0, 0, 0, 0, 2, 0, 1, 6],
#           [8, 11, 0, 0, 0, 0, 1, 0, 7],
#           [0, 0, 2, 0, 0, 0, 6, 7, 0]
#           ]

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
                    #print("collision")
                    continue

                #print(src.to_string(), dst.to_string(), src.get_top_value(), dst.get_bot_empty())
                #print(src.get_move_tile_src_index())
                #print(dst.get_move_tile_dst_index())
                
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


debug=0
seen=defaultdict(int)
def do_all_moves(state):
    global g
    global debug
    global seen
    next_states=state.get_legal_moves()
    sum=0
   # print("==="+state.to_string())
    #print("===")
    #print("===")
    #for cost,next_state in next_states:
        #print(next_state.to_string())
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
#print(init_state.to_string())
#init_state.set_state("A_._A,._._B,B_._C,C_._D,D_._.")
#init_state.set_state("._._D,C_._A,C_._B,B_._A,D_._.")
#start_string="._._D,C_._A,C_._B,B_._A,D_._."
#start_string="._._A,C_._C,A_._B,B_._D,D_._."
start_string="._._A,A_._C,C_._B,B_._D,D_._."
init_state.set_state(start_string)
print(init_state.to_string())
#sys.exit()
next_states=init_state.get_legal_moves()
#for s in next_states:
#    print(s[1].to_string())

g = nx.DiGraph()
#g.add_edge("a","b")
print(do_all_moves(init_state))
print(debug)
#print(g.edges(True))

shortest_path=nx.shortest_path(g,start_string,"._._A,A_._B,B_._C,C_._D,D_._.","weight")
shortest_path_length=nx.shortest_path_length(g,start_string,"._._A,A_._B,B_._C,C_._D,D_._.","weight")
print(shortest_path)
print(shortest_path_length)


import sys
import getopt
import copy
from collections import defaultdict
lines = open(0).read().strip().split("\n")

def run_instructions_brute(state,i,input_value):
    global INPUT_IDS
    state=copy.deepcopy(state)
    state[lines[INPUT_IDS[i]].split(" ")[1]]=input_value
    #print(f'setting {lines[INPUT_IDS[i]].split(" ")[1]} to {input_value}')
    for line in lines[INPUT_IDS[i]+1:INPUT_IDS[i+1]]:
        #print(input_value, state)
        #mutate state by instructions between i:th and i+1:th input instruction
        instr=line.split(" ")[0] 
        p_1=line.split(" ")[1] 
        p_2=line.split(" ")[2] 


        try:
            p_2=int(p_2)
        except:
            p_2=state[p_2]

        #print(instr,p_1,p_2)
        if instr=="add":
            state[p_1]=state[p_1]+p_2
        elif instr=="mul":
            state[p_1]=state[p_1]*p_2
        elif instr=="div":
            state[p_1]=state[p_1]//p_2
        elif instr=="mod":
            state[p_1]=state[p_1]%p_2
        elif instr=="eql":
            state[p_1]=1 if state[p_1]==p_2 else 0

    #print("result", state)
    return state

def run_instructions(state,i,input_value):
    index=INPUT_IDS[i]
    A=vars_per_chunk[index]["A"]
    B=vars_per_chunk[index]["B"]
    C=vars_per_chunk[index]["C"]
    if input_value == ((state["z"]%26)+B):
        return {
                "w":input_value,
                "x":0,
                "y":0,
                "z":state["z"]//A
                }
    else:
        return {
                "w":input_value,
                "x":1,
                "y":input_value+C,
                "z":26*(state["z"]//A)+input_value+C
                }



search_lists_medium={
        "0":[9],
        "1":[9],
        "2":[3],
        "3":[9],
        "4":[4],
        "5":[1,2,3,4,5,6,7,8,9],
        "6":[1,2,3,4,5,6,7,8,9],
        "7":[1,2,3,4,5,6,7,8,9],
        "8":[1,2,3,4,5,6,7,8,9],
        "9":[1,2,3,4,5,6,7,8,9],
        "10":[1,2,3,4,5,6,7,8,9],
        "11":[1,2,3,4,5,6,7,8,9],
        "12":[1,2,3,4,5,6,7,8,9],
        "13":[1,2,3,4,5,6,7,8,9]
        }
search_lists_big={
        "0":[1,2,3,4,5,6,7,8,9],
        "1":[1,2,3,4,5,6,7,8,9],
        "2":[1,2,3,4,5,6,7,8,9],
        "3":[1,2,3,4,5,6,7,8,9],
        "4":[1,2,3,4,5,6,7,8,9],
        "5":[1,2,3,4,5,6,7,8,9],
        "6":[1,2,3,4,5,6,7,8,9],
        "7":[1,2,3,4,5,6,7,8,9],
        "8":[1,2,3,4,5,6,7,8,9],
        "9":[1,2,3,4,5,6,7,8,9],
        "10":[1,2,3,4,5,6,7,8,9],
        "11":[1,2,3,4,5,6,7,8,9],
        "12":[1,2,3,4,5,6,7,8,9],
        "13":[1,2,3,4,5,6,7,8,9]
        }
search_lists_small={
        "0":[9],
        "1":[9],
        "2":[3],
        "3":[9],
        "4":[4],
        "5":[8],
        "6":[9],
        "7":[9],
        "8":[8],
        "9":[9],
        "10":[1],
        "11":[9],
        "12":[7],
        "13":[1,2,3,4,5,6,7,8,9]
        }

search_lists=search_lists_big

cache = defaultdict(int)
def loop(i,state,res):
    global cache
    if (i>len(INPUT_IDS)-2):
        if state["z"]==0 or print_all_opt:
            #return
            print(res, state)
            if not print_all_opt:
                sys.exit()
            return
        return
        #return 0

    search_range=search_lists[str(i)]
    if not do_part_2:
        search_range=reversed(search_range)

    for k in search_range:

        if cache[(i,k,state["z"])]>0:
            #print("OK")
            return
        cache[(i,k,state["z"])]+=1

        if i==13 and not (15<=state["z"]<=23):
            return

        #if i==13:
        #    print(state)
        
        if use_brute:
            new_state=run_instructions_brute(state,i,k)
        else:
            new_state=run_instructions(state,i,k)
        if i>len(INPUT_IDS)-3 and new_state["z"]==0:
            print(k,state, new_state) 
        #if i<4:
        #    print(k,new_state)
        loop(i+1,new_state,res+str(k))

def check_program(lines):
    state = {
        "w": 0,
        "x": 0,
        "y": 0,
        "z": 0,
    }
    loop(0,state,"")
#    for c_1 in reversed(range(1,10)):
#        new_state=run_instructions(state,0,c_1)
#        print(new_state) 
#        for c_2 in reversed(range(1,10)):
#            new_state=run_instructions(state,1,c_2)
#            print(new_state) 






print_all_opt = False
use_brute = False
do_part_2 = False
#timespan_profile = '5d'
try:
    opts, args = getopt.getopt(sys.argv[1:],"hp:i:c:",["profile=","interval=","cmd="])
except getopt.GetoptError:
    #print('test.py -i <inputfile> -o <outputfile>')
    print('incorrect usage. TODO add help')
    sys.exit(2)
for opt, arg in opts:
    if opt in ("-p", "--profile"):
        if arg=="1":
            print_all_opt=True
    if opt in ("-c", "--cmd"):
        if arg=="1":
            do_part_2=True

INPUT_IDS=[int(e[0]) for e in enumerate(lines) if list(e[1])[0]=="i"]
#print(INPUT_IDS)

vars_per_chunk={}
for i in INPUT_IDS:
    A=int(lines[i+4].split(" ")[2])
    B=int(lines[i+5].split(" ")[2])
    C=int(lines[i+15].split(" ")[2])
    vars_per_chunk[i]={"A":A,"B":B,"C":C}

print(vars_per_chunk)

INPUT_IDS+=[9999999999999999999999999]

check_program([e for e in lines])


state = {
    "w": 0,
    "x": 0,
    "y": 0,
    "z": 0,
}

#print(run_instructions(state,0,7))

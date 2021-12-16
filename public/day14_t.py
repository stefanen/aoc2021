from itertools import chain
from bidict import bidict
import collections
import sys
from collections import Counter 
from collections import defaultdict

def transform(x,y):
    return [rules[x+y],y]

def transform_20(state):
    for i in range(0,20):
        next_state=[state[0]]
        for x,y in zip(state, state[1:]):
                next_state.extend(transform(x,y))
        state=next_state
    #    print(state)
    return Counter(state)


input = open(0).read().strip()
lines=[e for e in input.split('\n')]
state=[e for e in lines[0]]
rules = defaultdict(lambda: "")

matrix= [ [ 0 for i in range(100) ] for j in range(100) ]

for i in range(0,len(lines[2:])):
    for j in range(0,len(lines[2:])):
            matrix[i][j]=0

#print(matrix)

t=bidict()

i=0
for rule in lines[2:]:
    t[i]=rule.split("->")[0].strip()
    i+=1

for rule in lines[2:]:
    from_1=rule.split("->")[0].strip()
    to_1=list(from_1)[0]+rule.split("->")[1].strip()
    to_2=rule.split("->")[1].strip()+list(from_1)[1]
    print(from_1,to_1,to_2)
    matrix[t.inverse[from_1]][t.inverse[to_1]]+=1
    matrix[t.inverse[from_1]][t.inverse[to_2]]+=1

    #rules[rule.split("->")[0].strip()]=rule.split("->")[1].strip()

#print(dict(sum(map(Counter, matrix), Counter())))

print(matrix)

init = [ 0 for i in range(100) ]
state_t="OHFNNCKCVOBHSSHONBNF"
for x,y in zip(state_t, state_t[1:]):
    init[t.inverse[x+y]]+=1
    #print(init)

res=[90086590031,90084832351,90060317495,90096098268,90066561080,90072925415,90052085137,90071375399,90059350203,90072942572,90066535196,90106485285,90059113312,90103116532,90064788020,90055763724,90048069264,90121973995,90059350203,90109558276,90087216228,90083205264
        ,90068535893,90069706933,90072709517,90077594990,90078862657,90083364364,90055945163,90111873339,90064628479,90081145554,90050021302,90068535893,90084151344,90082457953,90077168955,90052909516,90077538950,90099902951,90080654067,90085382579,90049406781,90087442754
        ,90064280210,90085346084,90092434368,90095309730,90098289087,90065279474,90049406781,90091401583,90074386048,90096098268,90084606110,90100926727,90068312872,90110187937,90062500893,90085499976,90066961163,90092241197,90077871160,90052251034,90089973805,90096098268
        ,90096098268,90067895072,90098313097,90074405004,90065041919,90063761528,90060867752,90062718752,90085422924,90071875352,90064517607,90092662218,90075573552,90077570530,90090084440,90070361649,90082961286,90077061796,90081471889,90052909516,90074405004,90063520344
        ,90071507828,90082956591,90081874735,90067765788,90126038147,90071360852,90074405004,90061732058,90059350203,90069136669,90061986995,90058684090]

res=init
res=[0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,0,1,0,0,0,1,0,0,2,1,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,1,0,0,2
        ,0,1,1,0,1,0,1,0,0,0,1,0,0,0,0,0,1,0,1,0,0,1,0]

res=[500724891914,330354068832,91074158191,442076723715,117774977007,134313140650,19795147739,150858648481,454450030211,17553095597,47859933937,465330757611,45538574702,297725819585,165154912529,360356297942,0,479125999487,389290301609


        ,744491784404,0,115210768033,318169132849,0,82572513947,474122555068,22770160672,95725214445,0,354133827199,39592764551,116328674365,6596263104,150264118692,177049053756,207227999607,0,636270751815


        ,230436924866,149122969615,0,106075000342,0,0,29366423776,0,708229774125,149122969615,232661885737,354825139864,152776817354,502721003974,0,149139600799,603422841218,298234573745,28938686228

        ,116328674365,0,0,470340807844,604118844666,301714394411,13194321036,0,0,825180395435,70221999971,167615525330,122400153799,93050639862,257685052678,235564580607,0,0,0


        ,57878947741,442010036918,0,35108787069,0,457749504005,331877989996,165171465483,186110386931,165215872188,381260590001,180177397438,250374639808,372234919235,0,421863804443,1489017408692,57600897093,444622085269

        ,0,1,45538574702,79189319665,305345237558]

sum=0
for i in res:
    sum+=i
print(sum)


j=0
res_dict=defaultdict(lambda: 0)
print(len(res))
for r in res:
    res_dict[list(t[j])[0]]+=r
    res_dict[list(t[j])[1]]+=r
    j+=1

res_dict["F"]+=1
res_dict["O"]+=1

for k, v in res_dict.items():
    res_dict[k]=v//2

res_list=sorted(Counter(res_dict).values())
print(Counter(res_dict))
print(res_list[-1]-res_list[0])
sys.exit()
#print(state)

cache=defaultdict()

is_first=True
for rule in rules:
    is_first=False

    print(rule)
    cache[rule]=transform_20(list(rule))
    if not is_first:
        cache[rule][list(rule)[0]]-=1

print(cache)
#sys.exit()
for i in range(0,20):
    print(i)
    next_state=[state[0]]
    for x,y in zip(state, state[1:]):
            next_state.extend(transform(x,y))
    state=next_state
#    print(state)
    print(Counter(state))

print("last phase")

res=Counter()
print(state[0],state[-1])
print(len(state))
i=0
for x,y in zip(state, state[1:]):
    if i%10000==0:
        print(i)
    i+=1
    res=res+cache[x+y]

print(res)
print(sorted(res.values())[-1]-sorted(res.values())[0])

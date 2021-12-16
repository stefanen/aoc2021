from itertools import chain
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
for rule in lines[2:]:
    rules[rule.split("->")[0].strip()]=rule.split("->")[1].strip()

print(rules)
print(state)

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

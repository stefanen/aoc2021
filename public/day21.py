start_a=4
score_a=0
start_b=5
score_b=0
target=100

def next_p(old,step):
    t=old+step
    if t>10:
        return t-10
    return t

def combos(n):
    if n==3:
        return 1

def g(p):
    (x_p,x_s,y_p,y_s, turn) = p
    if x_s>=target:
        return [1,0]
    if y_s>=target:
        return [0,1]
    sum_a=[0,0]
    steps=[(3,1),(4,3),(5,6),(6,7),(7,6),(8,3),(9,1)]
    if turn=="x":
        for step in steps:
            new_x_p=next_p(x_p,step[0])
            new_x_s=x_s+new_x_p
            sum_a=[step[1]*x+y for x,y in zip(
                g((new_x_p,new_x_s,y_p,y_s,"y"))
                ,sum_a)]
        return sum_a
    for step in steps:
        new_y_p=next_p(y_p,step[0])
        new_y_s=y_s+new_y_p
        sum_a=[step[1]*x+y for x,y in zip(
            g((x_p,x_s,new_y_p,new_y_s,"x"))
            ,sum_a)]
    return sum_a

def memoize(f):
    memo = {}
    def helper(x):
        if x not in memo:
            memo[x] = f(x)
        return memo[x]
    return helper


g=memoize(g)
print(g((start_a,0,start_b,0,"x")))

#dice_state=1
#for i in range(0,1000):
#    dice_sum=0
#    dice_sum+=dice_state
#
#
#    print(dice_sum)
#    if i%2==0:
#        start_a+=dice_sum
#        while start_a>10:
#            start_a-=10
#        score_a+=start_a
#    else:
#        start_b+=dice_sum
#        while start_b>10:
#            start_b-=10
#        score_b+=start_b
#
#    print(score_a, score_b)
#
#    if score_a>=21 or score_b>=21:
#         
#        print("done")
#        print(i)
#        print(min(score_a, score_b)*3*(i+1))
#        break


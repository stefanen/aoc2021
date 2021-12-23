start_a=4
score_a=0
start_b=8
score_b=0

dice_state=1
for i in range(0,1000):
    dice_sum=0
    dice_sum+=dice_state


    print(dice_sum)
    if i%2==0:
        start_a+=dice_sum
        while start_a>10:
            start_a-=10
        score_a+=start_a
    else:
        start_b+=dice_sum
        while start_b>10:
            start_b-=10
        score_b+=start_b

    print(score_a, score_b)

    if score_a>=21 or score_b>=21:
         
        print("done")
        print(i)
        print(min(score_a, score_b)*3*(i+1))
        break


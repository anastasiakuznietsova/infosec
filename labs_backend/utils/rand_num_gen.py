from math import pi, sqrt
from config import PRNG_COMPARISON_MODULE, PRNG_MULTIPLIER,PRNG_INCREMENT,PRNG_SEED

def pseudo_rand_num(n:int):
    m = PRNG_COMPARISON_MODULE
    a = PRNG_MULTIPLIER
    c = PRNG_INCREMENT
    x_0 = PRNG_SEED
    period = 0

    seq=[]
    unique_seq = ''
    x = []
    i=0

    while i<n:
        if period:
            seq.append(unique_seq)
            i += period
        else:
            x.append(x_0)
            x_0 = (a*x_0 + c) % m
            i+=1
        if (~period) and (x_0 in x):
            period = len(x)
            unique_seq = " ".join(str(x_i) for x_i in x)
            seq.append(unique_seq)
    return x,period, " ".join(seq)

def euclide(a,b):
    if a<b:
        a,b = b,a
    while True:
        r = a%b
        if r<=0:
            return b
        a = b
        b = r

def to_test_generator(arr):
    count_one = 0
    count_all = 0
    for i in range(0,len(arr)-1, 2):
        count_all+=1
        if euclide(arr[i+1],arr[i])==1:
            count_one+=1

    prob = count_one/count_all
    pi_est = sqrt(6 / prob)
    prob_act = 6/(pi**2)

    return prob,prob_act,pi_est,pi

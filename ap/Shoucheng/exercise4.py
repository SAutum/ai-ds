# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np

# list of distance 1 to a power of 2
def f_distance_int(n):
    l1 = [2**i+1 for i in range (1, n+1) if 2**i+1<=n]
    l2 = [2**i-1 for i in range (2, n+1) if 2**i-1<=n]
    l = list(set(l1 + l2))
    #l.sort()
    return l

#define a function to calculate all prime numbers 
def is_prime(n):
    p = [2]
    i=3
    j=0
    while i <=n:
        for j in range(0,len(p)):
            if i % p[j] == 0:
                i=i+1
                break
            elif i % p[j] != 0 and j==len(p)-1:
                p.append(i)
            else: continue
    return p
        
def main():
    n = 1000
    intersection = set(f_distance_int(n)).intersection(set(is_prime(n)))
    return intersection

if __name__=='__main__':
    main()



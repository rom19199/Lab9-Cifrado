# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 12:27:26 2021

@author: hugo_
"""

import random 
import base64
from math import gcd


def primesInRange(x, y):
    prime_list = []
    for n in range(x, y):
        isPrime = True

        for num in range(2, n):
            if n % num == 0:
                isPrime = False
                
        if isPrime:
            prime_list.append(n)
    return prime_list

prime_list = primesInRange(200,1000)
randomPrime = random.choice(prime_list)

# print('Generated random prime number: ', randomPrime)

def xgcd(a, b):
    
    if b == 0:
        return 0,1,0
 
    u0 = 1
    u1 = 0
    v0 = 0
    v1 = 1
 
    while b != 0:
        q = a//b
        r = a - b * q
        u = u0 - q * u1
        v = v0 - q * v1
        #Update a,b
        a = b
        b = r
        #Update for next iteration
        u0 = u1
        u1 = u
        v0 = v1
        v1 = v
 
    return  a, u0, v0

def modInv(n, a):
   
    mcd , u , v = xgcd(n,a)
    if mcd != 1:
        print("No existe inverso")
        return 0
     
    return u%a


def generator(minn,maxx):
    valido = False
    
    p = random.choice(primesInRange(minn, maxx))
    q = random.choice(primesInRange(minn,maxx))
    
    while p == q:
       p = random.choice(primesInRange(minn, maxx))
       q = random.choice(primesInRange(minn,maxx))
        
    N = p*q
    e=random.randint(2,N) % N
    phi = N - p - q + 1
    while (e % N) == 1 and (e % N) == ((N-1) % N) and gcd(e,phi) > 1 and valido == False:
        e = random.randint(2, N) % N
    d = modInv(e,phi)
    
    publicKey= base64.b64encode((str(e)+ '.' +str(N)).encode('ascii')).decode('ascii')
    privateKey= base64.b64encode((str(d)+ '.' +str(N)).encode('ascii')).decode('ascii')
    
    return publicKey,privateKey

print(generator(200,1000))

    
from Crypto.Util.number import *
from random import randint
import os

FLAG = os.getenv("FLAG").encode()
flag1 = FLAG[:15]
flag2 = FLAG[15:]

def crypto1():
    p = getPrime(1024)
    q = getPrime(1024)
    n = p * q
    e = 0x10001
    x1 = randint(0,2**11)
    y1 = randint(0,2**114)
    x2 = randint(0,2**11)
    y2 = randint(0,2**514)
    hint1 = x1*p+y1*q-0x114
    hint2 = x2*p+y2*q-0x514
    c = pow(bytes_to_long(flag1), e, n)
    print(n)
    print(c)
    print(hint1)
    print(hint2)

def crypto2():
    p = getPrime(1024)
    q = getPrime(1024)
    n = p * q
    e = 0x10001
    hint = pow(514*p - 114*q, n - p - q, n)
    c = pow(bytes_to_long(flag2),e,n)
    print(n)
    print(c)
    print(hint)

print("==================================================================")
crypto1()
print("==================================================================")
crypto2()
print("==================================================================")

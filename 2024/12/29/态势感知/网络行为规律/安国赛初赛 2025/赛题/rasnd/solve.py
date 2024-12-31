from Crypto.Util.number import *
from random import randint
from pwn import *
from math import gcd
from tqdm import *
from gmpy2 import iroot

if __name__ == '__main__':
    r = remote('node6.anna.nssctf.cn', 28764, level = 'debug')
    r.recvline()
    n1 = int(r.recvline().decode().strip())
    c1 = int(r.recvline().decode().strip())
    hint1 = int(r.recvline().decode().strip()) + 0x114
    hint2 = int(r.recvline().decode().strip()) + 0x514
    st = 0
    for x1 in trange(1, 2**11):
        if st: break
        for x2 in range(1, 2**11):
            if st: break
            xx =  hint1 * x2 - hint2 * x1
            pp = gcd(xx, n1)
            if 1 < pp < n1:
                p1 = pp
                q1 = n1 // p1
                phi1 = n1 - p1 - q1 + 1
                d1 = inverse(65537, phi1)
                f1 = long_to_bytes(pow(c1, d1, n1)).decode()
                st = 1

    r.recvline()
    n2 = int(r.recvline().decode().strip())
    c2 = int(r.recvline().decode().strip())
    hint = int(r.recvline().decode().strip())
    xx = inverse(hint, n2) # xx = 514*p - 114*q
    
    A = 514
    B = -xx
    C = -114*n2
    delta = iroot(B**2 - 4*A*C, 2)
    assert delta[1] == True
    x1 = (-B + delta[0])//2//A
    x2 = (-B - delta[0])//2//A
    if 1 < gcd(x1, n2) < n2:
        p2 = gcd(x1, n2)
    if 1 < gcd(x2, n2) < n2:
        p2 = gcd(x2, n2)
    q2 = n2 // p2
    phi2 = n2 - p2 - q2 + 1
    d2 = inverse(65537, phi2)
    f2 = long_to_bytes(pow(c2, d2, n2)).decode()
    print(f1 + f2)


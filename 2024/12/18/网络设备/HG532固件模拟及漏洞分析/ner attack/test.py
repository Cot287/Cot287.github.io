from Crypto.Util.number import *
from wiener_attack import ext_wiener_attack_2

if __name__ == '__main__':
    nbits = 1024
    dbits = nbits*5//14 - 10
    p = getPrime(nbits//2)
    q = getPrime(nbits//2)
    N = p * q
    phi = N - p - q + 1
    while 1:
        try:
            d1 = getRandomNBitInteger(dbits)
            e1 = inverse(d1, phi)
            d2 = getRandomNBitInteger(dbits)
            e2 = inverse(d2, phi)
            break
        except: continue
    ext_wiener_attack_2(N, e1, e2, dbits/nbits)

from gmpy2 import iroot
from tqdm import trange
def trival_division(x):
    if x < 2: return 0
    sqrtx = int(iroot(x, 2)[0])
    for i in trange(2, sqrtx+1):
        if x % i == 0:
            return 0
    return 1

def E_sieve_edu(N):
    vis = [1, 1] + [0] * (N-1)
    primes = []
    # 输出初始状态
    for i in range(N+1):
        if vis[i] == 0:print(f'{i}', end = ' ')
    print()
    # sieve
    for i in range(2, N+1):
        if vis[i] == 0:
            primes.append(i)
            t = 2*i
            while t <= N:
                vis[t] = 1
                t += i
            print(f'prime:{i}')
            for k in range(N+1):
                if vis[k] == 0:print(f'{k}', end = ' ')
            print()
    return primes

def fermat(N, k, debug = True):
    from random import randrange
    from math import gcd
    if N & 1 == 0 : return False
    for _ in range(k):
        a = randrange(1, N)
        if debug:print(f'a = {a}')

        t = gcd(a, N)
        if debug:print(f'({a}, {N}) = {t}')
        if t > 1 : return False

        t = pow(a, N-1, N)
        if debug:print(f'{a}^{N-1} mod {N} = {t}')
        if t > 1 : return False 
    return True

from random import randint
def Miller_Rabin(n, k, debug = True):
    n = abs(n)
    if n == 2 or n == 3: return True
    if n % 2 == 0 or n < 2: return False
    s = n - 1
    r = 0
    while s & 1 == 0:
        s >>= 1
        r += 1
    if debug : print(f'{n - 1} = {s}*2^{r}; (r, s) = {r, s}')
    for _ in range(k):
        a = randint(2, n-1)
        if debug : print(f'\na = {a}')
        x = pow(a, s, n)
        if debug : print(f'x = {x}', end = ', ')
        if x == 1 or x == n - 1:continue
        st = 0 # 标记是否出现-1
        for __ in range(r-1):
            x = x * x % n
            if debug : print(f'{x}', end = ', ')
            if x == n - 1:
                st = 1
                break
        if st == 0:return False
    return True

def AKS(n, debug = True):
    from time import time
    nbits = len(bin(n)) - 2
    logn = log(n,2)
    
    # 找到[l, r] 中是否有某个数的 pw 次方等于 n
    def binary_search(l, r, pw, n):
        if l > r : return False
        mid = (l + r)//2
        mid_power = mid**pw
        if mid_power == n:
            return True
        elif mid_power > n:
            return binary_search(l, mid - 1, pw, n)
        else:
            return binary_search(mid+1, r, pw, n)

    # 特判 n <= 30
    if n in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:return True
    if n <= 30:return False

    # 1 - 判断是否为方幂
    if debug: 
        print(f'Determine whether n is a k-th power.')
        start_time = time()
    # print(f'nbits = {nbits}')
    for pw in range(2, nbits):
        l = 1 << ((nbits - 1)//pw)
        r = 1 << (nbits//pw + 1)
        if binary_search(l, r, pw, n): return False
    if debug: print(f'use {time() - start_time}s\n')

    # 2 - 找到最小的r使 ord_r(n) > (logn)^2
    logn = log(n,2)
    if debug: 
        print(f'Find the smallest r such that ord_r(n) > (logn)^2')
        start_time = time()
    for r in range(ceil(logn**2), ceil(logn**5)):
        gg = gcd(r, n)
        if gg > 1 : continue
        t = n
        st = 1
        for k in range(ceil(logn**2)):
            if t == 1: 
                st = 0
                break
            t = (t*n) % r
        if st:
            if debug: 
                print(f'k = {k}, r = {r}')
                print(f'use {time() - start_time}s\n')
            break

    # 3 - 处理 n<r 或者 n 存在小因子的情形
    if debug: 
        print(f'n<r or n has small prime factors')
        start_time = time()
    for a in range(2, r+1):
        if 1 < gcd(a, n) < n:return False
    if n <= r : return True
    if debug : print(f'use {time() - start_time}s\n')

    # 4 - 验证方程
    if debug: 
        print(f'Verify equation')
        start_time = time()
    facr = list(factor(r))
    phir = prod([(p-1)*p**(e-1) for p, e in facr])
    PR.<X> = PolynomialRing(Zmod(n))
    QR = PR.quotient(X^r - 1)
    # phir 可能出现丢精问题

    '''只检测一次
    a = 1
    if not QR(X+a)^n == QR(X^n + a):
        if debug: print(f'use {time() - start_time}s\n')
        return False
    '''
    for a in range(1, int(phir**0.5 * logn)):
        if not QR(X+a)^n == QR(X^n + a):
            if debug: print(f'use {time() - start_time}s\n')
            return False
    if debug: print(f'use {time() - start_time}s\n')
    return True  




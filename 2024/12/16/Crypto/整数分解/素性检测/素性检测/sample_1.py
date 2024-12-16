from Crypto.Util.number import *
if __name__ == '__main__':
    N = 15347
    factor_base = [2]
    for i in range(2, 50):
        if isPrime(i) and kronecker(N, i) == 1:
            factor_base.append(i)

    sqtN = floor(N^0.5)
    Q = lambda x: (x+sqtN)^2 - N
    upper = int((2*N)^0.5) - sqtN
    T = [Q(i) for i in range(1, upper)]

    TT = [[i] for i in T]
    for pri in factor_base:
        for j in range(len(T)):
            if TT[j][0] % pri == 0:
                TT[j].append([pri, 0])
            while TT[j][0] % pri == 0:
                TT[j][0] //= pri
                TT[j][-1][1] += 1
                
    for i in range(len(T)):
        if TT[i][0] == 1:
            print(i+1, T[i], TT[i])

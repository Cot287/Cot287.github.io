# d < N^0.25
def wiener(N:int, e:int, debug = True):
    N = Integer(N)
    e = Integer(e)
    cf = (e / N).continued_fraction().convergents()
    for f in cf:
        k = f.numer()
        d = f.denom()
        if k == 0:
            continue
        phi_N = int(ceil((e * d / k) - 1))
        b = -(N - phi_N + 1)
        delta = b ^ 2 - 4 * N
        if delta >= 0:
            delta_sqrt = sqrt(delta)
            p = (-b + delta_sqrt) / 2
            q = (-b - delta_sqrt) / 2
            if p.is_integer() and q.is_integer() and (p * q) % N == 0:
                if debug:
                    p = int(p % N)
                    q = int(q % N)
                    print(f'┃p = {p}, q = {q}')
                    return p, q

# d_max < N^aln, aln < 5/14
def ext_wiener_attack_2(N, e1, e2, al2):
    import gmpy2
    M1 = int(gmpy2.mpz(N)**0.5)
    M2 = int(gmpy2.mpz(N)**(1+al2))
    A = matrix([
        [1, -N, 0, N^2],
        [0, e1, -e1, -e1*N],
        [0, 0, e2, -e2*N],
        [0, 0, 0, e1*e2]
    ]) * diagonal_matrix([N, M1, M2, 1])
    v = A.LLL()[0]
    v = (v[0]//N, v[1]//M1, v[2]//M2, v[3])
    try:
        s = int(v[1]//v[0])
        P.<x> = PolynomialRing(ZZ)
        f = x^2 + (s-1)*x + N
        p = int(f.roots()[0][0])
        q = N // p
        assert p * q == N and 1 < p < N
        print(f'┃p = {p}, q = {q}')
        return p, q
    except:
        pass
    return
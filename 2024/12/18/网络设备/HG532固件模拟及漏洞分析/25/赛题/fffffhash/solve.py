from Crypto.Util.number import *
mod = 2**128
h = 201431453607244229943761366749810895688
x = 0x0000000001000000000000000000013b
b0 = 0x6c62272e07bb014262b821756295c58d

def Babai_CVP(mat, target):
    M = mat.LLL()
    G = M.gram_schmidt()[0]
    diff = target
    for i in reversed(range(G.nrows())):
        diff -=  M[i] * ((diff * G[i]) / (G[i] * G[i])).round()
    return target - diff

def solve(M, lbounds, ubounds, weight = None):
    mat, lb, ub = copy(M), copy(lbounds), copy(ubounds)
    num_var  = mat.nrows()
    num_ineq = mat.ncols()
    assert len(lb) == len(ub) == num_ineq
    assert all([lb[i] <= ub[i] for i in range(num_ineq)])

    max_element = 0 
    for i in range(num_var):
        for j in range(num_ineq):
            max_element = max(max_element, abs(mat[i, j]))

    if weight == None:
        weight = num_ineq * max_element

    # scaling process begins
    max_diff = max([ub[i] - lb[i] for i in range(num_ineq)])
    applied_weights = []

    for i in range(num_ineq):
        ineq_weight = weight if lb[i] == ub[i] else max_diff // (ub[i] - lb[i])
        applied_weights.append(ineq_weight)
        for j in range(num_var):
            mat[j, i] *= ineq_weight
        lb[i] *= ineq_weight
        ub[i] *= ineq_weight

    # Solve CVP
    target = vector([(lb[i] + ub[i]) // 2 for i in range(num_ineq)])
    result = Babai_CVP(mat, target)

    try:
        assert all([lb[i] <= result[i] <= ub[i] for i in range(num_ineq)])
        return [result[i]//applied_weights[i] for i in range(num_ineq)]
    except:
        print(f'[+] nothing find')
        return

def recover(c):
    s = []
    b = b0
    for ci in c:
        # b*x + ci = b*x ^^ si
        s.append((b*x + ci)^^(b*x))
        b = b*x + ci
    return s

if __name__ == '__main__':
    for length in range(10, 50):
        A = matrix(ZZ, length+1, length+1)
        for i in range(length-1):
            A[i, -1] = -x^(i+1)
            A[i, i] = 1
        A[-2, -1] = h - b0*x^length
        A[-2, -2] = 1
        A[-1, -1] = mod
        L = A.LLL()
        lb = [-255] * (length-1) + [1, -255]
        ub = [255] * (length-1) + [1, 255]
        v = solve(L, lb, ub)
        print(v)
        try:
            vv = ([v[-1]] + v[:-2])[::-1]
            print(vv)
            s = recover([int(i) for i in vv])
            if all([0 <= i < 256 for i in s]):
                hx = bytes(s).hex()
                print(hx)
                break
        except:
            continue
    
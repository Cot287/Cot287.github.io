from subprocess import check_output
from re import findall
import sys
sys.set_int_max_str_digits(0)
dimension_min = 7

def flatter(M):
    z = "[[" + "]\n[".join(" ".join(map(str, row)) for row in M) + "]]"
    ret = check_output(["flatter"], input=z.encode())
    return matrix(M.nrows(), M.ncols(), map(int, findall(b"-?\\d+", ret)))

if __name__ == "__main__":
    # a, b, f, rlwe_modulus = load('C:/Users/28893/Desktop/信安国赛初赛 2025/lwewl/rlwe_ciphertext.sobj')
    a, b, f, rlwe_modulus = load('/home/cot287/rlwe_ciphertext.sobj')
    P.<x> = PolynomialRing(Zmod(rlwe_modulus))
    PR = P.quo(f)
    A1 = matrix(ZZ, 65, 64)
    for i in range(64):
        A1[i] = (-PR(a)*x^i).list()
    A1[64] = PR(b).list()
    A2 = diagonal_matrix([1] * 65)
    A3 = diagonal_matrix([rlwe_modulus] * 64)
    A4 = matrix(ZZ, 64, 65)
    A = block_matrix([[A1, A2], [A3, A4]])
    print(f'LLL start')
    L = flatter(A)
    print(f'Babai start')
    lb = [-5] * 64 + [0] * 64 + [1]
    ub = [5] * 64 + [255] * 64 + [1]
    tar = -L[0]
    f2 = bytes(tar[64:-1])
    
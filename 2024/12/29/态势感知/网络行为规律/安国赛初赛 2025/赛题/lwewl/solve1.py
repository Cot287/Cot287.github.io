from Crypto.Util.number import *
from tqdm import *
from string import ascii_lowercase
import itertools
P1, P2 = load('C:/Users/28893/Desktop/信安国赛初赛 2025/lwewl/lwe_public_key.sobj')
cipher1, cipher2 = load('C:/Users/28893/Desktop/信安国赛初赛 2025/lwewl/lwe_ciphertext.sobj')
P1 = matrix(P1)
P2 = matrix(P2).T
A = block_matrix([[P2.T], [P1.T]])
L = A.LLL()
e = matrix([int(i)//257 for i in L[0]]).T
# s = P1.solve_right(P2 - 257*e)
s = ((P1[:512]).inverse()) * ((P2 - 257*e)[:512])
assert P1*s + 257*e == P2

ss = matrix(Zmod(1048583), s)
cipher1 = matrix(Zmod(1048583), cipher1)
cipher2 = matrix(Zmod(1048583), cipher2).T
cc = cipher2 - cipher1*ss
ccc = [int(i)%257 for i in cc.T[0]]

f1_split = []
ls = '0123456789abcdef-'
for i in range(18):
    ii = ''
    for k in range(-2, 2):
        try:
            if chr(ccc[i] + 23*k) in ls:
                ii += chr(ccc[i] + 23*k)
        except:
            continue
    f1_split.append(ii)
print(f1_split)

f2 = '-8819-856a8fe5ada0'
i = [] * 16
for i in range(16):
    f1 = ''
    ii = i
    for j in range(18):
        if len(f1_split[j]) > 1:
            f1 += f1_split[j][ii & 1]
            ii >>= 1
        else:
            f1 += f1_split[j]
    print('NSSCTF{' + f1 + f2 + '}')
# NSSCTF{a3bc5491-fa53-4f47-8819-856a8fe5ada0}

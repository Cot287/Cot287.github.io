from Crypto.Util.number import *
from random import randint
from secret import flag

assert flag.startswith(b'flag{') and flag.endswith(b'}')
flag = flag[5:-1]
flag1 = flag[:len(flag)//2]
flag2 = flag[len(flag)//2:]

def distribution(lbound, rbound, dim):
    return [randint(lbound, rbound) for _ in range(dim)]

class LWE:
    def __init__(self, lwe_dim, lwe_num_samples, lwe_plaintext_modulus, lwe_ciphertext_modulus):
        self.lwe_dim = lwe_dim
        self.lwe_num_samples = lwe_num_samples
        self.lwe_plaintext_modulus = lwe_plaintext_modulus
        self.lwe_ciphertext_modulus = lwe_ciphertext_modulus
        self.lwe_secret_key = distribution(0, self.lwe_ciphertext_modulus - 1, self.lwe_dim)

    def lwe_encrypt(self):
        a = distribution(0, lwe_ciphertext_modulus - 1, self.lwe_dim)
        e = distribution(-15, 15, 1)[0]
        return a, sum([a[i] * self.lwe_secret_key[i] for i in range(self.lwe_dim)]) + e * lwe_plaintext_modulus

    def lwe_keygen(self):
        A = []
        B = []
        for _ in range(self.lwe_num_samples):
            sample = self.lwe_encrypt()
            A.append(sample[0])
            B.append(sample[1])
        return A, B

    def encrypt(self, message, lwe_pubkey1, lwe_pubkey2):
        const = vector(ZZ, distribution(-1, 1, self.lwe_num_samples))
        e = distribution(-15, 15, 1)[0]
        return const * matrix(GF(lwe_ciphertext_modulus), lwe_pubkey1), const * vector(GF(lwe_ciphertext_modulus), lwe_pubkey2) + message + e * lwe_plaintext_modulus

lwe_dim = 512
lwe_num_samples = 612
lwe_plaintext_modulus = 257
lwe_ciphertext_modulus = 1048583

lwe = LWE(lwe_dim, lwe_num_samples, lwe_plaintext_modulus, lwe_ciphertext_modulus)
lwe_pubkey1, lwe_pubkey2 = lwe.lwe_keygen()
lwe_public_key = [lwe_pubkey1, lwe_pubkey2]
lwe_cipher1 = []
lwe_cipher2 = []
for flag_char in flag1:
    tmp1, tmp2 = lwe.encrypt(flag_char, lwe_pubkey1, lwe_pubkey2)
    lwe_cipher1.append(tmp1)
    lwe_cipher2.append(tmp2)

lwe_ciphertext = [lwe_cipher1, lwe_cipher2]
save(lwe_public_key, "lwe_public_key")
save(lwe_ciphertext, "lwe_ciphertext")


# -------------------------------------------------------------------------------------------------------
rlwe_dim = 64
rlwe_modulus = getPrime(128)
P.<x> = PolynomialRing(Zmod(rlwe_modulus))
while True:
    monomials = [x^i for i in range(rlwe_dim + 1)]
    c = distribution(0, rlwe_modulus - 1, rlwe_dim) + [1]
    f = sum([c[i] * monomials[i] for i in range(rlwe_dim + 1)])
    PR = P.quo(f)
    if f.is_irreducible():
        break
a = distribution(0, rlwe_modulus - 1, rlwe_dim)
e = distribution(-5, 5, rlwe_dim)
s = [flag2[i] for i in range(len(flag2))]
b = PR(a) * PR(s) + PR(e)
rlwe_ciphertext = a, b, f, rlwe_modulus
save(rlwe_ciphertext, "rlwe_ciphertext")

import time
import random, sys 
from primes_gmpy2 import generate_prime
from gmpy2 import mpz, powmod, invert, random_state, mpz_urandomb, rint_round, log2, gcd

rand = random_state(random.randrange(sys.maxsize))

#TODO paillier: n = pq, g = n+1, l = (p-1)(q-1), m = l**-1 mod n, pub = (n, g), prv = (l, m)
class PublicKey(object):
    def __init__(self, n):
        self.n = n
        self.n_sq = n * n
        self.g = n + 1
        self.bits = mpz(rint_round(log2(self.n)))

class PrivateKey(object):
    def __init__(self, p, q, n):
        self.l = (p-1) * (q-1)
        self.m = invert(self.l, n)#l  mod n 的乘法逆元

def generate_keypair(bits):
    p = generate_prime(bits // 2)
    q = generate_prime(bits // 2)
    n = p * q
    return PrivateKey(p, q, n), PublicKey(n)

#TODO c = g^m * (r^n mod n^2) mod n^2
def encrypt(pub, plain):
    while True:
        r = mpz_urandomb(rand, pub.bits)
        if r > 0 and r < pub.n and gcd(r, pub.n) == 1:
            break
    x = powmod(r, pub.n, pub.n_sq)
    # if plain < 0:
    #     plain = plain + pub.n_sq
    cipher = (powmod(pub.g, plain, pub.n_sq) * x) % pub.n_sq
    return cipher

#TODO m = (c^l mod n^2 - 1) / n * m mod n
def decrypt(priv, pub, cipher):
    x = powmod(cipher, priv.l, pub.n_sq) - 1
    plain = ((x // pub.n) * priv.m) % pub.n
    if plain > pub.n/2:
        plain = plain - pub.n
    """// 取整除 - 返回商的整数部分"""
    return plain

#TODO E(m1)E(m2) mod n^2 = E(m1+m2)
def e_add(pub, a, b):
    return a * b % pub.n_sq

#TODO E(m1 + n) = E(m1) * (g^n mod n^2) mod n^2
def e_add_const(pub, a, n):
    return a * powmod(pub.g, n, pub.n_sq) % pub.n_sq

#TODO a = E(m1), E(m1*a) = E(m1)^a mod n^2
def e_mul_const(pub, a, n):
    return powmod(a, n, pub.n_sq)

if __name__ == '__main__':
    priv, pub = generate_keypair(1024)
    #
    # c_1 = encrypt(pub, 1)
    # c_2 = encrypt(pub, 2)
    # ans = e_add(pub, c_1, c_2)
    # m = decrypt(priv, pub, ans)
    # print(m)
    #
    # mul = 3
    # ans = e_mul_const(pub, c_2, 3)
    # m = decrypt(priv, pub, ans)
    # print(m)
    #
    # c_3 = encrypt(pub, -10001)
    # m = decrypt(priv, pub, c_3)
    # print(m)

    c_4 = encrypt(pub, 4)
    c_5 = encrypt(pub, 0)
    m = decrypt(priv, pub, powmod(c_4, c_5, pub.n_sq))
    print(m)
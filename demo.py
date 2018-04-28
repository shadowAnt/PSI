from paillier_gmpy2 import *
from numpy import *
import numpy as np
import random
from functools import reduce

keyword = [0, 1, 2]
m = len(keyword)
inverted_index = [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
doc = reduce(lambda x, y : set(x) | set(y), inverted_index) #{1, 2, 3, 4, 5}

priv, pub = generate_keypair(512)

#TODO sava coefficients to Pw and encrypt all coefficients to I_
Pw = []; I_ = []
for i in inverted_index:
    coe = [int(x) for x in poly(i)]
    Pw.append(coe)
    I_i = [encrypt(pub, x) for x in coe]
    I_.append(I_i)

#TODO construct matrix MD
MD = []
for i in keyword:
    md = [(mpz(i) ** j) for j in range(m, 0, -1)]
    MD.append(md)
MD = np.array(MD).T

#TODO the polynomial of keyword dictionary
PD = poly(keyword)

#TODO the Q consist of 0, 1
Q = poly([0, 1])
q = len([0, 1])
PQ = poly1d(PD) / Q
PQ = PQ[0] #多项式对象

#TODO to get trapdoor
pad = []
for i in range(q):
    pad.append(random.randint(100,200))
PQ1 = (PQ * poly(pad)).c #多项式系数
a0 = int(PQ1[-1])
a1 = PQ1[:-1]
TQ1 = np.array(a1)
TQ2 = encrypt(pub, a0)

V = np.dot(TQ1, MD)
V = [int(x) for x in V] #[0, 32563, 64408]
V3 = V
V1 = [e_add(pub, (encrypt(pub, x)), TQ2) for x in V]
V = [(x + a0) for x in V]

# DV1 = [decrypt(priv, pub, x) for x in V1] #0对应的i是非Q
# PR1 = np.dot(DV1, Pw)
# root = roots(PR1)
# root = [int(round(x)) for x in root]
# ans = doc & set(root)
# print(ans)

#TODO PR = V1 * I_
# I_ = np.array(I_)
# I_ = I_.T
# PR = []
# for i in range(len(I_)):
#     temp = [powmod(x, y, pub.n_sq) for x, y in zip(I_[i], V)]
#     ans = reduce(lambda x, y: np.mod((x * y), pub.n_sq), temp)
#     PR.append(ans)
#
# PR1 = [decrypt(priv, pub, x) for x in PR]
# root = roots(PR1)
# print(root)
# root = [int(round(x)) for x in root]
# ans = doc & set(root)
# print(ans)

I_ = np.array(I_)
I_ = I_.T
PR = []; sum = []
for i in range(len(I_)):
    temp = [powmod(x, y, pub.n_sq) for x, y in zip(I_[i], V3)]
    ans = reduce(lambda x, y: np.mod((x * y), pub.n_sq), temp)
    PR.append(ans)
for i in range(len(I_)):
    temp = I_[i]
    ans = reduce(lambda x, y: np.mod((x * y), pub.n_sq), temp)
    sum.append(ans)
print(sum)
sum = [np.mod(e_mul_const(pub, x, a0), pub.n_sq) for x in sum]
PR = [np.mod(e_add(pub, x, y), pub.n_sq) for x, y  in zip(PR, sum)]

PR1 = [decrypt(priv, pub, x) for x in PR]
root = roots(PR1)
print(root)
root = [int(round(x)) for x in root]
ans = doc & set(root)
print(ans)

if __name__ == "__main__":
    # print(inverted_index[keyword[2]])
    print()


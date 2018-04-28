'''
generate a prime of bits length
'''
import random
import sys
from gmpy2 import mpz, is_prime, random_state, mpz_urandomb
import time

#TODO choose a number from [0, sys.maxsize-1] to be seed
rand = random_state(random.randrange(sys.maxsize))

#TODO generate an integer of b bits that is prime using the gmpy2 library
def generate_prime(bits):
    bits -= 1
    base = mpz(2)**(bits)
    while True:
        add = mpz_urandomb(rand, (bits))
        possible = base + add
        if is_prime(possible):
            return possible

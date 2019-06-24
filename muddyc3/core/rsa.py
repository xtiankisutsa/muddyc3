# _____ ___________ ___________  ________   __  _____  _       ___ ______ _____  ___ _____ ___________ 
#/  __ \  _  |  _  \  ___|  _  \ | ___ \ \ / / |  __ \| |     / _ \|  _  \_   _|/ _ \_   _|  _  | ___ \
#| /  \/ | | | | | | |__ | | | | | |_/ /\ V /  | |  \/| |    / /_\ \ | | | | | / /_\ \| | | | | | |_/ /
#| |   | | | | | | |  __|| | | | | ___ \ \ /   | | __ | |    |  _  | | | | | | |  _  || | | | | |    / 
#| \__/\ \_/ / |/ /| |___| |/ /  | |_/ / | |   | |_\ \| |____| | | | |/ / _| |_| | | || | \ \_/ / |\ \ 
# \____/\___/|___/ \____/|___/   \____/  \_/    \____/\_____/\_| |_/___/  \___/\_| |_/\_/  \___/\_| \_|
#                                                                                                      
# 
'''
    620031587
    Net-Centric Computing Assignment
    Part A - RSA Encryption
'''

import random

'''
    Euclid's algorithm for determining the greatest common divisor
    Use iteration to make it faster for larger integers
'''
def gcd(a, b):

    while b != 0:
        a, b = b, a % b
    return a

'''
    Euclid's extended algorithm for finding the multiplicative inverse of two numbers
'''
def multiplicative_inverse(e, phi):

    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi
    
    while e > 0:
        temp1 = temp_phi/e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2
        
        x = x2- temp1* x1
        y = d - temp1 * y1
        
        x2 = x1
        x1 = x
        d = y1
        y1 = y
    
    if temp_phi == 1:
        return d + phi

'''
    Tests to see if a number is prime.
'''
def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in xrange(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True

def generate_keypair(p, q):

    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')
    # n = pq
    n = p * q
    # hi is the totient of n
    phi = (p-1) * (q-1)
    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)
    # Use Euclid's Algorithm to verify that e and phi(n) are comprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)
    # Return public and private keypair
    # Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))

def Mod(x,e,m):

    X = x
    E = e
    Y = 1
    while E > 0:
        if E % 2 == 0:
            X = (X * X) % m
            E = E/2
        else:
            Y = (X * Y) % m
            E = E - 1
    return Y


def encrypt(pk, plaintext):

    # Unpack the key into it's components
    key, n = pk
    # Convert each letter in the plaintext to numbers based on the character using a^b mod m
    cipher = [Mod((ord(char)), key, n) % n for char in plaintext]
    # Return the array of bytes
    return " ".join(map(str, cipher))



def decrypt(pk, ciphertext):

    key, n = pk
    ciphertext = map(int,ciphertext.split(" "))
    plain = [((char ** key) % n) for char in ciphertext]

    plain_a = []
    for ch in plain:
        try:
            plain_a.append(chr(ch))
        except:
            pass

    return ''.join(plain_a)

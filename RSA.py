# -*- coding: utf-8 -*-
"""
Mahmoud Sajjadi
May 14, 2023


This program implements a plain RSA encryption scheme.

The public key is the product of two large prime numbers, p and q.
The private key is the product of p-1 and q-1, modulo p*q.

The encryption algorithm works as follows:

1. Generate two large prime numbers, p and q.
2. Calculate N = p*q.
3. Calculate e, the public exponent.
4. Calculate d, the private exponent.
5. Return the triple (N, e, d).

The decryption algorithm works as follows:

1. Calculate x = (ye)^(-1) mod N.
2. Return x.

"""

import argparse
import random
import math

# Checking if a number is prime
def is_prime(n):
  """Returns True if n is prime, False otherwise."""
    if n < 2 or n % 2 == 0:
        return False
    if n == 2 or n == 3:
        return True

    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False

    return True

# print(is_prime(23))

# Extended Euclidean algorithm for computing modular inverses
def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y

# Generate an RSA key pair
def gen_rsa(p, q):
    """Generates a public and private key pair for plain RSA encryption.

  Args:
    n: The desired security level.

  Returns:
    A tuple (N, e, d), where N is the public key, e is the public exponent, and d is the private exponent.
  """
    N = p * q
    phi_n = (p - 1) * (q - 1)
    
    e = random.randint(2, p-1)
    
    while math.gcd(e, p-1) != 1:
      e = random.randint(2, p-1)
    # e = 3  # chosen as the public exponent
    
    # _, d, _ = egcd(e, phi_n)
    d = pow(e, -1, phi_n)
    # d = d % phi_n
    return N, e, d

# print(gen_rsa(23, 29))

# Encrypt a message using RSA
def encrypt(plaintext, n, e):
    return pow(plaintext, e, n)

# Decrypt a message using RSA
def decrypt(ciphertext, d, n):
    return pow(ciphertext, d, n)

# Parse command line arguments
parser = argparse.ArgumentParser(description='RSA encryption')
parser.add_argument('-gen', metavar='<n>', type=int, help='generate RSA key pair with n-bit primes')
# parser.add_argument('-enc', metavar=('<N>', '<e>', '<plaintext>'), type=int, nargs=3, help='encrypt plaintext using RSA public key')
parser.add_argument('-enc', metavar=('<N>', '<e>', '<plaintext>'), type=str, nargs=3, help='encrypt plaintext (in hexadecimal) using RSA public key')
parser.add_argument('-dec', metavar=('<N>', '<d>', '<ciphertext>'), type=int, nargs=3, help='decrypt ciphertext using RSA private key')
args = parser.parse_args()

if args.gen:
    # Generate an RSA key pair with n-bit primes
    n_bits = args.gen
    while True:
        p = random.getrandbits(n_bits)
        if is_prime(p):
            break
    while True:
        q = random.getrandbits(n_bits)
        if is_prime(q) and p != q:
            break
    N, e, d = gen_rsa(p, q)
    print(f'N = {N}')
    print(f'e = {e}')
    print(f'd = {d}')

elif args.enc:
    # Encrypt the plaintext using RSA
    N, e, plaintext = args.enc
    N = int(N)
    e = int(e)
    plaintext = plaintext.encode()  # Convert plaintext to bytes
    # print(int.from_bytes(plaintext, 'big'))
    # plaintext_bin = ''.join(format(ord(c), '08b') for c in plaintext)
    # print(plaintext_bin)
    # plaintext_hex = plaintext.encode().hex()  # Convert plaintext to hexadecimal
    # plaintext_int = int(plaintext_bin, 2)  # Convert hexadecimal to integer
    # print(plaintext_int)
    # ciphertext = encrypt(plaintext_int, N, e)
    ciphertext = encrypt(int.from_bytes(plaintext, 'big'), N, e)
    # ciphertext_hex = hex(ciphertext)[2:]  # Convert ciphertext to hexadecimal string
    print(f'Ciphertext: {ciphertext}')

elif args.dec:
    # Decrypt the ciphertext using RSA
    n, d, ciphertext = args.dec
    d = int(d)
    # ciphertext_int = int(ciphertext)
    # print(ciphertext)
    # n = 91
    plaintext_int = decrypt(ciphertext, d, n)  # Decrypt the ciphertext
    # print(plaintext_int)
    # plaintext_hex = hex(plaintext_int)[2:]
    plaintext_bytes = plaintext_int.to_bytes((plaintext_int.bit_length() + 7) // 8, 'big')
    # print(plaintext_bytes)
    plaintext = plaintext_bytes.decode('utf-8', 'replace')  # Convert decrypted plaintext to string
    # print(plaintext_hex)
    # plaintext = bytes.fromhex(plaintext_hex).decode('latin-1')
    print(f'Plaintext: {plaintext}')

else:
    parser.print_help()

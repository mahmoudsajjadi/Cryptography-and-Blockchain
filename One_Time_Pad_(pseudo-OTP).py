#
# Mahmoud Sajjadi, Apr 30, 2023
#


'''
Encryption Algorithm

This algorithm uses a 128-bit key to encrypt and decrypt a human-readable string.

Steps:

Key Generation: Generate a 128-bit key.
Encryption: Use the key to encrypt the human-readable string.
Decryption: Use the key to decrypt the encrypted string.
Input:

Key Generation: The length of the key.
Encryption: The 128-bit key and the human-readable string.
Decryption: The 128-bit key and the encrypted string.
Output:

Key Generation: The 128-bit key.
Encryption: The encrypted string.
Decryption: The human-readable string.
'''
import sys
import random

def generate_key(n):
    """
    Generates an n-bit key
    """
    key = ""
    for i in range(n):
        key += str(random.randint(0,1))
    return key

def encrypt(key, plaintext):
    """
    Encrypts plaintext using the given key
    Performs bitwise XOR of two strings key and plaintext 
    """
    ciphertext = ""
    plaintext_bin = ''.join(format(ord(c), '08b') for c in plaintext)
    # print('plaintext_bin:', plaintext_bin)
    for i in range(len(plaintext_bin)):
        # ciphertext += format(ord(plaintext_bin[i]) ^ int(key[i % len(key)]), '08b')
        # ciphertext += chr(ord(plaintext_bin[i]) ^ int(key[i % len(key)]))
        ciphertext += str(int(plaintext_bin[i]) ^ int(key[i % len(key)]))
    return ciphertext

def decrypt(key, ciphertext):
    """
    Decrypts ciphertext using the given key
    """

    plaintext_bin = ""
    for i in range(0, len(ciphertext)):
        plaintext_bin += str(int(ciphertext[i]) ^ int(key[i % len(key)]))
    plaintext = ""
    for i in range(0, len(plaintext_bin), 8):
        plaintext += chr(int(plaintext_bin[i:i+8], 2))
    return plaintext


def main():
    if len(sys.argv) < 3:
        print("correct format: " + sys.argv[0] + 
              " -gen <n:length of the key> | -enc <key> <plaintext> | -dec <key> <ciphertext>")
        return
    
    if sys.argv[1] == "-gen":
        n = int(sys.argv[2])
        key = generate_key(n)
        print(key)
    
    elif sys.argv[1] == "-enc":
        key = sys.argv[2]
        plaintext = sys.argv[3]
        ciphertext = encrypt(key, plaintext)
        print(ciphertext)
    
    elif sys.argv[1] == "-dec":
        key = sys.argv[2]
        ciphertext = sys.argv[3]
        plaintext = decrypt(key, ciphertext)
        print(plaintext)
    
    else:
        print("correct format: " + sys.argv[0] + 
              " -gen <n:length of the key> | -enc <key> <plaintext> | -dec <key> <ciphertext>")
        return

if __name__ == '__main__':
    main()
    

# vigenere_cipher.py

import re

def prepare_text(text):
    return re.sub(r'[^A-Za-z]', '', text).upper()

def generate_key(plaintext, key):
    key = key.upper()
    return (key * (len(plaintext) // len(key))) + key[:len(plaintext) % len(key)]

def encrypt(plaintext, key):  # ganti dari enkripsi
    plaintext = prepare_text(plaintext)
    key = generate_key(plaintext, key)
    ciphertext = ''
    for p, k in zip(plaintext, key):
        ciphertext += chr(((ord(p) - 65 + (ord(k) - 65)) % 26) + 65)
    return ciphertext

def decrypt(ciphertext, key):  # ganti dari dekripsi
    key = generate_key(ciphertext, key)
    plaintext = ''
    for c, k in zip(ciphertext, key):
        plaintext += chr(((ord(c) - 65 - (ord(k) - 65)) % 26) + 65)
    return plaintext

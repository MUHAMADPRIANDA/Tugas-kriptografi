def extend_key(plaintext, key):
    key = key.upper().replace(" ", "")
    plaintext = plaintext.upper().replace(" ", "")
    while len(key) < len(plaintext):
        key += plaintext[len(key)]
    return key

def enkripsi(plaintext, key):
    plaintext = plaintext.upper().replace(" ", "")
    key = extend_key(plaintext, key)
    cipher_text = ''
    for p, k in zip(plaintext, key):
        total = (ord(p) - 65 + ord(k) - 65) % 26
        cipher_text += chr(total + 65)
    return cipher_text

def dekripsi(ciphertext, key):
    ciphertext = ciphertext.upper().replace(" ", "")
    key = key.upper().replace(" ", "")
    plaintext = ''
    for i in range(len(ciphertext)):
        p = (ord(ciphertext[i]) - ord(key[i]) + 26) % 26
        char = chr(p + 65)
        plaintext += char
        key += char
    return plaintext

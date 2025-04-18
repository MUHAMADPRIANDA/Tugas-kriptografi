def extend_key(plaintext, key):
    key = key.upper().replace(" ", "")
    plaintext = plaintext.upper().replace(" ", "")
    while len(key) < len(plaintext):
        key += plaintext[len(key)]
    return key

def encrypt(plaintext, key):
    plaintext = plaintext.upper().replace(" ", "")
    key = extend_key(plaintext, key)
    cipher_text = ''
    for p, k in zip(plaintext, key):
        total = (ord(p) - 65 + ord(k) - 65) % 26
        cipher_text += chr(total + 65)
    return cipher_text

def decrypt(ciphertext, key):
    ciphertext = ciphertext.upper().replace(" ", "")
    key = key.upper().replace(" ", "")
    plaintext = ''
    for i in range(len(ciphertext)):
        p = (ord(ciphertext[i]) - ord(key[i]) + 26) % 26
        char = chr(p + 65)
        plaintext += char
        key += char  # extend key with the plaintext char
    return plaintext

# Program utama untuk memilih enkripsi atau dekripsi di terminal
if __name__ == "__main__":
    while True:
        print("\n------------Vigenere Cipher (Auto-Key Mode)------------")
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            plaintext = input("Enter Plain Text: ")
            key = input("Enter Key: ")
            encrypted = encrypt(plaintext, key)
            print("Cipher Text:", encrypted)

        elif choice == '2':
            ciphertext = input("Enter Cipher Text: ")
            key = input("Enter Key: ")
            decrypted = decrypt(ciphertext, key)
            print("Decrypted Plain Text:", decrypted)

        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")
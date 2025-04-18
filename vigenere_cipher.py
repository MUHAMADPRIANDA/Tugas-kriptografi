import re
import os

def prepare_text(text):
    """Membersihkan teks dari angka, spasi, dan tanda baca, hanya menyisakan huruf alfabet."""
    return re.sub(r'[^A-Za-z]', '', text).upper()

def generate_key(plaintext, key):
    """Mengulang key agar panjangnya sama dengan plainteks."""
    key = key.upper()
    return (key * (len(plaintext) // len(key))) + key[:len(plaintext) % len(key)]

def vigenere_encrypt(plaintext, key):
    """Mengenkripsi plainteks menggunakan Vigenere Cipher."""
    plaintext = prepare_text(plaintext)
    key = generate_key(plaintext, key)
    ciphertext = ''
    for p, k in zip(plaintext, key):
        ciphertext += chr(((ord(p) - 65 + (ord(k) - 65)) % 26) + 65)
    return ciphertext

def vigenere_decrypt(ciphertext, key):
    """Mendekripsi cipherteks menggunakan Vigenere Cipher."""
    key = generate_key(ciphertext, key)
    plaintext = ''
    for c, k in zip(ciphertext, key):
        plaintext += chr(((ord(c) - 65 - (ord(k) - 65)) % 26) + 65)
    return plaintext

def save_to_file(filename, content):
    """Menyimpan teks ke dalam file."""
    with open(filename, 'w') as file:
        file.write(content)

def load_from_file(filename):
    """Membaca teks dari file."""
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return file.read()
    return None

def main():
    while True:
        print("\nVigenere Cipher Encryption/Decryption Calculator")
        print("1. Enkripsi teks")
        print("2. Dekripsi teks")
        print("3. Simpan ciphertext ke file")
        print("4. Muat teks dari file")
        print("5. Keluar")
        
        choice = input("Pilih opsi (1-5): ")
        
        if choice == '1':
            plaintext = input("Masukkan plainteks: ")
            key = input("Masukkan kunci: ")
            ciphertext = vigenere_encrypt(plaintext, key)
            print("Ciphertext:", ciphertext)
        
        elif choice == '2':
            ciphertext = input("Masukkan cipherteks: ")
            key = input("Masukkan kunci: ")
            plaintext = vigenere_decrypt(ciphertext, key)
            print("Plainteks:", plaintext)
        
        elif choice == '3':
            content = input("Masukkan teks yang ingin disimpan: ")
            filename = input("Masukkan nama file: ")
            save_to_file(filename, content)
            print("Teks telah disimpan ke dalam file.")
        
        elif choice == '4':
            filename = input("Masukkan nama file yang ingin dimuat: ")
            content = load_from_file(filename)
            if content:
                print("Isi file:", content)
            else:
                print("File tidak ditemukan.")
        
        elif choice == '5':
            print("Keluar dari program.")
            break
        
        else:
            print("Pilihan tidak valid, coba lagi.")

if __name__ == "__main__":
    main()

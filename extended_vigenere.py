import base64

def encrypt_text(text, key):
    key_bytes = key.encode('utf-8')
    key_length = len(key_bytes)
    text_bytes = text.encode('utf-8')
    
    encrypted_bytes = bytearray()
    for i, byte in enumerate(text_bytes):
        encrypted_byte = (byte + key_bytes[i % key_length]) % 256
        encrypted_bytes.append(encrypted_byte)

    # Encode ke base64 agar aman ditampilkan sebagai teks
    return base64.b64encode(encrypted_bytes).decode('utf-8')

def decrypt_text(cipher_text, key):
    try:
        encrypted_bytes = base64.b64decode(cipher_text)
    except Exception:
        return "[ERROR] Format ciphertext tidak valid (bukan base64)."

    key_bytes = key.encode('utf-8')
    key_length = len(key_bytes)

    decrypted_bytes = bytearray()
    for i, byte in enumerate(encrypted_bytes):
        decrypted_byte = (byte - key_bytes[i % key_length]) % 256
        decrypted_bytes.append(decrypted_byte)

    return decrypted_bytes.decode('utf-8', errors='replace')

def encrypt_file(input_file, output_file, key):
    key_bytes = key.encode('utf-8')
    key_length = len(key_bytes)

    # Baca file dalam mode binary
    with open(input_file, 'rb') as f:
        data = f.read()

    encrypted_bytes = bytearray()
    for i, byte in enumerate(data):
        encrypted_byte = (byte + key_bytes[i % key_length]) % 256
        encrypted_bytes.append(encrypted_byte)

    # Encode hasil enkripsi ke base64 agar aman disimpan sebagai teks
    encoded_data = base64.b64encode(encrypted_bytes)

    # Simpan hasil enkripsi ke file output
    with open(output_file, 'wb') as f:
        f.write(encoded_data)


def decrypt_file(input_file, output_file, key):
    key_bytes = key.encode('utf-8')
    key_length = len(key_bytes)

    # Baca file yang terenkripsi dalam mode binary
    with open(input_file, 'rb') as f:
        encoded_data = f.read()

    # Decode data Base64
    try:
        encrypted_bytes = base64.b64decode(encoded_data)
    except Exception as e:
        return f"[ERROR] Format file terenkripsi tidak valid: {str(e)}"

    decrypted_bytes = bytearray()
    for i, byte in enumerate(encrypted_bytes):
        decrypted_byte = (byte - key_bytes[i % key_length]) % 256
        decrypted_bytes.append(decrypted_byte)

    # Simpan hasil dekripsi ke file output
    with open(output_file, 'wb') as f:
        f.write(decrypted_bytes)


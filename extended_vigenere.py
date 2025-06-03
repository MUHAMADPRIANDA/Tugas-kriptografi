def encrypt_text(text, key):
    key_bytes = key.encode('utf-8')
    key_length = len(key_bytes)
    text_bytes = text.encode('utf-8')
    result = bytearray()
    
    for i, byte in enumerate(text_bytes):
        encrypted_byte = (byte + key_bytes[i % key_length]) % 256
        result.append(encrypted_byte)

    return result.decode('latin1') 

def decrypt_text(text, key):
    key_bytes = key.encode('utf-8')
    key_length = len(key_bytes)
    text_bytes = text.encode('latin1')
    result = bytearray()
    
    for i, byte in enumerate(text_bytes):
        decrypted_byte = (byte - key_bytes[i % key_length]) % 256
        result.append(decrypted_byte)

    return result.decode('utf-8', errors='replace')

def encrypt_file(input_file, output_file, key):
    """Encrypts a file using Extended Vigenere Cipher."""
    key_bytes = key.encode('utf-8')
    key_length = len(key_bytes)

    with open(input_file, "rb") as f:
        file_data = f.read()

    encrypted_data = bytearray()
    for i, byte in enumerate(file_data):
        encrypted_data.append((byte + key_bytes[i % key_length]) % 256)

    with open(output_file, "wb") as f:
        f.write(encrypted_data)


def decrypt_file(input_file, output_file, key):
    """Decrypts a file using Extended Vigenere Cipher."""
    key_bytes = key.encode('utf-8')
    key_length = len(key_bytes)

    with open(input_file, "rb") as f:
        file_data = f.read()

    decrypted_data = bytearray()
    for i, byte in enumerate(file_data):
        decrypted_data.append((byte - key_bytes[i % key_length]) % 256)

    with open(output_file, "wb") as f:
        f.write(decrypted_data)

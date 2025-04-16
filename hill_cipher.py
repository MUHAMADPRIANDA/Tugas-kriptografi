import numpy as np
import re

def mod_inverse(det, mod=26):
    """Menghitung invers modulo dengan metode brute-force"""
    det = det % mod
    for i in range(1, mod):
        if (det * i) % mod == 1:
            return i
    return None

def generate_key_matrix(key):
    """Mengubah kunci menjadi matriks 2x2 atau 3x3"""
    key = [ord(c) - ord('A') for c in key.upper()]
    size = int(len(key) ** 0.5)
    if size * size != len(key):
        raise ValueError("Kunci harus berukuran 4 (2x2) atau 9 (3x3).")

    return np.array(key).reshape(size, size)

def matrix_mod_inverse(matrix, mod=26):
    """Menghitung invers modulo dari matriks untuk dekripsi Hill Cipher"""
    det = int(round(np.linalg.det(matrix))) % mod
    det_inv = mod_inverse(det, mod)
    if det_inv is None:
        raise ValueError("Determinant tidak memiliki invers modulo.")

    size = matrix.shape[0]
    if size == 2:
        inv_matrix = np.array([
            [ matrix[1][1], -matrix[0][1]],
            [-matrix[1][0],  matrix[0][0]]
        ])
    elif size == 3:
        cofactors = np.zeros_like(matrix)
        for r in range(3):
            for c in range(3):
                minor = np.delete(np.delete(matrix, r, axis=0), c, axis=1)
                cofactors[r][c] = ((-1)**(r+c)) * int(round(np.linalg.det(minor)))
        inv_matrix = cofactors.T  # adjugate
    else:
        raise ValueError("Ukuran matriks tidak didukung.")

    inv_matrix = (det_inv * inv_matrix) % mod
    return inv_matrix.astype(int)

def process_text(text, size):
    """Memastikan panjang teks kelipatan ukuran matriks"""
    text = re.sub('[^A-Z]', '', text.upper())
    padding = (size - len(text) % size) % size
    text += 'X' * padding
    return text

def text_to_matrix(text, size):
    """Ubah teks ke dalam bentuk matriks kolom"""
    nums = [ord(c) - ord('A') for c in text]
    return np.array(nums).reshape(-1, size).T

def matrix_to_text(matrix):
    """Ubah matriks hasil ke bentuk teks"""
    nums = matrix.T.flatten()
    return ''.join(chr(n % 26 + ord('A')) for n in nums)

def hill_encrypt(text, key):
    key_matrix = generate_key_matrix(key)
    size = key_matrix.shape[0]
    text = process_text(text, size)
    text_matrix = text_to_matrix(text, size)
    result_matrix = np.dot(key_matrix, text_matrix) % 26
    return matrix_to_text(result_matrix)

def hill_decrypt(text, key):
    key_matrix = generate_key_matrix(key)
    size = key_matrix.shape[0]
    text = process_text(text, size)
    text_matrix = text_to_matrix(text, size)
    inverse_key_matrix = matrix_mod_inverse(key_matrix)
    result_matrix = np.dot(inverse_key_matrix, text_matrix) % 26
    return matrix_to_text(result_matrix)

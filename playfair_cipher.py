def buat_matriks_kunci(kunci):
    abjad = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # Tanpa 'J'
    kunci = kunci.upper().replace(" ", "").replace("J", "I")
    matriks = []
    sudah_digunakan = set()

    for huruf in kunci + abjad:
        if huruf not in sudah_digunakan and huruf in abjad:
            matriks.append(huruf)
            sudah_digunakan.add(huruf)
        if len(matriks) == 25:
            break

    return [matriks[i:i+5] for i in range(0, 25, 5)]

def cari_posisi(matriks, huruf):
    for i, baris in enumerate(matriks):
        if huruf in baris:
            return i, baris.index(huruf)
    return None, None

def siapkan_plaintext(teks):
    teks = teks.upper().replace(" ", "").replace("J", "I")
    hasil = []
    i = 0
    while i < len(teks):
        a = teks[i]
        if i + 1 < len(teks):
            b = teks[i + 1]
            if a == b:
                hasil.append(a + 'X')
                i += 1
            else:
                hasil.append(a + b)
                i += 2
        else:
            hasil.append(a + 'X')
            i += 1
    return hasil

def encrypt(plaintext, kunci):
    matriks = buat_matriks_kunci(kunci)
    pasangan = siapkan_plaintext(plaintext)
    hasil = ''

    for pair in pasangan:
        a, b = pair[0], pair[1]
        ax, ay = cari_posisi(matriks, a)
        bx, by = cari_posisi(matriks, b)

        if ax == bx:  # Sama baris
            hasil += matriks[ax][(ay + 1) % 5]
            hasil += matriks[bx][(by + 1) % 5]
        elif ay == by:  # Sama kolom
            hasil += matriks[(ax + 1) % 5][ay]
            hasil += matriks[(bx + 1) % 5][by]
        else:  # Bentuk persegi
            hasil += matriks[ax][by]
            hasil += matriks[bx][ay]

    return hasil

def decrypt(ciphertext, kunci):
    matriks = buat_matriks_kunci(kunci)
    pasangan = [ciphertext[i:i+2] for i in range(0, len(ciphertext), 2)]
    hasil = ''

    for pair in pasangan:
        a, b = pair[0], pair[1]
        ax, ay = cari_posisi(matriks, a)
        bx, by = cari_posisi(matriks, b)

        if ax == bx:
            hasil += matriks[ax][(ay - 1) % 5]
            hasil += matriks[bx][(by - 1) % 5]
        elif ay == by:
            hasil += matriks[(ax - 1) % 5][ay]
            hasil += matriks[(bx - 1) % 5][by]
        else:
            hasil += matriks[ax][by]
            hasil += matriks[bx][ay]

    return hasil
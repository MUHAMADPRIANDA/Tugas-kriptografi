def buat_matriks_kunci(kunci):
    abjad = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    kunci = kunci.upper().replace(" ", "")
    matriks = []
    sudah_digunakan = set()

    for huruf in kunci + abjad:
        if huruf not in sudah_digunakan and huruf in abjad:
            matriks.append(huruf)
            sudah_digunakan.add(huruf)
        if len(matriks) == 26:
            break

    return [matriks[i:i+5] for i in range(0, 25, 5)]  # 5x5 grid, 26 huruf (1 sisa nanti dipisah)


def cari_posisi(matriks, huruf):
    for i, baris in enumerate(matriks):
        if huruf in baris:
            return i, baris.index(huruf)
    return None, None


def siapkan_plaintext(teks):
    teks = teks.upper().replace(" ", "")
    hasil = []
    i = 0
    while i < len(teks):
        a = teks[i]
        b = ''
        if i + 1 < len(teks):
            b = teks[i+1]
        if a == b:
            hasil.append(a + 'X')
            i += 1
        else:
            if b:
                hasil.append(a + b)
                i += 2
            else:
                hasil.append(a + 'X')
                i += 1
    return hasil


def enkripsi(plaintext, kunci):
    matriks = buat_matriks_kunci(kunci)
    pasangan = siapkan_plaintext(plaintext)
    hasil = ''

    for pair in pasangan:
        a, b = pair[0], pair[1]
        ax, ay = cari_posisi(matriks, a)
        bx, by = cari_posisi(matriks, b)

        if ax == bx:
            hasil += matriks[ax][(ay + 1) % 5]
            hasil += matriks[bx][(by + 1) % 5]
        elif ay == by:
            hasil += matriks[(ax + 1) % 5][ay]
            hasil += matriks[(bx + 1) % 5][by]
        else:
            hasil += matriks[ax][by]
            hasil += matriks[bx][ay]

    return hasil


def dekripsi(ciphertext, kunci):
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


# Program utama dengan menu berbahasa Indonesia
if __name__ == "__main__":
    while True:
        print("\n------------ Playfair Cipher (Mode 26 Huruf) ------------")
        print("1. Enkripsi")
        print("2. Dekripsi")
        print("3. Keluar")
        pilihan = input("Pilih menu (1/2/3): ")

        if pilihan == '1':
            plaintext = input("Masukkan Plain Text: ")
            kunci = input("Masukkan Kunci: ")
            hasil = enkripsi(plaintext, kunci)
            print("Hasil Enkripsi:", hasil)

        elif pilihan == '2':
            ciphertext = input("Masukkan Cipher Text: ")
            kunci = input("Masukkan Kunci: ")
            hasil = dekripsi(ciphertext, kunci)
            print("Hasil Dekripsi:", hasil)

        elif pilihan == '3':
            print("Program dihentikan.")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

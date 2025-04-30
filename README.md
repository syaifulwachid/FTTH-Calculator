# Kalkulator Estimasi Kebutuhan Material FTTH

Program ini digunakan untuk menghitung kebutuhan material dan loss budget dalam perencanaan jaringan Fiber To The Home (FTTH).

## Fitur Utama

1. **Perhitungan Material**:
   - Jumlah FAT yang dibutuhkan
   - Jenis dan jumlah kabel
   - Jenis dan jumlah FDT
   - Jenis dan jumlah splitter (FDT dan FAT)
   - Sisa core yang tersedia

2. **Perhitungan Loss Budget**:
   - Loss per FAT
   - Loss konektor
   - Loss splice
   - Loss kabel
   - Loss splitter
   - Total loss dengan margin keamanan

3. **Informasi Core dan Tube**:
   - Core active dan idle per FAT
   - Posisi tube dan warnanya
   - Core monitor per tube
   - Warna core sesuai standar

## Cara Penggunaan

1. **Input Data**:
   - Jumlah rumah (default: 500)
   - Jarak total dalam meter (default: 1000)
   - Pilih jenis kabel (default: 24 Core)
   - Pilih jenis FDT
   - Pilih jenis splitter FDT (default: 1:8)
   - Pilih jenis splitter FAT (default: 1:16)

2. **Hasil Perhitungan**:
   - Tampilan summary di bagian atas
   - Detail per FAT dengan slider
   - Informasi core monitor per tube
   - Opsi untuk menyimpan hasil

## Standar Warna Core

1. Biru
2. Oranye
3. Hijau
4. Coklat
5. Abu-abu
6. Putih
7. Merah
8. Hitam
9. Kuning
10. Ungu
11. Merah Muda
12. Aqua

## Pola Core per Tube

- Setiap tube memiliki 12 core
- 5 FAT per tube (menggunakan 10 core)
- Core 11 dan 12 di setiap tube adalah core monitor
- Warna tube mengikuti urutan warna standar

## Batas Loss

- Batas maksimum loss yang direkomendasikan: 28 dB
- Margin keamanan: 3 dB
- Peringatan akan muncul jika total loss melebihi batas

## Persyaratan Sistem

- Python 3.x
- Tkinter
- Sistem operasi: Windows/Linux/MacOS

## Cara Menjalankan

1. Pastikan Python terinstal
2. Jalankan file `Calculator.py`
3. Masukkan data yang diperlukan
4. Klik tombol "Hitung Kebutuhan Material"

## Kontak

Dikembangkan oleh Syaiful Wachid
Senior Project Designer
Fiberhome Indonesia

# Kalkulator Estimasi Kebutuhan Material FTTH

## Deskripsi
Program ini adalah kalkulator yang dirancang untuk menghitung kebutuhan material dalam proyek Fiber To The Home (FTTH). Pengguna dapat memasukkan jumlah rumah yang akan dilayani, memilih jenis kabel dan FDT (Fiber Distribution Terminal), dan program akan menghitung jumlah FAT (Fiber Access Terminal), kabel, dan FDT yang dibutuhkan.

## Fitur
- Menghitung jumlah FAT yang dibutuhkan berdasarkan jumlah rumah.
- Menghitung jumlah kabel yang dibutuhkan berdasarkan jenis kabel yang dipilih.
- Menghitung jumlah FDT yang dibutuhkan berdasarkan jenis FDT yang dipilih.
- Menampilkan sisa core setelah pemakaian dan jumlah rumah yang masih bisa dicover.
- Menyimpan hasil kalkulasi ke dalam file teks.

## Jenis Kabel yang Didukung
- 12 Core
- 24 Core
- 36 Core
- 48 Core
- 72 Core
- 96 Core
- 144 Core
- 192 Core
- 216 Core
- 288 Core

## Jenis FDT yang Didukung
- FDT 48
- FDT 72
- FDT 96
- FDT 144
- FDT 288

## Cara Penggunaan
1. Jalankan program.
2. Masukkan jumlah rumah yang ingin dilayani.
3. Pilih jenis kabel dari dropdown yang tersedia.
4. Pilih jenis FDT dari dropdown yang tersedia.
5. Klik tombol "Hitung Kebutuhan Material" untuk melakukan perhitungan.
6. Hasil perhitungan akan ditampilkan dalam jendela pop-up.
7. Anda dapat memilih untuk menyimpan hasil kalkulasi ke dalam file teks.

## Persyaratan
- Python 3.x
- Tkinter (biasanya sudah terinstal dengan Python)

## Instalasi
1. Pastikan Python 3.x terinstal di sistem Anda.
2. Salin kode program ke dalam file Python (misalnya, `FTTH_Calculator.py`).
3. Jalankan program menggunakan perintah:
   ```bash
   python FTTH_Calculator.py
   ```
```bash
   import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import filedialog

# Fungsi untuk menghitung kebutuhan material
def calculate_material():
    try:
        # Ambil jumlah rumah dari input
        num_houses = int(entry_houses.get())
        
        # Ambil jenis kabel dan FDT dari input
        selected_cable = cable_var.get()
        selected_fdt = fdt_var.get()
        
        # Hitung jumlah FAT yang dibutuhkan
        fat_needed = (num_houses + 15) // 16  # 1 FAT bisa mengcover 16 rumah
        
        # Hitung jumlah kabel yang dibutuhkan
        if selected_cable == "12 Core":
            cable_needed = (fat_needed + 5) // 6  # 1 kabel 12 core untuk 5 FAT
            total_cores = cable_needed * 12
        elif selected_cable == "24 Core":
            cable_needed = (fat_needed + 9) // 10  # 1 kabel 24 core untuk 10 FAT
            total_cores = cable_needed * 24
        elif selected_cable == "36 Core":  # Tambahan untuk kabel 36 Core
            cable_needed = (fat_needed + 14) // 15  # 1 kabel 36 core untuk 15 FAT
            total_cores = cable_needed * 36
        elif selected_cable == "48 Core":
            cable_needed = (fat_needed + 19) // 20  # 1 kabel 48 core untuk setiap 20 FAT
            total_cores = cable_needed * 48
        elif selected_cable == "72 Core":  # Tambahan untuk kabel 72 Core
            cable_needed = (fat_needed + 29) // 30  # 1 kabel 72 core untuk 30 FAT
            total_cores = cable_needed * 72
        elif selected_cable == "96 Core":  # Tambahan untuk kabel 96 Core
            cable_needed = (fat_needed + 39) // 40  # 1 kabel 96 core untuk 40 FAT
            total_cores = cable_needed * 96
        elif selected_cable == "144 Core":  # Tambahan untuk kabel 144 Core
            cable_needed = (fat_needed + 59) // 60  # 1 kabel 144 core untuk 60 FAT
            total_cores = cable_needed * 144
        elif selected_cable == "192 Core":  # Tambahan untuk kabel 192 Core
            cable_needed = (fat_needed + 79) // 80  # 1 kabel 192 core untuk 80 FAT
            total_cores = cable_needed * 192
        elif selected_cable == "216 Core":  # Tambahan untuk kabel 216 Core
            cable_needed = (fat_needed + 89) // 90  # 1 kabel 216 core untuk 90 FAT
            total_cores = cable_needed * 216
        elif selected_cable == "288 Core":  # Tambahan untuk kabel 288 Core
            cable_needed = (fat_needed + 119) // 120  # 1 kabel 288 core untuk 120 FAT
            total_cores = cable_needed * 288
        
        # Hitung jumlah FDT yang dibutuhkan
        if selected_fdt == "FDT 48":
            fdt_needed = (fat_needed + 19) // 20  # 1 FDT 48 untuk maksimal 20 FAT
            fdt_cores = 48
        elif selected_fdt == "FDT 72":
            fdt_needed = (fat_needed + 29) // 30  # 1 FDT 72 untuk setiap 30 FAT
        elif selected_fdt == "FDT 96":  # Tambahan untuk FDT 96
            fdt_needed = (fat_needed + 39) // 40  # 1 FDT 96 untuk setiap 40 FAT
        elif selected_fdt == "FDT 144":  # Tambahan untuk FDT 144
            fdt_needed = (fat_needed + 59) // 60  # 1 FDT 144 untuk setiap 60 FAT
        elif selected_fdt == "FDT 288":  # Tambahan untuk FDT 288
            fdt_needed = (fat_needed + 119) // 120  # 1 FDT 288 untuk setiap 120 FAT
        
        # Hitung sisa core
        used_cores = fat_needed * 2  # 2 core per FAT
        remaining_cores = total_cores - used_cores
        
        # Hitung total FAT yang masih bisa ditambahkan
        # Setiap tube berisi 12 core, dengan 2 core idle per tube
        cores_per_tube = 12
        idle_cores_per_tube = 2
        
        # Hitung jumlah tube yang ada
        total_tubes = total_cores // cores_per_tube
        
        # Hitung total core idle yang harus disisakan
        total_idle_cores = total_tubes * idle_cores_per_tube
        
        # Hitung core yang bisa digunakan untuk FAT
        usable_cores = remaining_cores - total_idle_cores
        
        # Hitung total FAT yang bisa ditambahkan
        additional_fat = usable_cores // 2  # 2 core per FAT
        additional_fat = max(0, additional_fat)  # Tidak boleh negatif
        
        # Hitung jumlah rumah yang masih bisa dicover
        houses_coverable = additional_fat * 16  # 1 FAT bisa mengcover 16 rumah
        
        # Tampilkan hasil
        result = f"Jumlah rumah yang diinput: {num_houses}\n\n"
        result += f"Jumlah FAT yang dibutuhkan: {fat_needed}\n"
        result += f"Jenis kabel yang dipilih: {selected_cable} (Jumlah: {cable_needed})\n"
        result += f"Jenis FDT yang dipilih: {selected_fdt} (Jumlah: {fdt_needed})\n"
        result += f"Sisa core setelah pemakaian: {remaining_cores}\n\n"
        result += f"Total FAT yang masih bisa ditambahkan: {additional_fat}\n"
        result += f"Jumlah rumah yang masih bisa dicover oleh sisa FAT: {houses_coverable}\n\n"
        result += f"Jumlah tube yang digunakan: {total_tubes}\n"
        result += f"Total sisa core idle: {total_idle_cores}\n"
        result += f"Sisa core yang bisa digunakan untuk FAT tambahan: {usable_cores}\n\n"
        
        # Saran penggunaan jenis kabel ganda
        if selected_cable == "24 Core" and additional_fat > 0:
            result += "Saran: Pertimbangkan menggunakan kabel 48 Core untuk efisiensi material.\n"
        elif selected_cable == "48 Core" and additional_fat > 0:
            result += "Saran: Anda sudah menggunakan kabel 48 Core, tidak perlu ganda.\n"
        
        # Tampilkan hasil perhitungan
        messagebox.showinfo("Hasil Perhitungan", result)
        
        # Tanyakan apakah ingin menyimpan hasil
        if messagebox.askyesno("Simpan Hasil", "Apakah Anda ingin menyimpan hasil kalkulasi?"):
            save_to_file(result)
    
    except ValueError:
        messagebox.showerror("Input Error", "Harap masukkan jumlah rumah yang valid.")

# Fungsi untuk menyimpan hasil ke file
def save_to_file(content):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                               filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(content)
        messagebox.showinfo("Simpan File", "Hasil telah disimpan ke file.")

# Membuat antarmuka pengguna
root = tk.Tk()
root.title("Kalkulator Estimasi Kebutuhan Material FTTH")

# Menyesuaikan ukuran jendela
root.geometry("430x350")  # Set ukuran jendela (lebar x tinggi)

# Label dan input untuk jumlah rumah
label_houses = tk.Label(root, text="Masukkan jumlah rumah:")
label_houses.pack(pady=10)

entry_houses = tk.Entry(root)
entry_houses.pack(pady=5)

# Dropdown untuk memilih jenis kabel
cable_var = tk.StringVar()
label_cable = tk.Label(root, text="Pilih jenis kabel:")
label_cable.pack(pady=10)

cable_options = ["12 Core", "24 Core", "36 Core", "48 Core", "72 Core", "96 Core", "144 Core", "192 Core", "216 Core", "288 Core"]  # Tambahkan semua opsi kabel baru
cable_dropdown = ttk.Combobox(root, textvariable=cable_var, values=cable_options)
cable_dropdown.pack(pady=5)
cable_dropdown.current(0)  # Set default to first option

# Dropdown untuk memilih jenis FDT
fdt_var = tk.StringVar()
label_fdt = tk.Label(root, text="Pilih jenis FDT:")
label_fdt.pack(pady=10)

fdt_options = ["FDT 48", "FDT 72", "FDT 96", "FDT 144", "FDT 288"]  # Tambahkan semua opsi FDT baru
fdt_dropdown = ttk.Combobox(root, textvariable=fdt_var, values=fdt_options)
fdt_dropdown.pack(pady=5)
fdt_dropdown.current(0)  # Set default to first option

# Tombol untuk menghitung
button_calculate = tk.Button(root, text="Hitung Kebutuhan Material", command=calculate_material)
button_calculate.pack(pady=20)

# Menampilkan informasi pada body form utama
label_name = tk.Label(root, text="  Developed By Syaiful Wachid")
label_name.pack(anchor='w', pady=0)  # Rata kiri
label_position = tk.Label(root, text="  Senior Project Designer                                                                       @ 27 Dec 2024")
label_position.pack(anchor='w', pady=0)  # Rata kiri
label_company = tk.Label(root, text="  Fiberhome Indonesia")
label_company.pack(anchor='w', pady=0)  # Rata kiri


# Menjalankan aplikasi
root.mainloop()
```

## Kontribusi
Jika Anda ingin berkontribusi pada proyek ini, silakan fork repositori ini dan kirim pull request dengan perubahan yang diinginkan.

## Lisensi
Proyek ini dilisensikan di bawah [MIT License](LICENSE).

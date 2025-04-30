import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import filedialog
from tkinter import scrolledtext

# Fungsi untuk menghitung kebutuhan material
def calculate_material():
    try:
        # Ambil jumlah rumah dari input
        num_houses = int(entry_houses.get())
        
        # Ambil jarak dari input
        distance = float(entry_distance.get())
        
        # Ambil jenis kabel, FDT, dan splitter dari input
        selected_cable = cable_var.get()
        selected_fdt = fdt_var.get()
        selected_fdt_splitter = fdt_splitter_var.get()
        selected_fat_splitter = fat_splitter_var.get()
        
        # Hitung jumlah FAT yang dibutuhkan
        fat_needed = (num_houses + 15) // 16  # 1 FAT bisa mengcover 16 rumah
        
        # Hitung jumlah kabel yang dibutuhkan
        if selected_cable == "12 Core":
            cable_needed = (fat_needed + 5) // 6  # 1 kabel 12 core untuk 5 FAT
            total_cores = cable_needed * 12
        elif selected_cable == "24 Core":
            cable_needed = (fat_needed + 9) // 10  # 1 kabel 24 core untuk 10 FAT
            total_cores = cable_needed * 24
        elif selected_cable == "36 Core":
            cable_needed = (fat_needed + 14) // 15  # 1 kabel 36 core untuk 15 FAT
            total_cores = cable_needed * 36
        elif selected_cable == "48 Core":
            cable_needed = (fat_needed + 19) // 20  # 1 kabel 48 core untuk setiap 20 FAT
            total_cores = cable_needed * 48
        elif selected_cable == "72 Core":
            cable_needed = (fat_needed + 29) // 30  # 1 kabel 72 core untuk 30 FAT
            total_cores = cable_needed * 72
        elif selected_cable == "96 Core":
            cable_needed = (fat_needed + 39) // 40  # 1 kabel 96 core untuk 40 FAT
            total_cores = cable_needed * 96
        elif selected_cable == "144 Core":
            cable_needed = (fat_needed + 59) // 60  # 1 kabel 144 core untuk 60 FAT
            total_cores = cable_needed * 144
        elif selected_cable == "192 Core":
            cable_needed = (fat_needed + 79) // 80  # 1 kabel 192 core untuk 80 FAT
            total_cores = cable_needed * 192
        elif selected_cable == "216 Core":
            cable_needed = (fat_needed + 89) // 90  # 1 kabel 216 core untuk 90 FAT
            total_cores = cable_needed * 216
        elif selected_cable == "288 Core":
            cable_needed = (fat_needed + 119) // 120  # 1 kabel 288 core untuk 120 FAT
            total_cores = cable_needed * 288
        
        # Hitung jumlah FDT yang dibutuhkan
        if selected_fdt == "FDT 48":
            fdt_needed = (fat_needed + 19) // 20  # 1 FDT 48 untuk maksimal 20 FAT
            fdt_cores = 48
        elif selected_fdt == "FDT 72":
            fdt_needed = (fat_needed + 29) // 30  # 1 FDT 72 untuk setiap 30 FAT
        elif selected_fdt == "FDT 96":
            fdt_needed = (fat_needed + 39) // 40  # 1 FDT 96 untuk setiap 40 FAT
        elif selected_fdt == "FDT 144":
            fdt_needed = (fat_needed + 59) // 60  # 1 FDT 144 untuk setiap 60 FAT
        elif selected_fdt == "FDT 288":
            fdt_needed = (fat_needed + 119) // 120  # 1 FDT 288 untuk setiap 120 FAT
        
        # Hitung jumlah splitter FDT yang dibutuhkan
        fdt_splitter_ratio = int(selected_fdt_splitter.split(":")[1])
        fdt_splitters_needed = (fat_needed + fdt_splitter_ratio - 1) // fdt_splitter_ratio
        
        # Hitung jumlah splitter FAT yang dibutuhkan
        fat_splitter_ratio = int(selected_fat_splitter.split(":")[1])
        fat_splitters_needed = (num_houses + fat_splitter_ratio - 1) // fat_splitter_ratio
        
        # Hitung sisa core
        used_cores = fat_needed * 2  # 2 core per FAT
        remaining_cores = total_cores - used_cores
        
        # Hitung total FAT yang masih bisa ditambahkan
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

        # Hitung Loss Budget
        # Loss per komponen (dalam dB)
        connector_loss = 0.3  # Loss per konektor (standar SC/APC)
        splice_loss = 0.1    # Loss per splice (fusion splice)
        splitter_loss = {    # Loss per splitter berdasarkan rasio
            "1:4": 7.2,      # Loss splitter 1:4
            "1:8": 10.5,     # Loss splitter 1:8
            "1:16": 13.8    # Loss splitter 1:16
        }
        cable_loss = 0.35    # Loss per km kabel (1310nm)
        
        # Hitung jarak antar FAT
        distance_between_fat = distance / fat_needed  # Jarak rata-rata antar FAT dalam meter
        
        # Hitung loss budget untuk setiap FAT
        fat_loss_details = []
        cumulative_loss = 0.0
        
        for fat_number in range(1, fat_needed + 1):
            # Hitung jarak dari FDT ke FAT saat ini
            current_distance = distance_between_fat * fat_number
            
            # Hitung loss untuk FAT saat ini
            current_connector_loss = 2 * connector_loss  # 2 konektor per FAT
            current_splice_loss = splice_loss
            current_cable_loss = cable_loss * (current_distance / 1000)  # Konversi ke km
            
            # Loss splitter FDT (hanya untuk FAT pertama)
            fdt_splitter_loss = splitter_loss[selected_fdt_splitter] if fat_number == 1 else 0
            
            # Loss splitter FAT
            fat_splitter_loss = splitter_loss[selected_fat_splitter]
            
            # Total loss untuk FAT saat ini
            current_total_loss = (current_connector_loss + 
                                current_splice_loss + 
                                current_cable_loss + 
                                fdt_splitter_loss + 
                                fat_splitter_loss)
            
            # Tambahkan margin keamanan
            current_total_loss_with_margin = current_total_loss + 3.0
            
            # Simpan detail loss untuk FAT ini
            fat_loss_details.append({
                'fat_number': fat_number,
                'distance': current_distance,
                'connector_loss': current_connector_loss,
                'splice_loss': current_splice_loss,
                'cable_loss': current_cable_loss,
                'fdt_splitter_loss': fdt_splitter_loss,
                'fat_splitter_loss': fat_splitter_loss,
                'total_loss': current_total_loss,
                'total_loss_with_margin': current_total_loss_with_margin
            })
            
            # Update cumulative loss
            cumulative_loss = current_total_loss_with_margin

        # Pisahkan summary dan detail FAT
        summary = f"Jumlah rumah yang diinput: {num_houses}\n"
        summary += f"Jarak total: {distance} meter\n"
        summary += f"Jarak rata-rata antar FAT: {distance_between_fat:.2f} meter\n\n"
        summary += f"Jumlah FAT yang dibutuhkan: {fat_needed}\n"
        summary += f"Jenis kabel yang dipilih: {selected_cable} (Jumlah: {cable_needed})\n"
        summary += f"Jenis FDT yang dipilih: {selected_fdt} (Jumlah: {fdt_needed})\n"
        summary += f"Jenis Splitter FDT: {selected_fdt_splitter} (Jumlah: {fdt_splitters_needed})\n"
        summary += f"Jenis Splitter FAT: {selected_fat_splitter} (Jumlah: {fat_splitters_needed})\n"
        summary += f"Sisa core setelah pemakaian: {remaining_cores}\n\n"
        summary += f"Total FAT yang masih bisa ditambahkan: {additional_fat}\n"
        summary += f"Jumlah rumah yang masih bisa dicover oleh sisa FAT: {houses_coverable}\n\n"
        summary += f"Jumlah tube yang digunakan: {total_tubes}\n"
        summary += f"Total sisa core idle: {total_idle_cores}\n"
        summary += f"Sisa core yang bisa digunakan untuk FAT tambahan: {usable_cores}\n\n"
        
        # Tampilkan FAT dengan loss tertinggi
        max_loss_fat = max(fat_loss_details, key=lambda x: x['total_loss_with_margin'])
        summary += f"FAT dengan Loss Tertinggi: FAT {max_loss_fat['fat_number']}\n"
        summary += f"Total Loss: {max_loss_fat['total_loss_with_margin']:.2f} dB\n"
        summary += f"Jarak dari FDT: {max_loss_fat['distance']:.2f} meter\n\n"
        
        if max_loss_fat['total_loss_with_margin'] > 28:
            summary += "Saran untuk mengurangi loss:\n"
            summary += "1. Pertimbangkan untuk menambahkan FDT baru untuk mengurangi jarak\n"
            summary += "2. Gunakan splitter dengan rasio yang lebih kecil\n"
            summary += "3. Periksa kualitas koneksi dan splice\n"
            summary += "4. Pertimbangkan untuk menggunakan kabel dengan loss yang lebih rendah\n\n"
        
        # Saran penggunaan jenis kabel ganda
        if selected_cable == "24 Core" and additional_fat > 0:
            summary += "Saran: Pertimbangkan menggunakan kabel 48 Core untuk efisiensi material.\n"
        elif selected_cable == "48 Core" and additional_fat > 0:
            summary += "Saran: Anda sudah menggunakan kabel 48 Core, tidak perlu ganda.\n"
        
        # Tambahkan informasi core monitor di akhir summary
        summary += "\nCore Monitor per Tube:\n"
        for tube in range(1, (len(fat_loss_details) + 4) // 5 + 1):
            monitor_core1 = tube * 12 - 1
            monitor_core2 = tube * 12
            summary += f"Tube {tube}: Core {monitor_core1} (Merah Muda) dan Core {monitor_core2} (Aqua)\n"
        summary += "\n"
        
        # Tampilkan hasil dalam jendela baru dengan slider
        show_results_window(fat_loss_details, summary)
    
    except ValueError:
        messagebox.showerror("Input Error", "Harap masukkan jumlah rumah dan jarak yang valid.")

# Fungsi untuk menampilkan warna kabel
def show_cable_colors():
    # Warna standar untuk kabel fiber optik
    colors = {
        1: "Biru",
        2: "Oranye",
        3: "Hijau",
        4: "Coklat",
        5: "Abu-abu",
        6: "Putih",
        7: "Merah",
        8: "Hitam",
        9: "Kuning",
        10: "Ungu",
        11: "Merah Muda",
        12: "Aqua"
    }
    
    # Buat string untuk menampilkan warna
    color_text = "--- Warna Kabel Fiber Optik ---\n\n"
    for core, color in colors.items():
        color_text += f"Core {core}: {color}\n"
    
    # Tampilkan dalam messagebox
    messagebox.showinfo("Warna Kabel", color_text)

# Fungsi untuk menyimpan hasil ke file
def save_to_file(content):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                               filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(content)
        messagebox.showinfo("Simpan File", "Hasil telah disimpan ke file.")

def get_core_colors(core_number):
    # Warna standar untuk kabel fiber optik
    colors = {
        1: "Biru",
        2: "Oranye",
        3: "Hijau",
        4: "Coklat",
        5: "Abu-abu",
        6: "Putih",
        7: "Merah",
        8: "Hitam",
        9: "Kuning",
        10: "Ungu",
        11: "Merah Muda",
        12: "Aqua"
    }
    # Hitung warna berdasarkan pola 12 core
    actual_core = ((core_number - 1) % 12) + 1
    return colors.get(actual_core, "Tidak Diketahui")

def calculate_core_numbers(fat_number):
    # Hitung tube number
    tube_number = (fat_number - 1) // 5 + 1
    
    # Hitung base core number untuk tube ini
    base_core = (tube_number - 1) * 12
    
    # Hitung posisi dalam tube (0-4)
    position_in_tube = (fat_number - 1) % 5
    
    # Hitung core active dan idle
    core_active = base_core + (position_in_tube * 2) + 1
    core_idle = core_active + 1
    
    return core_active, core_idle, tube_number

def show_fat_details(fat_number, fat_loss_details):
    detail = fat_loss_details[fat_number - 1]
    result = f"FAT {detail['fat_number']}:\n"
    result += f"Jarak dari FDT: {detail['distance']:.2f} meter\n"
    
    # Hitung core active dan idle
    core_active, core_idle, tube_number = calculate_core_numbers(fat_number)
    
    # Tampilkan informasi core
    result += f"Core Active: Core {core_active} ({get_core_colors(core_active)})\n"
    result += f"Core Idle: Core {core_idle} ({get_core_colors(core_idle)})\n"
    result += f"Posisi Tube: Tube {tube_number} ({get_core_colors(tube_number)})\n\n"
    
    result += f"Loss Konektor: {detail['connector_loss']:.2f} dB\n"
    result += f"Loss Splice: {detail['splice_loss']:.2f} dB\n"
    result += f"Loss Kabel: {detail['cable_loss']:.2f} dB\n"
    if detail['fdt_splitter_loss'] > 0:
        result += f"Loss Splitter FDT: {detail['fdt_splitter_loss']:.2f} dB\n"
    result += f"Loss Splitter FAT: {detail['fat_splitter_loss']:.2f} dB\n"
    result += f"Total Loss: {detail['total_loss']:.2f} dB\n"
    result += f"Total Loss dengan Margin: {detail['total_loss_with_margin']:.2f} dB\n"
    
    if detail['total_loss_with_margin'] > 28:
        result += "WARNING: Loss melebihi batas yang direkomendasikan (28 dB)!\n"
    
    return result

def show_results_window(fat_loss_details, summary):
    # Buat jendela baru untuk menampilkan hasil
    result_window = tk.Toplevel()
    result_window.title("Hasil Perhitungan FTTH")
    
    # Menyesuaikan ukuran jendela hasil (lebar x tinggi)
    result_window.geometry("600x600")  # Sesuaikan tinggi dengan form utama
    
    # Frame untuk summary
    summary_frame = tk.Frame(result_window)
    summary_frame.pack(fill=tk.X, padx=10, pady=5)
    
    summary_text = scrolledtext.ScrolledText(summary_frame, height=15, width=70)
    summary_text.pack(fill=tk.X)
    summary_text.insert(tk.END, summary)
    summary_text.config(state=tk.DISABLED)
    
    # Frame untuk slider dan detail FAT
    detail_frame = tk.Frame(result_window)
    detail_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
    
    # Label untuk slider
    slider_label = tk.Label(detail_frame, text="Pilih FAT untuk melihat detail:")
    slider_label.pack()
    
    # Slider untuk memilih FAT
    fat_slider = tk.Scale(detail_frame, from_=1, to=len(fat_loss_details), 
                         orient=tk.HORIZONTAL, command=lambda x: update_fat_detail(x, fat_loss_details, detail_text))
    fat_slider.pack(fill=tk.X)
    
    # Text area untuk detail FAT
    detail_text = scrolledtext.ScrolledText(detail_frame, height=10, width=70)
    detail_text.pack(fill=tk.BOTH, expand=True)
    
    # Frame untuk tombol
    button_frame = tk.Frame(result_window)
    button_frame.pack(pady=10)
    
    # Tombol untuk menyimpan hasil
    save_button = tk.Button(button_frame, text="Simpan Hasil", 
                          command=lambda: save_to_file(summary + "\n--- Detail Per FAT ---\n\n" + 
                                                     "\n".join([show_fat_details(i+1, fat_loss_details) for i in range(len(fat_loss_details))])))
    save_button.pack(side=tk.LEFT, padx=5)
    
    # Tombol untuk menutup
    close_button = tk.Button(button_frame, text="Tutup", command=result_window.destroy)
    close_button.pack(side=tk.LEFT, padx=5)
    
    # Tampilkan detail FAT pertama
    update_fat_detail(1, fat_loss_details, detail_text)

def update_fat_detail(fat_number, fat_loss_details, detail_text):
    fat_number = int(float(fat_number))
    detail_text.config(state=tk.NORMAL)
    detail_text.delete(1.0, tk.END)
    detail_text.insert(tk.END, show_fat_details(fat_number, fat_loss_details))
    detail_text.config(state=tk.DISABLED)

# Membuat antarmuka pengguna
root = tk.Tk()
root.title("Kalkulator Estimasi Kebutuhan Material FTTH")
root.geometry("430x600")  # Ubah nilai ini untuk mengubah ukuran jendela utama

# Label dan input untuk jumlah rumah
label_houses = tk.Label(root, text="Masukkan jumlah rumah:")
label_houses.pack(pady=10)

entry_houses = tk.Entry(root)
entry_houses.pack(pady=5)
entry_houses.insert(0, "500")  # Nilai default jumlah rumah

# Label dan input untuk jarak
label_distance = tk.Label(root, text="Masukkan jarak total (meter):")
label_distance.pack(pady=10)

entry_distance = tk.Entry(root)
entry_distance.pack(pady=5)
entry_distance.insert(0, "1000")  # Nilai default jarak

# Dropdown untuk memilih jenis kabel
cable_var = tk.StringVar()
label_cable = tk.Label(root, text="Pilih jenis kabel:")
label_cable.pack(pady=10)

cable_options = ["12 Core", "24 Core", "36 Core", "48 Core", "72 Core", "96 Core", "144 Core", "192 Core", "216 Core", "288 Core"]
cable_dropdown = ttk.Combobox(root, textvariable=cable_var, values=cable_options)
cable_dropdown.pack(pady=5)
cable_dropdown.current(1)  # Default ke 24 Core

# Dropdown untuk memilih jenis FDT
fdt_var = tk.StringVar()
label_fdt = tk.Label(root, text="Pilih jenis FDT:")
label_fdt.pack(pady=10)

fdt_options = ["FDT 48", "FDT 72", "FDT 96", "FDT 144", "FDT 288"]
fdt_dropdown = ttk.Combobox(root, textvariable=fdt_var, values=fdt_options)
fdt_dropdown.pack(pady=5)
fdt_dropdown.current(0)

# Dropdown untuk memilih jenis Splitter FDT
fdt_splitter_var = tk.StringVar()
label_fdt_splitter = tk.Label(root, text="Pilih jenis Splitter FDT:")
label_fdt_splitter.pack(pady=10)

fdt_splitter_options = ["1:4", "1:8", "1:16"]
fdt_splitter_dropdown = ttk.Combobox(root, textvariable=fdt_splitter_var, values=fdt_splitter_options)
fdt_splitter_dropdown.pack(pady=5)
fdt_splitter_dropdown.current(1)  # Default ke 1:8

# Dropdown untuk memilih jenis Splitter FAT
fat_splitter_var = tk.StringVar()
label_fat_splitter = tk.Label(root, text="Pilih jenis Splitter FAT:")
label_fat_splitter.pack(pady=10)

fat_splitter_options = ["1:4", "1:8", "1:16"]
fat_splitter_dropdown = ttk.Combobox(root, textvariable=fat_splitter_var, values=fat_splitter_options)
fat_splitter_dropdown.pack(pady=5)
fat_splitter_dropdown.current(2)  # Default ke 1:16

# Tombol untuk menghitung
button_calculate = tk.Button(root, text="Hitung Kebutuhan Material", command=calculate_material)
button_calculate.pack(pady=10)

# Tombol untuk menampilkan warna kabel
button_colors = tk.Button(root, text="Tampilkan Warna Kabel", command=show_cable_colors)
button_colors.pack(pady=5)

# Menampilkan informasi pada body form utama
label_name = tk.Label(root, text="  Developed By Syaiful Wachid")
label_name.pack(anchor='w', pady=0)
label_position = tk.Label(root, text="  Senior Project Designer                                                                       @ 27 Dec 2024")
label_position.pack(anchor='w', pady=0)
label_company = tk.Label(root, text="  Fiberhome Indonesia")
label_company.pack(anchor='w', pady=0)

# Menjalankan aplikasi
root.mainloop()
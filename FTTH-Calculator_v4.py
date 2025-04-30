import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import filedialog
from tkinter import scrolledtext

# Definisi opsi-opsi dropdown
cable_options = ["12 Core", "24 Core", "36 Core", "48 Core", "72 Core", "96 Core", "144 Core", "192 Core", "216 Core", "288 Core"]
fdt_options = ["FDT 48", "FDT 72", "FDT 96", "FDT 144", "FDT 288"]
fdt_splitter_options = ["1:4", "1:8", "1:16"]
fat_splitter_options = ["1:4", "1:8", "1:16"]

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

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

def show_results_window(fat_loss_details, summary):
    # Buat jendela baru untuk menampilkan hasil
    result_window = tk.Toplevel()
    result_window.title("Hasil Perhitungan FTTH")
    result_window.geometry("600x600")
    center_window(result_window)  # Posisikan di tengah layar
    
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
root.geometry("435x500")
center_window(root)  # Posisikan di tengah layar

# Mengatur style
style = ttk.Style()
style.configure('TFrame', background='#f0f0f0')
style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
style.configure('TButton', font=('Arial', 10))
style.configure('TCombobox', font=('Arial', 10))

# Frame utama
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill=tk.BOTH, expand=True)

# Header
header_frame = ttk.Frame(main_frame)
header_frame.pack(fill=tk.X, pady=(0, 20))

title_label = ttk.Label(header_frame, text="Kalkulator Estimasi FTTH", font=('Arial', 16, 'bold'))
title_label.pack()

# Input frame
input_frame = ttk.LabelFrame(main_frame, text="Input Data", padding="15")
input_frame.pack(fill=tk.X, pady=(0, 20))

# Grid untuk input
input_frame.columnconfigure(0, weight=1)
input_frame.columnconfigure(1, weight=2)

# Jumlah rumah
ttk.Label(input_frame, text="Jumlah Rumah:").grid(row=0, column=0, sticky=tk.W, pady=5)
entry_houses = ttk.Entry(input_frame, width=20)
entry_houses.grid(row=0, column=1, sticky=tk.W, pady=5)
entry_houses.insert(0, "500")

# Jarak
ttk.Label(input_frame, text="Jarak Total (meter):").grid(row=1, column=0, sticky=tk.W, pady=5)
entry_distance = ttk.Entry(input_frame, width=20)
entry_distance.grid(row=1, column=1, sticky=tk.W, pady=5)
entry_distance.insert(0, "1000")

# Jenis kabel
ttk.Label(input_frame, text="Jenis Kabel:").grid(row=2, column=0, sticky=tk.W, pady=5)
cable_var = tk.StringVar()
cable_dropdown = ttk.Combobox(input_frame, textvariable=cable_var, values=cable_options, width=17)
cable_dropdown.grid(row=2, column=1, sticky=tk.W, pady=5)
cable_dropdown.current(1)

# Jenis FDT
ttk.Label(input_frame, text="Jenis FDT:").grid(row=3, column=0, sticky=tk.W, pady=5)
fdt_var = tk.StringVar()
fdt_dropdown = ttk.Combobox(input_frame, textvariable=fdt_var, values=fdt_options, width=17)
fdt_dropdown.grid(row=3, column=1, sticky=tk.W, pady=5)
fdt_dropdown.current(0)

# Splitter FDT
ttk.Label(input_frame, text="Splitter FDT:").grid(row=4, column=0, sticky=tk.W, pady=5)
fdt_splitter_var = tk.StringVar()
fdt_splitter_dropdown = ttk.Combobox(input_frame, textvariable=fdt_splitter_var, values=fdt_splitter_options, width=17)
fdt_splitter_dropdown.grid(row=4, column=1, sticky=tk.W, pady=5)
fdt_splitter_dropdown.current(1)

# Splitter FAT
ttk.Label(input_frame, text="Splitter FAT:").grid(row=5, column=0, sticky=tk.W, pady=5)
fat_splitter_var = tk.StringVar()
fat_splitter_dropdown = ttk.Combobox(input_frame, textvariable=fat_splitter_var, values=fat_splitter_options, width=17)
fat_splitter_dropdown.grid(row=5, column=1, sticky=tk.W, pady=5)
fat_splitter_dropdown.current(2)

# Button frame
button_frame = ttk.Frame(main_frame)
button_frame.pack(fill=tk.X, pady=(0, 20))

# Tombol hitung
button_calculate = ttk.Button(button_frame, text="Hitung Kebutuhan Material", command=calculate_material, width=25)
button_calculate.pack(side=tk.LEFT, padx=5)

# Tombol warna kabel
button_colors = ttk.Button(button_frame, text="Tampilkan Warna Kabel", command=show_cable_colors, width=25)
button_colors.pack(side=tk.LEFT, padx=5)

# Footer frame
footer_frame = ttk.Frame(main_frame)
footer_frame.pack(fill=tk.X, pady=(20, 0))

# Informasi developer
ttk.Label(footer_frame, text="Developed By Syaiful Wachid", font=('Arial', 9)).pack(anchor='w')
ttk.Label(footer_frame, text="Senior Project Designer", font=('Arial', 9)).pack(anchor='w')
ttk.Label(footer_frame, text="Fiberhome Indonesia", font=('Arial', 9)).pack(anchor='w')
ttk.Label(footer_frame, text="@ 27 Dec 2024", font=('Arial', 9)).pack(anchor='e')

# Menjalankan aplikasi
root.mainloop()
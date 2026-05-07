"""
app.py
Entry point utama aplikasi StatPro.
"""

import customtkinter as ctk
import pandas as pd
from tkinter import filedialog, messagebox
from datetime import datetime

from ui.theme import apply_ctk_theme, apply_mpl_theme, C as COLORS
from ui.sidebar import Sidebar
from ui.dialogs import PilihKolomDialog
from utils.file_reader import baca_file
from core.statistics import hitung_statistik
from core.interpreter import generate_interpretasi

# Import Tabs
from ui.tabs.tab_distribusi import TabDistribusi
from ui.tabs.tab_grafik import TabGrafik
from ui.tabs.tab_interpretasi import TabInterpretasi
from ui.tabs.tab_boxplot import TabBoxplot
from ui.tabs.tab_laporan import TabLaporan

class StatistikApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # 1. Inisialisasi Tema & Jendela
        apply_ctk_theme()
        apply_mpl_theme()
        
        self.title("StatPro — Kalkulator Statistik Data Kelompok")
        self.geometry("1440x900")
        self.configure(fg_color=COLORS["bg_dark"])
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 2. Sidebar (Panel Kiri)
        self.sidebar = Sidebar(self, upload_callback=self._upload_file)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # 3. Container Utama (Panel Kanan)
        self.main_container = ctk.CTkFrame(self, fg_color=COLORS["bg_dark"])
        self.main_container.grid(row=0, column=1, sticky="nsew")
        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        # 4. Tabview System
        self.tabs = ctk.CTkTabview(
            self.main_container, 
            fg_color=COLORS["bg_dark"], 
            segmented_button_selected_color=COLORS["accent"],
            segmented_button_selected_hover_color=COLORS["accent_h"],
            segmented_button_unselected_color=COLORS["bg_card2"]
        )
        self.tabs.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))

        # 5. Inisialisasi Tab
        # Pastikan inisialisasi TabInterpretasi menggunakan TAB_NAME agar konsisten
        self.tabs.add(TabDistribusi.TAB_NAME)
        self.tabs.add(TabGrafik.TAB_NAME)
        self.tabs.add(TabBoxplot.TAB_NAME)
        self.tabs.add(TabInterpretasi.TAB_NAME)
        self.tabs.add(TabLaporan.TAB_NAME)

        # Hubungkan Instance Tab
        self.tab_dist = TabDistribusi(self.tabs)
        self.tab_grafik = TabGrafik(self.tabs)
        self.tab_boxplot = TabBoxplot(self.tabs)
        self.tab_interp = TabInterpretasi(self.tabs.tab(TabInterpretasi.TAB_NAME))
        self.tab_laporan = TabLaporan(self.tabs)

        # State Data
        self._last_stats = None
        self._last_col = None

    def _upload_file(self):
        """Handler untuk tombol upload di sidebar."""
        path = filedialog.askopenfilename(
            filetypes=[("Excel / CSV", "*.xlsx *.xls *.csv")]
        )
        if not path:
            return

        try:
            # Baca file dan buka dialog pilihan kolom
            df, sheet_name = baca_file(path)
            dialog = PilihKolomDialog(self, df, sheet_name)
            self.wait_window(dialog)

            if dialog.result_col:
                col = dialog.result_col
                # Pastikan data dikonversi ke numerik dan hapus NaN
                series = pd.to_numeric(df[col], errors="coerce").dropna()
                data = series.values

                if len(data) == 0:
                    raise ValueError(f"Kolom '{col}' tidak mengandung data numerik yang valid.")
                
                # Jalankan pemrosesan
                self._process(data, col, path.split("/")[-1])

        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat membaca file:\n{str(e)}")

    def _process(self, data, col_name, filename):
        """Fungsi pusat untuk menghitung dan memperbarui seluruh UI."""
        try:
            # 1. Kalkulasi Inti (statistics.py)
            classes, stats, data_sorted = hitung_statistik(data)
            
            # 2. Update Sidebar
            ts = datetime.now().strftime("%H:%M:%S")
            self.sidebar.update_file_info(f"📄 {filename}\n📊 {col_name}")
            self.sidebar.update_stats(stats)
            self.sidebar.update_timestamp(ts)

            # 3. Update Tab Distribusi & Grafik
            self.tab_dist.update(classes, stats, col_name)
            self.tab_grafik.update(classes, stats)

            # 4. Update Boxplot (menggunakan data mentah yang sudah disorting)
            self.tab_boxplot.update(data_sorted, col_name)

            # 5. Update Interpretasi (menggunakan interpreter.py)
            self.tab_interp.update_data(stats, col_name)

            # 6. Update Laporan Akhir
            # Kita panggil kembali generate_interpretasi untuk dikirim ke tab laporan
            interpretasi = generate_interpretasi(stats, col_name)
            self.tab_laporan.update(stats, interpretasi, col_name)

            # Simpan state terakhir
            self._last_stats = stats
            self._last_col = col_name

            # Beri notifikasi kecil (opsional)
            print(f"Analisis selesai: {col_name} ({len(data)} baris)")

        except Exception as e:
            messagebox.showerror("Processing Error", f"Gagal menganalisis data:\n{str(e)}")

if __name__ == "__main__":
    app = StatistikApp()
    # Atur window agar muncul di tengah layar (opsional)
    app.update()
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    x = (screen_width // 2) - (1440 // 2)
    y = (screen_height // 2) - (900 // 2)
    app.geometry(f"1440x900+{x}+{y}")
    
    app.mainloop()
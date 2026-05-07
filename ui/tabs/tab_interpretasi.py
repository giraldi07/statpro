"""
ui/tabs/tab_interpretasi.py
Tab Interpretasi — Menampilkan narasi interpretasi statistik otomatis.
"""

import customtkinter as ctk
from ui.theme import C as COLORS, F
from core.interpreter import generate_interpretasi  # Impor logika interpreter

class TabInterpretasi(ctk.CTkFrame):
    TAB_NAME = "📝  Interpretasi"

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        # Container utama dengan padding
        self.container = ctk.CTkScrollableFrame(
            self, 
            fg_color=COLORS["bg_dark"],
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["accent"]
        )
        self.container.pack(fill="both", expand=True, padx=10, pady=10)

        # Header
        self.header_label = ctk.CTkLabel(
            self.container,
            text="ANALISIS NARATIF OTOMATIS",
            font=F(16, "bold"),
            text_color=COLORS["accent3"]
        )
        self.header_label.pack(anchor="w", padx=20, pady=(10, 5))

        # Box Teks Interpretasi
        self.text_box = ctk.CTkTextbox(
            self.container,
            font=F(13),
            text_color=COLORS["text_primary"],
            fg_color=COLORS["bg_card"],
            border_color=COLORS["border"],
            border_width=1,
            wrap="word",
            height=650  # Ditingkatkan karena narasi lebih panjang
        )
        self.text_box.pack(fill="both", expand=True, padx=20, pady=10)
        self.text_box.insert("0.0", "Belum ada data untuk diinterpretasi. Silakan upload file dan pilih kolom terlebih dahulu.")
        self.text_box.configure(state="disabled")

    def update_data(self, stats: dict, col_name: str):
        """Memperbarui narasi menggunakan core/interpreter.py"""
        
        # Ambil data interpretasi dari engine interpreter
        interp = generate_interpretasi(stats, col_name)
        
        self.text_box.configure(state="normal")
        self.text_box.delete("0.0", "end")

        # Susun ulang tampilan narasi agar lebih profesional
        baris = "═" * 60
        tipis = "─" * 60
        
        rekomendasi_str = "\n".join([f"  {r}" for r in interp['recommendations']])

        narasi = (
            f"{baris}\n"
            f" LAPORAN ANALISIS STATISTIK: {col_name.upper()}\n"
            f"{baris}\n\n"
            
            f"1. BENTUK DISTRIBUSI\n"
            f"   Status: {interp['dist_type']}\n"
            f"   {interp['dist_desc']}\n\n"
            
            f"2. KERUNCINGAN DATA (KURTOSIS)\n"
            f"   {interp['kurt_desc']}\n\n"
            
            f"3. VARIABILITAS & KONSISTENSI\n"
            f"   Level: {interp['var_level']}\n"
            f"   {interp['var_desc']}\n\n"
            
            f"4. ANALISIS OUTLIER (ANOMALI)\n"
            f"   {interp['outlier_desc']}\n\n"
            
            f"5. TENDENSI SENTRAL\n"
            f"{interp['central_desc']}\n\n"
            
            f"{tipis}\n"
            f"6. REKOMENDASI TINDAK LANJUT\n"
            f"{rekomendasi_str}\n"
            f"{tipis}\n\n"
            f"Laporan ini dihasilkan secara otomatis berdasarkan perhitungan data berkelompok."
        )

        self.text_box.insert("0.0", narasi)
        self.text_box.configure(state="disabled")
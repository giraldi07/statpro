"""
Tab Interpretasi — Menampilkan narasi interpretasi statistik otomatis.
"""

import customtkinter as ctk
from ui.theme import C as COLORS, F, F_MONO

class TabInterpretasi(ctk.CTkFrame):
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
        # Judul Interpretasi
        self.header_label = ctk.CTkLabel(
            self.container,
            text="INTERPRETASI DATA",
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
            height=600
        )
        self.text_box.pack(fill="both", expand=True, padx=20, pady=10)
        self.text_box.insert("0.0", "Belum ada data untuk diinterpretasi. Silakan upload file terlebih dahulu.")
        self.text_box.configure(state="disabled")

    def update_data(self, stats, col_name):
        """Memperbarui narasi interpretasi berdasarkan hasil perhitungan."""
        self.text_box.configure(state="normal")
        self.text_box.delete("0.0", "end")
        n = stats['n']
        mean = stats['mean']
        median = stats['median']
        mode = stats['modus'] if 'modus' in stats else stats.get('mode', '-')
        std_dev = stats['std_dev']
        min_val = stats['min']
        max_val = stats['max']
        skema_distribusi = "Simetris"
        if mean > median:
            skema_distribusi = "Menceng Kanan (Positive Skew)"
        elif mean < median:
            skema_distribusi = "Menceng Kiri (Negative Skew)"
        narasi = f"""HASIL ANALISIS DATA: {col_name}\n{'─'*50}\n\n1. RANGKUMAN DATA\nData '{col_name}' memiliki total sampel sebanyak {n} observasi. Rentang nilai (range) data bergerak dari nilai minimum {min_val:.2f} hingga nilai maksimum {max_val:.2f}.\n\n2. PEMUSATAN DATA (CENTRAL TENDENCY)\nRata-rata (Mean) dari data ini adalah {mean:.2f}. Nilai tengah (Median) berada pada angka {median:.2f}, sementara nilai yang paling sering muncul (Mode) adalah {mode:.2f}.\n\n3. DISTRIBUSI DATA\nBerdasarkan perbandingan Mean dan Median, distribusi data cenderung bersifat {skema_distribusi}. \n\n4. VARIABILITAS\nStandar Deviasi sebesar {std_dev:.2f} menunjukkan tingkat penyebaran data terhadap rata-ratanya. Semakin besar nilai ini, semakin bervariasi atau heterogen data yang Anda miliki.\n\n{'─'*50}\nInterpretasi ini dihasilkan secara otomatis oleh StatPro.\n"""
        self.text_box.insert("0.0", narasi)
        self.text_box.configure(state="disabled")

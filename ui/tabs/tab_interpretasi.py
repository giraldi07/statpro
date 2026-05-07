"""
ui/tabs/tab_interpretasi.py
Tab Interpretasi — Narasi edukatif dengan perspektif Akuntansi & Statistik.
"""

import customtkinter as ctk
from ui.theme import C as COLORS, F
from core.interpreter import generate_interpretasi

class TabInterpretasi:
    TAB_NAME = "📝  Interpretasi"

    def __init__(self, tabview: ctk.CTkTabview):
        self._tab = tabview.tab(self.TAB_NAME)
        self._tab.configure(fg_color=COLORS["bg_dark"])
        
        self.container = ctk.CTkScrollableFrame(
            self._tab,
            fg_color=COLORS["bg_dark"],
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["accent"]
        )
        self.container.pack(fill="both", expand=True, padx=10, pady=10)

        # Header Laporan
        self.header_label = ctk.CTkLabel(
            self.container,
            text="EKSEKUTIF SUMMARY & ANALISIS AKUNTANSI",
            font=F(16, "bold"),
            text_color=COLORS["accent3"]
        )
        self.header_label.pack(anchor="w", padx=20, pady=(10, 5))

        # Text Box dengan Custom Formatting
        self.text_box = ctk.CTkTextbox(
            self.container,
            font=F(13),
            text_color=COLORS["text_primary"],
            fg_color=COLORS["bg_card"],
            border_color=COLORS["border"],
            border_width=1,
            wrap="word",
            height=800,
            padx=20,
            pady=20
        )
        self.text_box.pack(fill="both", expand=True, padx=20, pady=10)
        self.text_box.insert("0.0", "Menunggu input data untuk memulai analisis naratif...")
        self.text_box.configure(state="disabled")

    def update_data(self, stats: dict, col_name: str):
        interp = generate_interpretasi(stats, col_name)
        
        self.text_box.configure(state="normal")
        self.text_box.delete("0.0", "end")

        # Karakter dekoratif untuk struktur laporan
        sep = "═" * 70
        sub_sep = "─" * 70
        
        # Logika Edukatif Tambahan (Perspektif Akuntansi)
        accounting_perspective = self._get_accounting_insight(stats, interp)

        narasi = (
            f"{sep}\n"
            f" ANALISIS NARATIF EKSEKUTIF: {col_name.upper()}\n"
            f" Fokus Bidang: Statistik Deskriptif untuk Akuntansi & Keuangan\n"
            f"{sep}\n\n"

            f"A. PROFIL DISTRIBUSI (Karakteristik Data)\n"
            f"{sub_sep}\n"
            f"• Status Distribusi: {interp['dist_type']}\n"
            f"  Interpretasi: {interp['dist_desc']}\n"
            f"  [Edukasi]: Dalam akuntansi, skewness (kemiringan) membantu mendeteksi "
            f"apakah transaksi cenderung menumpuk di nilai kecil (misal: beban rutin) "
            f"atau nilai besar (misal: belanja modal).\n\n"

            f"B. VOLATILITAS & RISIKO (Variabilitas)\n"
            f"{sub_sep}\n"
            f"• Tingkat Variabilitas: {interp['var_level']}\n"
            f"  Detail: {interp['var_desc']}\n"
            f"  [Insight Akuntansi]: {accounting_perspective['risk_insight']}\n\n"

            f"C. ANALISIS KERUNCINGAN (Kurtosis)\n"
            f"{sub_sep}\n"
            f"• Karakteristik Kurva: {interp['kurt_desc']}\n"
            f"  [Edukasi]: Data yang terlalu 'runcing' (Leptokurtic) menunjukkan transaksi "
            f"yang sangat homogen, sedangkan data 'datar' (Platykurtic) menunjukkan "
            f"rentang nilai transaksi yang sangat beragam dan sulit diprediksi.\n\n"

            f"D. DETEKSI ANOMALI & FRAUD (Outliers)\n"
            f"{sub_sep}\n"
            f"• Hasil Scanning: {interp['outlier_desc']}\n"
            f"  [Audit Point]: {accounting_perspective['audit_point']}\n\n"

            f"E. TITIK ACUAN UTAMA (Tendensi Sentral)\n"
            f"{sub_sep}\n"
            f"• Ringkasan: {interp['central_desc']}\n"
            f"  [Analisis]: Rata-rata (Mean) digunakan sebagai estimasi anggaran, sedangkan "
            f"Median lebih aman digunakan jika data memiliki outlier ekstrem agar tidak bias.\n\n"

            f"F. STRATEGI & REKOMENDASI MANAJERIAL\n"
            f"{sub_sep}\n"
            + "\n".join([f"  ✅ {r}" for r in interp['recommendations']]) +
            f"\n\n{sep}\n"
            f"Laporan ini bersifat edukatif dan otomatis. Harap tinjau kembali "
            f"berdasarkan standar akuntansi yang berlaku (PSAK/IFRS)."
        )

        self.text_box.insert("0.0", narasi)
        self.text_box.configure(state="disabled")

    def _get_accounting_insight(self, stats, interp):
        """Menghasilkan wawasan spesifik akuntansi berdasarkan hasil statistik."""
        insights = {
            "risk_insight": "Variabilitas stabil, memudahkan proses budgeting.",
            "audit_point": "Tidak ditemukan transaksi mencurigakan secara statistik."
        }

        # Contoh logika insight berdasarkan Koefisien Variasi (CV)
        cv = stats.get('cv', 0)
        if cv > 30:
            insights["risk_insight"] = (
                "Variabilitas TINGGI. Dalam keuangan, ini menunjukkan risiko "
                "ketidakpastian anggaran yang tinggi. Diperlukan pencadangan dana darurat."
            )
        else:
            insights["risk_insight"] = (
                "Variabilitas RENDAH. Transaksi cenderung konsisten, "
                "memudahkan prediksi arus kas (Cash Flow) di periode mendatang."
            )

        # Contoh logika audit berdasarkan Outlier
        outlier_count = stats.get('outlier_count', 0)
        if outlier_count > 0:
            insights["audit_point"] = (
                f"Terdapat {outlier_count} transaksi ekstrem. Dalam audit, ini adalah "
                f"'Red Flag' yang harus diverifikasi manual untuk memastikan tidak ada "
                f"salah saji material atau kecurangan (fraud)."
            )
        else:
            insights["audit_point"] = (
                "Data bersih dari nilai ekstrem. Probabilitas kesalahan input atau "
                "transaksi tidak wajar tergolong rendah."
            )

        return insights
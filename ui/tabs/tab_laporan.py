"""
Tab Laporan Lengkap — Rekap semua hasil analisis & interpretasi.
"""

import customtkinter as ctk
from ui.theme import C, F
from ui.widgets import SectionHeader, Divider


from tkinter import filedialog, messagebox
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

class TabLaporan:
    TAB_NAME = "📄  Laporan"

    def __init__(self, tabview: ctk.CTkTabview):
        tab = tabview.tab(self.TAB_NAME)
        tab.configure(fg_color=C["bg_dark"])
        self._tab = tab
        self._frame = ctk.CTkScrollableFrame(tab, fg_color=C["bg_card"], corner_radius=10)
        self._frame.pack(fill="both", expand=True, padx=10, pady=10)
        SectionHeader(self._frame, text="LAPORAN ANALISIS STATISTIK").pack(anchor="w", pady=(0, 8))
        Divider(self._frame).pack(fill="x", pady=(0, 12))

        # Tombol ekspor PDF
        self._export_btn = ctk.CTkButton(
            self._frame, text="⬇️  Ekspor ke PDF", command=self._export_pdf, height=36, font=F(12, "bold"), fg_color=C["accent"]
        )
        self._export_btn.pack(anchor="e", pady=(0, 10), padx=10)

        # Container laporan
        self._content = ctk.CTkFrame(self._frame, fg_color="transparent")
        self._content.pack(fill="both", expand=True)

        self._last_stats = None
        self._last_interpretasi = None
        self._last_col = None

        self._clear()

    def _clear(self):
        for w in self._content.winfo_children():
            w.destroy()
        ctk.CTkLabel(
            self._content,
            text="Laporan lengkap akan ditampilkan di sini setelah analisis.",
            text_color=C["text_muted"],
            font=F(12),
            justify="left",
            wraplength=900
        ).pack(anchor="w", pady=8)

    def update(self, stats, interpretasi, col_name):
        self._last_stats = stats
        self._last_interpretasi = interpretasi
        self._last_col = col_name
        for w in self._content.winfo_children():
            w.destroy()

        SectionHeader(self._content, text=f"LAPORAN DATA: {col_name}").pack(anchor="w", pady=(0, 8))
        Divider(self._content).pack(fill="x", pady=(0, 12))

        # Ringkasan Statistik
        ctk.CTkLabel(
            self._content, text="RINGKASAN STATISTIK", font=F(13, "bold"), text_color=C["accent"]
        ).pack(anchor="w", pady=(0, 4))
        tbl = ctk.CTkFrame(self._content, fg_color=C["bg_card2"])
        tbl.pack(anchor="w", fill="x", padx=0, pady=(0, 10))
        for k, v in stats.items():
            row = ctk.CTkFrame(tbl, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=1)
            ctk.CTkLabel(row, text=f"{k}", font=F(11, "bold"), width=120, anchor="w", text_color=C["text_secondary"]).pack(side="left")
            ctk.CTkLabel(row, text=f":  {v}", font=F(11), anchor="w", text_color=C["text_primary"]).pack(side="left")

        Divider(self._content).pack(fill="x", pady=(8, 8))

        # Interpretasi
        ctk.CTkLabel(
            self._content, text="INTERPRETASI", font=F(13, "bold"), text_color=C["accent3"]
        ).pack(anchor="w", pady=(0, 4))
        for key in ["dist_desc", "var_desc", "outlier_desc", "kurt_desc", "central_desc"]:
            ctk.CTkLabel(
                self._content, text=interpretasi[key], font=F(11), text_color=C["text_primary"], wraplength=900, justify="left"
            ).pack(anchor="w", pady=(0, 6))

        Divider(self._content).pack(fill="x", pady=(8, 8))

        # Rekomendasi
        ctk.CTkLabel(
            self._content, text="REKOMENDASI", font=F(13, "bold"), text_color=C["accent2"]
        ).pack(anchor="w", pady=(0, 4))
        for r in interpretasi["recommendations"]:
            ctk.CTkLabel(
                self._content, text=f"• {r}", font=F(11), text_color=C["text_secondary"], wraplength=900, justify="left"
            ).pack(anchor="w", padx=12, pady=(0, 2))

    def _export_pdf(self):
        if not self._last_stats or not self._last_interpretasi:
            messagebox.showwarning("Export PDF", "Tidak ada laporan yang bisa diekspor.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], title="Simpan Laporan PDF")
        if not file_path:
            return
        try:
            self._generate_pdf(file_path)
            messagebox.showinfo("Export PDF", f"Laporan berhasil diekspor ke:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Export PDF", f"Gagal ekspor PDF:\n{e}")

    def _generate_pdf(self, file_path):
        stats = self._last_stats
        interpretasi = self._last_interpretasi
        col_name = self._last_col
        c = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4
        y = height - 2*cm
        c.setFont("Helvetica-Bold", 16)
        c.drawString(2*cm, y, f"LAPORAN DATA: {col_name}")
        y -= 1*cm
        c.setFont("Helvetica-Bold", 12)
        c.drawString(2*cm, y, "RINGKASAN STATISTIK:")
        y -= 0.7*cm
        c.setFont("Helvetica", 10)
        for k, v in stats.items():
            c.drawString(2.2*cm, y, f"{k:15}: {v}")
            y -= 0.5*cm
            if y < 3*cm:
                c.showPage(); y = height - 2*cm
        y -= 0.3*cm
        c.setFont("Helvetica-Bold", 12)
        c.drawString(2*cm, y, "INTERPRETASI:")
        y -= 0.7*cm
        c.setFont("Helvetica", 10)
        for key in ["dist_desc", "var_desc", "outlier_desc", "kurt_desc", "central_desc"]:
            for line in interpretasi[key].split("\n"):
                c.drawString(2.2*cm, y, line)
                y -= 0.5*cm
                if y < 3*cm:
                    c.showPage(); y = height - 2*cm
            y -= 0.2*cm
        y -= 0.2*cm
        c.setFont("Helvetica-Bold", 12)
        c.drawString(2*cm, y, "REKOMENDASI:")
        y -= 0.7*cm
        c.setFont("Helvetica", 10)
        for r in interpretasi["recommendations"]:
            c.drawString(2.2*cm, y, f"• {r}")
            y -= 0.5*cm
            if y < 3*cm:
                c.showPage(); y = height - 2*cm
        c.save()

"""
ui/tabs/tab_laporan.py
Tab Laporan Lengkap — Rekap semua hasil analisis & interpretasi.
"""

import customtkinter as ctk
from ui.theme import C, F
from ui.widgets import SectionHeader, Divider
from tkinter import filedialog, messagebox

# Library PDF
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

class TabLaporan:
    TAB_NAME = "📄  Laporan"

    def __init__(self, tabview: ctk.CTkTabview):
        tab = tabview.tab(self.TAB_NAME)
        tab.configure(fg_color=C["bg_dark"])
        self._tab = tab
        
        # Frame Utama
        self._frame = ctk.CTkScrollableFrame(tab, fg_color=C["bg_card"], corner_radius=10)
        self._frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        SectionHeader(self._frame, text="REKAPITULASI LAPORAN AKHIR").pack(anchor="w", pady=(0, 8))
        Divider(self._frame).pack(fill="x", pady=(0, 12))

        # Tombol ekspor PDF
        self._export_btn = ctk.CTkButton(
            self._frame, 
            text="⬇️  Unduh Laporan Formal (PDF)", 
            command=self._export_pdf, 
            height=40, 
            font=F(12, "bold"), 
            fg_color=C["accent"],
            hover_color=C["accent_h"]
        )
        self._export_btn.pack(anchor="e", pady=(0, 15), padx=10)

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
            text="Silakan lakukan analisis pada tab data terlebih dahulu untuk menyusun laporan.",
            text_color=C["text_muted"],
            font=F(12),
            pady=40
        ).pack(expand=True)

    def update(self, stats, interpretasi, col_name):
        self._last_stats = stats
        self._last_interpretasi = interpretasi
        self._last_col = col_name
        
        for w in self._content.winfo_children():
            w.destroy()

        # 1. Header Laporan
        header_frm = ctk.CTkFrame(self._content, fg_color=C["bg_card2"], corner_radius=8)
        header_frm.pack(fill="x", pady=(0, 15), padx=2)
        
        ctk.CTkLabel(header_frm, text=f"LAPORAN ANALISIS: {col_name.upper()}", 
                     font=F(14, "bold"), text_color=C["text_primary"]).pack(pady=(10, 2))
        ctk.CTkLabel(header_frm, text=f"Metode: Distribusi Frekuensi Data Berkelompok (Sturges Rule)", 
                     font=F(10), text_color=C["text_secondary"]).pack(pady=(0, 10))

        # 2. Tabel Ringkasan Statistik (Grid System agar Rapi)
        ctk.CTkLabel(self._content, text="I. RINGKASAN PARAMETER", font=F(12, "bold"), 
                     text_color=C["accent"]).pack(anchor="w", pady=(10, 5))
        
        tbl = ctk.CTkFrame(self._content, fg_color="transparent")
        tbl.pack(fill="x", pady=(0, 15))
        
        # Mapping untuk label yang lebih manusiawi
        display_map = [
            ("n", "Ukuran Sampel (n)"),
            ("k", "Jumlah Kelas (k)"),
            ("c", "Lebar Kelas (c)"),
            ("mean_grouped", "Rata-rata (Mean)"),
            ("median_grouped", "Nilai Tengah (Median)"),
            ("modus_grouped", "Nilai Dominan (Modus)"),
            ("std_dev_grouped", "Simpangan Baku (Std Dev)"),
            ("cv", "Koefisien Variansi (%)"),
        ]

        for i, (key, label) in enumerate(display_map):
            row_idx = i // 2
            col_idx = i % 2
            
            val = stats.get(key, 0)
            val_str = f"{val:.4f}" if isinstance(val, float) else str(val)
            if key == "cv": val_str += "%"

            item = ctk.CTkFrame(tbl, fg_color=C["bg_card2"], corner_radius=6)
            item.grid(row=row_idx, column=col_idx, sticky="nsew", padx=4, pady=4)
            
            ctk.CTkLabel(item, text=label, font=F(9), text_color=C["text_muted"]).pack(side="left", padx=10, pady=8)
            ctk.CTkLabel(item, text=val_str, font=F(10, "bold"), text_color=C["accent3"]).pack(side="right", padx=10)
        
        tbl.grid_columnconfigure((0, 1), weight=1)

        # 3. Narasi Interpretasi
        ctk.CTkLabel(self._content, text="II. ANALISIS NARATIF", font=F(12, "bold"), 
                     text_color=C["accent3"]).pack(anchor="w", pady=(10, 5))
        
        interp_box = ctk.CTkFrame(self._content, fg_color=C["bg_card2"], corner_radius=8, border_width=1, border_color=C["border"])
        interp_box.pack(fill="x", pady=(0, 15))

        interp_keys = [
            ("Karakteristik Distribusi", "dist_desc"),
            ("Variabilitas Data", "var_desc"),
            ("Analisis Anomali (Outlier)", "outlier_desc"),
            ("Bentuk Kurva (Kurtosis)", "kurt_desc"),
            ("Tendensi Sentral", "central_desc")
        ]

        for label, key in interp_keys:
            txt_frm = ctk.CTkFrame(interp_box, fg_color="transparent")
            txt_frm.pack(fill="x", padx=15, pady=8)
            
            ctk.CTkLabel(txt_frm, text=f"• {label}", font=F(10, "bold"), text_color=C["text_secondary"]).pack(anchor="w")
            ctk.CTkLabel(txt_frm, text=interpretasi[key], font=F(11), text_color=C["text_primary"], 
                         wraplength=850, justify="left").pack(anchor="w", padx=(12, 0))

        # 4. Rekomendasi
        ctk.CTkLabel(self._content, text="III. REKOMENDASI TINDAK LANJUT", font=F(12, "bold"), 
                     text_color=C["accent2"]).pack(anchor="w", pady=(10, 5))
        
        rekom_frm = ctk.CTkFrame(self._content, fg_color=C["bg_card2"], corner_radius=8)
        rekom_frm.pack(fill="x", pady=(0, 10))

        for r in interpretasi["recommendations"]:
            ctk.CTkLabel(rekom_frm, text=f"  {r}", font=F(11), text_color=C["text_primary"], 
                         wraplength=850, justify="left", anchor="w").pack(fill="x", padx=10, pady=5)

    def _export_pdf(self):
        if not self._last_stats or not self._last_interpretasi:
            messagebox.showwarning("Export PDF", "Data analisis tidak ditemukan.")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Simpan Laporan Formal",
            initialfile=f"Laporan_Statistik_{self._last_col}.pdf"
        )
        
        if not file_path: return

        try:
            self._generate_pdf_v2(file_path)
            messagebox.showinfo("Sukses", f"Laporan PDF berhasil disimpan di:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membuat PDF:\n{str(e)}")

    def _generate_pdf_v2(self, file_path):
        """Generasi PDF menggunakan Platypus untuk layout yang jauh lebih rapi."""
        doc = SimpleDocTemplate(file_path, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
        styles = getSampleStyleSheet()
        
        # Custom Styles
        title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=16, alignment=1, spaceAfter=20)
        sub_style = ParagraphStyle('SubStyle', parent=styles['Heading2'], fontSize=12, color=colors.HexColor("#2C3E50"), spaceBefore=15, spaceAfter=10)
        body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=10, leading=14, alignment=4) # alignment 4 = justify
        
        story = []

        # Header
        story.append(Paragraph(f"LAPORAN ANALISIS STATISTIK: {self._last_col.upper()}", title_style))
        story.append(Paragraph(f"Tanggal Analisis: {datetime.now().strftime('%d %B %Y, %H:%M')}", body_style))
        story.append(Spacer(1, 12))

        # I. Ringkasan Statistik dalam Tabel
        story.append(Paragraph("I. RINGKASAN PARAMETER", sub_style))
        
        data_tbl = [["Parameter", "Nilai"]]
        mapping = [
            ("Ukuran Sampel (n)", self._last_stats["n"]),
            ("Jumlah Kelas (k)", self._last_stats["k"]),
            ("Lebar Kelas (c)", f"{self._last_stats['c']:.4f}"),
            ("Rata-rata (Mean)", f"{self._last_stats['mean_grouped']:.4f}"),
            ("Median", f"{self._last_stats['median_grouped']:.4f}"),
            ("Modus", f"{self._last_stats['modus_grouped']:.4f}"),
            ("Simpangan Baku", f"{self._last_stats['std_dev_grouped']:.4f}"),
            ("Koefisien Variansi", f"{self._last_stats['cv']:.2f}%"),
        ]
        data_tbl.extend(mapping)

        t = Table(data_tbl, colWidths=[8*cm, 4*cm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.HexColor("#34495E")),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(t)

        # II. Interpretasi
        story.append(Paragraph("II. ANALISIS NARATIF", sub_style))
        interp_keys = [
            ("Karakteristik Distribusi", "dist_desc"),
            ("Variabilitas Data", "var_desc"),
            ("Analisis Anomali", "outlier_desc"),
            ("Bentuk Kurva (Kurtosis)", "kurt_desc"),
            ("Tendensi Sentral", "central_desc")
        ]
        
        for label, key in interp_keys:
            story.append(Paragraph(f"<b>{label}:</b>", body_style))
            story.append(Paragraph(self._last_interpretasi[key], body_style))
            story.append(Spacer(1, 8))

        # III. Rekomendasi
        story.append(Paragraph("III. REKOMENDASI TINDAK LANJUT", sub_style))
        for r in self._last_interpretasi["recommendations"]:
            story.append(Paragraph(f"• {r}", body_style))
            story.append(Spacer(1, 4))

        # Footer
        story.append(Spacer(1, 30))
        story.append(Paragraph("<i>Laporan ini dihasilkan secara otomatis oleh StatPro System by Giraldi Prama Yudistira.S.Ikom.</i>", body_style))

        doc.build(story)

from datetime import datetime # Tambahkan di bagian import atas jika belum ada
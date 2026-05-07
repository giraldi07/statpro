"""
ui/dialogs.py
Dialog modal untuk memilih kolom yang akan dianalisis.
"""

import numpy as np
import pandas as pd
import customtkinter as ctk
from tkinter import ttk

from ui.theme import C, F, F_MONO


class PilihKolomDialog(ctk.CTkToplevel):
    """
    Dialog pilih kolom dengan:
    - Chips info (jumlah kolom, baris)
    - Dropdown kolom numerik
    - Preview tabel 10 baris pertama
    - Info bar statistik ringkas (Data Mentah)
    """

    def __init__(self, parent, df: pd.DataFrame, sheet_name: str | None = None):
        super().__init__(parent)
        self.title("Konfigurasi Analisis")
        self.geometry("740x620")  # Sedikit lebih lebar untuk kenyamanan preview
        self.resizable(False, False)
        
        # Membuat dialog benar-benar modal
        self.grab_set()
        self.focus_set()
        
        self.configure(fg_color=C["bg_dark"])

        self.result_col: str | None = None
        self.df = df
        self._closing = False

        self.protocol("WM_DELETE_WINDOW", self._cancel)

        # Hanya ambil kolom yang benar-benar numerik
        num_cols = list(df.select_dtypes(include=[np.number]).columns)

        self._build_header(sheet_name)
        self._build_body(num_cols, df)
        self._build_footer()

        # Inisialisasi preview
        if num_cols:
            self.after(100, lambda: self._preview(self.col_var.get()))
        else:
            self.info_lbl.configure(text="⚠ Tidak ditemukan kolom numerik dalam file ini.", text_color=C["warning"])

    # ── Build UI ──────────────────────────────────────────────
    def _build_header(self, sheet_name: str | None) -> None:
        header = ctk.CTkFrame(self, fg_color=C["bg_card"], corner_radius=0, height=72)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="⚙  Konfigurasi Analisis",
            font=F(18, "bold"),
            text_color=C["text_primary"],
        ).pack(side="left", padx=24)

        if sheet_name:
            ctk.CTkLabel(
                header,
                text=f"Sheet: {sheet_name}",
                font=F(11),
                text_color=C["accent"],
            ).pack(side="right", padx=24)

    def _build_body(self, num_cols: list[str], df: pd.DataFrame) -> None:
        body = ctk.CTkFrame(self, fg_color=C["bg_dark"])
        body.pack(fill="both", expand=True, padx=20, pady=14)

        # Chips info - Ringkasan Dataset
        chip_row = ctk.CTkFrame(body, fg_color="transparent")
        chip_row.pack(fill="x", pady=(0, 12))
        
        metadata = [
            ("Variabel Numerik", len(num_cols)),
            ("Total Baris", len(df)),
            ("Total Kolom", len(df.columns)),
        ]

        for label, val in metadata:
            chip = ctk.CTkFrame(chip_row, fg_color=C["bg_card2"], corner_radius=20)
            chip.pack(side="left", padx=4)
            ctk.CTkLabel(chip, text=f"{label}: ", text_color=C["text_secondary"],
                         font=F(10)).pack(side="left", padx=(12, 0), pady=6)
            ctk.CTkLabel(chip, text=str(val), text_color=C["accent"],
                         font=F(10, "bold")).pack(side="left", padx=(0, 12), pady=6)

        # Dropdown Pemilihan Kolom
        ctk.CTkLabel(body, text="Pilih Kolom Utama",
                     font=F(12, "bold"), text_color=C["text_primary"]).pack(anchor="w", pady=(0, 6))

        self.col_var = ctk.StringVar(value=num_cols[0] if num_cols else "")
        self.menu = ctk.CTkOptionMenu(
            body,
            variable=self.col_var,
            values=num_cols if num_cols else ["Tidak ada kolom numerik"],
            command=self._preview,
            fg_color=C["bg_card2"],
            button_color=C["accent"],
            button_hover_color=C["accent_h"],
            dropdown_fg_color=C["bg_card"],
            font=F(12),
            height=38,
        )
        self.menu.pack(fill="x", pady=(0, 10))

        # Info bar - Statistik Deskriptif Cepat
        self.info_lbl = ctk.CTkLabel(
            body, text="Memuat informasi kolom...",
            font=F(10),
            text_color=C["accent3"],
            fg_color=C["bg_card2"],
            corner_radius=8,
            padx=12, pady=8,
        )
        self.info_lbl.pack(fill="x", pady=(0, 10))

        # Preview tabel menggunakan Treeview
        ctk.CTkLabel(body, text="Cuplikan Data Mentah",
                     font=F(10), text_color=C["text_muted"]).pack(anchor="w", pady=(0, 4))

        tree_outer = ctk.CTkFrame(body, fg_color=C["bg_card"], corner_radius=8)
        tree_outer.pack(fill="both", expand=True)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Dark.Treeview",
            background=C["bg_card"],
            foreground=C["text_primary"],
            fieldbackground=C["bg_card"],
            rowheight=28,
            font=("Segoe UI", 9),
            borderwidth=0,
        )
        style.configure(
            "Dark.Treeview.Heading",
            background=C["table_header"],
            foreground=C["text_secondary"],
            font=("Segoe UI", 9, "bold"),
            relief="flat",
        )
        style.map("Dark.Treeview", background=[("selected", C["accent"])])

        self.tree = ttk.Treeview(tree_outer, style="Dark.Treeview", show="headings")
        vsb = ttk.Scrollbar(tree_outer, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True, padx=2, pady=2)

    def _build_footer(self) -> None:
        footer = ctk.CTkFrame(self, fg_color=C["bg_card"], corner_radius=0, height=64)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        ctk.CTkButton(
            footer, text="Batal", width=100, height=36,
            fg_color="transparent", border_width=1, border_color=C["border"],
            text_color=C["text_secondary"], corner_radius=8,
            command=self._cancel,
        ).pack(side="right", padx=(8, 24), pady=14)

        ctk.CTkButton(
            footer, text="Proses Data ➔", width=150, height=36,
            fg_color=C["accent"], hover_color=C["accent_h"],
            corner_radius=8, font=F(12, "bold"),
            command=self._confirm,
        ).pack(side="right", padx=8, pady=14)

    # ── Logika ──────────────────────────────────────────────
    def _preview(self, col_name: str) -> None:
        if self._closing or not self.winfo_exists() or col_name == "Tidak ada kolom numerik":
            return

        # Ambil kolom terpilih + 4 kolom pertama lainnya sebagai konteks
        other_cols = [c for c in self.df.columns if c != col_name][:4]
        cols_show = [col_name] + other_cols
        
        # Reset Treeview
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = cols_show
        
        for c in cols_show:
            self.tree.heading(c, text=str(c))
            self.tree.column(c, width=120, anchor="center")

        # Isi 10 baris pertama
        for _, row_data in self.df[cols_show].head(10).iterrows():
            vals = []
            for v in row_data:
                if pd.isna(v):
                    vals.append("—")
                elif isinstance(v, (float, np.float64)):
                    vals.append(f"{v:.4f}")
                else:
                    vals.append(str(v))
            self.tree.insert("", "end", values=vals)

        # Update Info Bar (Statistik Mentah)
        series = self.df[col_name].dropna()
        if not series.empty:
            self.info_lbl.configure(
                text=(
                    f"✓ {len(series)} Baris Valid  ·  "
                    f"Min: {series.min():.2f}  ·  "
                    f"Max: {series.max():.2f}  ·  "
                    f"Rata-rata: {series.mean():.4f}"
                ),
                text_color=C["accent3"]
            )
        else:
            self.info_lbl.configure(text="⚠ Kolom terpilih tidak mengandung data valid.", text_color=C["warning"])

    def _confirm(self) -> None:
        if self._closing or self.col_var.get() == "Tidak ada kolom numerik":
            return
        self.result_col = self.col_var.get()
        self._close_dialog()

    def _cancel(self) -> None:
        self.result_col = None
        self._close_dialog()

    def _close_dialog(self) -> None:
        self._closing = True
        self.grab_release()
        self.destroy()
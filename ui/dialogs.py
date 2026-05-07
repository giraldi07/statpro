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
    - Info bar statistik ringkas kolom yang dipilih
    """

    def __init__(self, parent, df: pd.DataFrame, sheet_name: str | None = None):
        super().__init__(parent)
        self.title("Konfigurasi Analisis")
        self.geometry("700x600")
        self.resizable(False, False)
        self.grab_set()
        self.configure(fg_color=C["bg_dark"])

        self.result_col: str | None = None
        self.df = df
        self._closing = False

        self.protocol("WM_DELETE_WINDOW", self._cancel)

        num_cols = list(df.select_dtypes(include=[np.number]).columns)

        self._build_header(sheet_name)
        self._build_body(num_cols, df)
        self._build_footer()

        self.after(50, lambda: self._preview(self.col_var.get()))

    # ── Build ─────────────────────────────────────────────────
    def _build_header(self, sheet_name: str | None) -> None:
        header = ctk.CTkFrame(self, fg_color=C["bg_card"], corner_radius=0, height=72)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="⚙  Konfigurasi Analisis",
            font=F(18, "bold"),
            text_color=C["text_primary"],
        ).pack(side="left", padx=24, pady=0)

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

        # Chips info
        chip_row = ctk.CTkFrame(body, fg_color="transparent")
        chip_row.pack(fill="x", pady=(0, 12))
        for label, val in [
            ("Kolom Numerik", len(num_cols)),
            ("Total Baris", len(df)),
            ("Total Kolom", len(df.columns)),
        ]:
            chip = ctk.CTkFrame(chip_row, fg_color=C["bg_card2"], corner_radius=20)
            chip.pack(side="left", padx=4)
            ctk.CTkLabel(chip, text=f"{label}: ", text_color=C["text_secondary"],
                         font=F(10)).pack(side="left", padx=(12, 0), pady=6)
            ctk.CTkLabel(chip, text=str(val), text_color=C["accent"],
                         font=F(10, "bold")).pack(side="left", padx=(0, 12), pady=6)

        # Dropdown
        ctk.CTkLabel(body, text="Pilih Kolom untuk Dianalisis",
                     font=F(12, "bold"), text_color=C["text_primary"]).pack(anchor="w", pady=(0, 6))

        self.col_var = ctk.StringVar(value=num_cols[0] if num_cols else "")
        ctk.CTkOptionMenu(
            body,
            variable=self.col_var,
            values=num_cols,
            command=self._preview,
            fg_color=C["bg_card2"],
            button_color=C["accent"],
            button_hover_color=C["accent_h"],
            dropdown_fg_color=C["bg_card"],
            font=F(12),
            height=38,
        ).pack(fill="x", pady=(0, 10))

        # Info bar
        self.info_lbl = ctk.CTkLabel(
            body, text="",
            font=F(10),
            text_color=C["accent3"],
            fg_color=C["bg_card2"],
            corner_radius=8,
            padx=12, pady=6,
        )
        self.info_lbl.pack(fill="x", pady=(0, 10))

        # Preview tabel
        ctk.CTkLabel(body, text="Preview Data (10 baris pertama)",
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
            rowheight=26,
            font=("Helvetica", 10),
            borderwidth=0,
        )
        style.configure(
            "Dark.Treeview.Heading",
            background=C["table_header"],
            foreground=C["text_secondary"],
            font=("Helvetica", 10, "bold"),
            relief="flat",
        )
        style.map("Dark.Treeview", background=[("selected", C["accent"])])

        self.tree = ttk.Treeview(tree_outer, style="Dark.Treeview", show="headings", height=8)
        vsb = ttk.Scrollbar(tree_outer, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True, padx=2, pady=2)

    def _build_footer(self) -> None:
        footer = ctk.CTkFrame(self, fg_color=C["bg_card"], corner_radius=0, height=64)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        ctk.CTkButton(
            footer, text="Batal", width=110, height=38,
            fg_color=C["bg_card2"], hover_color=C["bg_dark"],
            text_color=C["text_secondary"], corner_radius=8,
            command=self._cancel,
        ).pack(side="right", padx=(8, 20), pady=13)

        ctk.CTkButton(
            footer, text="Mulai Analisis  →", width=160, height=38,
            fg_color=C["accent"], hover_color=C["accent_h"],
            corner_radius=8, font=F(12, "bold"),
            command=self._confirm,
        ).pack(side="right", padx=8, pady=13)

    # ── Callback ──────────────────────────────────────────────
    def _preview(self, col_name: str) -> None:
        if self._closing or not self.winfo_exists():
            return

        cols_show = [col_name] + [c for c in self.df.columns if c != col_name][:4]
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = cols_show
        for c in cols_show:
            self.tree.heading(c, text=str(c))
            self.tree.column(c, width=110, minwidth=60)

        for _, row_data in self.df[cols_show].head(10).iterrows():
            vals = [
                "—" if pd.isna(v) else (f"{v:.4f}" if isinstance(v, float) else str(v))
                for v in row_data
            ]
            self.tree.insert("", "end", values=vals)

        series = self.df[col_name].dropna()
        null_count = int(self.df[col_name].isna().sum())
        if self.winfo_exists():
            self.info_lbl.configure(
                text=(
                    f"  ✓  {len(series)} nilai valid  ·  {null_count} kosong/NaN  "
                    f"·  Min = {series.min():.4f}  "
                    f"·  Max = {series.max():.4f}  "
                    f"·  Mean = {series.mean():.4f}"
                )
            )

    def _safe_destroy(self) -> None:
        try:
            if self.winfo_exists():
                self.grab_release()
                self.destroy()
        except Exception:
            pass

    def _confirm(self) -> None:
        if self._closing:
            return
        self._closing = True
        self.result_col = self.col_var.get()
        self.withdraw()
        self.after(100, self._safe_destroy)

    def _cancel(self) -> None:
        if self._closing:
            return
        self._closing = True
        self.result_col = None
        self.withdraw()
        self.after(100, self._safe_destroy)
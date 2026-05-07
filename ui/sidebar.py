"""
ui/sidebar.py
Sidebar kiri: brand, tombol upload, dan kartu statistik ringkasan.
"""

import customtkinter as ctk
from ui.theme import C, F
from ui.widgets import StatMetric, Divider


class Sidebar(ctk.CTkFrame):
    """
    Panel kiri yang menampilkan:
    - Brand header
    - Tombol upload file
    - Label info file
    - Scrollable metric cards
    - Timestamp analisis terakhir
    """

    def __init__(self, parent, upload_callback, **kwargs):
        super().__init__(parent, width=285, corner_radius=0,
                         fg_color=C["bg_sidebar"], **kwargs)
        self.grid_propagate(False)
        self._upload_callback = upload_callback
        self._metrics: dict[str, StatMetric] = {}

        self._build_brand()
        self._build_upload_section()
        Divider(self).pack(fill="x", padx=16, pady=12)
        self._build_metrics()

    # ── Brand ────────────────────────────────────────────────
    def _build_brand(self) -> None:
        brand = ctk.CTkFrame(self, fg_color=C["bg_card"], height=72, corner_radius=0)
        brand.pack(fill="x")
        brand.pack_propagate(False)

        row = ctk.CTkFrame(brand, fg_color="transparent")
        row.place(relx=0, rely=0.25, x=20)

        ctk.CTkLabel(row, text="STAT", font=F(22, "bold"),
                     text_color=C["accent"]).pack(side="left")
        ctk.CTkLabel(row, text="PRO", font=F(22, "bold"),
                     text_color=C["text_primary"]).pack(side="left")

        ctk.CTkLabel(brand, text="Analisis Data Kelompok",
                     font=F(9), text_color=C["text_muted"]).place(x=20, y=50)

    # ── Upload ───────────────────────────────────────────────
    def _build_upload_section(self) -> None:
        frm = ctk.CTkFrame(self, fg_color="transparent")
        frm.pack(fill="x", padx=16, pady=(16, 0))

        ctk.CTkButton(
            frm,
            text="  📂  Unggah File",
            command=self._upload_callback,
            height=44,
            corner_radius=10,
            fg_color=C["accent"],
            hover_color=C["accent_h"],
            font=F(13, "bold"),
        ).pack(fill="x")

        self._file_lbl = ctk.CTkLabel(
            frm,
            text="Belum ada file dimuat",
            text_color=C["text_muted"],
            font=F(9),
            wraplength=245,
        )
        self._file_lbl.pack(pady=(8, 0))

    # ── Metrics ──────────────────────────────────────────────
    def _build_metrics(self) -> None:
        ctk.CTkLabel(
            self,
            text="RINGKASAN STATISTIK",
            font=F(9, "bold"),
            text_color=C["text_muted"],
        ).pack(anchor="w", padx=20, pady=(0, 6))

        sf = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=C["bg_card2"],
            scrollbar_button_hover_color=C["accent"],
        )
        sf.pack(fill="both", expand=True, padx=12, pady=(0, 8))

        metric_defs = [
            # (key,        label,                    color,              icon)
            ("n",         "Jumlah Data (n)",         C["accent"],        "⬡"),
            ("k",         "Jumlah Kelas (k)",        C["accent"],        "⬡"),
            ("c",         "Lebar Kelas (c)",         C["accent"],        "⬡"),
            ("mean",      "Mean  x̄",                C["accent3"],       "∑"),
            ("median",    "Median  Me",              C["accent3"],       "∑"),
            ("modus",     "Modus  Mo",               C["accent3"],       "∑"),
            ("std_dev",   "Std. Deviasi  s",         C["accent2"],       "σ"),
            ("variance",  "Variansi  s²",            C["accent2"],       "σ"),
            ("cv",        "Koef. Variasi  CV%",      C["accent2"],       "σ"),
            ("q1",        "Kuartil 1  Q₁",           C["accent4"],       "◈"),
            ("q3",        "Kuartil 3  Q₃",           C["accent4"],       "◈"),
            ("iqr",       "IQR  (Q₃ − Q₁)",         C["accent4"],       "◈"),
            ("skewness",  "Skewness",                C["text_secondary"],"~"),
            ("kurtosis",  "Kurtosis",                C["text_secondary"],"~"),
        ]
        for key, label, color, icon in metric_defs:
            m = StatMetric(sf, label=label, color=color, icon=icon)
            m.pack(fill="x", pady=3)
            self._metrics[key] = m

        # Timestamp
        self._ts_lbl = ctk.CTkLabel(
            self, text="", font=F(8), text_color=C["text_muted"]
        )
        self._ts_lbl.pack(pady=(0, 6))

    # ── Public API ───────────────────────────────────────────
    def update_file_info(self, text: str) -> None:
        self._file_lbl.configure(text=text)

    def update_stats(self, stats: dict) -> None:
        mapping = {
            "n":        str(stats["n"]),
            "k":        str(stats["k"]),
            "c":        str(stats["c"]),
            "mean":     f"{stats['mean']:.4f}",
            "median":   f"{stats['median']:.4f}",
            "modus":    f"{stats['modus']:.4f}",
            "std_dev":  f"{stats['std_dev']:.4f}",
            "variance": f"{stats['variance']:.4f}",
            "cv":       f"{stats['cv']:.2f}%",
            "q1":       f"{stats['q1']:.4f}",
            "q3":       f"{stats['q3']:.4f}",
            "iqr":      f"{stats['iqr']:.4f}",
            "skewness": f"{stats['skewness']:.4f}",
            "kurtosis": f"{stats['kurtosis']:.4f}",
        }
        for key, val in mapping.items():
            self._metrics[key].set_value(val)

    def update_timestamp(self, ts: str) -> None:
        self._ts_lbl.configure(text=f"Dianalisis: {ts}")
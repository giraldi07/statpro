"""
ui/tabs/tab_distribusi.py
Tab 1 — Tabel Distribusi Frekuensi Kelompok.
"""

import customtkinter as ctk
from ui.theme import C, F, F_MONO


class TabDistribusi:
    """
    Mengelola konten Tab 'Distribusi Frekuensi'.
    Dipasang ke CTkTabview dari luar.
    """

    TAB_NAME = "📊  Distribusi Frekuensi"

    def __init__(self, tabview: ctk.CTkTabview):
        tab = tabview.tab(self.TAB_NAME)
        tab.configure(fg_color=C["bg_dark"])
        self._tab = tab
        self._build()

    # ── Build ────────────────────────────────────────────────
    def _build(self) -> None:
        # Banner info
        self._banner_frame = ctk.CTkFrame(
            self._tab, fg_color=C["bg_card"], corner_radius=10, height=48
        )
        self._banner_frame.pack(fill="x", pady=(0, 8))
        self._banner_frame.pack_propagate(False)

        self._banner_lbl = ctk.CTkLabel(
            self._banner_frame,
            text="Unggah file untuk memulai analisis",
            text_color=C["text_muted"],
            font=F(11),
        )
        self._banner_lbl.pack(expand=True)

        # Tabel scroll
        self._outer = ctk.CTkScrollableFrame(
            self._tab,
            fg_color=C["bg_card"],
            corner_radius=10,
            scrollbar_button_color=C["bg_card2"],
            scrollbar_button_hover_color=C["accent"],
        )
        self._outer.pack(fill="both", expand=True)

        self._tbl = ctk.CTkFrame(self._outer, fg_color="transparent")
        self._tbl.pack(fill="x")

        self._draw_header()

        # Rumus note
        note = ctk.CTkFrame(self._tab, fg_color=C["bg_card2"], corner_radius=8)
        note.pack(fill="x", pady=(8, 0))
        ctk.CTkLabel(
            note,
            text=(
                "Rumus:  k = 1 + 3.322·log₁₀(n) [Sturges]  ·  c = ⌈Range / k⌉  ·  "
                "x̄ = Σ(fᵢ·xᵢ) / n  ·  "
                "Me = Lme + [(n/2 − F₋) / fme]·c  ·  "
                "Mo = Lmo + [d₁ / (d₁+d₂)]·c"
            ),
            font=F(9),
            text_color=C["text_muted"],
            pady=8,
        ).pack()

    def _draw_header(self) -> None:
        headers = [
            "No.",
            "Interval Kelas",
            "Titik Tengah (xᵢ)",
            "Frekuensi (fᵢ)",
            "F. Relatif (%)",
            "F. Kumulatif",
            "fᵢ · xᵢ",
            "fᵢ (xᵢ − x̄)²",
        ]
        for i, h in enumerate(headers):
            ctk.CTkLabel(
                self._tbl,
                text=h,
                font=F(10, "bold"),
                text_color=C["text_secondary"],
                fg_color=C["table_header"],
                pady=12,
                padx=8,
                corner_radius=0,
            ).grid(row=0, column=i, sticky="nsew", padx=1, pady=(0, 1))
        self._tbl.grid_columnconfigure(tuple(range(len(headers))), weight=1)

    # ── Public API ───────────────────────────────────────────
    def update(self, classes: list[dict], stats: dict, col_name: str) -> None:
        # Hapus baris lama (row > 0)
        for w in self._tbl.winfo_children():
            info = w.grid_info()
            if info and int(info["row"]) > 0:
                w.destroy()

        mean = stats["mean"]
        n = stats["n"]
        max_f = max(cls["f"] for cls in classes)
        total_f = total_fx = total_fdev2 = 0.0

        for i, cls in enumerate(classes):
            row = i + 1
            fdev2 = cls["f"] * (cls["mid"] - mean) ** 2
            total_f    += cls["f"]
            total_fx   += cls["fx"]
            total_fdev2 += fdev2
            f_rel = cls["f"] / n * 100

            bracket  = ")" if i < len(classes) - 1 else "]"
            interval = f"[{cls['lower']:.2f}, {cls['upper']:.2f}{bracket}"

            cells = [
                str(row),
                interval,
                f"{cls['mid']:.4f}",
                str(cls["f"]),
                f"{f_rel:.2f}%",
                str(cls["cum_f"]),
                f"{cls['fx']:.4f}",
                f"{fdev2:.4f}",
            ]
            bg = C["table_even"] if i % 2 == 0 else C["table_odd"]
            is_mode = cls["f"] == max_f

            for j, val in enumerate(cells):
                fw    = "bold" if j == 3 else "normal"
                color = C["accent4"] if (j == 3 and is_mode) else C["text_primary"]
                ctk.CTkLabel(
                    self._tbl,
                    text=val,
                    font=F_MONO(10) if j not in (0, 1) else F(10, fw),
                    text_color=color,
                    fg_color=bg,
                    pady=8,
                    padx=6,
                    corner_radius=0,
                ).grid(row=row, column=j, sticky="nsew", padx=1)

        # Baris total
        total_row = len(classes) + 1
        totals = [
            "Σ", "—", "—",
            str(int(total_f)),
            "100.00%",
            str(int(total_f)),
            f"{total_fx:.4f}",
            f"{total_fdev2:.4f}",
        ]
        for j, val in enumerate(totals):
            ctk.CTkLabel(
                self._tbl,
                text=val,
                font=F(10, "bold"),
                text_color=C["accent"],
                fg_color=C["table_total"],
                pady=10,
                padx=6,
            ).grid(row=total_row, column=j, sticky="nsew", padx=1, pady=1)

        # Update banner
        self._banner_lbl.configure(
            text=(
                f"📊  Kolom: {col_name}  ·  n = {stats['n']}  ·  "
                f"k = {stats['k']} kelas  ·  c = {stats['c']}  ·  "
                f"Range = {stats['range']:.4f}"
            ),
            text_color=C["accent3"],
        )
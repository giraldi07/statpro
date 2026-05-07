"""
ui/widgets.py
Widget-widget reusable yang dipakai di berbagai bagian UI.
"""

import customtkinter as ctk
from ui.theme import C, F, F_MONO


# ─────────────────────────────────────────────────────────────
#  StatMetric — kartu statistik di sidebar
# ─────────────────────────────────────────────────────────────
class StatMetric(ctk.CTkFrame):
    """
    Kartu kecil yang menampilkan satu nilai statistik.
    Dilengkapi garis bawah berwarna sesuai kategori.
    """

    def __init__(
        self,
        parent,
        label: str,
        value: str = "—",
        color: str = C["accent"],
        icon: str = "▸",
        **kwargs,
    ):
        super().__init__(parent, fg_color=C["bg_card2"], corner_radius=10, **kwargs)

        inner = ctk.CTkFrame(self, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=12, pady=10)

        ctk.CTkLabel(
            inner,
            text=f"{icon}  {label}",
            font=F(9),
            text_color=C["text_muted"],
            anchor="w",
        ).pack(fill="x")

        self._val_lbl = ctk.CTkLabel(
            inner,
            text=value,
            font=F_MONO(16, "bold"),
            text_color=color,
            anchor="w",
        )
        self._val_lbl.pack(fill="x", pady=(2, 0))

        # Garis aksen bawah
        ctk.CTkFrame(self, fg_color=color, height=2, corner_radius=0).pack(
            fill="x", side="bottom"
        )

    def set_value(self, value: str) -> None:
        self._val_lbl.configure(text=value)


# ─────────────────────────────────────────────────────────────
#  InterpretasiCard — kartu penjelasan di tab interpretasi
# ─────────────────────────────────────────────────────────────
class InterpretasiCard(ctk.CTkFrame):
    """
    Kartu analisis dengan aksen warna di sisi kiri dan badge status.

    PENTING: badge_color harus berupa hex #RRGGBB 6-digit.
    Transparansi badge background dihandle via fg_color eksplisit,
    BUKAN dengan menambahkan suffix hex ke string warna.
    """

    # Peta warna → warna latar badge (pre-defined, aman untuk Tkinter)
    _BADGE_BG: dict[str, str] = {
        C["success"]:        "#1A3A2A",
        C["warning"]:        "#3A3010",
        C["danger"]:         "#3A1020",
        C["accent"]:         "#1E1A40",
        C["accent2"]:        "#3A1828",
        C["accent3"]:        "#0E2E2C",
        C["accent4"]:        "#2E2610",
        C["text_secondary"]: "#1E2030",
    }
    _DEFAULT_BADGE_BG = "#1E2030"

    def __init__(
        self,
        parent,
        title: str,
        badge: str,
        badge_color: str,
        content: str,
        icon: str = "◈",
        **kwargs,
    ):
        super().__init__(parent, fg_color=C["bg_card"], corner_radius=12, **kwargs)

        # Garis aksen kiri
        ctk.CTkFrame(self, fg_color=badge_color, width=4, corner_radius=2).pack(
            side="left", fill="y"
        )

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=16, pady=14)

        # ── Baris header
        header_row = ctk.CTkFrame(body, fg_color="transparent")
        header_row.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(
            header_row,
            text=f"{icon}  {title}",
            font=F(13, "bold"),
            text_color=C["text_primary"],
        ).pack(side="left")

        # Latar badge: ambil dari peta, fallback ke default
        badge_bg = self._BADGE_BG.get(badge_color, self._DEFAULT_BADGE_BG)

        badge_frame = ctk.CTkFrame(
            header_row,
            fg_color=badge_bg,    # <── warna solid yang valid, bukan hex+alpha
            corner_radius=20,
        )
        badge_frame.pack(side="right")

        ctk.CTkLabel(
            badge_frame,
            text=badge,
            text_color=badge_color,
            font=F(10, "bold"),
            padx=10,
            pady=3,
        ).pack()

        # ── Konten teks
        ctk.CTkLabel(
            body,
            text=content,
            wraplength=660,
            justify="left",
            font=F(11),
            text_color=C["text_secondary"],
            anchor="w",
        ).pack(fill="x")


# ─────────────────────────────────────────────────────────────
#  SectionHeader — judul seksi di laporan / tab
# ─────────────────────────────────────────────────────────────
class SectionHeader(ctk.CTkLabel):
    def __init__(self, parent, text: str, **kwargs):
        super().__init__(
            parent,
            text=text,
            font=F(14, "bold"),
            text_color=C["text_primary"],
            anchor="w",
            **kwargs,
        )


# ─────────────────────────────────────────────────────────────
#  Divider
# ─────────────────────────────────────────────────────────────
class Divider(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent, height=1, fg_color=C["border"], **kwargs
        )
"""
ui/theme.py
Semua konstanta visual: warna, font, dan konfigurasi matplotlib.
Import C (colors) dan FONT dari sini di seluruh modul UI.
"""

import customtkinter as ctk
import matplotlib.pyplot as plt

# ─────────────────────────────────────────────────────────────
#  WARNA (dict C)
#  Semua warna adalah hex 6-digit (#RRGGBB) standar Tkinter.
#  JANGAN pernah append suffix alpha hex ("30", "50", dll) ke
#  warna ini — Tkinter tidak mendukung format #RRGGBBAA.
#  Untuk efek transparan gunakan fungsi hex_to_rgba() di bawah.
# ─────────────────────────────────────────────────────────────
C: dict[str, str] = {
    # Background
    "bg_dark":     "#0F1117",
    "bg_card":     "#1A1D27",
    "bg_card2":    "#222533",
    "bg_sidebar":  "#13151F",
    "bg_input":    "#1E2130",

    # Aksen
    "accent":      "#6C63FF",
    "accent_h":    "#5952D4",   # hover accent
    "accent2":     "#FF6584",
    "accent3":     "#43E8D8",
    "accent4":     "#FFD166",

    # Teks
    "text_primary":   "#F0F2FF",
    "text_secondary": "#8B90A0",
    "text_muted":     "#555A6E",

    # Semantik
    "success":  "#4ADE80",
    "warning":  "#FFD166",
    "danger":   "#FF6584",

    # Border & Table
    "border":       "#2A2D3E",
    "table_even":   "#1E2130",
    "table_odd":    "#1A1D27",
    "table_header": "#252838",
    "table_total":  "#1E2840",
}

# Alias pendek yang sering dipakai
ACCENT  = C["accent"]
SUCCESS = C["success"]
WARNING = C["warning"]
DANGER  = C["danger"]


def hex_to_rgba(hex_color: str, alpha: float) -> tuple[float, float, float, float]:
    """
    Konversi warna hex (#RRGGBB) ke tuple RGBA (0.0–1.0) untuk matplotlib.
    Gunakan ini di tempat yang butuh transparansi, bukan suffix string.
    """
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    return (r, g, b, alpha)


# ─────────────────────────────────────────────────────────────
#  FONT HELPER
# ─────────────────────────────────────────────────────────────
def F(size: int = 12, weight: str = "normal") -> ctk.CTkFont:
    """Shorthand untuk membuat CTkFont."""
    return ctk.CTkFont(family="Helvetica", size=size, weight=weight)


def F_MONO(size: int = 11, weight: str = "normal") -> ctk.CTkFont:
    """Monospace font untuk nilai numerik."""
    return ctk.CTkFont(family="Courier New", size=size, weight=weight)


# ─────────────────────────────────────────────────────────────
#  MATPLOTLIB DARK THEME
# ─────────────────────────────────────────────────────────────
def apply_mpl_theme() -> None:
    """Terapkan dark theme ke seluruh figure matplotlib."""
    plt.rcParams.update({
        "figure.facecolor":  C["bg_card"],
        "axes.facecolor":    C["bg_card2"],
        "axes.edgecolor":    C["border"],
        "axes.labelcolor":   C["text_secondary"],
        "axes.titlecolor":   C["text_primary"],
        "xtick.color":       C["text_secondary"],
        "ytick.color":       C["text_secondary"],
        "grid.color":        C["border"],
        "grid.alpha":        0.4,
        "text.color":        C["text_primary"],
        "legend.facecolor":  C["bg_card"],
        "legend.edgecolor":  C["border"],
        "legend.labelcolor": C["text_primary"],
        "font.family":       "DejaVu Sans",
    })


# ─────────────────────────────────────────────────────────────
#  CTK GLOBAL CONFIG
# ─────────────────────────────────────────────────────────────
def apply_ctk_theme() -> None:
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
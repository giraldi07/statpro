"""
ui/tabs/tab_grafik.py
Tab 2 — Histogram, Poligon Frekuensi, dan Frekuensi Relatif.
"""

import customtkinter as ctk
import matplotlib.ticker as mticker
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from ui.theme import C, F, hex_to_rgba


class TabGrafik:
    TAB_NAME = "📈  Grafik & Visualisasi"

    def __init__(self, tabview: ctk.CTkTabview):
        tab = tabview.tab(self.TAB_NAME)
        tab.configure(fg_color=C["bg_dark"])
        self._tab = tab

        self._frame = ctk.CTkFrame(tab, fg_color=C["bg_card"], corner_radius=10)
        self._frame.pack(fill="both", expand=True)

        ctk.CTkLabel(
            self._frame,
            text="📈  Histogram & Poligon Frekuensi akan tampil di sini",
            text_color=C["text_muted"],
            font=F(14),
        ).pack(expand=True)

    def update(self, classes: list[dict], stats: dict) -> None:
        for w in self._frame.winfo_children():
            w.destroy()

        lowers = [cls["lower"] for cls in classes]
        uppers = [cls["upper"] for cls in classes]
        mids   = [cls["mid"]   for cls in classes]
        freqs  = [cls["f"]     for cls in classes]
        f_rel  = [f / stats["n"] * 100 for f in freqs]
        c      = stats["c"]

        fig = Figure(figsize=(13, 4.8), dpi=100)
        fig.patch.set_facecolor(C["bg_card"])

        ax1 = fig.add_subplot(1, 2, 1)
        ax2 = fig.add_subplot(1, 2, 2)

        for ax in (ax1, ax2):
            ax.set_facecolor(C["bg_card2"])
            ax.tick_params(colors=C["text_secondary"])
            for spine in ax.spines.values():
                spine.set_edgecolor(C["border"])

        # ── Plot kiri: Histogram + Poligon ───────────────────
        bars = ax1.bar(
            lowers, freqs, width=c, align="edge",
            color=hex_to_rgba(C["accent"], 0.7),
            edgecolor=C["accent"],
            linewidth=0.8,
            label="Histogram",
        )
        ext_mids  = [lowers[0] - c / 2] + mids + [uppers[-1] + c / 2]
        ext_freqs = [0] + freqs + [0]

        ax1.fill_between(ext_mids, ext_freqs,
                         color=hex_to_rgba(C["accent3"], 0.08))
        ax1.plot(
            ext_mids, ext_freqs,
            marker="o", markersize=5,
            color=C["accent3"], linewidth=2,
            label="Poligon Frekuensi",
            markerfacecolor=C["bg_card"],
            markeredgewidth=2,
        )

        ax1.axvline(stats["mean"],   color=C["success"], linestyle="--",
                    linewidth=1.5, label=f"Mean = {stats['mean']:.2f}", alpha=0.9)
        ax1.axvline(stats["median"], color=C["warning"], linestyle=":",
                    linewidth=1.5, label=f"Median = {stats['median']:.2f}", alpha=0.9)

        max_f = max(freqs)
        for bar_, f in zip(bars, freqs):
            if f > 0:
                ax1.text(
                    bar_.get_x() + bar_.get_width() / 2,
                    bar_.get_height() + max_f * 0.015,
                    str(f), ha="center", va="bottom",
                    fontsize=8, color=C["text_secondary"],
                )

        ax1.set_xlabel("Nilai", fontsize=10, color=C["text_secondary"])
        ax1.set_ylabel("Frekuensi (f)", fontsize=10, color=C["text_secondary"])
        ax1.set_title("Histogram & Poligon Frekuensi",
                      fontsize=11, weight="bold", pad=12, color=C["text_primary"])
        ax1.legend(fontsize=8, loc="upper right")
        ax1.grid(axis="y", linestyle="--", alpha=0.3, color=C["border"])
        ax1.set_xlim(lowers[0] - c * 0.5, uppers[-1] + c * 0.5)
        ax1.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))

        # ── Plot kanan: Frekuensi Relatif ────────────────────
        bar_colors = [
            hex_to_rgba(C["accent2"], 0.85) if f == max(freqs)
            else hex_to_rgba(C["accent"], 0.75)
            for f in freqs
        ]
        bars3 = ax2.bar(range(len(classes)), f_rel, color=bar_colors,
                        width=0.7, edgecolor="none")

        ax2.set_xticks(range(len(classes)))
        ax2.set_xticklabels([f"K{i+1}" for i in range(len(classes))], fontsize=9)
        ax2.set_ylabel("Frekuensi Relatif (%)", fontsize=10, color=C["text_secondary"])
        ax2.set_title("Distribusi Frekuensi Relatif",
                      fontsize=11, weight="bold", pad=12, color=C["text_primary"])
        ax2.grid(axis="y", linestyle="--", alpha=0.3, color=C["border"])

        for bar_, v in zip(bars3, f_rel):
            ax2.text(
                bar_.get_x() + bar_.get_width() / 2,
                bar_.get_height() + 0.3,
                f"{v:.1f}%",
                ha="center", va="bottom",
                fontsize=8, color=C["text_secondary"],
            )

        mode_idx = freqs.index(max(freqs))
        ax2.text(
            0.02, 0.97,
            f"★ Kelas modus: K{mode_idx + 1}\n"
            f"  [{classes[mode_idx]['lower']:.2f}, {classes[mode_idx]['upper']:.2f})",
            transform=ax2.transAxes, fontsize=8,
            va="top", color=C["accent2"],
            bbox=dict(boxstyle="round,pad=0.4",
                      facecolor=C["bg_card2"], alpha=0.8,
                      edgecolor=C["border"]),
        )

        fig.tight_layout(pad=2)

        canvas = FigureCanvasTkAgg(fig, master=self._frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)
"""
Tab Boxplot & Violin Plot
"""

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from ui.theme import C, F

class TabBoxplot:
    TAB_NAME = "📊  Boxplot & Violin"

    def __init__(self, tabview: ctk.CTkTabview):
        tab = tabview.tab(self.TAB_NAME)
        tab.configure(fg_color=C["bg_dark"])
        self._tab = tab
        self._frame = ctk.CTkFrame(tab, fg_color=C["bg_card"], corner_radius=10)
        self._frame.pack(fill="both", expand=True)
        ctk.CTkLabel(
            self._frame,
            text="Boxplot & Violin Plot akan tampil di sini",
            text_color=C["text_muted"],
            font=F(14),
        ).pack(expand=True)

    def update(self, data, col_name):
        for w in self._frame.winfo_children():
            w.destroy()
        fig = Figure(figsize=(7, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.boxplot(data, vert=True, patch_artist=True,
                   boxprops=dict(facecolor=C["accent3"]))
        ax.set_title(f"Boxplot: {col_name}")
        ax.set_facecolor(C["bg_card2"])
        canvas = FigureCanvasTkAgg(fig, master=self._frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

import customtkinter as ctk
import pandas as pd
from tkinter import filedialog, messagebox
from datetime import datetime

from ui.theme import apply_ctk_theme, apply_mpl_theme, C as COLORS
from ui.sidebar import Sidebar
from ui.dialogs import PilihKolomDialog
from utils.file_reader import baca_file
from core.statistics import hitung_statistik
from core.interpreter import generate_interpretasi

# Import Tabs
from ui.tabs.tab_distribusi import TabDistribusi
from ui.tabs.tab_grafik import TabGrafik
from ui.tabs.tab_interpretasi import TabInterpretasi
from ui.tabs.tab_boxplot import TabBoxplot
from ui.tabs.tab_laporan import TabLaporan

class StatistikApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        apply_ctk_theme()
        apply_mpl_theme()
        self.title("StatPro — Kalkulator Statistik")
        self.geometry("1400x900")
        self.configure(fg_color=COLORS["bg_dark"])
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.sidebar = Sidebar(self, upload_callback=self._upload_file)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.main_container = ctk.CTkFrame(self, fg_color=COLORS["bg_dark"])
        self.main_container.grid(row=0, column=1, sticky="nsew")
        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.tabs = ctk.CTkTabview(self.main_container, fg_color=COLORS["bg_dark"], segmented_button_selected_color=COLORS["accent"])
        self.tabs.grid(row=1, column=0, sticky="nsew", padx=12, pady=12)
        # Tambahkan semua tab
        self.tabs.add(TabDistribusi.TAB_NAME)
        self.tabs.add(TabGrafik.TAB_NAME)
        self.tabs.add(TabBoxplot.TAB_NAME)
        self.tabs.add("Interpretasi")
        self.tabs.add(TabLaporan.TAB_NAME)
        self.tab_dist = TabDistribusi(self.tabs)
        self.tab_grafik = TabGrafik(self.tabs)
        self.tab_boxplot = TabBoxplot(self.tabs)
        self.tab_interp = TabInterpretasi(self.tabs.tab("Interpretasi"))
        self.tab_laporan = TabLaporan(self.tabs)
        self._last_data = None
        self._last_col = None
        self._last_stats = None
        self._last_interpretasi = None

    def _upload_file(self):
        path = filedialog.askopenfilename(filetypes=[("Excel / CSV", "*.xlsx *.xls *.csv")])
        if not path:
            return
        try:
            df, sheet_name = baca_file(path)
            dialog = PilihKolomDialog(self, df, sheet_name)
            self.wait_window(dialog)
            if dialog.result_col:
                series = df[dialog.result_col].dropna()
                data = pd.to_numeric(series, errors="coerce").dropna().values
                if len(data) == 0:
                    raise ValueError("Kolom yang dipilih tidak mengandung data numerik yang valid.")
                self._process(data, dialog.result_col, path.split("/")[-1])
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memproses file:\n{str(e)}")

    def _process(self, data, col_name, filename):
        classes, stats, data_sorted = hitung_statistik(data)
        ts = datetime.now().strftime("%H:%M:%S")
        self.sidebar.update_file_info(f"{filename} > {col_name}")
        self.sidebar.update_stats(stats)
        self.sidebar.update_timestamp(ts)
        self.tab_dist.update(classes, stats, col_name)
        self.tab_grafik.update(classes, stats)
        self.tab_boxplot.update(data_sorted, col_name)
        interpretasi = generate_interpretasi(stats, col_name)
        self.tab_interp.update_data(stats, col_name)
        self.tab_laporan.update(stats, interpretasi, col_name)
        self._last_data = data_sorted
        self._last_col = col_name
        self._last_stats = stats
        self._last_interpretasi = interpretasi

if __name__ == "__main__":
    app = StatistikApp()
    app.mainloop()

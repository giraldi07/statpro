"""
StatPro — Kalkulator Statistik Deskriptif Pro
Entry point: jalankan file ini untuk memulai aplikasi.
"""

from ui.app import StatistikApp


if __name__ == "__main__":
    app = StatistikApp()
    app.mainloop()
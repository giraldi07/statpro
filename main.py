"""
StatPro — Kalkulator Statistik Deskriptif Pro
Entry point: jalankan file ini untuk memulai aplikasi.
"""

from ui.app import StatistikApp

def main():
    # 1. Coba tutup splash screen jika dijalankan sebagai EXE
    try:
        import pyi_splash
        # Pastikan aplikasi sudah ter-load sepenuhnya sebelum menutup splash
        # Kamu bisa memberikan sedikit delay jika diperlukan, tapi biasanya 
        # inisialisasi StatistikApp() sudah cukup memakan waktu.
        pyi_splash.update_text("Inisialisasi Modul Statistik...")
        
        app = StatistikApp()
        
        # Tutup splash screen tepat sebelum jendela utama muncul
        pyi_splash.close()
    except ImportError:
        # Jika dijalankan sebagai skrip .py biasa, abaikan saja
        app = StatistikApp()

    app.mainloop()

if __name__ == "__main__":
    main()
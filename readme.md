# StatPro — Kalkulator Statistik Deskriptif Pro

## Struktur Proyek

```
StatPro/
├── main.py                  ← Entry point, jalankan ini
├── README.md
├── requirements.txt
│
├── core/                    ← Business logic (tidak ada UI)
│   ├── __init__.py
│   ├── statistics.py        ← Kalkulasi statistik deskriptif
│   └── interpreter.py       ← Generator teks interpretasi otomatis
│
├── ui/                      ← Semua komponen UI
│   ├── __init__.py
│   ├── theme.py             ← Warna, font, konstanta visual
│   ├── app.py               ← Window utama & layout
│   ├── sidebar.py           ← Sidebar + metric cards
│   ├── dialogs.py           ← Dialog pilih kolom
│   ├── tabs/
│   │   ├── __init__.py
│   │   ├── tab_distribusi.py   ← Tab tabel distribusi frekuensi
│   │   ├── tab_grafik.py       ← Tab histogram & frekuensi relatif
│   │   ├── tab_interpretasi.py ← Tab interpretasi & analisis
│   │   ├── tab_boxplot.py      ← Tab box plot & violin plot
│   │   └── tab_laporan.py      ← Tab laporan lengkap
│   └── widgets.py           ← Widget reusable (StatMetric, InterpretasiCard, dll)
│
└── utils/
    ├── __init__.py
    └── file_reader.py       ← Baca Excel/CSV dengan deteksi encoding
```

## Instalasi

```bash
pip install -r requirements.txt
```

## Menjalankan

```bash
python main.py
```

## Dependensi

Lihat `requirements.txt`
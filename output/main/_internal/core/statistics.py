import math
import numpy as np
import pandas as pd

def hitung_statistik(data: np.ndarray) -> tuple[list[dict], dict, np.ndarray]:
    """
    Hitung statistik deskriptif lengkap dari array data numerik.
    Menggunakan logika murni Data Berkelompok (Grouped Data).
    """
    # ── Proteksi Array Kosong
    if len(data) == 0:
        return [], {}, np.array([])

    data_sorted = np.sort(np.asarray(data, dtype=float))
    n = len(data_sorted)

    val_min = float(data_sorted[0])
    val_max = float(data_sorted[-1])
    range_val = val_max - val_min

    # ── Aturan Sturges
    k = max(5, int(math.ceil(1 + 3.322 * math.log10(n)))) if n > 0 else 0

    # ── Lebar Kelas & Pembuatan Batas (Binning)
    # Jika semua data bernilai sama (range = 0)
    if range_val == 0:
        c = 1.0
        k = 1
        bins = [val_min - 0.5, val_max + 0.5]
    else:
        c = range_val / k
        # linspace memastikan batas terendah dan tertinggi tercover 100% secara presisi
        bins = np.linspace(val_min, val_max, k + 1).tolist()

    # Gunakan np.histogram untuk ekstraksi frekuensi yang akurat dan bebas bug
    hist, bin_edges = np.histogram(data_sorted, bins=bins)

    # ── Bangun kelas distribusi frekuensi
    classes: list[dict] = []
    cum_f = 0
    sum_fx = 0.0

    for i in range(k):
        lower = float(bin_edges[i])
        upper = float(bin_edges[i + 1])
        f = int(hist[i])
        mid = (lower + upper) / 2.0
        
        cum_f += f
        fx = f * mid
        sum_fx += fx

        classes.append({
            "lower": lower,
            "upper": upper,
            "mid": mid,
            "f": f,
            "cum_f": cum_f,
            "fx": fx
        })

    # Mean Grouped
    mean_grouped = sum_fx / n if n > 0 else 0.0

    # ── Fungsi Bantuan untuk Kuartil (Data Kelompok)
    def get_quartile_grouped(q_fraction: float) -> float:
        target_f = q_fraction * n
        # Cari kelas dimana frekuensi kumulatif pertama kali mencapai atau melewati target_f
        idx = next((i for i, cls in enumerate(classes) if cls["cum_f"] >= target_f), len(classes) - 1)
        cls = classes[idx]
        F_sblm = classes[idx - 1]["cum_f"] if idx > 0 else 0
        
        if cls["f"] == 0:
            return cls["lower"]
        return cls["lower"] + ((target_f - F_sblm) / cls["f"]) * c

    # Hitung Q1, Median (Q2), dan Q3 secara konsisten menggunakan rumus data kelompok
    q1_grouped = get_quartile_grouped(0.25)
    median_grouped = get_quartile_grouped(0.50)
    q3_grouped = get_quartile_grouped(0.75)
    iqr_grouped = q3_grouped - q1_grouped

    # ── Modus (Data Kelompok)
    max_f = max((cls["f"] for cls in classes), default=0)
    mo_idx = next((i for i, cls in enumerate(classes) if cls["f"] == max_f), 0)
    mo_class = classes[mo_idx]
    
    d1 = mo_class["f"] - (classes[mo_idx - 1]["f"] if mo_idx > 0 else 0)
    d2 = mo_class["f"] - (classes[mo_idx + 1]["f"] if mo_idx < len(classes) - 1 else 0)
    
    modus_grouped = (
        mo_class["lower"] + (d1 / (d1 + d2)) * c
        if (d1 + d2) != 0
        else mo_class["mid"]
    )

    # ── Variansi & Std Dev (Data Kelompok)
    sum_f_devq = sum(cls["f"] * (cls["mid"] - mean_grouped) ** 2 for cls in classes)
    variance_grouped = sum_f_devq / (n - 1) if n > 1 else 0.0
    std_dev_grouped = math.sqrt(variance_grouped)
    cv = (std_dev_grouped / mean_grouped * 100) if mean_grouped != 0 else 0.0

    # ── Statistik tambahan (Raw Data)
    # Tetap dipertahankan untuk referensi komparasi bentuk sebaran
    series = pd.Series(data_sorted)
    skewness = float(series.skew()) if n > 2 else 0.0
    kurtosis = float(series.kurt()) if n > 3 else 0.0

    # ── Deteksi Outlier (Menggunakan IQR Grouped)
    lower_fence = q1_grouped - 1.5 * iqr_grouped
    upper_fence = q3_grouped + 1.5 * iqr_grouped
    outliers = data_sorted[(data_sorted < lower_fence) | (data_sorted > upper_fence)]
    pct_outlier = len(outliers) / n * 100 if n > 0 else 0.0

    stats = {
        "n": n,
        "k": k,
        "c": c,
        "min": val_min,
        "max": val_max,
        "range": range_val,
        "mean_grouped": mean_grouped,
        "median_grouped": median_grouped,
        "modus_grouped": modus_grouped,
        "variance_grouped": variance_grouped,
        "std_dev_grouped": std_dev_grouped,
        "cv": cv,
        "cv_grouped": cv,
        "skewness_grouped": skewness, 
        "kurtosis_grouped": kurtosis,
        "q1_grouped": q1_grouped,
        "q2_grouped": median_grouped,
        "q3_grouped": q3_grouped,
        "iqr_grouped": iqr_grouped,
        "skewness_raw": skewness,
        "kurtosis_raw": kurtosis,
        "outlier_count": len(outliers),
        "pct_outlier": pct_outlier,
        "lower_fence": lower_fence,
        "upper_fence": upper_fence,
    }
    
    return classes, stats, data_sorted
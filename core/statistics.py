"""
core/statistics.py
Seluruh kalkulasi statistik deskriptif — tidak ada UI di sini.
"""

import math
import numpy as np
import pandas as pd


def hitung_statistik(data: np.ndarray) -> tuple[list[dict], dict, np.ndarray]:
    """
    Hitung statistik deskriptif lengkap dari array data numerik.

    Returns:
        classes   : list of dict per kelas distribusi frekuensi
        stats     : dict ringkasan statistik
        data_sorted: data yang sudah diurutkan
    """
    data_sorted = np.sort(data)
    n = len(data_sorted)

    val_min = float(np.min(data_sorted))
    val_max = float(np.max(data_sorted))
    range_val = val_max - val_min

    # Jumlah kelas (Sturges), minimal 5
    k = max(5, int(math.ceil(1 + 3.322 * math.log10(n))))

    # Lebar kelas: dibulatkan ke atas
    c = math.ceil(range_val / k) if range_val > 0 else 1

    # ── Bangun kelas distribusi frekuensi
    classes: list[dict] = []
    lower = val_min
    for i in range(k):
        upper = lower + c
        mid = (lower + upper) / 2
        if i == k - 1:
            f = int(np.sum((data_sorted >= lower) & (data_sorted <= upper)))
        else:
            f = int(np.sum((data_sorted >= lower) & (data_sorted < upper)))
        classes.append({"lower": lower, "upper": upper, "mid": mid, "f": f})
        lower = upper

    # Koreksi total frekuensi
    total_f = sum(cls["f"] for cls in classes)
    if total_f != n:
        classes[-1]["f"] += n - total_f

    # Frekuensi kumulatif & f·x
    cum_f = 0
    sum_fx = 0.0
    for cls in classes:
        cum_f += cls["f"]
        cls["cum_f"] = cum_f
        cls["fx"] = cls["f"] * cls["mid"]
        sum_fx += cls["fx"]

    mean_grouped = sum_fx / n

    # ── Median
    half_n = n / 2
    med_idx = next(
        (i for i, cls in enumerate(classes) if cls["cum_f"] >= half_n),
        len(classes) - 1,
    )
    med_class = classes[med_idx]
    F_sblm = classes[med_idx - 1]["cum_f"] if med_idx > 0 else 0
    median_grouped = (
        med_class["lower"] + ((half_n - F_sblm) / med_class["f"]) * c
        if med_class["f"] != 0
        else med_class["lower"]
    )

    # ── Modus
    max_f = max(cls["f"] for cls in classes)
    mo_idx = next(i for i, cls in enumerate(classes) if cls["f"] == max_f)
    mo_class = classes[mo_idx]
    d1 = mo_class["f"] - (classes[mo_idx - 1]["f"] if mo_idx > 0 else 0)
    d2 = mo_class["f"] - (
        classes[mo_idx + 1]["f"] if mo_idx < len(classes) - 1 else 0
    )
    modus_grouped = (
        mo_class["lower"] + (d1 / (d1 + d2)) * c
        if (d1 + d2) != 0
        else mo_class["mid"]
    )

    # ── Variansi & Std Dev (data berkelompok)
    sum_f_devq = sum(
        cls["f"] * (cls["mid"] - mean_grouped) ** 2 for cls in classes
    )
    variance_grouped = sum_f_devq / (n - 1) if n > 1 else 0.0
    std_dev_grouped = math.sqrt(variance_grouped)
    cv = (std_dev_grouped / mean_grouped * 100) if mean_grouped != 0 else 0.0

    # ── Statistik tambahan dari data mentah
    series = pd.Series(data_sorted)
    q1 = float(np.percentile(data_sorted, 25))
    q2 = float(np.percentile(data_sorted, 50))
    q3 = float(np.percentile(data_sorted, 75))
    iqr = q3 - q1
    skewness = float(series.skew())
    kurtosis = float(series.kurt())

    # ── Deteksi outlier (metode IQR)
    lower_fence = q1 - 1.5 * iqr
    upper_fence = q3 + 1.5 * iqr
    outliers = data_sorted[
        (data_sorted < lower_fence) | (data_sorted > upper_fence)
    ]
    pct_outlier = len(outliers) / n * 100

    stats = {
        "n": n,
        "k": k,
        "c": c,
        "min": val_min,
        "max": val_max,
        "range": range_val,
        "mean": mean_grouped,
        "median": median_grouped,
        "modus": modus_grouped,
        "variance": variance_grouped,
        "std_dev": std_dev_grouped,
        "cv": cv,
        "q1": q1,
        "q2": q2,
        "q3": q3,
        "iqr": iqr,
        "skewness": skewness,
        "kurtosis": kurtosis,
        "outlier_count": len(outliers),
        "pct_outlier": pct_outlier,
        "lower_fence": lower_fence,
        "upper_fence": upper_fence,
    }
    return classes, stats, data_sorted
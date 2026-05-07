"""
core/interpreter.py
Generator teks interpretasi otomatis berdasarkan hasil statistik.
Tidak ada UI — hanya menghasilkan dict berisi teks & metadata warna logis.
"""

from ui.theme import C  # Warna diambil dari theme agar konsisten


def generate_interpretasi(stats: dict, col_name: str = "data") -> dict:
    """
    Hasilkan interpretasi naratif mendalam dari dict stats.

    Returns dict dengan key:
        dist_type, dist_desc, dist_color
        var_level, var_desc, var_color
        outlier_desc, outlier_color
        kurt_desc
        central_desc
        recommendations (list of str)
    """
    n          = stats["n"]
    mean       = stats["mean"]
    median     = stats["median"]
    modus      = stats["modus"]
    std_dev    = stats["std_dev"]
    cv         = stats["cv"]
    skewness   = stats["skewness"]
    kurtosis   = stats["kurtosis"]
    iqr        = stats["iqr"]           # noqa: F841 (digunakan secara implisit)
    out_count  = stats["outlier_count"]
    pct_out    = stats["pct_outlier"]
    val_min    = stats["min"]
    val_max    = stats["max"]

    # ─── Distribusi (simetri & skewness) ────────────────────
    diff_mm  = abs(mean - median)
    pct_diff = (diff_mm / abs(mean) * 100) if mean != 0 else 0

    if pct_diff < 2:
        dist_type  = "SIMETRIS"
        dist_desc  = (
            f"Data '{col_name}' menunjukkan distribusi yang hampir simetris sempurna. "
            f"Mean ({mean:.4f}) dan Median ({median:.4f}) sangat berdekatan "
            f"(selisih {diff_mm:.4f} atau {pct_diff:.2f}%), sehingga data tersebar "
            "merata di sekitar nilai tengah tanpa kecenderungan condong ke arah manapun. "
            "Distribusi ini ideal untuk analisis statistik parametrik."
        )
        dist_color = C["success"]
    elif skewness > 0.5:
        dist_type  = "CONDONG KANAN (Positif)"
        dist_desc  = (
            f"Data '{col_name}' memiliki distribusi condong ke kanan (skewness = {skewness:.4f}). "
            f"Mean ({mean:.4f}) > Median ({median:.4f}) karena ada nilai-nilai ekstrim tinggi "
            "yang 'menarik' rata-rata ke atas. Dalam konteks bisnis, ini umum terjadi pada "
            "data pendapatan, penjualan, atau waktu respons — di mana sebagian kecil "
            "transaksi bernilai sangat besar. Median lebih representatif sebagai ukuran pusat."
        )
        dist_color = C["warning"]
    elif skewness < -0.5:
        dist_type  = "CONDONG KIRI (Negatif)"
        dist_desc  = (
            f"Data '{col_name}' memiliki distribusi condong ke kiri (skewness = {skewness:.4f}). "
            f"Mean ({mean:.4f}) < Median ({median:.4f}) karena ada nilai-nilai ekstrim rendah "
            "yang menarik rata-rata ke bawah. Kondisi ini umum pada data skor ujian ketika "
            "sebagian besar peserta mendapat nilai tinggi, atau data usia saat ada kelompok "
            "usia sangat muda yang dominan."
        )
        dist_color = C["accent2"]
    else:
        dist_type  = "MENDEKATI SIMETRIS"
        dist_desc  = (
            f"Data '{col_name}' mendekati distribusi simetris (skewness = {skewness:.4f}). "
            f"Selisih Mean ({mean:.4f}) dan Median ({median:.4f}) sebesar {pct_diff:.2f}% "
            "masih dalam batas wajar. Data dapat dianalisis menggunakan metode statistik "
            "parametrik maupun non-parametrik."
        )
        dist_color = C["accent3"]

    # ─── Variabilitas ────────────────────────────────────────
    if cv < 15:
        var_level = "SANGAT RENDAH"
        var_desc  = (
            f"CV = {cv:.2f}% tergolong SANGAT RENDAH — data sangat homogen dan konsisten. "
            f"Simpangan baku {std_dev:.4f} hanya {cv:.2f}% dari rata-rata. "
            "Data ini sangat andal untuk estimasi, prediksi, dan pengendalian kualitas. "
            "Proses atau fenomena yang menghasilkan data ini berjalan sangat stabil."
        )
        var_color = C["success"]
    elif cv < 30:
        var_level = "SEDANG"
        var_desc  = (
            f"CV = {cv:.2f}% menunjukkan variabilitas SEDANG. "
            "Data cukup beragam namun masih dapat dikelola dan diinterpretasikan dengan "
            f"menggunakan rata-rata. Standar deviasi {std_dev:.4f} menggambarkan sebaran "
            "moderat di sekitar nilai tengah — masih layak dijadikan acuan kebijakan."
        )
        var_color = C["warning"]
    else:
        var_level = "TINGGI"
        var_desc  = (
            f"CV = {cv:.2f}% tergolong TINGGI — data sangat heterogen dan bervariasi. "
            f"Rentang antara nilai minimum ({val_min:.4f}) dan maksimum ({val_max:.4f}) "
            f"sangat lebar. Mean mungkin tidak representatif; gunakan MEDIAN ({median:.4f}) "
            "sebagai ukuran pusat yang lebih robust. Perlu investigasi lebih lanjut "
            "terhadap faktor penyebab variasi tinggi ini."
        )
        var_color = C["danger"]

    # ─── Outlier ─────────────────────────────────────────────
    if out_count == 0:
        outlier_desc  = (
            "Tidak ditemukan outlier dalam dataset ini menggunakan metode IQR "
            f"(batas bawah: {stats['lower_fence']:.4f}, batas atas: {stats['upper_fence']:.4f}). "
            "Data bersih dari nilai-nilai ekstrim yang dapat mendistorsi analisis. "
            "Hasil statistik dapat diandalkan sepenuhnya."
        )
        outlier_color = C["success"]
    elif pct_out < 5:
        outlier_desc  = (
            f"Ditemukan {out_count} outlier ({pct_out:.1f}% dari total data). "
            "Jumlah ini masih dalam batas wajar dan tidak terlalu mempengaruhi statistik. "
            "Periksa apakah outlier ini merupakan kesalahan pengukuran/input, "
            "atau memang nilai valid yang penting secara kontekstual (mis. transaksi besar, "
            "kejadian ekstrim). Jika valid, pertahankan; jika error, pertimbangkan koreksi."
        )
        outlier_color = C["warning"]
    else:
        outlier_desc  = (
            f"Ditemukan {out_count} outlier ({pct_out:.1f}% dari total data) — jumlah "
            "SIGNIFIKAN yang perlu perhatian serius. Outlier dalam jumlah besar dapat "
            "mendistorsi mean, variance, dan seluruh kesimpulan analisis. "
            "Sangat disarankan: (1) validasi ulang data sumber, (2) gunakan Median "
            "sebagai ukuran pusat, (3) pertimbangkan analisis terpisah untuk data "
            "utama dan outlier."
        )
        outlier_color = C["danger"]

    # ─── Kurtosis ────────────────────────────────────────────
    if kurtosis > 1:
        kurt_desc = (
            f"Kurtosis = {kurtosis:.4f} (LEPTOKURTIK) — kurva lebih lancip dari distribusi "
            "normal. Terdapat konsentrasi data tinggi di sekitar nilai tengah sekaligus "
            "kemungkinan nilai-nilai ekstrim (heavy tail). Variasi kejadian langka lebih "
            "tinggi dari yang diprediksi model normal."
        )
    elif kurtosis < -1:
        kurt_desc = (
            f"Kurtosis = {kurtosis:.4f} (PLATIKURTIK) — kurva lebih datar dari distribusi "
            "normal. Data tersebar merata tanpa puncak tajam, menunjukkan distribusi "
            "yang seragam. Tidak ada nilai yang sangat dominan mendekati rata-rata."
        )
    else:
        kurt_desc = (
            f"Kurtosis = {kurtosis:.4f} (MESOKURTIK) — mendekati distribusi normal. "
            "Bentuk kurva seimbang antara ketajaman puncak dan sebaran ekornya. "
            "Ini mendukung penggunaan uji statistik berbasis asumsi normalitas."
        )

    # ─── Tendensi Sentral ────────────────────────────────────
    if median > mean:
        diff_note = (
            f"Median lebih tinggi dari Mean sebesar {median - mean:.4f}, "
            "mengonfirmasi kecenderungan distribusi condong ke kiri."
        )
    elif mean > median:
        diff_note = (
            f"Mean lebih tinggi dari Median sebesar {mean - median:.4f}, "
            "mengonfirmasi kecenderungan distribusi condong ke kanan."
        )
    else:
        diff_note = "Mean = Median, menandakan distribusi yang sempurna simetris."

    central_desc = (
        f"Tiga ukuran tendensi sentral dari {n} data:\n\n"
        f"• MEAN ({mean:.4f}): Rata-rata aritmetika — dihitung dari semua nilai. "
        f"Sensitif terhadap outlier. {diff_note}\n\n"
        f"• MEDIAN ({median:.4f}): Nilai tengah yang membagi data 50:50. "
        "Tidak terpengaruh outlier sehingga lebih robust. "
        "Digunakan ketika distribusi tidak simetris.\n\n"
        f"• MODUS ({modus:.4f}): Nilai/kelompok yang paling sering muncul. "
        "Merepresentasikan nilai tipikal yang paling dominan. "
        "Berguna untuk data kategorikal dan identifikasi pola dominan."
    )

    # ─── Rekomendasi ─────────────────────────────────────────
    rekom: list[str] = []
    if cv > 30:
        rekom.append(
            f"⚠  Gunakan MEDIAN ({median:.4f}) bukan MEAN sebagai representasi utama "
            "karena variabilitas tinggi (CV > 30%)"
        )
    if out_count > 0:
        rekom.append(
            f"⚠  Selidiki {out_count} outlier sebelum mengambil kesimpulan final — "
            "pastikan bukan error input data"
        )
    if abs(skewness) > 1:
        rekom.append(
            "⚠  Pertimbangkan transformasi data (log/sqrt) agar mendekati distribusi "
            "normal jika ingin menggunakan uji parametrik"
        )
    if n < 30:
        rekom.append(
            f"⚠  Jumlah data kecil (n={n} < 30) — interpretasi harus hati-hati, "
            "gunakan uji non-parametrik jika memungkinkan"
        )
    if not rekom:
        rekom.append(
            f"✓  Data berkualitas baik — Mean ({mean:.4f}) layak digunakan "
            "sebagai ukuran representatif utama"
        )
        rekom.append(
            "✓  Distribusi mendukung penggunaan statistik parametrik (t-test, ANOVA, dll)"
        )
        rekom.append(
            "✓  Tidak ada tanda-tanda anomali signifikan pada dataset ini"
        )

    return {
        "dist_type":       dist_type,
        "dist_desc":       dist_desc,
        "dist_color":      dist_color,
        "var_level":       var_level,
        "var_desc":        var_desc,
        "var_color":       var_color,
        "outlier_desc":    outlier_desc,
        "outlier_color":   outlier_color,
        "kurt_desc":       kurt_desc,
        "central_desc":    central_desc,
        "recommendations": rekom,
    }
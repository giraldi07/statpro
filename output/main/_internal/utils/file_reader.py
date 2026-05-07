"""
utils/file_reader.py
Baca file Excel / CSV dengan toleransi tinggi terhadap encoding & separator.
"""

import numpy as np
import pandas as pd
import chardet


def detect_encoding(path: str) -> str:
    """Deteksi encoding file binary menggunakan chardet."""
    with open(path, "rb") as f:
        raw = f.read(100_000)
    result = chardet.detect(raw)
    enc = result.get("encoding") or "utf-8"
    enc = enc.lower().replace("-", "")
    alias = {
        "ascii":       "utf-8",
        "utf8bom":     "utf-8-sig",
        "utf8":        "utf-8",
        "iso88591":    "latin-1",
        "windows1252": "cp1252",
    }
    return alias.get(enc, enc)


def _coerce_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Coba konversi kolom object ke numerik.
    Angka dengan format lokal (1.234,56 atau 1,234.56) dinormalisasi dulu.
    """
    for col in df.columns:
        if df[col].dtype == object:
            converted = (
                df[col]
                .astype(str)
                .str.strip()
                .str.replace(r"\s+", "", regex=True)
                .str.replace(r"\.(?=\d{3}(?:[,\s]|$))", "", regex=True)
                .str.replace(",", ".", regex=False)
            )
            numeric = pd.to_numeric(converted, errors="coerce")
            if numeric.notna().sum() / max(len(df), 1) > 0.5:
                df[col] = numeric
    return df


def baca_file(path: str) -> tuple[pd.DataFrame, str | None]:
    """
    Membaca file Excel atau CSV.

    Returns:
        (DataFrame, sheet_name_or_None)
    Raises:
        ValueError jika tidak ada kolom numerik yang terbaca.
    """
    ext = path.rsplit(".", 1)[-1].lower()

    if ext in ("xlsx", "xls", "xlsm", "xlsb"):
        xl = pd.ExcelFile(path)
        best_df, best_num, best_sheet = None, -1, None
        for sname in xl.sheet_names:
            try:
                df = xl.parse(sname, header=0)
                df.columns = [str(c).strip() for c in df.columns]
                df = _coerce_numeric_columns(df)
                ncols = len(df.select_dtypes(include=[np.number]).columns)
                if ncols > best_num:
                    best_num, best_df, best_sheet = ncols, df, sname
            except Exception:
                continue
        if best_df is None or best_num == 0:
            raise ValueError("Tidak ada kolom numerik yang dapat dibaca dari file Excel.")
        return best_df, best_sheet

    else:  # CSV / TXT
        enc = detect_encoding(path)
        for sep in (";", ",", "\t", " "):
            try:
                df = pd.read_csv(
                    path, sep=sep, encoding=enc,
                    engine="python", on_bad_lines="skip",
                    skip_blank_lines=True,
                )
                df.columns = [str(c).strip() for c in df.columns]
                df = _coerce_numeric_columns(df)
                if (
                    len(df.select_dtypes(include=[np.number]).columns) > 0
                    and len(df) >= 5
                ):
                    return df, None
            except Exception:
                continue

        # Fallback: satu kolom tanpa header
        df = pd.read_csv(
            path, header=None, encoding=enc,
            engine="python", on_bad_lines="skip",
        )
        df.columns = [str(c).strip() for c in df.columns]
        df = _coerce_numeric_columns(df)
        return df, None
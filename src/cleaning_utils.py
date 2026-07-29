"""
Funciones reutilizables de limpieza y validación para el dataset
de suicidio INEGI (EDR 2006-2023).

Se van agregando conforme se definen las reglas en 02_cleaning.ipynb.
"""

import pandas as pd
from simpledbf import Dbf5


def load_dbf(path: str) -> pd.DataFrame:
    """Carga una tabla .dbf de INEGI (microdatos o catálogos) a un DataFrame."""
    dbf = Dbf5(path, codec="latin1")
    return dbf.to_dataframe()


def load_raw_year(path: str, year: int) -> pd.DataFrame:
    """Carga un archivo crudo (CSV o DBF ya convertido) de un año específico."""
    df = pd.read_csv(path, encoding="utf-8", low_memory=False)
    df["anio_carga"] = year
    return df


def standardize_columns(df: pd.DataFrame, column_map: dict) -> pd.DataFrame:
    """Renombra columnas según un mapeo estándar (para unificar nomenclatura entre años)."""
    return df.rename(columns=column_map)


def flag_duplicates(df: pd.DataFrame, subset: list = None) -> pd.DataFrame:
    """Marca duplicados exactos (o por subset de columnas) sin eliminarlos todavía."""
    df = df.copy()
    df["_is_duplicate"] = df.duplicated(subset=subset, keep="first")
    return df


def null_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Resumen de nulos por columna: conteo y porcentaje."""
    resumen = pd.DataFrame({
        "n_nulos": df.isnull().sum(),
        "pct_nulos": (df.isnull().sum() / len(df) * 100).round(2),
    })
    return resumen.sort_values("pct_nulos", ascending=False)


def dtype_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Resumen de tipo de dato y cardinalidad (valores únicos) por columna."""
    resumen = pd.DataFrame({
        "dtype": df.dtypes.astype(str),
        "n_unicos": df.nunique(),
        "n_nulos": df.isnull().sum(),
    })
    return resumen.sort_values("n_unicos", ascending=False)


def duplicate_report(df: pd.DataFrame, subset: list = None) -> dict:
    """Conteo de duplicados exactos (o por subset de columnas)."""
    total = len(df)
    duplicados = df.duplicated(subset=subset, keep="first").sum()
    return {
        "total_registros": total,
        "duplicados": int(duplicados),
        "pct_duplicados": round(duplicados / total * 100, 2) if total else 0,
    }


def profiling_report(df: pd.DataFrame, subset_dedup: list = None) -> None:
    """Imprime un resumen rápido de perfilado: shape, nulos, tipos, duplicados.
    Sustituye a ydata-profiling para mantener compatibilidad con Python 3.14+.
    """
    print(f"Shape: {df.shape[0]:,} filas x {df.shape[1]} columnas\n")
    print("--- Nulos por columna ---")
    print(null_summary(df))
    print("\n--- Tipos y cardinalidad ---")
    print(dtype_summary(df))
    print("\n--- Duplicados ---")
    print(duplicate_report(df, subset=subset_dedup))

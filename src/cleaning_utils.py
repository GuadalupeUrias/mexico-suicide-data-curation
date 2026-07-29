"""
Funciones reutilizables de limpieza y validación para el dataset
de suicidio INEGI (EDR 2006-2023).

Se van agregando conforme se definen las reglas en 02_cleaning.ipynb.
"""

import pandas as pd
from dbfread import DBF

# Nombres oficiales segun docs/data_dictionary.md (formato documentado por INEGI).
# Los archivos .dbf guardan los campos en MAYUSCULAS internamente; esta lista
# permite recuperar el formato "legible" documentado.
DEFUN_CANONICAL_COLUMNS = [
    "Ent_regis", "Mun_regis", "Tloc_regis", "Loc_regis", "Ent_resid", "Mun_resid",
    "Tloc_resid", "Loc_resid", "Ent_ocurr", "Mun_ocurr", "Tloc_ocurr", "Loc_ocurr",
    "Causa_def", "Cod_adicio", "Lista_mex", "Sexo", "Ent_nac", "Afromex", "Conindig",
    "Lengua", "Cve_lengua", "Nacionalid", "Nacesp_cve", "Edad", "Sem_gest", "Gramos",
    "Dia_ocurr", "Mes_ocurr", "Anio_ocur", "Dia_regis", "Mes_regis", "Anio_regis",
    "Dia_nacim", "Mes_nacim", "Anio_nacim", "Cond_act", "Ocupacion", "Escolarida",
    "Edo_civil", "Tipo_defun", "Ocurr_trab", "Lugar_ocur", "Par_agre", "Vio_fami",
    "Asist_medi", "Cirugia", "Natviole", "Necropsia", "Usonecrops", "Encefalica",
    "Donador", "Sitio_ocur", "Cond_cert", "Derechohab", "Embarazo", "Rel_emba",
    "Horas", "Minutos", "Capitulo", "Grupo", "Lista1", "Gr_lismex", "Area_ur",
    "Edad_agru", "Complicaro", "Dia_cert", "Mes_cert", "Anio_cert", "Maternas",
    "Ent_ocules", "Mun_ocules", "Loc_ocules", "Razon_m", "Dis_re_oax",
]


def load_dbf(path: str, encoding: str = "latin1") -> pd.DataFrame:
    """Carga una tabla .dbf de INEGI (microdatos o catalogos) a un DataFrame.
    Usa dbfread en lugar de simpledbf: mas confiable con archivos grandes en Windows
    (simpledbf puede colgarse con archivos de 100MB+ por su manejo de temporales).
    """
    table = DBF(path, encoding=encoding, ignore_missing_memofile=True)
    return pd.DataFrame(iter(table))


def normalize_columns(df: pd.DataFrame, canonical_names: list = None) -> pd.DataFrame:
    """Renombra columnas MAYUSCULAS (como las guarda el .dbf) al formato
    documentado en data_dictionary.md (ej. TIPO_DEFUN -> Tipo_defun).
    Columnas que no encuentren match quedan sin cambio (se imprime aviso).
    """
    canonical_names = canonical_names or DEFUN_CANONICAL_COLUMNS
    lookup = {name.upper(): name for name in canonical_names}
    df = df.copy()
    new_columns = []
    sin_match = []
    for col in df.columns:
        match = lookup.get(col.upper())
        if match:
            new_columns.append(match)
        else:
            new_columns.append(col)
            sin_match.append(col)
    df.columns = new_columns
    if sin_match:
        print(f"Columnas sin match en canonical_names (sin cambio): {sin_match}")
    return df


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

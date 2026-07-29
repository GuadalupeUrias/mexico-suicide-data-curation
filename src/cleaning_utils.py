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

# Nombres canonicos para las tablas de CATALOGO (CATMINDE, CATEMLDE23, LISTAMEX,
# CAPGPO, GPOLIMEX, LISTA1, PARENTESCO, PAISES, OCUPACIONES, COD_ADICIO, LENGUAS).
# Estas tablas usan nombres de columna distintos a DEFUN23 (Cve, Descrip, etc.),
# por eso necesitan su propia lista al normalizar.
CATALOG_CANONICAL_COLUMNS = [
    "Cve", "Descrip", "Cve_ent", "Cve_mun", "Cve_loc", "Nom_loc",
    "Cap", "Gpo", "Clave",
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


# Codigos de "no especificado" / "se ignora" / "no aplica" segun
# docs/data_dictionary.md, para las variables mas relevantes al analisis.
# No es exhaustivo de las 74 variables: cubre las que probablemente se usen
# en el analisis (sociodemograficas, geograficas y de contexto del hecho).
DEFUN_NULL_LIKE_CODES = {
    "Sexo": ["9"],
    "Edo_civil": ["8", "9"],
    "Escolarida": ["88", "99"],
    "Cond_act": ["8", "9"],
    "Nacionalid": ["9"],
    "Lengua": ["8", "9"],
    "Conindig": ["8", "9"],
    "Afromex": ["8", "9"],
    "Ent_nac": ["997", "998", "999"],
    "Ocupacion": ["997", "998", "999"],
    "Asist_medi": ["9"],
    "Necropsia": ["9"],
    "Usonecrops": ["8", "9"],
    "Ocurr_trab": ["8", "9"],
    "Lugar_ocur": ["9", "88"],
    "Sitio_ocur": ["99"],
    "Derechohab": ["99"],
    "Cond_cert": ["8", "9"],
    "Area_ur": ["9"],
    "Edad_agru": ["30"],
    "Tipo_defun": ["9"],
}


def special_code_report(df: pd.DataFrame, code_map: dict = None) -> pd.DataFrame:
    """Detecta valores categoricos que funcionan como nulos ('no especificado',
    'se ignora', 'no aplica') pero que pandas NO reconoce como NaN, porque estan
    codificados como numeros/strings (8, 9, 88, 99, 997, 998, 999, etc).

    Retorna una tabla: columna, codigo, descripcion generica, conteo, pct sobre el total.
    """
    code_map = code_map or DEFUN_NULL_LIKE_CODES
    total = len(df)
    filas = []
    for col, codigos in code_map.items():
        if col not in df.columns:
            continue
        serie = df[col].astype(str).str.strip()
        for codigo in codigos:
            conteo = (serie == str(codigo)).sum()
            if conteo > 0:
                filas.append({
                    "columna": col,
                    "codigo": codigo,
                    "conteo": int(conteo),
                    "pct_del_total": round(conteo / total * 100, 2) if total else 0,
                })
    resultado = pd.DataFrame(filas)
    if not resultado.empty:
        resultado = resultado.sort_values("pct_del_total", ascending=False).reset_index(drop=True)
    return resultado


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


# ============================================================
# FASE 2: LIMPIEZA
# Funciones que aplican las reglas documentadas en docs/methodology.md
# ============================================================

def recode_null_codes(df: pd.DataFrame, code_map: dict = None) -> pd.DataFrame:
    """Recodifica los codigos categoricos de 'no especificado'/'se ignora'/
    'no aplica' (8, 9, 88, 99, 997, 998, 999...) a NaN explicito de pandas.

    Decision metodologica (ver docs/methodology.md): NO se imputan estos
    valores, se preservan como nulos explicitos para mantener la honestidad
    del dato original.

    Retorna un DataFrame nuevo (no modifica el original) mas un resumen impreso
    de cuantos valores se recodificaron por columna.
    """
    code_map = code_map or DEFUN_NULL_LIKE_CODES
    df = df.copy()
    resumen = []
    for col, codigos in code_map.items():
        if col not in df.columns:
            continue
        serie_str = df[col].astype(str).str.strip()
        mask = serie_str.isin([str(c) for c in codigos])
        n_recodificados = int(mask.sum())
        if n_recodificados > 0:
            df.loc[mask, col] = pd.NA
            resumen.append({"columna": col, "n_recodificados_a_NaN": n_recodificados})
    if resumen:
        print("Recodificacion aplicada:")
        print(pd.DataFrame(resumen).to_string(index=False))
    return df


def split_edad(df: pd.DataFrame, col: str = "Edad") -> pd.DataFrame:
    """Separa la variable Edad (que mezcla unidad + valor en un solo codigo)
    en dos columnas nuevas: edad_valor (numero) y edad_unidad (horas/dias/
    meses/anios/no_especificado). Conserva la columna original sin modificar.

    Codificacion INEGI: 1001-1023=horas, 2001-2029=dias, 3001-3011=meses,
    4001-4120=anios, 4998/1098/2098/3098=no especificado.
    """
    df = df.copy()
    unidades = {"1": "horas", "2": "dias", "3": "meses", "4": "anios"}

    def _parse(codigo):
        if pd.isna(codigo):
            return pd.NA, pd.NA
        codigo_str = str(int(codigo)) if isinstance(codigo, float) else str(codigo)
        codigo_str = codigo_str.strip()
        if len(codigo_str) < 2:
            return pd.NA, pd.NA
        prefijo = codigo_str[0]
        resto = codigo_str[1:]
        unidad = unidades.get(prefijo, "no_especificado")
        if unidad == "no_especificado" or resto in ("998", "098", "97", "11"):
            return pd.NA, "no_especificado"
        try:
            valor = int(resto)
        except ValueError:
            return pd.NA, "no_especificado"
        return valor, unidad

    parsed = df[col].apply(_parse)
    df["edad_valor"] = parsed.apply(lambda x: x[0])
    df["edad_unidad"] = parsed.apply(lambda x: x[1])
    return df


def translate_catalog(
    df: pd.DataFrame,
    df_col: str,
    catalog_df: pd.DataFrame,
    catalog_code_col: str,
    catalog_desc_col: str,
    new_col_name: str,
) -> pd.DataFrame:
    """Cruza una columna codificada del dataset principal contra una tabla de
    catalogo (ej. CATMINDE.dbf, CATEMLDE23.dbf) y agrega una columna nueva
    con la etiqueta descriptiva. Conserva la columna de codigo original.
    """
    df = df.copy()
    lookup = dict(zip(
        catalog_df[catalog_code_col].astype(str).str.strip(),
        catalog_df[catalog_desc_col],
    ))
    df[new_col_name] = df[df_col].astype(str).str.strip().map(lookup)
    return df

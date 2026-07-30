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

# Alias de columnas que cambiaron de nombre entre anios/versiones del
# certificado de defuncion. Confirmado con evidencia cruzada (ver
# docs/methodology.md): PRESUNTO (usado en 2019-2021) es la misma variable
# que Tipo_defun (usado desde 2022), y el codigo "3" = Suicidio coincide en
# ambos esquemas (validado contra cifra oficial INEGI 2019: 7,233 vs 7,225
# obtenidos, diferencia 0.11%).
COLUMN_ALIASES = {
    "PRESUNTO": "Tipo_defun",
}


def apply_column_aliases(df: pd.DataFrame, alias_map: dict = None) -> pd.DataFrame:
    """Renombra columnas que cambiaron de nombre entre anios (ej. PRESUNTO ->
    Tipo_defun). Se aplica DESPUES de normalize_columns(). No sobreescribe si
    la columna canonica ya existe (evita colisiones)."""
    alias_map = alias_map or COLUMN_ALIASES
    df = df.copy()
    rename_dict = {}
    for old_name, new_name in alias_map.items():
        if old_name in df.columns and new_name not in df.columns:
            rename_dict[old_name] = new_name
    if rename_dict:
        df = df.rename(columns=rename_dict)
        print(f"Alias aplicados: {rename_dict}")
    return df


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


# ============================================================
# FASE 3: VALIDACION
# Controles de calidad sobre el dataset ya limpio (data/processed/)
# ============================================================

def validate_dates(df: pd.DataFrame, year_col: str, month_col: str, day_col: str) -> dict:
    """Reconstruye fechas a partir de columnas separadas de anio/mes/dia y
    reporta cuantas son invalidas (no forman una fecha real de calendario).
    """
    fechas = pd.to_datetime({
        "year": pd.to_numeric(df[year_col], errors="coerce"),
        "month": pd.to_numeric(df[month_col], errors="coerce"),
        "day": pd.to_numeric(df[day_col], errors="coerce"),
    }, errors="coerce")
    total = len(df)
    invalidas = int(fechas.isna().sum())
    return {
        "total_registros": total,
        "fechas_invalidas": invalidas,
        "pct_invalidas": round(invalidas / total * 100, 2) if total else 0,
    }


def validate_codes_against_catalog(
    df: pd.DataFrame, df_col: str, catalog_df: pd.DataFrame, catalog_code_col: str
) -> dict:
    """Verifica que todos los codigos usados en df_col existan en el catalogo
    de referencia. Retorna los codigos 'huerfanos' (sin match) y su conteo.
    """
    codigos_dataset = set(df[df_col].dropna().astype(str).str.strip())
    codigos_catalogo = set(catalog_df[catalog_code_col].astype(str).str.strip())
    huerfanos = codigos_dataset - codigos_catalogo
    n_registros_huerfanos = int(df[df_col].astype(str).str.strip().isin(huerfanos).sum())
    return {
        "codigos_huerfanos": sorted(huerfanos),
        "n_codigos_huerfanos": len(huerfanos),
        "n_registros_afectados": n_registros_huerfanos,
    }


def validate_cross_consistency(df: pd.DataFrame, col_a: str, valor_a, col_b: str, valores_b_validos: list) -> dict:
    """Verifica consistencia entre dos variables relacionadas. Ejemplo de uso:
    si Tipo_defun == 3 (suicidio), Causa_def deberia caer en el rango CIE-10
    de lesiones autoinfligidas (X60-X84).

    valores_b_validos puede ser una lista de valores exactos, o se puede pasar
    una funcion lambda como filtro personalizado via 'valores_b_validos'.
    """
    subset = df[df[col_a] == valor_a]
    if callable(valores_b_validos):
        es_valido = subset[col_b].apply(valores_b_validos)
    else:
        es_valido = subset[col_b].isin(valores_b_validos)
    n_inconsistentes = int((~es_valido).sum())
    return {
        "total_subset": len(subset),
        "n_inconsistentes": n_inconsistentes,
        "pct_inconsistentes": round(n_inconsistentes / len(subset) * 100, 2) if len(subset) else 0,
    }


# ============================================================
# ESCALAMIENTO MULTI-ANIO
# Funciones para procesar varios anios (ej. 2019-2023) de forma
# parametrizada, con auditoria de esquema previa a la consolidacion.
# ============================================================

def audit_year_schema(year: int, raw_dir: str = "../data/raw", filename_pattern: str = "DEFUN{yy}.dbf") -> dict:
    """Carga SOLO el esquema (nombres de columna) del archivo DEFUN de un anio
    especifico, sin cargar todos los registros a memoria innecesariamente
    (dbfread es lazy, pero aqui forzamos solo la lectura de columnas).

    Retorna un diccionario con: anio, columnas encontradas, columnas
    faltantes vs. DEFUN_CANONICAL_COLUMNS, y columnas extra no documentadas.
    """
    yy = str(year)[-2:]
    path = f"{raw_dir}/{year}/{filename_pattern.format(yy=yy)}"
    df_sample = load_dbf(path)
    df_sample = normalize_columns(df_sample)
    df_sample = apply_column_aliases(df_sample)
    columnas_encontradas = set(df_sample.columns)
    columnas_esperadas = set(DEFUN_CANONICAL_COLUMNS)
    return {
        "anio": year,
        "n_columnas": len(columnas_encontradas),
        "faltantes": sorted(columnas_esperadas - columnas_encontradas),
        "extra_no_documentadas": sorted(columnas_encontradas - columnas_esperadas),
    }


def audit_multiple_years(years: list, raw_dir: str = "../data/raw", filename_pattern: str = "DEFUN{yy}.dbf") -> pd.DataFrame:
    """Corre audit_year_schema para una lista de anios y devuelve un resumen
    tabular. Revisar ANTES de intentar concatenar multiples anios: si hay
    columnas faltantes/extra, hay que decidir como manejarlo (documentar en
    methodology.md, no simplemente ignorar).
    """
    resultados = []
    for year in years:
        try:
            r = audit_year_schema(year, raw_dir=raw_dir, filename_pattern=filename_pattern)
        except Exception as e:
            r = {"anio": year, "n_columnas": None, "faltantes": [f"ERROR: {e}"], "extra_no_documentadas": []}
        resultados.append(r)
    return pd.DataFrame(resultados)


def load_and_filter_year(
    year: int,
    raw_dir: str = "../data/raw",
    filename_pattern: str = "DEFUN{yy}.dbf",
    tipo_defun_col: str = "Tipo_defun",
    tipo_defun_suicidio: str = "3",
) -> pd.DataFrame:
    """Carga el archivo DEFUN de un anio especifico, normaliza columnas,
    filtra al universo de suicidio (Tipo_defun == 3), y agrega una columna
    'anio_dataset' para identificar la fuente al consolidar.
    """
    yy = str(year)[-2:]
    path = f"{raw_dir}/{year}/{filename_pattern.format(yy=yy)}"
    df = load_dbf(path)
    df = normalize_columns(df)
    df = apply_column_aliases(df)
    df_filtrado = df[df[tipo_defun_col].astype(str).str.strip() == tipo_defun_suicidio].copy()
    df_filtrado["anio_dataset"] = year
    return df_filtrado


def consolidate_years(years: list, raw_dir: str = "../data/raw", filename_pattern: str = "DEFUN{yy}.dbf") -> pd.DataFrame:
    """Procesa una lista de anios (carga + filtro de suicidio) y los
    consolida en un solo DataFrame con columna 'anio_dataset'. Imprime un
    resumen de cuantos registros aporto cada anio.
    """
    dfs = []
    for year in years:
        df_year = load_and_filter_year(year, raw_dir=raw_dir, filename_pattern=filename_pattern)
        print(f"{year}: {len(df_year):,} registros de suicidio")
        dfs.append(df_year)
    consolidado = pd.concat(dfs, ignore_index=True)
    print(f"\nTotal consolidado: {len(consolidado):,} registros, {len(years)} anios")
    return consolidado


# ============================================================
# FASE 4: DOCUMENTACION
# Generacion automatica de docs/data_dictionary.md a partir del
# diseno de registro oficial de INEGI.
# Fuente: https://www.inegi.org.mx/rnm/index.php/catalog/1140
# (tabla DEFUN24, Estadisticas de Defunciones Registradas 2024, 74 variables)
# ============================================================

# Descripciones oficiales por variable. Las llaves coinciden con
# DEFUN_CANONICAL_COLUMNS de arriba; se manejan por separado porque una es
# "cual es el nombre correcto" y la otra es "que significa cada nombre".
DEFUN_DESCRIPTIONS = {
    "Ent_regis": "Entidad federativa de registro",
    "Mun_regis": "Municipio de registro",
    "Tloc_regis": "Tamano de localidad de registro (asignado por numero de habitantes, no viene del certificado)",
    "Loc_regis": "Localidad de registro",
    "Ent_resid": "Entidad federativa de residencia habitual del fallecido",
    "Mun_resid": "Municipio de residencia habitual del fallecido",
    "Tloc_resid": "Tamano de localidad de residencia habitual (asignado por numero de habitantes)",
    "Loc_resid": "Localidad de residencia habitual",
    "Ent_ocurr": "Entidad federativa de ocurrencia (domicilio donde sucedio la defuncion)",
    "Mun_ocurr": "Municipio de ocurrencia",
    "Tloc_ocurr": "Tamano de localidad de ocurrencia (asignado por numero de habitantes)",
    "Loc_ocurr": "Localidad de ocurrencia",
    "Causa_def": "Causa de la defuncion, lista detallada (codigo CIE-10)",
    "Cod_adicio": "Codigo adicional CIE-10",
    "Lista_mex": "Causa de la defuncion segun Lista Mexicana",
    "Sexo": "Sexo (1=Hombre, 2=Mujer, 99=Se ignora)",
    "Ent_nac": "Lugar de nacimiento (entidad federativa o pais si nacio en el extranjero)",
    "Afromex": "Condicion de autoadscripcion como persona afromexicana (1=Si, 2=No, 9=Se ignora)",
    "Conindig": "Condicion de autoadscripcion como persona indigena (1=Si, 2=No, 9=Se ignora)",
    "Lengua": "Condicion de habla de lengua indigena (1=Si, 2=No, 9=Se ignora)",
    "Cve_lengua": "Clave de la lengua indigena hablada",
    "Nacionalid": "Nacionalidad (1=Mexicana, 2=Otra, 9=Se ignora)",
    "Nacesp_cve": "Nacionalidad extranjera especifica",
    "Edad": "Edad cumplida del fallecido (unidad depende del rango: horas/dias/meses/anios; ver split_edad)",
    "Sem_gest": "Semanas de gestacion (solo para fallecidos con menos de 28 dias de edad)",
    "Gramos": "Peso al nacer en gramos (solo para fallecidos con menos de 28 dias de edad)",
    "Dia_ocurr": "Dia de la defuncion",
    "Mes_ocurr": "Mes de la defuncion",
    "Anio_ocur": "Anio de la defuncion",
    "Dia_regis": "Dia de registro",
    "Mes_regis": "Mes de registro",
    "Anio_regis": "Anio de registro",
    "Dia_nacim": "Dia de nacimiento",
    "Mes_nacim": "Mes de nacimiento",
    "Anio_nacim": "Anio de nacimiento",
    "Cond_act": "Condicion de actividad economica (1=Trabajaba, 2=No, 9=Se ignora)",
    "Ocupacion": "Ocupacion (codigo; 997-999=Se ignora)",
    "Escolarida": "Nivel de escolaridad (1=Ninguna...10=Posgrado, 88/99=Se ignora)",
    "Edo_civil": "Estado conyugal (1=Soltera/o, 2=Viuda/o, 3=Divorciada/o, 4=Union libre, 5=Casada/o, 6=Separada/o, 8/9=Se ignora)",
    "Tipo_defun": "Tipo de defuncion (1=Accidente, 2=Agresion, 3=Lesion autoinfligida intencional [suicidio], 4=Enfermedad, 5=Intervencion legal, 9=Se ignora)",
    "Ocurr_trab": "Ocurrio en el desempeno de su trabajo (1=Si, 2=No, 8/9=Se ignora)",
    "Lugar_ocur": "Lugar donde ocurrio la lesion: tipo de sitio fisico (0=Vivienda particular, 1=Vivienda colectiva, 2=Escuela/oficina publica, 3=Area deportiva, 4=Calle/carretera, 5=Area comercial, 6=Area industrial, 7=Granja, 8=Otro, 9/88=Se ignora)",
    "Par_agre": "Parentesco de la persona presuntamente agresora con el fallecido",
    "Vio_fami": "Condicion de violencia familiar en relacion con la persona agresora",
    "Asist_medi": "Tuvo atencion medica durante la enfermedad o lesion antes de la muerte (1=Si, 2=No, 9=Se ignora)",
    "Cirugia": "Se realizo cirugia en las ultimas 4 semanas previas al fallecimiento (1=Si, 2=No, 9=Se ignora)",
    "Natviole": "La defuncion fue accidental o violenta (1=Si, 2=No, 9=Se ignora)",
    "Necropsia": "Se practico necropsia (1=Si, 2=No, 9=Se ignora)",
    "Usonecrops": "Los hallazgos de la necropsia se usaron en la certificacion (1=Si, 2=No, 8/9=Se ignora)",
    "Encefalica": "Presento muerte encefalica (1=Si, 2=No)",
    "Donador": "Fue donador(a) de organos (1=Si, 2=No)",
    "Sitio_ocur": "Sitio de ocurrencia de la defuncion: tipo de institucion (1=Secretaria de Salud, 2=IMSS Bienestar, 3=IMSS, 4=ISSSTE, 5=PEMEX, 6=SEDENA, 7=SEMAR, 8=Otra unidad medica publica, 9=Unidad medica privada, 10=Via publica, 11=Hogar, 12=Otro, 13=IMSS Bienestar OPD, 99=Se ignora)",
    "Cond_cert": "Persona que certifico (1=Medica/o tratante, 2=Medica/o legista, 3=Otra/o medica/o, 4=Autorizada SSA, 5=Autoridad civil, 8=Otro)",
    "Derechohab": "Afiliacion a servicios de salud (1=Ninguna, 2=IMSS, 3=ISSSTE, 4=PEMEX, 5=SEDENA, 6=SEMAR, 8=Otra, 10=IMSS Bienestar, 11=ISSFAM, 99=Se ignora)",
    "Embarazo": "Momento de la defuncion respecto al embarazo, en mujeres de 10-54 anios (1=Embarazo, 2=Parto, 3=Puerperio, 4=43 dias-11 meses posparto, 5=No embarazada)",
    "Rel_emba": "Las causas fueron complicaciones propias del embarazo, parto o puerperio (1=Si, 2=No)",
    "Horas": "Hora de la defuncion",
    "Minutos": "Minuto de la defuncion",
    "Capitulo": "Capitulo CIE-10 de la causa de defuncion (variable derivada)",
    "Grupo": "Grupo CIE-10 de la causa de defuncion (variable derivada)",
    "Lista1": "Causa de defuncion, Lista 1 CIE-10 (variable derivada)",
    "Gr_lismex": "Grupo segun Lista Mexicana (variable derivada)",
    "Area_ur": "Area urbana/rural de residencia habitual (1=Urbana, 2=Rural)",
    "Edad_agru": "Edad agrupada en rangos quinquenales oficiales (variable derivada de Edad)",
    "Complicaro": "Las causas anotadas complicaron el embarazo, parto o puerperio (1=Si, 2=No)",
    "Dia_cert": "Dia de certificacion",
    "Mes_cert": "Mes de certificacion",
    "Anio_cert": "Anio de certificacion",
    "Maternas": "Causas maternas detalladas (CIE-10, variable derivada)",
    "Ent_ocules": "Entidad federativa donde ocurrio la lesion (distinto del domicilio donde ocurrio la defuncion)",
    "Mun_ocules": "Municipio donde ocurrio la lesion",
    "Loc_ocules": "Localidad donde ocurrio la lesion",
    "Razon_m": "Razon materna (variable derivada, sin pregunta directa en el certificado)",
    "Dis_re_oax": "Distrito de registro especifico para el estado de Oaxaca",
    # Variables agregadas por este pipeline (no son originales de INEGI):
    "anio_dataset": "Anio del archivo fuente (agregada por consolidate_years, no es original de INEGI)",
    "edad_valor": "Valor numerico de la edad, ya separado de su unidad (agregada por split_edad)",
    "edad_unidad": "Unidad de la edad: horas/dias/meses/anios/no_especificado (agregada por split_edad)",
    "sexo_desc": "Etiqueta legible de Sexo (agregada en 02_cleaning.ipynb)",
    "causa_def_desc": "Etiqueta legible de Causa_def via catalogo CATMINDE (agregada en 02_cleaning.ipynb)",
    "ent_ocurr_desc": "Etiqueta legible de Ent_ocurr via catalogo geografico (agregada en 02_cleaning.ipynb)",
}


def generar_data_dictionary(df: pd.DataFrame, output_path: str = "../docs/data_dictionary.md") -> pd.DataFrame:
    """Genera el diccionario de datos a partir de las columnas de df,
    usando DEFUN_DESCRIPTIONS como fuente de descripciones oficiales.
    Guarda el resultado como Markdown en output_path y tambien lo regresa
    como DataFrame para inspeccion rapida en el notebook.

    Columnas sin match en DEFUN_DESCRIPTIONS quedan marcadas con TODO,
    para que sea evidente que falta documentarlas (no se deja en blanco).
    """
    filas = []
    for col in df.columns:
        serie = df[col]
        filas.append({
            "variable": col,
            "descripcion": DEFUN_DESCRIPTIONS.get(
                col, "**TODO: sin descripcion, verificar en diseno de registro oficial**"
            ),
            "tipo_dato": str(serie.dtype),
            "pct_nulos": round(serie.isnull().mean() * 100, 2),
            "n_unicos": serie.nunique(),
            "ejemplo": serie.dropna().iloc[0] if serie.notna().any() else "N/A",
        })
    df_dicc = pd.DataFrame(filas)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Diccionario de Datos - Suicidios Mexico (EDR/ISS, INEGI)\n\n")
        f.write("Descripciones basadas en el diseno de registro oficial de INEGI:\n")
        f.write("https://www.inegi.org.mx/rnm/index.php/catalog/1140\n\n")
        f.write(df_dicc.to_markdown(index=False))

    n_todo = (df_dicc["descripcion"].str.startswith("**TODO")).sum()
    print(f"Diccionario guardado en: {output_path}")
    print(f"Variables documentadas: {len(df_dicc) - n_todo} de {len(df_dicc)}"
          + (f" ({n_todo} pendientes de descripcion)" if n_todo else " (completo)"))
    return df_dicc

# Diccionario de datos

Fuente: INEGI, Estadísticas de Defunciones Registradas (EDR) 2023, tabla `DEFUN23.dbf`.
Documento base: `Descripcion_BD_Defunciones_2023.pdf` (INEGI, 2024).

> Este diccionario cubre la tabla principal (74 variables). Las tablas de catálogo
> (geográfico, causas, etc.) se documentan en la sección "Catálogos de referencia".

## Variable de filtrado (universo de este proyecto)

| Variable | Descripción | Valor de interés |
|---|---|---|
| `Tipo_defun` | Presunción de tipo de defunción | `3` = Suicidio (Lesión autoinfligida). Resto: 1=Accidente, 2=Homicidio, 4=Enfermedad, 5=Intervención legal, 9=Se ignora |

## Tabla principal (DEFUN23.dbf) — 74 variables

| # | Variable | Descripción | Tipo/long | Rango |
|---|---|---|---|---|
| 1 | Ent_regis | Entidad de registro | C(2) | 01-32 |
| 2 | Mun_regis | Municipio de registro | C(3) | 001-570 |
| 3 | Tloc_regis | Tamaño de localidad de registro | N(2) | 1-17, 99 |
| 4 | Loc_regis | Localidad de registro | C(4) | 0001-6999, 7777 |
| 5 | Ent_resid | Entidad de residencia habitual | C(2) | 01-35, 99 |
| 6 | Mun_resid | Municipio de residencia habitual | C(3) | 001-570, 999 |
| 7 | Tloc_resid | Tamaño de localidad de residencia | N(2) | 1-17, 99 |
| 8 | Loc_resid | Localidad de residencia | C(4) | 0001-6999, 7777, 9999 |
| 9 | Ent_ocurr | Entidad de ocurrencia | C(2) | 01-32, 99 |
| 10 | Mun_ocurr | Municipio de ocurrencia | C(3) | 001-570, 999 |
| 11 | Tloc_ocurr | Tamaño de localidad de ocurrencia | N(2) | 1-17, 99 |
| 12 | Loc_ocurr | Localidad de ocurrencia | C(4) | 0001-6999, 7777, 9999 |
| 13 | Causa_def | Causa básica de defunción (CIE-10 detallada) | C(4) | A000-R99X, U070-U129, V010-Y899 |
| 14 | Cod_adicio | Código adicional CIE-10 | C(4) | B950-P75X, S000-T983 |
| 15 | Lista_mex | Causa según lista mexicana | C(3) | 01-59, 61 |
| 16 | Sexo | Sexo del fallecido | N(1) | 1=Hombre, 2=Mujer, 9=No especificado |
| 17 | Ent_nac | Entidad/país de nacimiento | C(3) | 001-032, 101-535, 888, 997-999 |
| 18 | Afromex | Autodescripción afromexicana | C(1) | 1=Sí, 2=No, 8=No aplica, 9=No esp. |
| 19 | Conindig | Autodescripción indígena | C(1) | 1=Sí, 2=No, 8=No aplica, 9=No esp. |
| 20 | Lengua | Habla lengua indígena | C(1) | 1=Sí, 2=No, 8=No aplica, 9=Se ignora |
| 21 | Cve_lengua | Clave de lengua indígena | C(4) | ver catálogo LENGUAS |
| 22 | Nacionalid | Nacionalidad | C(1) | 1=Mexicana, 2=Extranjera, 9=No esp. |
| 23 | Nacesp_cve | Nacionalidad extranjera (código) | C(3) | ver catálogo PAISES |
| 24 | Edad | Edad del fallecido (codificada por unidad) | N(4) | 1001-1023=horas, 2001-2029=días, 3001-3011=meses, 4001-4120=años, 4998=no esp. |
| 25 | Sem_gest | Semanas de gestación (<28 días) | N(2) | 22-42, 88, 99 |
| 26 | Gramos | Peso en gramos (<28 días) | N(4) | 600-6000, 8888, 9999 |
| 27 | Dia_ocurr | Día de ocurrencia | N(2) | 1-31, 99 |
| 28 | Mes_ocurr | Mes de ocurrencia | N(2) | 1-12, 99 |
| 29 | Anio_ocur | Año de ocurrencia | N(4) | 1900-2023, 9999 |
| 30 | Dia_regis | Día de registro | N(2) | 1-31, 99 |
| 31 | Mes_regis | Mes de registro | N(2) | 1-12 |
| 32 | Anio_regis | Año de registro | N(4) | 2023 |
| 33 | Dia_nacim | Día de nacimiento | N(2) | 1-31, 99 |
| 34 | Mes_nacim | Mes de nacimiento | N(2) | 1-12, 99 |
| 35 | Anio_nacim | Año de nacimiento | N(4) | 1897-2023, 9999 |
| 36 | Cond_act | Condición de actividad económica | N(1) | 1=Sí, 2=No, 8=No aplica <5 años, 9=Se ignora |
| 37 | Ocupacion | Ocupación del fallecido | C(3) | ver catálogo OCUPACIONES (SINCO 2019) |
| 38 | Escolarida | Nivel de escolaridad | N(2) | 1-10, 88=No aplica <3 años, 99=No esp. |
| 39 | Edo_civil | Situación conyugal | N(1) | 1-6, 8=No aplica <12 años, 9=No esp. |
| **40** | **Tipo_defun** | **Tipo de defunción (presunción)** | **N(1)** | **1=Accidente, 2=Homicidio, 3=Suicidio, 4=Enfermedad, 5=Intervención legal, 9=Se ignora** |
| 41 | Ocurr_trab | Ocurrió en desempeño del trabajo | N(1) | 1=Sí, 2=No, 8=No aplica, 9=No esp. |
| 42 | Lugar_ocur | Espacio físico del hecho | N(2) | 0-9, 88=No aplica (muerte natural) |
| 43 | Par_agre | Parentesco del presunto agresor | N(2) | 1-72, 88, 99; ver catálogo PARENTESCO |
| 44 | Vio_fami | Violencia familiar (solo homicidios) | N(1) | 1=Sí, 2=No, 8=No aplica, 9=No esp. |
| 45 | Asist_medi | Atención médica antes de la muerte | N(1) | 1=Con, 2=Sin, 9=No esp. |
| 46 | Cirugia | Cirugía en últimas 4 semanas | C(1) | 1=Sí, 2=No, 8=No aplica, 9=No esp. |
| 47 | Natviole | Muerte accidental o violenta | C(1) | 1=Sí, 2=No, 8=No aplica |
| 48 | Necropsia | Se realizó necropsia | C(1) | 1=Sí, 2=No, 9=No esp. |
| 49 | Usonecrops | Necropsia usada en certificación | C(1) | 1=Sí, 2=No, 8=No aplica, 9=No esp. |
| 50 | Encefalica | Muerte encefálica | C(1) | 1=Sí, 2=No, 8=No aplica, 9=No esp. |
| 51 | Donador | Donador de órganos | C(1) | 1=Sí, 2=No, 8=No aplica, 9=No esp. |
| 52 | Sitio_ocur | Sitio de ocurrencia de la defunción | N(2) | 1-12, 99; ver etiquetas (institución de salud, vía pública, hogar...) |
| 53 | Cond_cert | Persona que certificó | N(1) | 1-5, 8, 9 |
| 54 | Derechohab | Afiliación a servicios de salud | N(2) | 1-10, 99 |
| 55 | Embarazo | Condición de embarazo (mujeres 10-54) | N(1) | 1-5, 8, 9 |
| 56 | Rel_emba | Relación causa-embarazo | N(1) | 1=Sí, 2=No, 8=No aplica, 9=No esp. |
| 57 | Horas | Hora de la defunción | N(2) | 0-23, 99 |
| 58 | Minutos | Minuto de la defunción | N(2) | 0-59, 99 |
| 59 | Capitulo | Capítulo CIE-10 | N(2) | 1-18, 20, 22 |
| 60 | Grupo | Grupo CIE-10 | N(2) | 1-35 |
| 61 | Lista1 | Lista de tabulación OMS 1990 | C(3) | 001-103, 902, 903 |
| 62 | Gr_lismex | Grupo lista mexicana | C(3) | 01-48, E49-E59 |
| 63 | Area_ur | Área urbana/rural de residencia | N(1) | 1=Urbana, 2=Rural, 9=No esp. |
| 64 | Edad_agru | Edad agrupada (quinquenal) | C(2) | 01-30 |
| 65 | Complicaro | Complicaciones de embarazo | N(1) | 1=Sí, 2=No, 8=No aplica, 9=No esp. |
| 66 | Dia_cert | Día de certificación | N(2) | 1-31, 99 |
| 67 | Mes_cert | Mes de certificación | N(2) | 1-12, 99 |
| 68 | Anio_cert | Año de certificación | N(4) | 2022-2023 |
| 69 | Maternas | Defunciones maternas | C(4) | ver catálogo CATMINDE |
| 70 | Ent_ocules | Entidad de ocurrencia de la lesión | C(2) | 01-35, 88, 99 |
| 71 | Mun_ocules | Municipio de ocurrencia de la lesión | C(3) | 001-570, 888, 999 |
| 72 | Loc_ocules | Localidad de ocurrencia de la lesión | C(4) | 0001-6999, 7777, 8888, 9999 |
| 73 | Razon_m | Contribuye a razón de mortalidad materna | N(1) | 1, vacío |
| 74 | Dis_re_oax | Distrito de registro de Oaxaca | C(3) | 901-930, 999 |

## Catálogos de referencia (tablas auxiliares)

| Archivo | Contenido | Relación |
|---|---|---|
| `CATEMLDE23.dbf` | Entidad, municipio, localidad (nombre) | `Cve_ent`, `Cve_mun`, `Cve_loc` ↔ `Ent_*`, `Mun_*`, `Loc_*` |
| `CATMINDE.dbf` | Causa de defunción detallada (CIE-10) | `Cve` ↔ `Causa_def` |
| `LISTAMEX.dbf` | Causa según lista mexicana | `Cve` ↔ `Lista_mex` |
| `CAPGPO.dbf` | Capítulo y grupo CIE-10 | `Cap`+`Gpo` ↔ `Capitulo`+`Grupo` |
| `GPOLIMEX.dbf` | Grupo lista mexicana | `Cve` ↔ `Gr_lismex` |
| `LISTA1.dbf` | Lista de tabulación OMS | `Cve` ↔ `Lista1` |
| `PARENTESCO.dbf` | Parentesco presunto agresor | `Cve` ↔ `Par_agre` |
| `PAISES.dbf` | Países/entidad de nacimiento | `Cve` ↔ `Ent_nac`, `Nacesp_cve` |
| `OCUPACIONES.dbf` | Ocupación (SINCO 2019) | `Cve` ↔ `Ocupacion` |
| `COD_ADICIO.dbf` | Código adicional CIE-10 | `Cve` ↔ `Cod_adicio` |
| `LENGUAS.dbf` | Lenguas indígenas (INALI) | `Clave` ↔ `Cve_lengua` |

## Convenciones
- Codificación de origen: `latin1` (típico en archivos `.dbf` de INEGI) — usar `codec='latin1'` al leer con `simpledbf`.
- Códigos "no especificado"/"se ignora" varían por variable (8, 9, 88, 98, 99, 888, 999, 9999 según longitud) — **no tratar como cero**, son nulos categóricos.
- La variable `Edad` mezcla unidades (horas/días/meses/años) en un solo campo numérico — requiere transformación antes de análisis.

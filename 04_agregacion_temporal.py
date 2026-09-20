"""Agregación temporal por UBIGEO y año para análisis exploratorio."""

from pathlib import Path

import pandas as pd

print("=" * 80)
print("PASO 3: AGREGACIÓN TEMPORAL (UBIGEO + AÑO)")
print("=" * 80)

datos_merged = pd.read_csv("data/clean/datos_merged.csv")
datos_merged = datos_merged[datos_merged["ANIO"] < 2026].copy()
print(f"\nDatos merged cargados: {datos_merged.shape[0]} registros, {datos_merged.shape[1]} columnas")
print(f"  Años disponibles: {sorted(datos_merged['ANIO'].unique())}")
print(f"  Distritos únicos: {datos_merged['UBIGEO'].nunique()}")

print("\n" + "=" * 80)
print("AGREGACIÓN POR UBIGEO + AÑO")
print("=" * 80)

agregado = datos_merged.groupby(
    ["UBIGEO", "ANIO", "DISTRITO", "POBLACION_TOTAL", "PORC_NBI", "P_MODALIDADES"],
    as_index=False,
)["cantidad"].sum()

print(f"\nDatos agregados por modalidad: {agregado.shape[0]} registros")

print("\n" + "=" * 80)
print("PIVOT MODALIDADES COMO COLUMNAS")
print("=" * 80)

pivot_modalidades = agregado.pivot_table(
    index=["UBIGEO", "ANIO", "DISTRITO", "POBLACION_TOTAL", "PORC_NBI"],
    columns="P_MODALIDADES",
    values="cantidad",
    aggfunc="sum",
    fill_value=0,
)

datos_temporales = pivot_modalidades.reset_index()
print(f"\nPivot completado: {datos_temporales.shape[0]} registros × {datos_temporales.shape[1]} columnas")
print(f"  Modalidades identificadas: {list(datos_temporales.columns[5:])}")

print("\n" + "=" * 80)
print("CÁLCULO DE MÉTRICAS")
print("=" * 80)

modalidades = [
    col for col in datos_temporales.columns if col not in ["UBIGEO", "ANIO", "DISTRITO", "POBLACION_TOTAL", "PORC_NBI"]
]

datos_temporales["TOTAL_DELITOS"] = datos_temporales[modalidades].sum(axis=1)
datos_temporales["TASA_DELITOS_10K"] = (
    (datos_temporales["TOTAL_DELITOS"] / datos_temporales["POBLACION_TOTAL"] * 10000)
    .round(2)
)

print(f"\nMétricas calculadas:")
print(
    f"  Total delitos - Min: {datos_temporales['TOTAL_DELITOS'].min():.0f}, "
    f"Max: {datos_temporales['TOTAL_DELITOS'].max():.0f}, "
    f"Media: {datos_temporales['TOTAL_DELITOS'].mean():.0f}"
)
print(
    f"  Tasa/10k - Min: {datos_temporales['TASA_DELITOS_10K'].min():.2f}, "
    f"Max: {datos_temporales['TASA_DELITOS_10K'].max():.2f}, "
    f"Media: {datos_temporales['TASA_DELITOS_10K'].mean():.2f}"
)

print("\n" + "=" * 80)
print("REORDENAMIENTO DE COLUMNAS")
print("=" * 80)

columnas_orden = [
    "UBIGEO",
    "ANIO",
    "DISTRITO",
    "POBLACION_TOTAL",
    "PORC_NBI",
    "TOTAL_DELITOS",
    "TASA_DELITOS_10K",
] + sorted(modalidades)

datos_temporales = datos_temporales[columnas_orden]

print("\nOrden final de columnas:")
for i, col in enumerate(columnas_orden, 1):
    print(f"  {i:2d}. {col}")

print("\n" + "=" * 80)
print("VALIDACIÓN")
print("=" * 80)

print(f"\nDimensiones esperadas: 344 registros (43 distritos × 8 años completos, 2018-2025)")
print(f"  Dimensiones actuales: {datos_temporales.shape[0]} registros × {datos_temporales.shape[1]} columnas")

distritos_por_año = datos_temporales.groupby("ANIO")["UBIGEO"].nunique()
print("\nDistritos por año:")
for año, count in distritos_por_año.items():
    print(f"  {año}: {count} distritos")

nulls = datos_temporales.isnull().sum()
if nulls.sum() > 0:
    print("\nValores nulos encontrados:")
    print(nulls[nulls > 0])
else:
    print("\nSin valores nulos")

print("\n" + "=" * 80)
print("GUARDANDO ARCHIVO")
print("=" * 80)

output_path = Path("data/processed/datos_temporales.csv")
datos_temporales.to_csv(output_path, index=False)

file_size = output_path.stat().st_size / 1024
print(f"\nArchivo guardado: {output_path}")
print(f"  Tamaño: {file_size:.2f} KB")
print(f"  Registros: {datos_temporales.shape[0]}")
print(f"  Columnas: {datos_temporales.shape[1]}")

print("\n" + "=" * 80)
print("RESUMEN FINAL - AGREGACIÓN TEMPORAL")
print("=" * 80)
print(
    f"""
Datos originales (merged):      {datos_merged.shape[0]:,} registros
Datos temporales (salida):      {datos_temporales.shape[0]:,} registros

Estructura:
  - 43 distritos de Lima
  - 8 años completos (2018-2025)
  - 7 modalidades de delito
  - Métricas: TOTAL_DELITOS, TASA_DELITOS_10K
  - Variables demográficas: POBLACION_TOTAL, PORC_NBI

Períodos:
  PRE-COVID:     2018-2019 ({len(datos_temporales[datos_temporales['ANIO'].isin([2018, 2019])])} registros)
  COVID PEAK:    2020-2021 ({len(datos_temporales[datos_temporales['ANIO'].isin([2020, 2021])])} registros)
  RECUPERACIÓN:  2022-2023 ({len(datos_temporales[datos_temporales['ANIO'].isin([2022, 2023])])} registros)
  ACTUAL:        2024-2025 ({len(datos_temporales[datos_temporales['ANIO'].isin([2024, 2025])])} registros)

Archivo de salida: {output_path}
"""
)

print("=" * 80)
print("PASO 3 COMPLETADO - LISTO PARA EDA")
print("=" * 80)

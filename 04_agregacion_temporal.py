"""
04_agregacion_temporal.py
Agregación de datos por UBIGEO + AÑO para análisis temporal EDA
Resultado: 344 registros (43 distritos × 8 años)
"""

import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================================
# 1. CARGAR DATOS MERGED
# ============================================================================
print("=" * 80)
print("PASO 3: AGREGACIÓN TEMPORAL (UBIGEO + AÑO)")
print("=" * 80)

datos_merged = pd.read_csv('data/clean/datos_merged.csv')
print(f"\n✓ Datos merged cargados: {datos_merged.shape[0]} registros, {datos_merged.shape[1]} columnas")
print(f"  Años disponibles: {sorted(datos_merged['ANIO'].unique())}")
print(f"  Distritos únicos: {datos_merged['UBIGEO'].nunique()}")

# ============================================================================
# 2. AGREGACIÓN POR UBIGEO + AÑO
# ============================================================================
print("\n" + "=" * 80)
print("AGREGACIÓN POR UBIGEO + AÑO")
print("=" * 80)

# Agrupar por UBIGEO, AÑO y MODALIDAD para crear pivot
agregado = datos_merged.groupby(['UBIGEO', 'ANIO', 'DISTRITO', 'POBLACION_TOTAL', 
                                  'PORC_NBI', 'P_MODALIDADES'], 
                                as_index=False)['cantidad'].sum()

print(f"\n✓ Datos agregados por modalidad: {agregado.shape[0]} registros")

# ============================================================================
# 3. PIVOT MODALIDADES COMO COLUMNAS
# ============================================================================
print("\n" + "=" * 80)
print("PIVOT MODALIDADES COMO COLUMNAS")
print("=" * 80)

pivot_modalidades = agregado.pivot_table(
    index=['UBIGEO', 'ANIO', 'DISTRITO', 'POBLACION_TOTAL', 'PORC_NBI'],
    columns='P_MODALIDADES',
    values='cantidad',
    aggfunc='sum',
    fill_value=0
)

datos_temporales = pivot_modalidades.reset_index()
print(f"\n✓ Pivot completado: {datos_temporales.shape[0]} registros × {datos_temporales.shape[1]} columnas")
print(f"  Modalidades identificadas: {list(datos_temporales.columns[5:])}")

# ============================================================================
# 4. CALCULAR TOTAL DE DELITOS Y TASA POR 10K
# ============================================================================
print("\n" + "=" * 80)
print("CÁLCULO DE MÉTRICAS")
print("=" * 80)

# Seleccionar columnas de modalidades (todo excepto UBIGEO, ANIO, DISTRITO, POBLACION_TOTAL, PORC_NBI)
modalidades = [col for col in datos_temporales.columns if col not in 
               ['UBIGEO', 'ANIO', 'DISTRITO', 'POBLACION_TOTAL', 'PORC_NBI']]

# Total de delitos
datos_temporales['TOTAL_DELITOS'] = datos_temporales[modalidades].sum(axis=1)

# Tasa por 10,000 habitantes
datos_temporales['TASA_DELITOS_10K'] = (datos_temporales['TOTAL_DELITOS'] / 
                                         datos_temporales['POBLACION_TOTAL'] * 10000).round(2)

print(f"\n✓ Métricas calculadas:")
print(f"  Total delitos - Min: {datos_temporales['TOTAL_DELITOS'].min():.0f}, " +
      f"Max: {datos_temporales['TOTAL_DELITOS'].max():.0f}, " +
      f"Media: {datos_temporales['TOTAL_DELITOS'].mean():.0f}")
print(f"  Tasa/10k - Min: {datos_temporales['TASA_DELITOS_10K'].min():.2f}, " +
      f"Max: {datos_temporales['TASA_DELITOS_10K'].max():.2f}, " +
      f"Media: {datos_temporales['TASA_DELITOS_10K'].mean():.2f}")

# ============================================================================
# 5. REORDENAR COLUMNAS
# ============================================================================
print("\n" + "=" * 80)
print("REORDENAMIENTO DE COLUMNAS")
print("=" * 80)

columnas_orden = ['UBIGEO', 'ANIO', 'DISTRITO', 'POBLACION_TOTAL', 'PORC_NBI', 
                  'TOTAL_DELITOS', 'TASA_DELITOS_10K'] + sorted(modalidades)

datos_temporales = datos_temporales[columnas_orden]

print(f"\n✓ Orden final de columnas:")
for i, col in enumerate(columnas_orden, 1):
    print(f"  {i:2d}. {col}")

# ============================================================================
# 6. VALIDACIÓN
# ============================================================================
print("\n" + "=" * 80)
print("VALIDACIÓN")
print("=" * 80)

print(f"\n✓ Dimensiones esperadas: 344 registros (43 distritos × 8 años)")
print(f"  Dimensiones actuales: {datos_temporales.shape[0]} registros × {datos_temporales.shape[1]} columnas")

# Verificar distritos por año
distritos_por_año = datos_temporales.groupby('ANIO')['UBIGEO'].nunique()
print(f"\n✓ Distritos por año:")
for año, count in distritos_por_año.items():
    print(f"  {año}: {count} distritos")

# Verificar valores nulos
nulls = datos_temporales.isnull().sum()
if nulls.sum() > 0:
    print(f"\n⚠ Valores nulos encontrados:")
    print(nulls[nulls > 0])
else:
    print(f"\n✓ Sin valores nulos")

# ============================================================================
# 7. GUARDAR ARCHIVO
# ============================================================================
print("\n" + "=" * 80)
print("GUARDANDO ARCHIVO")
print("=" * 80)

output_path = Path('data/processed/datos_temporales.csv')
datos_temporales.to_csv(output_path, index=False)

file_size = output_path.stat().st_size / 1024  # KB
print(f"\n✓ Archivo guardado: {output_path}")
print(f"  Tamaño: {file_size:.2f} KB")
print(f"  Registros: {datos_temporales.shape[0]}")
print(f"  Columnas: {datos_temporales.shape[1]}")

# ============================================================================
# 8. RESUMEN FINAL
# ============================================================================
print("\n" + "=" * 80)
print("RESUMEN FINAL - AGREGACIÓN TEMPORAL")
print("=" * 80)
print(f"""
Datos originales (merged):      {datos_merged.shape[0]:,} registros
Datos temporales (salida):      {datos_temporales.shape[0]:,} registros

Estructura:
  - 43 distritos de Lima
  - 8 años (2018-2026)
  - 7 modalidades de delito
  - Métricas: TOTAL_DELITOS, TASA_DELITOS_10K
  - Variables demográficas: POBLACION_TOTAL, PORC_NBI

Períodos:
  PRE-COVID:     2018-2019 ({len(datos_temporales[datos_temporales['ANIO'].isin([2018, 2019])])} registros)
  COVID PEAK:    2020-2021 ({len(datos_temporales[datos_temporales['ANIO'].isin([2020, 2021])])} registros)
  RECUPERACIÓN:  2022-2023 ({len(datos_temporales[datos_temporales['ANIO'].isin([2022, 2023])])} registros)
  ACTUAL:        2024-2026 ({len(datos_temporales[datos_temporales['ANIO'].isin([2024, 2025, 2026])])} registros)

Archivo de salida: {output_path}
""")

print("=" * 80)
print("✅ PASO 3 COMPLETADO - LISTO PARA EDA")
print("=" * 80)

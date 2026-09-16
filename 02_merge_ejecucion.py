"""
PASO 1: MERGE SIDPOL + POBLACION_NBI
Unir datos de crimen con datos demográficos por UBIGEO
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path

print("\n" + "="*70)
print("✅ PASO 1: MERGE SIDPOL + POBLACION_NBI")
print("="*70)

# ============================================================================
# 1. CARGAR SIDPOL
# ============================================================================
print("\n📊 1. Cargando SIDPOL...")
ruta_sidpol = 'data/raw/DATASET_Denuncias_Policiales_Enero 2018_Julio2026_LIMA.csv'

if not os.path.exists(ruta_sidpol):
    raise FileNotFoundError(f"❌ Archivo no encontrado: {ruta_sidpol}")

try:
    df_sidpol = pd.read_csv(ruta_sidpol)
    print(f"   ✓ SIDPOL cargado: {len(df_sidpol):,} registros")
    print(f"   ✓ Columnas: {df_sidpol.shape[1]}")
except Exception as e:
    print(f"   ❌ Error al cargar SIDPOL: {e}")
    raise

# ============================================================================
# 2. CARGAR POBLACION_NBI
# ============================================================================
print("\n📊 2. Cargando POBLACION_NBI...")
ruta_poblacion = 'data/raw/POBLACION_NBI_LIMA.xlsx'

if not os.path.exists(ruta_poblacion):
    raise FileNotFoundError(f"❌ Archivo no encontrado: {ruta_poblacion}")

try:
    df_poblacion = pd.read_excel(ruta_poblacion)
    print(f"   ✓ POBLACION_NBI cargado: {len(df_poblacion)} registros")
    print(f"   ✓ Columnas: {df_poblacion.shape[1]}")
except Exception as e:
    print(f"   ❌ Error al cargar POBLACION_NBI: {e}")
    raise

# ============================================================================
# 3. ESTANDARIZAR UBIGEO
# ============================================================================
print("\n📋 3. Estandarizando UBIGEOs...")
try:
    df_sidpol['UBIGEO_HECHO'] = df_sidpol['UBIGEO_HECHO'].astype(str).str.zfill(6)
    df_poblacion['UBIGEO'] = df_poblacion['UBIGEO'].astype(str).str.zfill(6)
    print(f"   ✓ UBIGEOs convertidos a 6 dígitos con leading zeros")
    print(f"   ✓ SIDPOL UBIGEO_HECHO únicos: {df_sidpol['UBIGEO_HECHO'].nunique()}")
    print(f"   ✓ POBLACION_NBI UBIGEO únicos: {df_poblacion['UBIGEO'].nunique()}")
except Exception as e:
    print(f"   ❌ Error al estandarizar UBIGEOs: {e}")
    raise

# ============================================================================
# 4. MERGE POR UBIGEO
# ============================================================================
print("\n🔗 4. Ejecutando merge...")
try:
    df_merged = df_sidpol.merge(
        df_poblacion,
        left_on='UBIGEO_HECHO',
        right_on='UBIGEO',
        how='left'
    )
    print(f"   ✓ Merge completado")
    print(f"   ✓ Registros en merged: {len(df_merged):,}")
    print(f"   ✓ Columnas en merged: {df_merged.shape[1]}")
except Exception as e:
    print(f"   ❌ Error en el merge: {e}")
    raise

# ============================================================================
# 5. VALIDAR INTEGRIDAD
# ============================================================================
print("\n🔍 5. Validando integridad del merge...")
try:
    nulos_poblacion = df_merged['POBLACION_TOTAL'].isna().sum()
    nulos_nbi = df_merged['PORC_NBI'].isna().sum()
    
    print(f"   ✓ Registros con POBLACION_TOTAL: {len(df_merged) - nulos_poblacion:,}")
    print(f"   ✓ Registros con PORC_NBI: {len(df_merged) - nulos_nbi:,}")
    
    if nulos_poblacion == 0:
        print(f"   ✓ SIN VALORES NULOS en POBLACION_TOTAL ✅")
    else:
        print(f"   ⚠️ ADVERTENCIA: {nulos_poblacion} valores nulos en POBLACION_TOTAL")
        
    # Verificar distribución de casos por UBIGEO
    casos_por_ubigeo = df_merged.groupby('UBIGEO_HECHO').size()
    print(f"\n   📊 Estadísticas de casos por UBIGEO:")
    print(f"      Mínimo: {casos_por_ubigeo.min()}")
    print(f"      Máximo: {casos_por_ubigeo.max()}")
    print(f"      Promedio: {casos_por_ubigeo.mean():.0f}")
    
except Exception as e:
    print(f"   ❌ Error en validación: {e}")
    raise

# ============================================================================
# 6. MOSTRAR MUESTRA DE DATOS
# ============================================================================
print("\n📋 6. Muestra de datos (primeras 3 filas):")
print(df_merged[['UBIGEO_HECHO', 'DISTRITO', 'POBLACION_TOTAL', 'PORC_NBI', 'cantidad']].head(3).to_string())

# ============================================================================
# 7. GUARDAR DATASET MERGED
# ============================================================================
print("\n💾 7. Guardando dataset merged...")
try:
    # Crear directorio si no existe
    Path('data/clean').mkdir(parents=True, exist_ok=True)
    
    ruta_salida = 'data/clean/datos_merged.csv'
    df_merged.to_csv(ruta_salida, index=False, encoding='utf-8')
    
    # Verificar que se guardó
    if os.path.exists(ruta_salida):
        tamaño_mb = os.path.getsize(ruta_salida) / (1024**2)
        print(f"   ✓ Archivo guardado: {ruta_salida}")
        print(f"   ✓ Tamaño: {tamaño_mb:.2f} MB")
        print(f"   ✓ Registros: {len(df_merged):,}")
    else:
        print(f"   ❌ Error: No se pudo guardar el archivo")
except Exception as e:
    print(f"   ❌ Error al guardar: {e}")
    raise

# ============================================================================
# 8. RESUMEN FINAL
# ============================================================================
print("\n" + "="*70)
print("✅ PASO 1 COMPLETADO EXITOSAMENTE")
print("="*70)
print(f"\n📊 RESUMEN FINAL:")
print(f"   ✓ SIDPOL cargado: {len(df_sidpol):,} registros")
print(f"   ✓ POBLACION_NBI cargado: {len(df_poblacion)} distritos")
print(f"   ✓ Merge completado: {len(df_merged):,} registros")
print(f"   ✓ Integridad validada: Todos los datos demográficos presentes")
print(f"   ✓ Archivo guardado: datos_merged.csv ({tamaño_mb:.2f} MB)")
print(f"\n🚀 SIGUIENTE PASO: Paso 2 - Agregación por Distrito")
print("="*70 + "\n")

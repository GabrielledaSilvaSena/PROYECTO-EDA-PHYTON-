"""
Script 2: Limpieza y transformación de los datos
Objetivo: Preparar el dataset para el análisis corrigiendo errores, 
          tipos de datos y valores nulos
"""
import pandas as pd
import os

# ---- Rutas ----
RUTA_CSV = 'DATA/RAW/bank-additional.csv'
RUTA_EXCEL = 'DATA/RAW/customer-details.xlsx'
RUTA_SALIDA = 'DATA/PROCESSED/bank_cleaned.csv'
RUTA_CLIENTES = 'DATA/PROCESSED/customer_cleaned.csv'

# ---- Cargar datos ----
print("Cargando datos...")
df = pd.read_csv(RUTA_CSV)
print(f"Registros cargados: {len(df)} filas, {len(df.columns)} columnas")

# ---- Eliminar columna índice duplicada ----
if 'Unnamed: 0' in df.columns:
    df = df.drop('Unnamed: 0', axis=1, errors='ignore')
    print("\nColumna Unnamed: 0 eliminada (era un índice duplicado)")

# ---- Verificar duplicados ----
print("\n--- Verificando duplicados ---")
duplicados = df.duplicated().sum()
print(f"Duplicados encontrados: {duplicados}")
if duplicados > 0:
    df = df.drop_duplicates()
    print(f"Duplicados eliminados. Registros restantes: {len(df)}")
else:
    print("No hay filas duplicadas. Dataset limpio en este aspecto.")

# ---- Ver nulos antes de limpiar ----
print("\n--- Valores nulos antes de limpiar ---")
print(df.isnull().sum())

# ---- Rellenar nulos en variables clave ----
print("\nRellenando nulos...")

# age: mediana porque es una variable numérica con posibles outliers
mediana_edad = df['age'].median()
df['age'] = df['age'].fillna(mediana_edad)
print(f"  age: rellenado con mediana ({mediana_edad:.0f} años)")

# Variables categóricas: 'unknown' para no inventar categorías
for col in ['job', 'education', 'marital']:
    n_nulos = df[col].isnull().sum()
    df[col] = df[col].fillna('unknown')
    print(f"  {col}: {n_nulos} nulos rellenados con 'unknown'")

# Variables binarias: 0 si es nulo (asumimos que no tiene el producto)
for col in ['default', 'housing', 'loan']:
    n_nulos = df[col].isnull().sum()
    df[col] = df[col].fillna(0).astype(int)
    print(f"  {col}: {n_nulos} nulos rellenados con 0, convertido a int")

# ---- Corregir columnas numéricas con coma decimal ----
# Estas columnas vinieron como texto porque usan coma como separador decimal
# Las convertimos a float para poder analizarlas correctamente
print("\n--- Convirtiendo columnas numéricas con coma decimal ---")
columnas_coma = ['euribor3m', 'cons.price.idx', 'cons.conf.idx', 'nr.employed']

for col in columnas_coma:
    if col in df.columns:
        df[col] = df[col].astype(str).str.replace(',', '.', regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce')
        print(f"  {col}: convertida a float correctamente")

# ---- Estandarizar texto a minúsculas ----
print("\nConvirtiendo texto a minúsculas...")
for col in ['marital', 'education', 'job', 'y', 'contact', 'poutcome']:
    if col in df.columns:
        df[col] = df[col].str.lower()

# ---- Verificar nulos que quedan ----
print("\n--- Nulos después de limpiar ---")
nulos_restantes = df.isnull().sum()
nulos_con_valor = nulos_restantes[nulos_restantes > 0]

if len(nulos_con_valor) > 0:
    print(nulos_con_valor)
    print("\nNota: Las columnas 'date' y otras variables económicas siguen teniendo")
    print("algunos nulos. Se dejan así porque:")
    print("  - 'date': no se usa en el análisis principal")
    print("  - Variables económicas (si quedan): la conversión de coma a punto")
    print("    puede dejar NaN en valores que no eran numéricos. No se imputan")
    print("    porque son indicadores macroeconómicos que requieren datos reales.")
else:
    print("No quedan nulos en las columnas principales.")

# ---- Guardar dataset limpio ----
os.makedirs('DATA/PROCESSED', exist_ok=True)
df.to_csv(RUTA_SALIDA, index=False)
print(f"\nDataset limpio guardado en: {RUTA_SALIDA}")
print(f"Registros finales: {len(df)} filas, {len(df.columns)} columnas")

# ---- Limpiar y combinar datos de clientes (Excel) ----
print("\n--- Limpiando datos de clientes (Excel) ---")
hojas = ['2012', '2013', '2014']
lista_dfs = []

for hoja in hojas:
    df_hoja = pd.read_excel(RUTA_EXCEL, sheet_name=hoja)
    lista_dfs.append(df_hoja)

df_clientes = pd.concat(lista_dfs, ignore_index=True)
print(f"Total clientes combinados: {len(df_clientes)}")

# Limpiar nulos en Income (usamos mediana)
if df_clientes['Income'].isnull().sum() > 0:
    mediana_income = df_clientes['Income'].median()
    df_clientes['Income'] = df_clientes['Income'].fillna(mediana_income)
    print(f"Income: nulos rellenados con mediana ({mediana_income:.0f})")

# Convertir Dt_Customer a fecha
df_clientes['Dt_Customer'] = pd.to_datetime(df_clientes['Dt_Customer'], errors='coerce')

df_clientes.to_csv(RUTA_CLIENTES, index=False)
print(f"Datos de clientes guardados en: {RUTA_CLIENTES}")

print("\n¡Limpieza completada!")
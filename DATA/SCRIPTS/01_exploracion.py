"""
Script 1: Exploración inicial de los datos
Objetivo: Primera vista del dataset para entender su estructura antes de limpiar
"""
import pandas as pd

# ---- Rutas de los archivos ----
RUTA_CSV = 'DATA/RAW/bank-additional.csv'
RUTA_EXCEL = 'DATA/RAW/customer-details.xlsx'
HOJAS_EXCEL = ['2012', '2013', '2014']

# ---- Cargar el archivo CSV ----
print("Cargando los datos...")
df = pd.read_csv(RUTA_CSV)

print(f"\nTotal de registros: {len(df)}")
print(f"Total de columnas: {len(df.columns)}")

# Ver las primeras filas
print("\n--- Primeras 5 filas ---")
print(df.head())

# Ver qué columnas tenemos
print("\n--- Columnas del dataset ---")
print(df.columns.tolist())

# Información general
print("\n--- Información del dataset ---")
df.info()

# Chequear valores nulos
print("\n--- Valores nulos ---")
print(df.isnull().sum())

# Estadísticas de las variables numéricas
print("\n--- Estadísticas básicas ---")
print(df.describe())

# Ver la distribución de algunas variables categóricas
print("\n--- Tipos de trabajo ---")
print(df['job'].value_counts())

print("\n--- Estado civil ---")
print(df['marital'].value_counts())

print("\n--- Nivel de educación ---")
print(df['education'].value_counts())

# La variable más importante: si el cliente aceptó o no
print("\n--- Variable objetivo (y) ---")
print(df['y'].value_counts())

total = len(df)
si = df[df['y'] == 'yes'].shape[0]
no = df[df['y'] == 'no'].shape[0]
print(f"\nSí: {si} ({si/total*100:.2f}%)")
print(f"No: {no} ({no/total*100:.2f}%)")

# ---- Cargar datos de clientes del Excel ----
print("\n\n--- Cargando datos de clientes ---")

dataframes_clientes = {}
for hoja in HOJAS_EXCEL:
    dataframes_clientes[hoja] = pd.read_excel(RUTA_EXCEL, sheet_name=hoja)
    print(f"Clientes {hoja}: {len(dataframes_clientes[hoja])} registros")

total_clientes = sum(len(df_hoja) for df_hoja in dataframes_clientes.values())
print(f"Total clientes: {total_clientes}")

# Ver cómo son los datos de 2012
print("\n--- Primeras filas de clientes 2012 ---")
print(dataframes_clientes['2012'].head())

print("\n--- Columnas disponibles ---")
print(dataframes_clientes['2012'].columns.tolist())

print("\nExploración inicial completada!")
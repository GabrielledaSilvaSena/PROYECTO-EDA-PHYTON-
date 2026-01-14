"""
Script para explorar los datos del proyecto
"""

import pandas as pd

# Cargar el archivo CSV
print("Cargando los datos...")
df = pd.read_csv('DATA/RAW/bank-additional.csv')

# Ver cuántos datos tenemos
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

# Ver el porcentaje
total = len(df)
si = df[df['y'] == 'yes'].shape[0]
no = df[df['y'] == 'no'].shape[0]
print(f"\nSí: {si} ({si/total*100:.2f}%)")
print(f"No: {no} ({no/total*100:.2f}%)")

# Ahora cargo los datos de clientes del Excel
print("\n\n--- Cargando datos de clientes ---")

# El Excel tiene 3 hojas, una por cada año
df_2012 = pd.read_excel('DATA/RAW/customer-details.xlsx', sheet_name='2012')
df_2013 = pd.read_excel('DATA/RAW/customer-details.xlsx', sheet_name='2013')
df_2014 = pd.read_excel('DATA/RAW/customer-details.xlsx', sheet_name='2014')

print(f"Clientes 2012: {len(df_2012)} registros")
print(f"Clientes 2013: {len(df_2013)} registros")
print(f"Clientes 2014: {len(df_2014)} registros")
print(f"Total clientes: {len(df_2012) + len(df_2013) + len(df_2014)}")

# Ver cómo son los datos de 2012
print("\n--- Primeras filas de clientes 2012 ---")
print(df_2012.head())

print("\n--- Columnas disponibles ---")
print(df_2012.columns.tolist())

print("\nExploración inicial completada!")
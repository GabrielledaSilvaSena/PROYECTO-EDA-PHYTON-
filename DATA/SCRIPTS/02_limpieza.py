"""
Limpieza de datos
"""

import pandas as pd

# Cargar datos
print("Cargando datos...")
df = pd.read_csv('DATA/RAW/bank-additional.csv')

print(f"\nTotal filas: {len(df)}")
print(f"Total columnas: {len(df.columns)}")

# Ver columnas
print("\nColumnas:")
print(df.columns.tolist())

# Hay una columna rara "Unnamed: 0" que parece un índice
df = df.drop('Unnamed: 0', axis=1)
print("\nColumna Unnamed eliminada")

# Chequear valores nulos
print("\n--- Valores nulos ---")
print(df.isnull().sum())

# Rellenar nulos en age con la mediana
print("\nRellenando nulos en age...")
mediana_edad = df['age'].median()
df['age'] = df['age'].fillna(mediana_edad)
print(f"Se usó la mediana: {mediana_edad}")

# Rellenar nulos en job, education, marital con "unknown"
print("\nRellenando nulos en job, education, marital...")
df['job'] = df['job'].fillna('unknown')
df['education'] = df['education'].fillna('unknown')  
df['marital'] = df['marital'].fillna('unknown')

# Las variables default, housing, loan tienen muchos nulos
# Asumo que si es nulo = no tiene (0)
print("\nRellenando nulos en default, housing, loan con 0...")
df['default'] = df['default'].fillna(0)
df['housing'] = df['housing'].fillna(0)
df['loan'] = df['loan'].fillna(0)

# Convertir texto a minúsculas para estandarizar
print("\nConvirtiendo texto a minúsculas...")
df['marital'] = df['marital'].str.lower()
df['education'] = df['education'].str.lower()
df['y'] = df['y'].str.lower()

# Verificar cuántos nulos quedan
print("\n--- Nulos después de limpiar ---")
nulos_restantes = df.isnull().sum()
print(nulos_restantes[nulos_restantes > 0])

# Guardar
print("\nGuardando datos limpios...")
df.to_csv('DATA/PROCESSED/bank_cleaned.csv', index=False)
print("Archivo guardado en DATA/PROCESSED/bank_cleaned.csv")

print(f"\nDataset final: {len(df)} filas, {len(df.columns)} columnas")
print("¡Listo!")
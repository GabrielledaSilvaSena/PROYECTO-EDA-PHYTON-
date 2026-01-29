"""
Análisis estadístico de los datos
"""

import pandas as pd

# Cargar datos limpios
print("Cargando datos limpios...")
df = pd.read_csv('DATA/PROCESSED/bank_cleaned.csv')
print(f"Datos cargados: {df.shape[0]} filas, {df.shape[1]} columnas")

# Análisis de la variable objetivo
print("\n=== ANÁLISIS DE LA VARIABLE OBJETIVO (y) ===")
print(df['y'].value_counts())
print("\nPorcentajes:")
print(df['y'].value_counts(normalize=True) * 100)

# Análisis por edad
print("\n=== ANÁLISIS POR EDAD ===")
print(f"Edad promedio: {df['age'].mean():.2f} años")
print(f"Edad mediana: {df['age'].median():.2f} años")
print(f"Edad mínima: {df['age'].min():.0f} años")
print(f"Edad máxima: {df['age'].max():.0f} años")

# Ver quiénes aceptan más por edad
print("\nTasa de aceptación por grupos de edad:")
df['grupo_edad'] = pd.cut(df['age'], bins=[0, 30, 40, 50, 60, 100], 
                           labels=['<30', '30-40', '40-50', '50-60', '>60'])
tabla_edad = pd.crosstab(df['grupo_edad'], df['y'], normalize='index') * 100
print(tabla_edad)

# Análisis por trabajo
print("\n=== ANÁLISIS POR TIPO DE TRABAJO ===")
print("\nDistribución de trabajos:")
print(df['job'].value_counts())

print("\nTasa de aceptación por trabajo:")
tabla_trabajo = pd.crosstab(df['job'], df['y'], normalize='index') * 100
print(tabla_trabajo['yes'].sort_values(ascending=False))

# Análisis por estado civil
print("\n=== ANÁLISIS POR ESTADO CIVIL ===")
print("\nDistribución:")
print(df['marital'].value_counts())

print("\nTasa de aceptación por estado civil:")
tabla_marital = pd.crosstab(df['marital'], df['y'], normalize='index') * 100
print(tabla_marital)

# Análisis por educación
print("\n=== ANÁLISIS POR EDUCACIÓN ===")
print("\nDistribución:")
print(df['education'].value_counts())

print("\nTasa de aceptación por nivel educativo:")
tabla_education = pd.crosstab(df['education'], df['y'], normalize='index') * 100
print(tabla_education['yes'].sort_values(ascending=False))

# Análisis de préstamos
print("\n=== ANÁLISIS DE PRÉSTAMOS ===")
print(f"\nClientes con préstamo hipotecario: {df['housing'].sum():.0f} ({df['housing'].sum()/len(df)*100:.1f}%)")
print(f"Clientes con otro préstamo: {df['loan'].sum():.0f} ({df['loan'].sum()/len(df)*100:.1f}%)")

print("\nTasa de aceptación según préstamos:")
print(f"Con hipoteca - Sí: {df[df['housing']==1]['y'].value_counts(normalize=True)['yes']*100:.2f}%")
print(f"Sin hipoteca - Sí: {df[df['housing']==0]['y'].value_counts(normalize=True)['yes']*100:.2f}%")

# Análisis de la duración de la llamada
print("\n=== ANÁLISIS DE DURACIÓN DE LLAMADA ===")
print(f"Duración promedio: {df['duration'].mean():.2f} segundos")
print(f"Duración mediana: {df['duration'].median():.2f} segundos")

print("\nDuración promedio según respuesta:")
print(f"Aceptaron (yes): {df[df['y']=='yes']['duration'].mean():.2f} segundos")
print(f"No aceptaron (no): {df[df['y']=='no']['duration'].mean():.2f} segundos")

# Análisis de campañas
print("\n=== ANÁLISIS DE CAMPAÑAS ===")
print(f"Número promedio de contactos: {df['campaign'].mean():.2f}")
print(f"Máximo de contactos a un cliente: {df['campaign'].max():.0f}")

print("\nTasa de aceptación según número de contactos:")
df['grupo_contactos'] = pd.cut(df['campaign'], bins=[0, 1, 2, 3, 100], 
                                labels=['1', '2', '3', '>3'])
tabla_contactos = pd.crosstab(df['grupo_contactos'], df['y'], normalize='index') * 100
print(tabla_contactos['yes'])

# Correlaciones básicas
print("\n=== CORRELACIONES ===")
columnas_numericas = ['age', 'duration', 'campaign', 'previous']
correlaciones = df[columnas_numericas].corr()
print("\nCorrelación entre variables numéricas:")
print(correlaciones)

print("\n¡Análisis completado!")
"""
Script 3: Análisis estadístico descriptivo
Objetivo: Entender qué factores influyen en que un cliente acepte o no
          el depósito a plazo, usando tablas cruzadas y estadísticas descriptivas
"""
import pandas as pd

# ---- Rutas ----
RUTA_LIMPIO = 'DATA/PROCESSED/bank_cleaned.csv'
RUTA_CLIENTES = 'DATA/PROCESSED/customer_cleaned.csv'
RUTA_MERGED = 'DATA/PROCESSED/bank_merged.csv'

# ---- Función reutilizable para analizar tasa de aceptación ----
def tasa_aceptacion(df, columna):
    """
    Calcula la tasa de aceptación (%) por categoría de una variable,
    e incluye el número de registros (n) para contexto.
    """
    tabla = pd.crosstab(df[columna], df['y'], normalize='index') * 100
    conteo = df[columna].value_counts().rename('n')
    resultado = tabla.join(conteo).sort_values('yes', ascending=False)
    return resultado

# ---- Cargar datos limpios ----
print("Cargando datos limpios...")
df = pd.read_csv(RUTA_LIMPIO)
print(f"Datos cargados: {df.shape[0]} filas, {df.shape[1]} columnas")

# ---- Variable objetivo ----
print("\n=== ANÁLISIS DE LA VARIABLE OBJETIVO (y) ===")
print(df['y'].value_counts())
print("\nPorcentajes:")
print(df['y'].value_counts(normalize=True) * 100)

# ---- Análisis por edad ----
print("\n=== ANÁLISIS POR EDAD ===")
print(f"Edad promedio: {df['age'].mean():.2f} años")
print(f"Edad mediana: {df['age'].median():.2f} años")
print(f"Rango: {df['age'].min():.0f} - {df['age'].max():.0f} años")

df['grupo_edad'] = pd.cut(df['age'], bins=[0, 30, 40, 50, 60, 100],
                          labels=['<30', '30-40', '40-50', '50-60', '>60'])

print("\nTasa de aceptación por grupos de edad (con n de registros):")
print(tasa_aceptacion(df, 'grupo_edad'))
print("\nNota: el grupo >60 tiene tasa alta pero menos registros,")
print("      hay que interpretar ese porcentaje con cautela.")

# ---- Análisis por trabajo ----
print("\n=== ANÁLISIS POR TIPO DE TRABAJO ===")
print(tasa_aceptacion(df, 'job'))
print("\nNota: 'student' y 'retired' lideran en aceptación.")
print("      Revisar la columna 'n' para ver que tienen menos volumen que 'admin.' o 'blue-collar'.")

# ---- Análisis por estado civil ----
print("\n=== ANÁLISIS POR ESTADO CIVIL ===")
print(tasa_aceptacion(df, 'marital'))

# ---- Análisis por educación ----
print("\n=== ANÁLISIS POR NIVEL EDUCATIVO ===")
print(tasa_aceptacion(df, 'education'))
print("\nNota: 'illiterate' aparece con tasa alta pero muy pocos registros (ver n).")
print("      No sacar conclusiones fuertes de esta categoría.")

# ---- Análisis de préstamos ----
print("\n=== ANÁLISIS DE PRÉSTAMOS ===")
print(f"Con préstamo hipotecario: {df['housing'].sum()} ({df['housing'].sum()/len(df)*100:.1f}%)")
print(f"Con préstamo personal: {df['loan'].sum()} ({df['loan'].sum()/len(df)*100:.1f}%)")

print("\nHipoteca vs aceptación:")
print(tasa_aceptacion(df, 'housing'))
print("\nPréstamo personal vs aceptación:")
print(tasa_aceptacion(df, 'loan'))

# ---- Análisis de duración de llamada ----
print("\n=== ANÁLISIS DE DURACIÓN DE LLAMADA ===")
print(f"Duración promedio global: {df['duration'].mean():.2f} segundos")
print(f"Duración mediana global: {df['duration'].median():.2f} segundos")

duracion_por_respuesta = df.groupby('y')['duration'].agg(['mean', 'median', 'count'])
duracion_por_respuesta.columns = ['promedio', 'mediana', 'n']
print("\nDuración según respuesta:")
print(duracion_por_respuesta)
print("\nLas llamadas con aceptación duran aprox. 2.5x más. Es el factor más diferenciador.")

# ---- Análisis de campañas ----
print("\n=== ANÁLISIS DE CAMPAÑAS ===")
print(f"Promedio de contactos: {df['campaign'].mean():.2f}")
print(f"Máximo de contactos: {df['campaign'].max():.0f}")

df['grupo_contactos'] = pd.cut(df['campaign'], bins=[0, 1, 2, 3, 100],
                                labels=['1', '2', '3', '>3'])
print("\nTasa de aceptación por número de contactos (con n):")
print(tasa_aceptacion(df, 'grupo_contactos'))
print("\nPatrón claro: más contactos = menos aceptación (fatiga de contacto).")

# ---- Variables económicas ----
print("\n=== ANÁLISIS DE VARIABLES ECONÓMICAS ===")
vars_economicas = ['euribor3m', 'cons.price.idx', 'cons.conf.idx', 'nr.employed', 'emp.var.rate']
vars_disponibles = [v for v in vars_economicas if v in df.columns]

print("\nEstadísticas de variables macroeconómicas:")
print(df[vars_disponibles].describe())

print("\nCorrelación de variables económicas con tasa de conversión:")
df_temp = df.copy()
df_temp['aceptacion'] = (df_temp['y'] == 'yes').astype(int)
print(df_temp[vars_disponibles + ['aceptacion']].corr()['aceptacion'].drop('aceptacion'))

# ---- Correlaciones generales ----
print("\n=== CORRELACIONES ===")
columnas_numericas = ['age', 'duration', 'campaign', 'previous'] + vars_disponibles
columnas_disponibles = [c for c in columnas_numericas if c in df.columns]
print(df[columnas_disponibles].corr())

# ---- Merge con datos de clientes (Excel) ----
print("\n=== ANÁLISIS COMBINADO CON DATOS DE CLIENTES ===")

try:
    df_clientes = pd.read_csv(RUTA_CLIENTES)
    print(f"Clientes cargados: {len(df_clientes)} registros")

    # Hacer el merge usando el identificador común
    df_merged = pd.merge(df, df_clientes, left_on='id_', right_on='ID', how='inner')
    print(f"Registros tras el merge: {len(df_merged)}")

    if len(df_merged) > 0:
        # Análisis de Income
        print("\nIngreso promedio según respuesta:")
        print(df_merged.groupby('y')['Income'].agg(['mean', 'median', 'count']))

        # Hijos en casa
        print("\nPromedio de niños en casa según respuesta:")
        print(df_merged.groupby('y')['Kidhome'].mean())

        print("\nPromedio de adolescentes en casa según respuesta:")
        print(df_merged.groupby('y')['Teenhome'].mean())

        # Visitas web
        print("\nVisitas web mensuales según respuesta:")
        print(df_merged.groupby('y')['NumWebVisitsMonth'].agg(['mean', 'median']))

        # Antigüedad como cliente
        print("\nAntigüedad como cliente según respuesta:")
        df_merged['Dt_Customer'] = pd.to_datetime(df_merged['Dt_Customer'])
        fecha_referencia = df_merged['Dt_Customer'].max()
        df_merged['antiguedad_anios'] = (fecha_referencia - df_merged['Dt_Customer']).dt.days / 365
        print(df_merged.groupby('y')['antiguedad_anios'].agg(['mean', 'median', 'count']))
        print("\nNota: los clientes más nuevos tienden a aceptar más.")
        print("      Los que aceptaron llevan ~1 año como clientes vs ~1.7 años los que no aceptaron.")

        # Guardar el dataset combinado (con antigüedad ya calculada)
        df_merged.to_csv(RUTA_MERGED, index=False)
        print(f"\nDataset combinado guardado en: {RUTA_MERGED}")
    else:
        print("El merge no encontró coincidencias entre los IDs.")
        print("Comprueba que el campo 'id_' del CSV coincide con 'ID' del Excel.")

except FileNotFoundError:
    print("No se encontró el archivo de clientes. Ejecuta primero 02_limpieza.py.")

print("\n¡Análisis completado!")
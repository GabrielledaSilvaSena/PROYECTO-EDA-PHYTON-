"""
Visualizaciones de los datos
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# Cargar datos limpios
print("Cargando datos...")
df = pd.read_csv('DATA/PROCESSED/bank_cleaned.csv')
print(f"Datos cargados: {df.shape[0]} filas")

# Crear carpeta para guardar las gráficas
import os
if not os.path.exists('DATA/PROCESSED/graficas'):
    os.makedirs('DATA/PROCESSED/graficas')
    print("Carpeta 'graficas' creada")

# 1. Distribución de la variable objetivo
print("\nCreando gráfica 1: Distribución variable objetivo...")
plt.figure(figsize=(8, 6))
df['y'].value_counts().plot(kind='bar', color=['salmon', 'lightblue'])
plt.title('Distribución de Respuestas (Sí/No)', fontsize=14, fontweight='bold')
plt.xlabel('Respuesta')
plt.ylabel('Número de clientes')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('DATA/PROCESSED/graficas/01_distribucion_objetivo.png')
plt.close()
print("✓ Guardada: 01_distribucion_objetivo.png")

# 2. Distribución de edad
print("\nCreando gráfica 2: Distribución de edad...")
plt.figure(figsize=(10, 6))
plt.hist(df['age'], bins=30, color='skyblue', edgecolor='black')
plt.title('Distribución de Edad de los Clientes', fontsize=14, fontweight='bold')
plt.xlabel('Edad')
plt.ylabel('Frecuencia')
plt.axvline(df['age'].mean(), color='red', linestyle='--', label=f'Media: {df["age"].mean():.1f}')
plt.legend()
plt.tight_layout()
plt.savefig('DATA/PROCESSED/graficas/02_distribucion_edad.png')
plt.close()
print("✓ Guardada: 02_distribucion_edad.png")

# 3. Aceptación por tipo de trabajo
print("\nCreando gráfica 3: Aceptación por trabajo...")
tabla_trabajo = pd.crosstab(df['job'], df['y'], normalize='index') * 100
tabla_trabajo = tabla_trabajo.sort_values('yes', ascending=True)

plt.figure(figsize=(10, 8))
tabla_trabajo['yes'].plot(kind='barh', color='lightgreen')
plt.title('Tasa de Aceptación por Tipo de Trabajo', fontsize=14, fontweight='bold')
plt.xlabel('% de Aceptación')
plt.ylabel('Tipo de Trabajo')
plt.tight_layout()
plt.savefig('DATA/PROCESSED/graficas/03_aceptacion_trabajo.png')
plt.close()
print("✓ Guardada: 03_aceptacion_trabajo.png")

# 4. Aceptación por educación
print("\nCreando gráfica 4: Aceptación por educación...")
tabla_edu = pd.crosstab(df['education'], df['y'], normalize='index') * 100
tabla_edu = tabla_edu.sort_values('yes', ascending=False)

plt.figure(figsize=(10, 6))
tabla_edu['yes'].plot(kind='bar', color='coral')
plt.title('Tasa de Aceptación por Nivel Educativo', fontsize=14, fontweight='bold')
plt.xlabel('Nivel Educativo')
plt.ylabel('% de Aceptación')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('DATA/PROCESSED/graficas/04_aceptacion_educacion.png')
plt.close()
print("✓ Guardada: 04_aceptacion_educacion.png")

# 5. Duración de llamada según respuesta
print("\nCreando gráfica 5: Duración de llamada...")
plt.figure(figsize=(10, 6))
df.boxplot(column='duration', by='y', patch_artist=True)
plt.title('Duración de Llamada según Respuesta', fontsize=14, fontweight='bold')
plt.suptitle('')  # Quitar el título automático
plt.xlabel('Respuesta')
plt.ylabel('Duración (segundos)')
plt.tight_layout()
plt.savefig('DATA/PROCESSED/graficas/05_duracion_llamada.png')
plt.close()
print("✓ Guardada: 05_duracion_llamada.png")

# 6. Grupos de edad vs aceptación
print("\nCreando gráfica 6: Aceptación por grupos de edad...")
df['grupo_edad'] = pd.cut(df['age'], bins=[0, 30, 40, 50, 60, 100], 
                           labels=['<30', '30-40', '40-50', '50-60', '>60'])
tabla_edad = pd.crosstab(df['grupo_edad'], df['y'], normalize='index') * 100

plt.figure(figsize=(10, 6))
tabla_edad.plot(kind='bar', stacked=False, color=['salmon', 'lightgreen'])
plt.title('Distribución de Respuestas por Grupo de Edad', fontsize=14, fontweight='bold')
plt.xlabel('Grupo de Edad')
plt.ylabel('Porcentaje (%)')
plt.legend(['No', 'Sí'], title='Respuesta')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('DATA/PROCESSED/graficas/06_edad_vs_respuesta.png')
plt.close()
print("✓ Guardada: 06_edad_vs_respuesta.png")

# 7. Estado civil
print("\nCreando gráfica 7: Distribución por estado civil...")
plt.figure(figsize=(8, 6))
df['marital'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['lightblue', 'lightcoral', 'lightgreen', 'yellow'])
plt.title('Distribución por Estado Civil', fontsize=14, fontweight='bold')
plt.ylabel('')
plt.tight_layout()
plt.savefig('DATA/PROCESSED/graficas/07_estado_civil.png')
plt.close()
print("✓ Guardada: 07_estado_civil.png")

# 8. Contactos vs aceptación
print("\nCreando gráfica 8: Número de contactos...")
df_contactos = df[df['campaign'] <= 10]  # Filtrar para mejor visualización
plt.figure(figsize=(10, 6))
tabla_contactos = pd.crosstab(df_contactos['campaign'], df_contactos['y'], normalize='index') * 100
tabla_contactos['yes'].plot(kind='line', marker='o', color='green', linewidth=2)
plt.title('Tasa de Aceptación según Número de Contactos', fontsize=14, fontweight='bold')
plt.xlabel('Número de Contactos')
plt.ylabel('% de Aceptación')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('DATA/PROCESSED/graficas/08_contactos_vs_aceptacion.png')
plt.close()
print("✓ Guardada: 08_contactos_vs_aceptacion.png")

# 9. Correlación entre variables numéricas
print("\nCreando gráfica 9: Matriz de correlación...")
columnas_num = ['age', 'duration', 'campaign', 'previous']
correlacion = df[columnas_num].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(correlacion, annot=True, cmap='coolwarm', center=0, square=True, linewidths=1)
plt.title('Correlación entre Variables Numéricas', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('DATA/PROCESSED/graficas/09_correlacion.png')
plt.close()
print("✓ Guardada: 09_correlacion.png")

# 10. Préstamos vs aceptación
print("\nCreando gráfica 10: Préstamos vs aceptación...")
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Hipoteca
tabla_housing = pd.crosstab(df['housing'], df['y'], normalize='index') * 100
tabla_housing.plot(kind='bar', ax=axes[0], color=['salmon', 'lightgreen'])
axes[0].set_title('Aceptación según Préstamo Hipotecario', fontweight='bold')
axes[0].set_xlabel('Tiene Hipoteca (0=No, 1=Sí)')
axes[0].set_ylabel('Porcentaje (%)')
axes[0].set_xticklabels(['No', 'Sí'], rotation=0)
axes[0].legend(['No acepta', 'Acepta'])

# Otro préstamo
tabla_loan = pd.crosstab(df['loan'], df['y'], normalize='index') * 100
tabla_loan.plot(kind='bar', ax=axes[1], color=['salmon', 'lightgreen'])
axes[1].set_title('Aceptación según Otro Préstamo', fontweight='bold')
axes[1].set_xlabel('Tiene Préstamo (0=No, 1=Sí)')
axes[1].set_ylabel('Porcentaje (%)')
axes[1].set_xticklabels(['No', 'Sí'], rotation=0)
axes[1].legend(['No acepta', 'Acepta'])

plt.tight_layout()
plt.savefig('DATA/PROCESSED/graficas/10_prestamos_vs_aceptacion.png')
plt.close()
print("✓ Guardada: 10_prestamos_vs_aceptacion.png")

print("\n" + "="*50)
print("✓ ¡Todas las visualizaciones creadas exitosamente!")
print(f"✓ Total: 10 gráficas guardadas en: DATA/PROCESSED/graficas/")
print("="*50)
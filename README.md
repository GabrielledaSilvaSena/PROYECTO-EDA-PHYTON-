# Proyecto EDA - Marketing Bancario

## Descripción

Este proyecto es un análisis exploratorio de datos (EDA) de campañas de marketing telefónico de un banco portugués. Las campañas intentaban vender depósitos a plazo a través de llamadas.

El objetivo es aplicar lo aprendido en el módulo "Python for Data" haciendo limpieza de datos, análisis descriptivo y visualizaciones para identificar qué factores influyen en que los clientes acepten o no el producto.

## Objetivos

- Limpiar y transformar los datos
- Hacer análisis estadístico descriptivo
- Identificar factores que influyen en la conversión
- Crear visualizaciones claras
- Documentar el proceso

## Estructura del Proyecto

```
PROYECTO-EDA-PHYTON/
│
├── .gitignore
├── README.md
│
├── DATA/
│   ├── RAW/
│   │   ├── bank-additional.csv
│   │   └── customer-details.xlsx
│   │
│   └── PROCESSED/
│       ├── bank_cleaned.csv
│       └── graficas/
│           ├── 01_distribucion_objetivo.png
│           ├── 02_distribucion_edad.png
│           └── ... (10 gráficos)
│
└── scripts/
    ├── 01_exploracion.py
    ├── 02_limpieza.py
    ├── 03_analisis.py
    └── 04_visualizacion.py
```

## Tecnologías

- Python 3
- Pandas (manipulación de datos)
- NumPy (operaciones numéricas)
- Matplotlib (gráficos)
- Seaborn (visualizaciones estadísticas)

## Los Datos

### bank-additional.csv (43,000 registros)

Información de las campañas de marketing:

| Variable | Descripción |
|----------|-------------|
| age | Edad del cliente |
| job | Profesión |
| marital | Estado civil |
| education | Nivel educativo |
| default | Historial de impagos (1: Sí, 0: No) |
| housing | Préstamo hipotecario (1: Sí, 0: No) |
| loan | Préstamo personal (1: Sí, 0: No) |
| contact | Método de contacto |
| duration | Duración de la llamada (segundos) |
| campaign | Número de contactos en esta campaña |
| pdays | Días desde el último contacto |
| previous | Contactos previos |
| poutcome | Resultado de campaña anterior |
| y | Variable objetivo: ¿Suscribió? (yes/no) |

### customer-details.xlsx

Información demográfica de clientes (3 hojas: 2012, 2013, 2014):

| Variable | Descripción |
|----------|-------------|
| Income | Ingreso anual |
| Kidhome | Número de niños |
| Teenhome | Número de adolescentes |
| Dt_Customer | Fecha de alta |
| NumWebVisitsMonth | Visitas mensuales al sitio web |
| ID | Identificador único |

## Instalación

Instalar las librerías necesarias:

```bash
pip install pandas numpy matplotlib seaborn openpyxl
```

## Cómo ejecutar

Los scripts se ejecutan en orden:

```bash
python scripts/01_exploracion.py
python scripts/02_limpieza.py
python scripts/03_analisis.py
python scripts/04_visualizacion.py
```

**Importante:** Hay que ejecutarlos en orden porque cada uno usa los resultados del anterior.

## Proceso de Análisis

### Script 1: Exploración (01_exploracion.py)

Primera exploración de los datos:
- Cargar los datasets
- Ver estructura y tipos de datos
- Identificar valores faltantes
- Estadísticas básicas
- Ver distribuciones de variables categóricas

Principales observaciones: El dataset tiene 43,000 registros con 24 columnas. Hay bastantes valores nulos y la variable objetivo está muy desbalanceada (88.7% "no", 11.3% "yes").

### Script 2: Limpieza (02_limpieza.py)

Limpieza y preparación de datos:

**Lo que hice:**
- Eliminé la columna duplicada (Unnamed: 0)
- Convertí todo el texto a minúsculas para estandarizar
- Rellené los valores nulos:
  - age: con la mediana (38 años)
  - job, education, marital: con 'unknown'
  - default, housing, loan: con 0 (asumo que si es nulo = no tiene)
- Verifiqué que no hubiera duplicados

Resultado: Dataset limpio guardado en DATA/PROCESSED/bank_cleaned.csv con 43,000 registros y 23 columnas.

### Script 3: Análisis (03_analisis.py)

Análisis estadístico de los datos. Hice análisis de:
- Distribución de la variable objetivo
- Grupos de edad
- Tipos de trabajo
- Estado civil
- Nivel educativo
- Préstamos (hipotecarios y personales)
- Duración de llamadas
- Número de contactos
- Correlaciones entre variables numéricas

Usé tablas cruzadas (pd.crosstab) y agrupaciones con pd.cut para hacer los análisis.

### Script 4: Visualizaciones (04_visualizacion.py)

Creé 10 gráficos para visualizar los hallazgos:

1. Distribución de respuestas (barras)
2. Distribución de edad (histograma)
3. Aceptación por trabajo (barras horizontales)
4. Aceptación por educación (barras)
5. Duración de llamada vs respuesta (boxplot)
6. Grupos de edad vs respuesta (barras agrupadas)
7. Distribución por estado civil (pie chart)
8. Número de contactos vs aceptación (línea)
9. Matriz de correlación (heatmap)
10. Préstamos vs aceptación (subplots)

Los gráficos se guardan en DATA/PROCESSED/graficas/

## Resultados

### Métricas generales

- Tasa de conversión: 11.3% (4,844 clientes aceptaron)
- Tasa de rechazo: 88.7% (38,156 clientes)
- Duración promedio de llamadas: 258 segundos
- Edad promedio: 39.74 años
- Número promedio de contactos: 2.57

### Hallazgos principales

**Por edad:**
Los mayores de 60 años son los que más aceptan (44.8%), seguidos por los menores de 30 (15%). Los grupos intermedios (30-60 años) tienen tasas más bajas (8-11%).

**Por profesión:**
Los que más aceptan son:
- Estudiantes: 31.3%
- Jubilados: 25.2%
- Desempleados: 14.4%

Los que menos:
- Blue-collar: 6.9%
- Servicios: 8.1%

**Duración de llamada:**
Este es un factor muy importante. Las llamadas que resultan en aceptación duran mucho más:
- Clientes que aceptaron: 553 segundos promedio
- Clientes que rechazaron: 221 segundos promedio

**Número de contactos:**
Encontré un patrón claro: menos contactos = mejor resultado
- 1 contacto: ~15% acepta
- 2-3 contactos: ~10% acepta  
- Más de 3 contactos: ~5% acepta

**Estado civil:**
Los solteros (13.9%) aceptan un poco más que los casados (10.2%) o divorciados (10.2%).

**Préstamos:**
Los clientes sin préstamos activos (ni hipotecarios ni personales) tienen más disposición a aceptar el producto.

## Conclusiones

La duración de la llamada es el factor más importante que encontré. Las llamadas exitosas duran 2.5 veces más que las que no funcionan.

**Perfil del cliente que más acepta:**
- Edad: mayor de 60 o menor de 30
- Ocupación: estudiante o jubilado
- Sin préstamos activos
- Primera o segunda llamada

**Insight clave:** Llamar varias veces al mismo cliente es contraproducente. La primera llamada es la que tiene más probabilidad de éxito.

### Posibles aplicaciones

Basándome en los hallazgos, se podría:
- Priorizar contactos iniciales (no insistir tanto)
- Enfocarse en mayores de 60 y estudiantes
- Invertir en llamadas más largas y de calidad
- Filtrar clientes sin compromisos financieros

### Limitaciones

- Los datos son históricos de un solo banco
- La variable objetivo está muy desbalanceada (88.7% vs 11.3%)
- No tengo información del contenido de las llamadas
- Algunas variables económicas tienen nulos que no rellené

### Mejoras posibles

- Usar técnicas de balanceo de datos (SMOTE, undersampling)
- Probar modelos predictivos de machine learning
- Incluir más variables de comportamiento digital
- Analizar el contenido de las llamadas

## Lo que aprendí

Durante este proyecto aprendí varias cosas:

Al principio me costó decidir cómo manejar los valores nulos. Tuve que pensar qué tenía más sentido para cada variable (usar mediana, usar 'unknown', o poner 0).

Las visualizaciones fueron más complicadas de lo que pensaba. Tuve que probar varias opciones hasta encontrar las que mostraban mejor los patrones.

También fue difícil decidir qué analizar y qué no. Hay tantas variables que podría haber hecho muchos más análisis, pero traté de enfocarme en lo más relevante.

Lo más interesante fue descubrir el patrón de la duración de llamada y el número de contactos. No esperaba que fueran factores tan importantes.

### Principales desafíos

- Decidir cómo tratar cada tipo de valor nulo
- Elegir qué visualizaciones usar
- Manejar el desbalance de la variable objetivo
- No sobre-analizar y mantener el foco

## Autor

Gabrielle da Silva Sena
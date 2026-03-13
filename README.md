# Proyecto EDA - Marketing Bancario

## Descripción

Este proyecto es un análisis exploratorio de datos (EDA) de campañas de marketing telefónico de un banco portugués. Las campañas intentaban vender depósitos a plazo a través de llamadas.

El objetivo es aplicar lo aprendido en el módulo "Python for Data" haciendo limpieza de datos, análisis descriptivo y visualizaciones para identificar qué factores influyen en que los clientes acepten o no el producto.

---

## Objetivos

- Limpiar y transformar los datos
- Hacer análisis estadístico descriptivo
- Identificar factores que influyen en la conversión
- Crear visualizaciones claras
- Documentar el proceso

---

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
│       ├── customer_cleaned.csv
│       ├── bank_merged.csv
│       └── graficas/
│           ├── 01_distribucion_objetivo.png
│           ├── 02_distribucion_edad.png
│           └── ... (12 gráficos)
│
└── scripts/
    ├── 01_exploracion.py
    ├── 02_limpieza.py
    ├── 03_analisis.py
    └── 04_visualizacion.py
```

---

## Tecnologías

- Python 3
- Pandas (manipulación de datos)
- Matplotlib (gráficos)
- Seaborn (visualizaciones estadísticas)
- OpenPyXL (lectura de archivos Excel)

---

## Los Datos

### bank-additional.csv (43,000 registros)

Información de las campañas de marketing:

| Variable | Descripción |
|---|---|
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
| euribor3m | Tasa Euribor a 3 meses |
| cons.price.idx | Índice de precios al consumidor |
| cons.conf.idx | Índice de confianza del consumidor |
| nr.employed | Número de empleados |
| y | Variable objetivo: ¿Suscribió? (yes/no) |

### customer-details.xlsx

Información demográfica de clientes (3 hojas: 2012, 2013, 2014):

| Variable | Descripción |
|---|---|
| Income | Ingreso anual |
| Kidhome | Número de niños |
| Teenhome | Número de adolescentes |
| Dt_Customer | Fecha de alta |
| NumWebVisitsMonth | Visitas mensuales al sitio web |
| ID | Identificador único |

---

## Instalación

```bash
pip install pandas matplotlib seaborn openpyxl
```

---

## Cómo ejecutar

Los scripts se ejecutan en orden, ya que cada uno usa los resultados del anterior:

```bash
python scripts/01_exploracion.py
python scripts/02_limpieza.py
python scripts/03_analisis.py
python scripts/04_visualizacion.py
```

---

## Proceso de Análisis

### Script 1: Exploración (`01_exploracion.py`)

Primera exploración de los datos:
- Cargar los datasets
- Ver estructura y tipos de datos
- Identificar valores faltantes
- Estadísticas básicas
- Ver distribuciones de variables categóricas

**Observaciones iniciales:** El dataset tiene 43,000 registros con 24 columnas. Hay valores nulos en varias columnas y la variable objetivo está muy desbalanceada (88.7% "no", 11.3% "yes").

---

### Script 2: Limpieza (`02_limpieza.py`)

Limpieza y preparación de datos:

**Lo que hice:**

- Eliminé la columna duplicada (`Unnamed: 0`)
- Verifiqué duplicados: no se encontró ninguno (documentado en el script)
- Convertí texto a minúsculas para estandarizar
- Rellené los valores nulos:
  - `age`: con la mediana (38 años), porque es menos sensible a outliers que la media
  - `job`, `education`, `marital`: con `'unknown'` para no inventar categorías
  - `default`, `housing`, `loan`: con `0` y convertidas a `int` (variables binarias)
- Corregí columnas numéricas que venían con coma decimal (`euribor3m`, `cons.price.idx`, `cons.conf.idx`, `nr.employed`): reemplacé la coma por punto y convertí a `float`
- Combiné las 3 hojas del Excel en un solo DataFrame de clientes

**Nulos que se dejaron sin imputar:**

La columna `date` no se usa en el análisis principal, por lo que sus nulos se dejan tal cual. Las variables económicas pueden conservar algún NaN tras la conversión decimal si el valor original no era numérico; no se imputan porque son indicadores macroeconómicos que requieren datos reales, no estimaciones.

**Resultado:** Dataset limpio guardado en `DATA/PROCESSED/bank_cleaned.csv` con 43,000 registros y 23 columnas.

---

### Script 3: Análisis (`03_analisis.py`)

Análisis estadístico de los datos. Incluye una función reutilizable `tasa_aceptacion(df, columna)` que calcula el porcentaje de aceptación y el número de registros (n) por categoría.

Se analizaron:
- Distribución de la variable objetivo
- Grupos de edad
- Tipos de trabajo
- Estado civil
- Nivel educativo
- Préstamos (hipotecarios y personales)
- Duración de llamadas
- Número de contactos
- Variables económicas (euribor3m, índices de precios y confianza)
- Correlaciones entre variables numéricas
- **Análisis combinado** con `customer-details.xlsx` (merge por ID), analizando ingreso, hijos en casa, visitas web y antigüedad como cliente (`Dt_Customer`)

---

### Script 4: Visualizaciones (`04_visualizacion.py`)

Se crearon 12 gráficos:
1. Distribución de respuestas (barras)
2. Distribución de edad (histograma)
3. Aceptación por trabajo (barras horizontales)
4. Aceptación por educación (barras)
5. Duración de llamada vs respuesta (boxplot)
6. Grupos de edad vs respuesta (barras agrupadas)
7. Distribución por estado civil (pie chart)
8. Número de contactos vs aceptación (línea)
9. Matriz de correlación ampliada (heatmap, incluye variables económicas)
10. Préstamos vs aceptación (subplots)
11. **Ingreso anual vs aceptación** (boxplot, datos del Excel combinados)
12. **Antigüedad como cliente vs aceptación** (boxplot, datos del Excel combinados)

Todos los gráficos se guardan en `DATA/PROCESSED/graficas/` con resolución 150 dpi.

---

## Resultados

### Métricas generales

- **Tasa de conversión:** 11.3% (4,844 clientes aceptaron)
- **Tasa de rechazo:** 88.7% (38,156 clientes)
- **Duración promedio de llamadas:** 258 segundos
- **Edad promedio:** 39.74 años
- **Número promedio de contactos:** 2.57

### Hallazgos principales

**Por edad:** Los mayores de 60 años tienen la tasa de aceptación más alta (44.8%), seguidos por los menores de 30 (15%). Los grupos intermedios (30-60 años) se mueven entre 8% y 11%. *Nota: el grupo >60 tiene menos registros que el resto, hay que interpretar este porcentaje con cautela.*

**Por profesión:** Los que más aceptan son estudiantes (31.3%) y jubilados (25.2%). Los que menos aceptan son blue-collar (6.9%) y servicios (8.1%). Estas diferencias son accionables para segmentar la campaña.

**Duración de llamada:** Es el factor más diferenciador del dataset. Las llamadas que resultan en aceptación duran en promedio 553 segundos, frente a 221 segundos en los rechazos (2.5x más).

**Número de contactos:** Patrón claro de fatiga de contacto. La tasa de aceptación cae progresivamente: ~15% en el primer contacto, ~10% en el segundo o tercero, y ~5% con más de 3 contactos.

**Estado civil:** Los solteros aceptan algo más (13.9%) que los casados o divorciados (10.2% ambos).

**Préstamos:** Los clientes sin préstamos activos tienen mayor disposición a aceptar. La diferencia no es muy grande pero es consistente.

**Variables económicas:** Tras corregir los tipos de dato, fue posible analizar euribor3m y los índices de precios y confianza. El euribor3m muestra correlación negativa con la aceptación: en momentos de tipos más bajos, la gente tiende más a contratar depósitos.

**Datos del Excel (merge):** Al combinar con `customer-details.xlsx`, se observa que las diferencias entre los grupos "yes" y "no" en Income, Kidhome, Teenhome y NumWebVisitsMonth son muy pequeñas y no permiten sacar conclusiones claras. El ingreso medio es prácticamente igual en ambos grupos (~93,000 € en rechazos vs ~92,500 € en aceptaciones).

**Antigüedad como cliente:** Este es uno de los hallazgos más interesantes del merge. Los clientes que aceptaron el producto llevaban como media ~1 año en el banco, frente a ~1.7 años los que rechazaron. Los clientes más nuevos parecen más receptivos a contratar depósitos a plazo.

---

## Conclusiones

La duración de la llamada es el factor más importante. Las llamadas exitosas duran 2.5 veces más.

**Perfil del cliente que más acepta:**
- Edad: mayor de 60 o menor de 30
- Ocupación: estudiante o jubilado
- Sin préstamos activos
- Primera o segunda llamada
- Entorno económico de tipos bajos (euribor bajo)
- Cliente relativamente nuevo en el banco (menos de 1 año)

**Insight clave:** Llamar varias veces al mismo cliente es contraproducente. La primera llamada es la que tiene más probabilidad de éxito.

---

## Limitaciones

- Los datos son históricos de un solo banco portugués
- La variable objetivo está muy desbalanceada (88.7% vs 11.3%)
- No hay información del contenido de las llamadas
- Algunas columnas con nulos no se imputaron porque no tienen sustituto lógico
- Categorías con pocos registros (como `illiterate`) pueden dar porcentajes engañosos

---

## Mejoras posibles

- Usar técnicas de balanceo de datos (SMOTE, undersampling) antes de modelar
- Probar modelos predictivos de machine learning
- Analizar la variable `date` para ver estacionalidad
- Incluir más variables del comportamiento digital

---

## Lo que aprendí

Al principio me costó decidir cómo manejar los valores nulos. Tuve que pensar qué tenía más sentido para cada variable: usar mediana para edad, `unknown` para categóricas, o 0 para las binarias. También aprendí que algunas columnas que parecían numéricas en realidad eran texto porque usaban coma como separador decimal, y eso hacía que pandas no las pudiera analizar bien hasta convertirlas.

Las visualizaciones fueron más complicadas de lo que pensaba. Tuve que probar varias opciones para encontrar las que mejor mostraban los patrones.

Lo más interesante fue descubrir el patrón de la duración de llamada y el de la fatiga de contacto. Y al hacer el merge con el Excel, me sorprendió descubrir que la antigüedad como cliente sí marca diferencia: los clientes más nuevos aceptan bastante más que los que llevan más tiempo en el banco. El ingreso en cambio no diferencia mucho entre los dos grupos, lo que también es un resultado válido.

---

## Autor

Gabrielle da Silva Sena

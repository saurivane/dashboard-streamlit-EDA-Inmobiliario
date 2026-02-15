# Dashboard Power BI - Propiedades Inmobiliarias Madrid

## Archivos Generados

Se ha generado el archivo `powerbi_dashboard/datos_dashboard.xlsx` con todas las hojas de datos necesarias para crear el dashboard.

## Instrucciones para Power BI Desktop

### 1. Importar Datos

1. Abrir Power BI Desktop
2. Ir a **Obtener datos** > **Excel**
3. Seleccionar el archivo `powerbi_dashboard/datos_dashboard.xlsx`
4. Seleccionar todas las hojas y hacer clic en **Cargar**

### 2. Crear Visualizaciones

#### Página 1: Visión General

| Visualización | Tipo | Origen de Datos |
|---------------|------|-----------------|
| Total Propiedades | Card | Metricas (Total Propiedades) |
| Precio Medio | Card | Metricas (Precio Medio) |
| Precio m² Medio | Card | Metricas (Precio m2 Medio) |
| Metros Medios | Card | Metricas (Metros Medios) |
| Distribución de Precios | Histogram | Datos_Originales (precio) |
| Distribución de Metros | Histogram | Datos_Originales (metros) |
| Precio por Habitaciones | Box Plot | Datos_Originales |
| Distribución Habitaciones | Pie Chart | Distribucion_Habitaciones |
| Particular vs Agencia | Pie Chart | Distribucion_Vendedor |
| Precio Medio por Vendedor | Bar Chart | Precio_Vendedor |

#### Página 2: Análisis

| Visualización | Tipo | Origen de Datos |
|---------------|------|-----------------|
| Matriz de Correlación | Matrix | Correlaciones |
| Precio vs Metros | Scatter | Datos_Originales |
| Precio Medio por Hab. | Bar Chart | Precio_Habitaciones |
| Precio m² por Hab. | Bar Chart | Precio_m2_Habitacion |

#### Página 3: Detalles por Ubicación

| Visualización | Tipo | Origen de Datos |
|---------------|------|-----------------|
| Propiedades por Ubicación | Bar Chart (Horizontal) | Precio_Ubicacion |
| Precio Medio por Ubicación | Bar Chart (Horizontal) | Precio_Ubicacion |
| Precio m² por Ubicación | Bar Chart (Horizontal) | Precio_m2_Ubicacion |
| Distribución Ascensor | Pie Chart | Distribucion_Ascensor |
| Tipo de Planta | Bar Chart | Distribucion_Planta |
| Precio vs Planta | Scatter | Datos_Originales |

#### Página 4: Datos

| Visualización | Tipo | Origen de Datos |
|---------------|------|-----------------|
| Tabla de Datos | Table | Datos_Originales |
| Top 10 Caras | Table | Top_Caras |
| Top 10 Económicas | Table | Top_Economicas |

#### Página 5: Conclusiones

| Visualización | Tipo | Origen de Datos |
|---------------|------|-----------------|
| KPIs Principales | Cards | Metricas |
| Comparativa Vendedor | Bar Chart | Precio_Vendedor |
| Distribución Habitaciones | Bar Chart | Distribucion_Habitaciones |

### 3. Filtros Globales

Crear slicers (segmentadores) con:
- **Rango de Precio**: Datos_Originales > precio (entre min y max)
- **Rango de Metros**: Datos_Originales > metros (entre min y max)
- **Habitaciones**: Datos_Originales > habitaciones
- **Ubicación**: Datos_Originales > ubicacion
- **Tipo de Vendedor**: Datos_Originales > vendedor

Aplicar estos slicers como filtros a nivel de página o informe.

### 4. Medidas DAX Recomendadas

```DAX
// Precio Medio
Precio Medio = AVERAGE(Datos_Originales[precio])

// Precio m² Medio
Precio m2 Medio = AVERAGE(Datos_Originales[precio_m2])

// Metros Medios
Metros Medios = AVERAGE(Datos_Originales[metros])

// Total Propiedades
Total Propiedades = COUNTROWS(Datos_Originales)

// Conteo Particular
Particulares = CALCULATE(COUNTROWS(Datos_Originales), Datos_Originales[vendedor] = "Particular")

// Conteo Agencia
Agencias = CALCULATE(COUNTROWS(Datos_Originales), Datos_Originales[vendedor] = "Agencia")
```

### 5. Colores (Igual que Streamlit)

- Primary: #4CAF50 (Verde)
- Secondary: #2196F3 (Azul)
- Light: #E8F5E9 (Verde claro)
- Background: #FFFFFF

### Estructura de Carpetas Recomendada

```
powerbi_dashboard/
├── datos_dashboard.xlsx    (datos listos para importar)
├── Dashboard_PBI_Guia.md  (este archivo)
└── (archivos .pbix se crean en Power BI Desktop)
```

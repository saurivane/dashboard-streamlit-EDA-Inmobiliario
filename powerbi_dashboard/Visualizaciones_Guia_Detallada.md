# Guía de Visualizaciones - Dashboard Power BI

## Datos Importados (14 hojas)

| Hoja | Descripción |
|------|-------------|
| Datos_Originales | Datos completos con precio_m2 calculado |
| Metricas | KPIs principales |
| Precio_Habitaciones | Precio medio por habitaciones |
| Distribucion_Habitaciones | Conteo por habitaciones |
| Precio_Ubicacion | Precio medio por ubicación |
| Precio_Vendedor | Precio medio por tipo vendedor |
| Distribucion_Vendedor | Conteo Particular vs Agencia |
| Distribucion_Ascensor | Conteo con/sin ascensor |
| Precio_m2_Habitacion | Precio m² medio por habitaciones |
| Precio_m2_Ubicacion | Precio m² medio por ubicación |
| Distribucion_Planta | Top 10 tipos de planta |
| Correlaciones | Matriz de correlación |
| Top_Caras | Top 10 propiedades más caras |
| Top_Economicas | Top 10 propiedades más económicas |

---

## PÁGINA 1: Visión General

### Fila 1: KPIs (Cards)
| Visual | Tabla | Campo |
|--------|-------|-------|
| Card: Total Propiedades | Metricas | Total Propiedades |
| Card: Precio Medio | Metricas | Precio Medio |
| Card: Precio m² Medio | Metricas | Precio m2 Medio |
| Card: Metros Medios | Metricas | Metros Medios |
| Card: Particulares | Metricas | Particulares |
| Card: Agencias | Metricas | Agencias |

### Fila 2: Gráficos
| Visual | Tipo | Ejes |
|--------|------|------|
| Histograma Precios | Histogram | Datos_Originales > precio |
| Histograma Metros | Histogram | Datos_Originales > metros |

### Fila 3: Distribución
| Visual | Tipo | Valores |
|--------|------|---------|
| Dist. Habitaciones | Pie/Donut | Categoría: Habitaciones, Valores: Conteo |
| Particular vs Agencia | Pie/Donut | Categoría: Vendedor, Valores: Conteo |

### Fila 4: Comparativa
| Visual | Tipo | Ejes |
|--------|------|------|
| Precio por Vendedor | Bar Horizontal | Eje X: Precio_Medio, Eje Y: Vendedor |

---

## PÁGINA 2: Análisis

| Visual | Tipo | Configuración |
|--------|------|---------------|
| Matriz Correlación | Table/Matrix | Filas: Variable1, Columnas: Variable2, Valores: Correlacion |
| Scatter Precio-Metros | Scatter | X: metros, Y: precio, Color: habitaciones |
| Bar Precio Habitaciones | Bar | Eje X: Habitaciones, Eje Y: Precio_Medio |
| Bar Precio m² Hab. | Bar | Eje X: Habitaciones, Eje Y: Precio_m2_Medio |

---

## PÁGINA 3: Detalles

| Visual | Tipo | Configuración |
|--------|------|---------------|
| Propiedades Ubicación | Bar Horizontal | Eje X: Conteo, Eje Y: Ubicacion (ordenar por Conteo) |
| Precio Medio Ubicación | Bar Horizontal | Eje X: Precio_Medio, Eje Y: Ubicacion |
| Precio m² Ubicación | Bar Horizontal | Eje X: Precio_m2_Medio, Eje Y: Ubicacion |
| Dist. Ascensor | Pie | Categoría: Ascensor, Valores: Conteo |
| Tipo Planta | Bar Horizontal | Eje X: Conteo, Eje Y: Planta |
| Scatter Planta-Precio | Scatter | X: numero_planta, Y: precio |

---

## PÁGINA 4: Datos

| Visual | Tipo | Tabla |
|--------|------|-------|
| Tabla Datos | Table | Datos_Originales |
| Top 10 Caras | Table | Top_Caras |
| Top 10 Económicas | Table | Top_Economicas |

---

## PÁGINA 5: Conclusiones

| Visual | Tipo | Configuración |
|--------|------|---------------|
| KPIs Resumen | Cards | Usar tabla Metricas |
| Comparativa Vendedor | Bar | Eje X: Vendedor, Eje Y: Precio_Medio |
| Dist. Habitaciones | Bar | Eje X: Habitaciones, Eje Y: Conteo |

---

## FILTROS (Slicers)

Crear los siguientes slicers en cada página (o como globales):

1. **Rango Precio**: Datos_Originales > precio (entre min y max)
2. **Rango Metros**: Datos_Originales > metros (entre min y max)
3. **Habitaciones**: Datos_Originales > habitaciones
4. **Ubicación**: Datos_Originales > ubicacion
5. **Vendedor**: Datos_Originales > vendedor

---

## Colores Recomendados

- Primary: #4CAF50 (Verde)
- Secondary: #2196F3 (Azul)  
- Background: White
- Text: #333333

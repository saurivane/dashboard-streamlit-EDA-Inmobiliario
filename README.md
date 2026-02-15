# Dashboard Inmobiliario Madrid

🔗 **Ver online:** https://dashboard-app-eda-inmobiliario.streamlit.app/

Dashboard interactivo para visualización y análisis exploratorio de datos de propiedades inmobiliarias en Madrid.

## 📊 Descripción

Este proyecto es un dashboard desarrollado con **Streamlit** que permite explorar datos de propiedades inmobiliarias de Madrid obtenidos de portales web. Incluye visualizaciones interactivas, filtros y métricas clave.

## 🛠️ Tecnologías

- **Streamlit** - Framework web para datos
- **Pandas** - Manipulación y análisis de datos
- **Plotly** - Gráficos interactivos

## 📁 Estructura

```
dashboard_ML/
├── analisis.csv        # Datos de propiedades
├── app.py              # Aplicación principal
├── requirements.txt    # Dependencias
├── .streamlit/
│   └── config.toml    # Configuración del tema
└── README.md          # Este archivo
```

## 🚀 Instalación

1. Clonar el repositorio:
```bash
git clone <repositorio>
cd dashboard_ML
```

2. Crear entorno virtual (opcional):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Ejecutar el dashboard:
```bash
streamlit run app.py
```

El dashboard se abrirá en: `http://localhost:8501`

## 🎨 Personalización

### Temas

Edita `.streamlit/config.toml` para cambiar el tema:

```toml
[theme]
base = "dark"
borderColor = "mediumSlateBlue"

[theme.sidebar]
showWidgetBorder = true
```

### Colores

Los colores principales se definen en `app.py`:
```python
COLORS = {
    'primary': '#4CAF50',
    'secondary': '#81C784',
    'accent': '#A5D6A7',
    ...
}
```

## 📱 Características

- **Filtros**: Precio, metros, habitaciones, ubicación
- **Métricas**: Total propiedades, precio medio, precio/m², metros medios
- **5 pestañas**:
  - Visión General: Histogramas y distribución
  - Análisis: Correlaciones y scatter plots
  - Detalles: Ubicación, ascensor, planta
  - Datos: Tabla de datos y estadísticas
  - Conclusiones: Resumen del análisis EDA

## 📄 Datos

El archivo `analisis.csv` contiene propiedades con los siguientes campos:
- `vendedor` - Particular o Agencia
- `precio` - Precio de venta
- `habitaciones` - Número de habitaciones
- `metros` - Metros cuadrados
- `planta` - Planta del edificio
- `garage` - Si tiene garaje
- `ascensor` - Si tiene ascensor
- `ubicacion` - Zona de Madrid
- `numero_planta` - Número de planta
- `valor_garage` - Valor del garaje
- `precio_total` - Precio total (incluyendo garaje)

## 📌 Requisitos

- Python 3.8+
- streamlit
- pandas
- plotly
- statsmodels (para trendlines)

## 📝 Licencia

MIT License

---

## 📊 Power BI Dashboard

Este proyecto también incluye un dashboard alternativo en **Power BI** con las mismas visualizaciones que el dashboard de Streamlit.

### Archivos

- `powerbi_dashboard/datos_dashboard.xlsx` - Datos procesados (14 hojas)
- `powerbi_dashboard/Dashboard_PBI_Guia.md` - Guía completa
- `powerbi_dashboard/Visualizaciones_Guia_Detallada.md` - Detalle de visualizaciones

### Datos Disponibles (14 hojas)

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

### Pasos para Crear el Dashboard

1. **Importar datos**: Abrir Power BI Desktop > Obtener datos > Excel > seleccionar `datos_dashboard.xlsx`

2. **Crear 5 páginas**:
   - **Visión General**: KPIs, histogramas, gráficos circulares
   - **Análisis**: Matriz correlación, scatter plots, barras
   - **Detalles**: Gráficos por ubicación y planta
   - **Datos**: Tablas de datos y top propiedades
   - **Conclusiones**: Resumen y comparativas

3. **Crear filtros (Slicers)**:
   - Rango de precio
   - Rango de metros
   - Habitaciones
   - Ubicación
   - Tipo de vendedor

4. **Medidas DAX recomendadas**:
```DAX
Total Propiedades = COUNTROWS(Datos_Originales)
Precio Medio = AVERAGE(Datos_Originales[precio])
Precio m2 Medio = AVERAGE(Datos_Originales[precio_m2])
Metros Medios = AVERAGE(Datos_Originales[metros])
```

### Colores

| Elemento | Color |
|----------|-------|
| Primary | #4CAF50 (Verde) |
| Secondary | #2196F3 (Azul) |
| Light | #E8F5E9 |
| Background | #FFFFFF |

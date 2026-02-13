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

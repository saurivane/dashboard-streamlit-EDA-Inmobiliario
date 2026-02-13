"""
Dashboard Inmobiliario de Madrid
Análisis exploratorio de datos de propiedades en venta
"""

# Importación de librerías necesarias
import streamlit as st  # Framework principal para crear la aplicación web
import pandas as pd     # Manipulación y análisis de datos
import plotly.express as px  # Creación de gráficos interactivos
from typing import Tuple  # Tipado para mejorar legibilidad

# Configuración inicial de la página de Streamlit
st.set_page_config(
    page_title="Dashboard Inmobiliario Madrid",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paleta de colores para mantener consistencia visual en los gráficos
# Colores basados en tonos verdes para dar sensación de naturaleza/vivienda
COLORS = {
    'primary': '#4CAF50',    # Verde principal
    'secondary': '#81C784',   # Verde secundario
    'accent': '#A5D6A7',      # Verde acento
    'light': '#C8E6C9',      # Verde claro
    'dark': '#1E1E1E',        # Negro oscuro para fondos
    'text': '#FFFFFF'        # Blanco para texto
}

# Estilos CSS personalizados para mejorar la apariencia del dashboard
# Se aplican estilos al título principal y subtítulo
st.markdown("""
    <style>
    .main-title {
        font-size: 42px !important;
        font-weight: bold;
        text-align: center;
        color: #4CAF50 !important;
        margin-bottom: 5px !important;
    }
    .subtitle {
        font-size: 18px !important;
        text-align: center;
        color: #AAAAAA !important;
        margin-bottom: 30px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Configuración de diseño para gráficos de barras y dispersión
# Define el estilo visual común para mantener coherencia
LAYOUT_OPTS = dict(
    paper_bgcolor='rgba(0,0,0,0)',       # Fondo transparente
    plot_bgcolor='rgba(0,0,0,0)',        # Fondo del gráfico transparente
    font=dict(color='#FFFFFF', size=12),# Fuente blanca
    title_font=dict(size=16, color='#FFFFFF'),# Título en blanco
    legend=dict(
        font=dict(color='#FFFFFF', size=11),
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(255,255,255,0.2)',
        borderwidth=1
    ),
    xaxis=dict(
        title_font=dict(color='#FFFFFF'),
        tickfont=dict(color='#CCCCCC'),
        gridcolor='rgba(255,255,255,0.1)'  # Grid sutil
    ),
    yaxis=dict(
        title_font=dict(color='#FFFFFF'),
        tickfont=dict(color='#CCCCCC'),
        gridcolor='rgba(255,255,255,0.1)'
    )
)

# Configuración específica para gráficos circulares (pie charts)
PIE_LAYOUT_OPTS = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#FFFFFF', size=12),
    title_font=dict(size=16, color='#FFFFFF'),
    legend=dict(
        font=dict(color='#FFFFFF', size=11),
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(255,255,255,0.2)',
        borderwidth=1
    )
)

# Configuración para mapas de correlación
CORR_LAYOUT_OPTS = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#FFFFFF', size=12),
    title_font=dict(size=16, color='#FFFFFF'),
    legend=dict(font=dict(color='#FFFFFF'))
)


# =============================================================================
# FUNCIONES DE CARGA Y PROCESAMIENTO DE DATOS
# =============================================================================

@st.cache_data(ttl=3600)
def load_data(csv_path: str) -> pd.DataFrame:
    """
    Carga los datos desde un archivo CSV.
    
    Args:
        csv_path: Ruta al archivo CSV con los datos de propiedades.
        
    Returns:
        DataFrame con los datos cargados.
        
    Nota:
        Utiliza @st.cache_data para evitar recargar los datos en cada interacción.
        El parámetro ttl=3600 indica que la caché expira después de 1 hora.
    """
    return pd.read_csv(csv_path)


@st.cache_data(ttl=3600)
def get_filter_options(df: pd.DataFrame) -> Tuple:
    """
    Extrae las opciones disponibles para los filtros basándose en los datos.
    
    Args:
        df: DataFrame con los datos de propiedades.
        
    Returns:
        Tupla con los valores mínimos/máximos de precio y metros,
        y listas de valores únicos para habitaciones, ubicaciones y vendedores.
    """
    return (
        int(df['precio'].min()),
        int(df['precio'].max()),
        int(df['metros'].min()),
        int(df['metros'].max()),
        sorted(df['habitaciones'].unique()),
        df['ubicacion'].dropna().unique(),
        df['vendedor'].unique()
    )


def apply_filters(
    df: pd.DataFrame,
    precio_range: Tuple[int, int],
    metros_range: Tuple[int, int],
    habitaciones: list,
    ubicaciones: list,
    vendedor: list
) -> pd.DataFrame:
    """
    Aplica filtros al DataFrame según los criterios seleccionados por el usuario.
    
    Args:
        df: DataFrame original con todos los datos.
        precio_range: Rango de precios (mínimo, máximo).
        metros_range: Rango de metros cuadrados (mínimo, máximo).
        habitaciones: Lista de habitaciones a incluir.
        ubicaciones: Lista de ubicaciones a incluir.
        vendedor: Lista de tipos de vendedor a incluir.
        
    Returns:
        DataFrame filtrado según los criterios especificados.
    """
    filtered = df[
        (df['precio'] >= precio_range[0]) & 
        (df['precio'] <= precio_range[1]) &
        (df['metros'] >= metros_range[0]) & 
        (df['metros'] <= metros_range[1])
    ]
    
    # Filtrar por número de habitaciones si se especificaron
    if habitaciones:
        filtered = filtered[filtered['habitaciones'].isin(habitaciones)]
    
    # Filtrar por ubicación si se especificaron
    if len(ubicaciones) > 0:
        filtered = filtered[filtered['ubicacion'].isin(ubicaciones)]
    
    # Filtrar por tipo de vendedor si se especificaron
    if vendedor:
        filtered = filtered[filtered['vendedor'].isin(vendedor)]
    
    return filtered


@st.cache_data
def calculate_metrics(_df: pd.DataFrame) -> Tuple:
    """
    Calcula métricas básicas del conjunto de datos filtrado.
    
    Args:
        _df: DataFrame con los datos filtrados.
        
    Returns:
        Tupla con (precio_medio, precio_por_m2, metros_medios).
    """
    precio_medio = _df['precio'].mean()
    precio_m2 = (_df['precio'] / _df['metros'].replace(0, 1)).mean()
    metros_medios = _df['metros'].mean()
    return precio_medio, precio_m2, metros_medios


@st.cache_data
def get_precio_m2(_df: pd.DataFrame) -> pd.DataFrame:
    """
    Añade una columna calculada con el precio por metro cuadrado.
    
    Args:
        _df: DataFrame con los datos de propiedades.
        
    Returns:
        DataFrame con la columna adicional 'precio_m2'.
    """
    df_copy = _df.copy()
    df_copy['precio_m2'] = df_copy['precio'] / df_copy['metros'].replace(0, 1)
    return df_copy


def get_grouped_stats(_df: pd.DataFrame) -> dict:
    """
    Calcula estadísticas agrupadas por diferentes categorías.
    
    Args:
        _df: DataFrame con los datos de propiedades.
        
    Returns:
        Diccionario con múltiples estadísticas agrupadas:
        - habitacion_count: Conteo por número de habitaciones
        - precio_hab: Precio medio por habitaciones
        - ubicacion_count: Top 10 ubicaciones por cantidad
        - precio_ubicacion: Top 10 precio medio por ubicación
        - ascensor_counts: Distribución de propiedades con/sin ascensor
        - planta_counts: Top 10 tipos de planta
        - vendedor_count: Conteo por tipo de vendedor
        - precio_vendedor: Precio medio por tipo de vendedor
        - precio_m2_vendedor: Precio m² medio por tipo de vendedor
    """
    precio_m2_df = _df.copy()
    precio_m2_df['precio_m2'] = precio_m2_df['precio'] / precio_m2_df['metros'].replace(0, 1)
    
    return {
        'habitacion_count': _df['habitaciones'].value_counts().sort_index(),
        'precio_hab': _df.groupby('habitaciones')['precio'].mean().reset_index(),
        'ubicacion_count': _df['ubicacion'].value_counts().head(10),
        'precio_ubicacion': _df.groupby('ubicacion')['precio'].mean().sort_values(ascending=False).head(10).reset_index(),
        'ascensor_counts': _df['ascensor'].value_counts(),
        'planta_counts': _df['planta'].value_counts().head(10),
        'vendedor_count': _df['vendedor'].value_counts(),
        'precio_vendedor': _df.groupby('vendedor')['precio'].mean().reset_index(),
        'precio_m2_vendedor': precio_m2_df.groupby('vendedor')['precio_m2'].mean().reset_index()
    }


# =============================================================================
# FUNCIONES DE RENDERIZADO DE LA INTERFAZ
# =============================================================================

# Cada función renderiza una sección o pestaña específica del dashboard

def render_metrics(filtered_df: pd.DataFrame):
    """
    Renderiza las métricas principales en la parte superior del dashboard.
    
    Muestra:
    - Total de propiedades filtradas
    - Precio medio
    - Precio por metro cuadrado
    - Metros cuadrados medios
    - Conteo de particulares y agencias
    """
    precio_medio, precio_m2, metros_medios = calculate_metrics(filtered_df)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🏠 Total Propiedades", f"{len(filtered_df):,}")
    col2.metric("💰 Precio Medio", f"€{precio_medio:,.0f}")
    col3.metric("📐 Precio m²", f"€{precio_m2:,.0f}")
    col4.metric("📏 Metros Medios", f"{metros_medios:.0f} m²")
    
    stats = get_grouped_stats(filtered_df)
    col5, col6 = st.columns(2)
    with col5:
        count_particular = stats['vendedor_count'].get('Particular', 0)
        st.metric("👤 Particulares", f"{count_particular}")
    with col6:
        count_agencia = stats['vendedor_count'].get('Agencia', 0)
        st.metric("🏢 Agencias", f"{count_agencia}")


def render_overview_tab(filtered_df: pd.DataFrame):
    """
    Pestaña 'Visión General': Muestra distribuciones generales de los datos.
    
    Gráficos incluidos:
    - Histograma de distribución de precios
    - Histograma de distribución de metros cuadrados
    - Boxplot de precio por habitaciones
    - Gráfico circular de distribución por habitaciones
    - Comparación particulares vs agencias
    """
    col_a, col_b = st.columns(2)
    
    with col_a:
        fig_hist = px.histogram(
            filtered_df, x="precio", nbins=25, 
            title="<b>Distribución de Precios</b>",
            color_discrete_sequence=[COLORS['primary']]
        )
        fig_hist.update_layout(**LAYOUT_OPTS)
        st.plotly_chart(fig_hist, width='stretch')
    
    with col_b:
        fig_hist_metros = px.histogram(
            filtered_df, x="metros", nbins=25, 
            title="<b>Distribución de Metros Cuadrados</b>",
            color_discrete_sequence=[COLORS['secondary']]
        )
        fig_hist_metros.update_layout(**LAYOUT_OPTS)
        st.plotly_chart(fig_hist_metros, width='stretch')

    col_c, col_d = st.columns(2)
    
    with col_c:
        fig_box = px.box(
            filtered_df, x="habitaciones", y="precio", 
            title="<b>Distribución de Precio por Habitaciones</b>",
            color_discrete_sequence=[COLORS['primary']]
        )
        fig_box.update_layout(**LAYOUT_OPTS)
        st.plotly_chart(fig_box, width='stretch')
    
    with col_d:
        stats = get_grouped_stats(filtered_df)
        fig_pie = px.pie(
            values=stats['habitacion_count'].values, 
            names=stats['habitacion_count'].index, 
            title="<b>Distribución por Habitaciones</b>",
            color_discrete_sequence=px.colors.sequential.Greens
        )
        fig_pie.update_layout(**PIE_LAYOUT_OPTS)
        st.plotly_chart(fig_pie, width='stretch')

    col_v1, col_v2 = st.columns(2)
    
    with col_v1:
        stats = get_grouped_stats(filtered_df)
        fig_vendedor = px.pie(
            values=stats['vendedor_count'].values,
            names=stats['vendedor_count'].index,
            title="<b>Particulares vs Agencias</b>",
            color_discrete_sequence=[COLORS['primary'], COLORS['secondary']]
        )
        fig_vendedor.update_layout(**PIE_LAYOUT_OPTS)
        st.plotly_chart(fig_vendedor, width='stretch')
    
    with col_v2:
        stats = get_grouped_stats(filtered_df)
        fig_precio_vendedor = px.bar(
            stats['precio_vendedor'], x="vendedor", y="precio",
            title="<b>Precio Medio: Particular vs Agencia</b>",
            color_discrete_sequence=[COLORS['primary'], COLORS['secondary']]
        )
        fig_precio_vendedor.update_layout(**LAYOUT_OPTS)
        st.plotly_chart(fig_precio_vendedor, width='stretch')


def render_analysis_tab(filtered_df: pd.DataFrame):
    """
    Pestaña 'Análisis': Muestra análisis estadísticos y correlaciones.
    
    Gráficos incluidos:
    - Matriz de correlación entre variables numéricas
    - Scatter plot de precio vs metros con línea de tendencia
    - Barras de precio medio por habitaciones
    - Barras de precio m² medio por habitaciones
    """
    col_e, col_f = st.columns(2)
    
    with col_e:
        df_corr = filtered_df[['precio', 'habitaciones', 'metros', 'numero_planta']].dropna()
        if len(df_corr) > 1:
            corr_matrix = df_corr.corr()
            fig_corr = px.imshow(
                corr_matrix, text_auto=True, 
                title="<b>Matriz de Correlación</b>",
                color_continuous_scale="Greens"
            )
            fig_corr.update_layout(**CORR_LAYOUT_OPTS)
            st.plotly_chart(fig_corr, width='stretch')
    
    with col_f:
        df_scatter = filtered_df[filtered_df['metros'] > 0]
        fig_scatter = px.scatter(
            df_scatter, x="metros", y="precio", 
            color="habitaciones",
            title="<b>Precio vs Metros Cuadrados</b>",
            trendline="ols",
            color_discrete_sequence=px.colors.sequential.Greens_r
        )
        fig_scatter.update_layout(**LAYOUT_OPTS)
        st.plotly_chart(fig_scatter, width='stretch')

    col_g, col_h = st.columns(2)
    
    with col_g:
        stats = get_grouped_stats(filtered_df)
        fig_bar = px.bar(
            stats['precio_hab'], x="habitaciones", y="precio", 
            title="<b>Precio Medio por Habitaciones</b>",
            color_discrete_sequence=[COLORS['primary']]
        )
        fig_bar.update_layout(**LAYOUT_OPTS)
        st.plotly_chart(fig_bar, width='stretch')
    
    with col_h:
        df_with_m2 = get_precio_m2(filtered_df)
        precio_m2_hab = df_with_m2.groupby('habitaciones')['precio_m2'].mean().reset_index()
        fig_bar_m2 = px.bar(
            precio_m2_hab, x="habitaciones", y="precio_m2", 
            title="<b>Precio m² Medio por Habitaciones</b>",
            color_discrete_sequence=[COLORS['secondary']]
        )
        fig_bar_m2.update_layout(**LAYOUT_OPTS)
        st.plotly_chart(fig_bar_m2, width='stretch')


def render_details_tab(filtered_df: pd.DataFrame):
    """
    Pestaña 'Detalles': Muestra información detallada por ubicación y características.
    
    Gráficos incluidos:
    - Top 10 propiedades por ubicación
    - Distribución de ascensor
    - Precio medio por ubicación
    - Precio vs número de planta
    - Precio m² por ubicación
    - Tipo de planta
    """
    stats = get_grouped_stats(filtered_df)
    
    col_i, col_j = st.columns(2)
    
    with col_i:
        fig_ubica = px.bar(
            x=stats['ubicacion_count'].values, 
            y=stats['ubicacion_count'].index,
            orientation='h', 
            title="<b>Top 10 Propiedades por Ubicación</b>",
            color_discrete_sequence=[COLORS['primary']]
        )
        fig_ubica.update_layout(**LAYOUT_OPTS)
        st.plotly_chart(fig_ubica, width='stretch')
    
    with col_j:
        labels = ['Con ascensor' if idx == True else 'Sin ascensor' for idx in stats['ascensor_counts'].index]
        fig_ascensor = px.pie(
            values=stats['ascensor_counts'].values, 
            names=labels,
            title="<b>Distribución de Ascensor</b>",
            color_discrete_sequence=[COLORS['primary'], COLORS['light']]
        )
        fig_ascensor.update_layout(**PIE_LAYOUT_OPTS)
        st.plotly_chart(fig_ascensor, width='stretch')

    col_k, col_l = st.columns(2)
    
    with col_k:
        fig_precio_ubica = px.bar(
            x="precio", y="ubicacion", orientation='h',
            data_frame=stats['precio_ubicacion'],
            title="<b>Precio Medio por Ubicación (Top 10)</b>",
            color_discrete_sequence=[COLORS['primary']]
        )
        fig_precio_ubica.update_layout(**LAYOUT_OPTS)
        st.plotly_chart(fig_precio_ubica, width='stretch')
    
    with col_l:
        df_planta = filtered_df.dropna(subset=['numero_planta', 'precio'])
        if len(df_planta) > 1:
            fig_planta = px.scatter(
                df_planta, x="numero_planta", y="precio", 
                title="<b>Precio vs Número de Planta</b>",
                trendline="ols",
                color_discrete_sequence=[COLORS['primary']]
            )
            fig_planta.update_layout(**LAYOUT_OPTS)
            st.plotly_chart(fig_planta, width='stretch')

    col_m, col_n = st.columns(2)
    
    with col_m:
        df_with_m2 = get_precio_m2(filtered_df)
        ubicacion_m2 = df_with_m2.groupby('ubicacion')['precio_m2'].mean().sort_values(ascending=False).head(10).reset_index()
        fig_m2_ubica = px.bar(
            x="precio_m2", y="ubicacion", orientation='h',
            data_frame=ubicacion_m2,
            title="<b>Precio m² por Ubicación (Top 10)</b>",
            color_discrete_sequence=[COLORS['secondary']]
        )
        fig_m2_ubica.update_layout(**LAYOUT_OPTS)
        st.plotly_chart(fig_m2_ubica, width='stretch')
    
    with col_n:
        planta_counts = filtered_df['planta'].value_counts().head(10)
        fig_planta_tipo = px.bar(
            x=planta_counts.values, y=planta_counts.index,
            orientation='h',
            title="<b>Tipo de Planta (Top 10)</b>",
            color_discrete_sequence=[COLORS['primary']]
        )
        fig_planta_tipo.update_layout(**LAYOUT_OPTS)
        st.plotly_chart(fig_planta_tipo, width='stretch')


def render_data_tab(filtered_df: pd.DataFrame):
    """
    Pestaña 'Datos': Muestra los datos crudos y estadísticas descriptivas.
    
    Secciones:
    - Tabla con los datos filtrados
    - Estadísticas descriptivas (describe())
    - Resumen de variables (min, max, media, mediana)
    - Top 10 propiedades más caras
    - Top 10 propiedades más económicas
    """
    st.markdown("### 📋 Datos Filtrados")
    st.dataframe(filtered_df.astype(str), width='stretch', hide_index=True)
    
    st.markdown("---")
    
    col_o, col_p = st.columns(2)
    
    with col_o:
        st.markdown("### 📊 Estadisticas Descriptivas")
        st.dataframe(filtered_df[['precio', 'habitaciones', 'metros']].describe().astype(str), width='stretch')
    
    with col_p:
        st.markdown("### 📈 Resumen de Variables")
        resumen = pd.DataFrame({
            'Variable': ['Precio', 'Metros', 'Habitaciones'],
            'Min': [f"€{int(filtered_df['precio'].min()):,}", f"{int(filtered_df['metros'].min())} m2", str(int(filtered_df['habitaciones'].min()))],
            'Max': [f"€{int(filtered_df['precio'].max()):,}", f"{int(filtered_df['metros'].max())} m2", str(int(filtered_df['habitaciones'].max()))],
            'Media': [f"€{int(filtered_df['precio'].mean()):,}", f"{int(filtered_df['metros'].mean())} m2", f"{filtered_df['habitaciones'].mean():.1f}"],
            'Mediana': [f"€{int(filtered_df['precio'].median()):,}", f"{int(filtered_df['metros'].median())} m2", f"{int(filtered_df['habitaciones'].median())}"]
        })
        st.dataframe(resumen, width='stretch', hide_index=True)

    st.markdown("---")
    
    col_q, col_r = st.columns(2)
    
    with col_q:
        st.markdown("### 💎 Top 10 Propiedades Mas Caras")
        top_expensive = filtered_df.nlargest(10, 'precio')[['precio', 'metros', 'habitaciones', 'ubicacion', 'vendedor']]
        st.dataframe(top_expensive.astype(str), width='stretch', hide_index=True)
    
    with col_r:
        st.markdown("### 💵 Top 10 Propiedades Mas Economicas")
        top_cheap = filtered_df.nsmallest(10, 'precio')[['precio', 'metros', 'habitaciones', 'ubicacion', 'vendedor']]
        st.dataframe(top_cheap.astype(str), width='stretch', hide_index=True)


def render_conclusions_tab(filtered_df: pd.DataFrame):
    """
    Pestaña 'Conclusiones': Muestra análisis final y recomendaciones.
    
    Secciones:
    - Análisis de precios (medio, mediano, rango)
    - Análisis de metros
    - Comparación particulares vs agencias
    - Hallazgos clave
    - Recomendaciones
    - Distribución de habitaciones
    """
    st.markdown("## 📈 Conclusiones del Análisis Exploratorio de Datos")
    
    precio_medio = filtered_df['precio'].mean()
    precio_mediano = filtered_df['precio'].median()
    precio_min = filtered_df['precio'].min()
    precio_max = filtered_df['precio'].max()
    
    metros_medio = filtered_df['metros'].mean()
    metros_mediano = filtered_df['metros'].median()
    
    precio_m2 = (filtered_df['precio'] / filtered_df['metros'].replace(0, 1)).mean()
    
    stats = get_grouped_stats(filtered_df)
    vendedor_stats = stats['vendedor_count']
    precio_por_vendedor = filtered_df.groupby('vendedor')['precio'].mean()
    
    df_with_m2 = filtered_df.copy()
    df_with_m2['precio_m2'] = df_with_m2['precio'] / df_with_m2['metros'].replace(0, 1)
    precio_m2_por_vendedor = df_with_m2.groupby('vendedor')['precio_m2'].mean()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💰 Análisis de Precios")
        st.markdown(f"""
        - **Precio medio:** €{precio_medio:,.0f}
        - **Precio mediano:** €{precio_mediano:,.0f}
        - **Rango de precios:** €{precio_min:,.0f} - €{precio_max:,.0f}
        - **Precio medio por m²:** €{precio_m2:,.0f}/m²
        """)
        
        st.markdown("### 📐 Análisis de Metros")
        st.markdown(f"""
        - **Metros medios:** {metros_medio:.0f} m²
        - **Metros medianos:** {metros_mediano:.0f} m²
        """)
    
    with col2:
        st.markdown("### 🏠 Particulares vs Agencias")
        st.markdown(f"""
        - **Propiedades de Particulares:** {vendedor_stats.get('Particular', 0)} ({vendedor_stats.get('Particular', 0)/len(filtered_df)*100:.1f}%)
        - **Propiedades de Agencias:** {vendedor_stats.get('Agencia', 0)} ({vendedor_stats.get('Agencia', 0)/len(filtered_df)*100:.1f}%)
        """)
        
        st.markdown("#### Precio medio por tipo de vendedor:")
        st.markdown(f"""
        - **Particular:** €{precio_por_vendedor.get('Particular', 0):,.0f}
        - **Agencia:** €{precio_por_vendedor.get('Agencia', 0):,.0f}
        """)
        
        st.markdown("#### Precio m² por tipo de vendedor:")
        st.markdown(f"""
        - **Particular:** €{precio_m2_por_vendedor.get('Particular', 0):,.0f}/m²
        - **Agencia:** €{precio_m2_por_vendedor.get('Agencia', 0):,.0f}/m²
        """)
    
    st.markdown("---")
    st.markdown("### 🔍 Hallazgos Clave")
    
    diferencia_precio = precio_por_vendedor.get('Agencia', 0) - precio_por_vendedor.get('Particular', 0)
    diferencia_m2 = precio_m2_por_vendedor.get('Agencia', 0) - precio_m2_por_vendedor.get('Particular', 0)
    
    conclusion_precio = f"mayor (€{abs(diferencia_precio):,.0f} de diferencia)" if diferencia_precio > 0 else f"menor (€{abs(diferencia_precio):,.0f} de diferencia)"
    conclusion_m2 = f"mayor en agencias (€{abs(diferencia_m2):,.0f}/m²)" if diferencia_m2 > 0 else "mayor en particulares"
    
    col_h1, col_h2 = st.columns(2)
    
    with col_h1:
        st.markdown("#### Observaciones principales:")
        st.markdown(f"""
        1. **Diferencia de precios:** Las propiedades de agencia tienen un precio medio {conclusion_precio} que las de particulares.
        
        2. **Precio por m²:** El precio por metro cuadrado es {conclusion_m2}.
        
        3. **Distribución de propiedades:** La mayoria de las propiedades en el mercado son de agencias.
        """)
    
    with col_h2:
        st.markdown("#### Recomendaciones:")
        st.markdown("""
        - **Para compradores:** Considerar propiedades de particulares para mejores precios.
        - **Para vendedores particulares:** Estudiar precios de agencias para competitividad.
        - **Inversion:** Las zonas con menor precio/m2 pueden ofrecer mejor rentabilidad.
        """)
    
    st.markdown("---")
    st.markdown("### 📊 Distribución de Habitaciones")
    
    habitacion_dist = filtered_df['habitaciones'].value_counts().sort_index()
    st.bar_chart(habitacion_dist, color=COLORS['primary'])


def main():
    """
    Función principal que orquesta toda la aplicación del dashboard.
    
    Flujo de ejecución:
    1. Carga los datos desde el archivo CSV
    2. Extrae las opciones disponibles para los filtros
    3. Genera la barra lateral con los filtros
    4. Aplica los filtros a los datos
    5. Renderiza las métricas principales
    6. Crea las pestañas con diferentes vistas de análisis
    """
    # Título principal del dashboard
    st.markdown('<p class="main-title">🏠 Dashboard Inmobiliario - Madrid</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Análisis exploratorio de datos de propiedades en venta</p>', unsafe_allow_html=True)

    # Carga de datos desde archivo CSV
    df = load_data("analisis.csv")
    
    # Obtención de las opciones de filtro basadas en los datos
    precio_min, precio_max, metros_min, metros_max, habitaciones_opts, ubicaciones_opts, vendedor_opts = get_filter_options(df)

    # =============================================================================
    # BARRA LATERAL DE FILTROS
    # =============================================================================
    with st.sidebar:
        st.markdown("🔍 Filtros")
        st.markdown("---")
        
        # Inicialización del estado de sesión para el botón de restablecer
        if 'reset_clicked' not in st.session_state:
            st.session_state.reset_clicked = False
        
        # Botón para restablecer todos los filtros a sus valores por defecto
        if st.button("🔄 Restablecer Filtros", key="reset_btn"):
            st.session_state.reset_clicked = True
        
        # Si se presionó el botón de restablecer, resetear todos los filtros
        if st.session_state.reset_clicked:
            st.session_state.precio_slider = (precio_min, precio_max)
            st.session_state.metros_slider = (metros_min, metros_max)
            st.session_state.habitaciones_multiselect = list(habitaciones_opts)
            st.session_state.ubicacion_multiselect = list(ubicaciones_opts)
            st.session_state.vendedor_multiselect = list(vendedor_opts)
            st.session_state.reset_clicked = False
            st.rerun()
        
        # Inicialización de los valores de los filtros en el estado de sesión
        if 'precio_slider' not in st.session_state:
            st.session_state.precio_slider = (precio_min, precio_max)
        if 'metros_slider' not in st.session_state:
            st.session_state.metros_slider = (metros_min, metros_max)
        if 'habitaciones_multiselect' not in st.session_state:
            st.session_state.habitaciones_multiselect = list(habitaciones_opts)
        if 'ubicacion_multiselect' not in st.session_state:
            st.session_state.ubicacion_multiselect = list(ubicaciones_opts)
        if 'vendedor_multiselect' not in st.session_state:
            st.session_state.vendedor_multiselect = list(vendedor_opts)

        # Widgets de filtro en la barra lateral
        st.slider(
            "Rango de precio (€)", 
            precio_min, precio_max, 
            key="precio_slider"
        )
        
        st.slider(
            "Rango de metros (m2)", 
            metros_min, metros_max, 
            key="metros_slider"
        )
        
        st.multiselect(
            "Habitaciones", 
            habitaciones_opts, 
            key="habitaciones_multiselect"
        )
        
        st.multiselect(
            "Ubicacion",
            ubicaciones_opts,
            key="ubicacion_multiselect"
        )
        
        st.multiselect(
            "Tipo de vendedor",
            vendedor_opts,
            key="vendedor_multiselect"
        )
        
        st.markdown("---")
        
        # Aplicación de filtros y muestra del conteo de propiedades filtradas
        df_filtered = apply_filters(df, st.session_state.precio_slider, st.session_state.metros_slider, st.session_state.habitaciones_multiselect, st.session_state.ubicacion_multiselect, st.session_state.vendedor_multiselect)
        st.markdown(f'**Propiedades filtradas:** {len(df_filtered)}')

    # Renderizado de métricas principales
    render_metrics(df_filtered)

    # =============================================================================
    # PESTAÑAS DEL DASHBOARD
    # =============================================================================
    # Creación de las 5 pestañas principales del dashboard
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Visión General", "📈 Análisis", "🗺️ Detalles", "📋 Datos", "💡 Conclusiones"])

    # Renderizado del contenido de cada pestaña
    with tab1:
        render_overview_tab(df_filtered)

    with tab2:
        render_analysis_tab(df_filtered)

    with tab3:
        render_details_tab(df_filtered)

    with tab4:
        render_data_tab(df_filtered)

    with tab5:
        render_conclusions_tab(df_filtered)

    # Pie de página
    st.markdown("---")
    st.markdown("📊 Dashboard de Análisis Exploratorio de Datos - Propiedades Madrid")


if __name__ == "__main__":
    main()

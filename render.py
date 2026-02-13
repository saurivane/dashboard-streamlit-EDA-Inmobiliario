"""
Funciones de renderizado de la interfaz de usuario
"""
import streamlit as st
import pandas as pd
import plotly.express as px

from config import COLORS, LAYOUT_OPTS, PIE_LAYOUT_OPTS, CORR_LAYOUT_OPTS
from data_loader import calculate_metrics, get_grouped_stats, get_precio_m2


def render_metrics(filtered_df: pd.DataFrame):
    """
    Renderiza las métricas principales en la parte superior del dashboard.
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

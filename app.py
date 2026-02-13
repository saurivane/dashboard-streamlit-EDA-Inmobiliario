"""
Dashboard Inmobiliario de Madrid
Análisis exploratorio de datos de propiedades en venta
"""
import streamlit as st

from config import COLORS
from data_loader import load_data, get_filter_options, apply_filters
from render import (
    render_metrics,
    render_overview_tab,
    render_analysis_tab,
    render_details_tab,
    render_data_tab,
    render_conclusions_tab
)

st.set_page_config(
    page_title="Dashboard Inmobiliario Madrid",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

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


def main():
    """
    Función principal que orquesta toda la aplicación del dashboard.
    """
    st.markdown('<p class="main-title">🏠 Dashboard Inmobiliario - Madrid</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Análisis exploratorio de datos de propiedades en venta</p>', unsafe_allow_html=True)

    df = load_data("analisis.csv")
    precio_min, precio_max, metros_min, metros_max, habitaciones_opts, ubicaciones_opts, vendedor_opts = get_filter_options(df)

    with st.sidebar:
        st.markdown("🔍 Filtros")
        st.markdown("---")
        
        if 'reset_clicked' not in st.session_state:
            st.session_state.reset_clicked = False
        
        if st.button("🔄 Restablecer Filtros", key="reset_btn"):
            st.session_state.reset_clicked = True
        
        if st.session_state.reset_clicked:
            st.session_state.precio_slider = (precio_min, precio_max)
            st.session_state.metros_slider = (metros_min, metros_max)
            st.session_state.habitaciones_multiselect = list(habitaciones_opts)
            st.session_state.ubicacion_multiselect = list(ubicaciones_opts)
            st.session_state.vendedor_multiselect = list(vendedor_opts)
            st.session_state.reset_clicked = False
            st.rerun()
        
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

        st.slider("Rango de precio (€)", precio_min, precio_max, key="precio_slider")
        st.slider("Rango de metros (m2)", metros_min, metros_max, key="metros_slider")
        st.multiselect("Habitaciones", habitaciones_opts, key="habitaciones_multiselect")
        st.multiselect("Ubicacion", ubicaciones_opts, key="ubicacion_multiselect")
        st.multiselect("Tipo de vendedor", vendedor_opts, key="vendedor_multiselect")
        
        st.markdown("---")
        
        df_filtered = apply_filters(
            df, 
            st.session_state.precio_slider, 
            st.session_state.metros_slider, 
            st.session_state.habitaciones_multiselect, 
            st.session_state.ubicacion_multiselect, 
            st.session_state.vendedor_multiselect
        )
        st.markdown(f'**Propiedades filtradas:** {len(df_filtered)}')

    render_metrics(df_filtered)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Visión General", 
        "📈 Análisis", 
        "🗺️ Detalles", 
        "📋 Datos", 
        "💡 Conclusiones"
    ])

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

    st.markdown("---")
    st.markdown("📊 Dashboard de Análisis Exploratorio de Datos - Propiedades Madrid")


if __name__ == "__main__":
    main()

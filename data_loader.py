"""
Funciones de carga y procesamiento de datos
"""
import streamlit as st
import pandas as pd
from typing import Tuple


@st.cache_data(ttl=3600)
def load_data(csv_path: str) -> pd.DataFrame:
    """
    Carga los datos desde un archivo CSV.
    """
    return pd.read_csv(csv_path)


@st.cache_data(ttl=3600)
def get_filter_options(df: pd.DataFrame) -> Tuple:
    """
    Extrae las opciones disponibles para los filtros.
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
    Aplica filtros al DataFrame según los criterios seleccionados.
    """
    filtered = df[
        (df['precio'] >= precio_range[0]) & 
        (df['precio'] <= precio_range[1]) &
        (df['metros'] >= metros_range[0]) & 
        (df['metros'] <= metros_range[1])
    ]
    
    if habitaciones:
        filtered = filtered[filtered['habitaciones'].isin(habitaciones)]
    
    if len(ubicaciones) > 0:
        filtered = filtered[filtered['ubicacion'].isin(ubicaciones)]
    
    if vendedor:
        filtered = filtered[filtered['vendedor'].isin(vendedor)]
    
    return filtered


@st.cache_data
def calculate_metrics(_df: pd.DataFrame) -> Tuple:
    """
    Calcula métricas básicas del conjunto de datos filtrado.
    """
    precio_medio = _df['precio'].mean()
    precio_m2 = (_df['precio'] / _df['metros'].replace(0, 1)).mean()
    metros_medios = _df['metros'].mean()
    return precio_medio, precio_m2, metros_medios


@st.cache_data
def get_precio_m2(_df: pd.DataFrame) -> pd.DataFrame:
    """
    Añade una columna calculada con el precio por metro cuadrado.
    """
    df_copy = _df.copy()
    df_copy['precio_m2'] = df_copy['precio'] / df_copy['metros'].replace(0, 1)
    return df_copy


def get_grouped_stats(_df: pd.DataFrame) -> dict:
    """
    Calcula estadísticas agrupadas por diferentes categorías.
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

"""
Generador de Dashboard Power BI - Datos y Métricas
Basado en el dashboard Streamlit de propiedades en Madrid
"""

import pandas as pd
import numpy as np

df = pd.read_csv("analisis.csv")

df["precio_m2"] = df["precio"] / df["metros"].replace(0, 1)

metrics_data = {
    "Metrica": [
        "Total Propiedades",
        "Precio Medio",
        "Precio m2 Medio",
        "Metros Medios",
        "Precio Minimo",
        "Precio Maximo",
        "Habitacion Mas Comun",
        "Particulares",
        "Agencias",
    ],
    "Valor": [
        len(df),
        df["precio"].mean(),
        df["precio_m2"].mean(),
        df["metros"].mean(),
        df["precio"].min(),
        df["precio"].max(),
        df["habitaciones"].mode()[0] if len(df["habitaciones"].mode()) > 0 else 0,
        len(df[df["vendedor"] == "Particular"]),
        len(df[df["vendedor"] == "Agencia"]),
    ],
}
metrics_df = pd.DataFrame(metrics_data)

precio_habitaciones = df.groupby("habitaciones")["precio"].mean().reset_index()
precio_habitaciones.columns = ["Habitaciones", "Precio_Medio"]

dist_habitaciones = df["habitaciones"].value_counts().reset_index()
dist_habitaciones.columns = ["Habitaciones", "Conteo"]

precio_ubicacion = (
    df.groupby("ubicacion")["precio"].agg(["mean", "count"]).reset_index()
)
precio_ubicacion.columns = ["Ubicacion", "Precio_Medio", "Conteo"]
precio_ubicacion = precio_ubicacion.sort_values("Precio_Medio", ascending=False)

precio_vendedor = df.groupby("vendedor")["precio"].agg(["mean", "count"]).reset_index()
precio_vendedor.columns = ["Vendedor", "Precio_Medio", "Conteo"]

dist_vendedor = df["vendedor"].value_counts().reset_index()
dist_vendedor.columns = ["Vendedor", "Conteo"]

dist_ascensor = df["ascensor"].value_counts().reset_index()
dist_ascensor.columns = ["Ascensor", "Conteo"]
dist_ascensor["Ascensor"] = dist_ascensor["Ascensor"].map(
    {True: "Con Ascensor", False: "Sin Ascensor"}
)

precio_m2_habitacion = df.groupby("habitaciones")["precio_m2"].mean().reset_index()
precio_m2_habitacion.columns = ["Habitaciones", "Precio_m2_Medio"]

precio_m2_ubicacion = df.groupby("ubicacion")["precio_m2"].mean().reset_index()
precio_m2_ubicacion.columns = ["Ubicacion", "Precio_m2_Medio"]
precio_m2_ubicacion = precio_m2_ubicacion.sort_values(
    "Precio_m2_Medio", ascending=False
)

dist_planta = df["planta"].value_counts().head(10).reset_index()
dist_planta.columns = ["Planta", "Conteo"]

corr_matrix = df[["precio", "habitaciones", "metros", "numero_planta"]].dropna().corr()
corr_data = []
for i in corr_matrix.columns:
    for j in corr_matrix.columns:
        corr_data.append(
            {"Variable1": i, "Variable2": j, "Correlacion": corr_matrix.loc[i, j]}
        )
corr_data = pd.DataFrame(corr_data)

top_caras = df.nlargest(10, "precio")[
    ["vendedor", "precio", "habitaciones", "metros", "ubicacion"]
]
top_economicas = df.nsmallest(10, "precio")[
    ["vendedor", "precio", "habitaciones", "metros", "ubicacion"]
]

with pd.ExcelWriter(
    "powerbi_dashboard/datos_dashboard.xlsx", engine="openpyxl"
) as writer:
    df.to_excel(writer, sheet_name="Datos_Originales", index=False)
    metrics_df.to_excel(writer, sheet_name="Metricas", index=False)
    precio_habitaciones.to_excel(writer, sheet_name="Precio_Habitaciones", index=False)
    dist_habitaciones.to_excel(
        writer, sheet_name="Distribucion_Habitaciones", index=False
    )
    precio_ubicacion.to_excel(writer, sheet_name="Precio_Ubicacion", index=False)
    precio_vendedor.to_excel(writer, sheet_name="Precio_Vendedor", index=False)
    dist_vendedor.to_excel(writer, sheet_name="Distribucion_Vendedor", index=False)
    dist_ascensor.to_excel(writer, sheet_name="Distribucion_Ascensor", index=False)
    precio_m2_habitacion.to_excel(
        writer, sheet_name="Precio_m2_Habitacion", index=False
    )
    precio_m2_ubicacion.to_excel(writer, sheet_name="Precio_m2_Ubicacion", index=False)
    dist_planta.to_excel(writer, sheet_name="Distribucion_Planta", index=False)
    corr_data.to_excel(writer, sheet_name="Correlaciones", index=False)
    top_caras.to_excel(writer, sheet_name="Top_Caras", index=False)
    top_economicas.to_excel(writer, sheet_name="Top_Economicas", index=False)

print("Archivo Excel generado: powerbi_dashboard/datos_dashboard.xlsx")
print("Hojas generadas:")
print("  - Datos_Originales: Datos completos con precio_m2 calculado")
print("  - Metricas: KPIs principales del dashboard")
print("  - Precio_Habitaciones: Precio medio por número de habitaciones")
print("  - Distribucion_Habitaciones: Conteo de propiedades por habitaciones")
print("  - Precio_Ubicacion: Precio medio y conteo por ubicación")
print("  - Precio_Vendedor: Precio medio por tipo de vendedor")
print("  - Distribucion_Vendedor: Conteo Particular vs Agencia")
print("  - Distribucion_Ascensor: Conteo con/sin ascensor")
print("  - Precio_m2_Habitacion: Precio m² medio por habitaciones")
print("  - Precio_m2_Ubicacion: Precio m² medio por ubicación")
print("  - Distribucion_Planta: Top 10 tipos de planta")
print("  - Correlaciones: Matriz de correlación")
print("  - Top_Caras: Top 10 propiedades más caras")
print("  - Top_Economicas: Top 10 propiedades más económicas")

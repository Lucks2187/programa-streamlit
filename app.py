import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Datos de ejemplo (puedes cargar desde Excel también)
data = [
    {
        "Fecha": "2025-04-21",
        "Hora": "03:00:00 p. m.",
        "Duracion": "00:45:00",
        "Programa": "PSL MEX - 7",
        "Sesion": "RETO 10: ROMPER PARADIGMAS",
    },
    {
        "Fecha": "2025-04-21",
        "Hora": "04:00:00 p. m.",
        "Duracion": "02:00:00",
        "Programa": "PSM MEX - 6",
        "Sesion": "Aprovechamiento del talento de la mujer en la organización",
    },
    # Agrega más registros si lo deseas
]

df = pd.DataFrame(data)

# Función para convertir a datetime

def convertir_fecha_hora(fecha_str, hora_str):
    hora, meridiano = hora_str.split(" ")[:2]
    h, m, s = map(int, hora.split(":"))
    if meridiano.lower() == "p. m." and h < 12:
        h += 12
    if meridiano.lower() == "a. m." and h == 12:
        h = 0
    return datetime.strptime(fecha_str, "%Y-%m-%d").replace(hour=h, minute=m, second=s)

# Calcular columnas
fechas_inicio = []
fechas_fin = []

for _, row in df.iterrows():
    inicio = convertir_fecha_hora(row["Fecha"], row["Hora"])
    d_h, d_m, d_s = map(int, row["Duracion"].split(":"))
    fin = inicio + timedelta(hours=d_h, minutes=d_m, seconds=d_s)
    fechas_inicio.append(inicio)
    fechas_fin.append(fin)

# Agregar al DataFrame



st.set_page_config(page_title="Calendario de Programas", layout="wide")
df["Inicio"] = fechas_inicio
df["Fin"] = fechas_fin

st.title("🗓️ Calendario de Programas")

# Filtro de búsqueda
busqueda = st.text_input("Buscar por programa, sesión o fecha (YYYY-MM-DD):")

if busqueda:
    df_filtrado = df[
        df["Programa"].str.contains(busqueda, case=False)
        | df["Sesion"].str.contains(busqueda, case=False)
        | df["Fecha"].str.contains(busqueda, case=False)
    ]
else:
    df_filtrado = df

# Mostrar tabla con información útil
st.dataframe(
    df_filtrado[["Fecha", "Programa", "Sesion", "Inicio", "Fin"]],
    use_container_width=True,
    hide_index=True,
)

st.info("Puedes buscar por parte del nombre del programa, sesión o una fecha específica.")

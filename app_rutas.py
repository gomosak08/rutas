import itertools
import requests
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
from pyproj import Transformer

st.set_page_config(page_title="Rutas Michoacán", layout="wide")

# =========================
# ORIGEN HARDCODEADO UTM
# =========================
ORIGEN_NOMBRE = "Mi origen"
ORIGEN_UTM_ESTE = 275000
ORIGEN_UTM_NORTE = 2180000
ORIGEN_ZONA_EPSG = "EPSG:32614"  # Michoacán normalmente 14N

st.title("Planeador de rutas Michoacán - UTM")

if "ruta_calculada" not in st.session_state:
    st.session_state.ruta_calculada = None

csv = st.file_uploader("Sube tu CSV", type=["csv"])

if csv:
    df = pd.read_csv(csv)

    st.subheader("Vista previa del CSV")
    st.dataframe(df.head(20))

    col_municipio = st.selectbox("Columna con nombre del municipio", df.columns)
    col_este = st.selectbox("Columna UTM ESTE / X / METROS ESTE", df.columns)
    col_norte = st.selectbox("Columna UTM NORTE / Y / METROS NORTE", df.columns)

    zona_utm = st.selectbox(
        "Zona UTM del CSV",
        ["14N - Michoacán común", "13N - alternativa"]
    )

    epsg_csv = "EPSG:32614" if zona_utm.startswith("14N") else "EPSG:32613"

    columnas_popup = st.multiselect(
        "Columnas a mostrar al hacer click en un pin",
        df.columns.tolist(),
        default=[col_municipio]
    )

    # =========================
    # LIMPIEZA Y CONVERSIÓN UTM CSV
    # =========================
    df = df.dropna(subset=[col_municipio, col_este, col_norte])
    df[col_este] = pd.to_numeric(df[col_este], errors="coerce")
    df[col_norte] = pd.to_numeric(df[col_norte], errors="coerce")
    df = df.dropna(subset=[col_este, col_norte])

    transformer_csv = Transformer.from_crs(
        epsg_csv,
        "EPSG:4326",
        always_xy=True
    )

    coords_convertidas = df.apply(
        lambda row: transformer_csv.transform(row[col_este], row[col_norte]),
        axis=1
    )

    df["LONGITUD"] = coords_convertidas.apply(lambda x: x[0])
    df["LATITUD"] = coords_convertidas.apply(lambda x: x[1])
    df["NOMBRE_MAPA"] = df[col_municipio].astype(str)

    # =========================
    # CONVERSIÓN ORIGEN HARDCODEADO
    # =========================
    transformer_origen = Transformer.from_crs(
        ORIGEN_ZONA_EPSG,
        "EPSG:4326",
        always_xy=True
    )

    origen_lon, origen_lat = transformer_origen.transform(
        ORIGEN_UTM_ESTE,
        ORIGEN_UTM_NORTE
    )

    # =========================
    # FUNCIONES
    # =========================
    def coords_destino(nombre):
        row = df[df["NOMBRE_MAPA"] == nombre].iloc[0]
        return float(row["LONGITUD"]), float(row["LATITUD"])

    def obtener_ruta(destinos):
        puntos = [(origen_lon, origen_lat)]

        for destino in destinos:
            puntos.append(coords_destino(destino))

        coord_str = ";".join([f"{lon},{lat}" for lon, lat in puntos])

        url = (
            f"https://router.project-osrm.org/route/v1/driving/{coord_str}"
            "?overview=full&geometries=geojson&steps=false"
        )

        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            st.error(f"Error consultando OSRM: {e}")
            return None

        if data.get("code") != "Ok":
            st.warning(f"OSRM no pudo calcular la ruta: {data.get('message', data)}")
            return None

        ruta = data["routes"][0]

        return {
            "orden": [ORIGEN_NOMBRE] + list(destinos),
            "distancia_km": ruta["distance"] / 1000,
            "duracion_min": ruta["duration"] / 60,
            "geometry": ruta["geometry"]["coordinates"]
        }

    def mejor_ruta(destinos):
        mejores = []

        for perm in itertools.permutations(destinos):
            ruta = obtener_ruta(perm)
            if ruta:
                mejores.append(ruta)

        if not mejores:
            return None

        return min(mejores, key=lambda x: x["distancia_km"])

    # =========================
    # SELECCIÓN DE DESTINOS
    # =========================
    st.subheader("Selecciona destinos")

    destinos = st.multiselect(
        "Busca y selecciona 2 o 3 municipios destino",
        sorted(df["NOMBRE_MAPA"].unique().tolist()),
        max_selections=3
    )

    col1, col2 = st.columns(2)

    with col1:
        calcular = st.button("Calcular mejor ruta")

    with col2:
        if st.button("Borrar ruta"):
            st.session_state.ruta_calculada = None

    if calcular:
        if len(destinos) < 2:
            st.error("Selecciona al menos 2 destinos.")
        elif len(destinos) > 3:
            st.error("Selecciona máximo 3 destinos.")
        else:
            st.session_state.ruta_calculada = mejor_ruta(destinos)

    # =========================
    # MAPA
    # =========================
    centro_lat = pd.concat([
        df["LATITUD"],
        pd.Series([origen_lat])
    ]).mean()

    centro_lon = pd.concat([
        df["LONGITUD"],
        pd.Series([origen_lon])
    ]).mean()

    mapa = folium.Map(
        location=[centro_lat, centro_lon],
        zoom_start=8
    )

    # Origen hardcodeado
    folium.Marker(
        location=[origen_lat, origen_lon],
        popup=f"<b>ORIGEN:</b> {ORIGEN_NOMBRE}<br><b>UTM Este:</b> {ORIGEN_UTM_ESTE}<br><b>UTM Norte:</b> {ORIGEN_UTM_NORTE}",
        tooltip=f"ORIGEN: {ORIGEN_NOMBRE}",
        icon=folium.Icon(color="green", icon="home")
    ).add_to(mapa)

    # Ruta calculada
    ruta = st.session_state.ruta_calculada

    if ruta is not None:
        st.success("Ruta óptima calculada")
        st.write("### Orden recomendado")
        st.write(" → ".join(ruta["orden"]))
        st.write(f"**Distancia:** {ruta['distancia_km']:.2f} km")
        st.write(f"**Duración estimada:** {ruta['duracion_min']:.1f} min")

        linea = [(lat, lon) for lon, lat in ruta["geometry"]]

        folium.PolyLine(
            linea,
            weight=6,
            opacity=0.9,
            tooltip="Ruta óptima"
        ).add_to(mapa)

    # Pines del CSV
    for _, row in df.iterrows():
        nombre = row["NOMBRE_MAPA"]

        popup_html = f"<b>{nombre}</b><br><br>"

        for col in columnas_popup:
            popup_html += f"<b>{col}:</b> {row[col]}<br>"

        if nombre in destinos:
            color = "red"
            tooltip = f"DESTINO: {nombre}"
        else:
            color = "blue"
            tooltip = nombre

        folium.Marker(
            location=[row["LATITUD"], row["LONGITUD"]],
            popup=folium.Popup(popup_html, max_width=400),
            tooltip=tooltip,
            icon=folium.Icon(color=color, icon="info-sign")
        ).add_to(mapa)

    st_folium(
        mapa,
        width=1200,
        height=700
    )

else:
    st.info("Sube un archivo CSV para comenzar.")
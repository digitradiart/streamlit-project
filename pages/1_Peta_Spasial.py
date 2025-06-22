import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import random
import os

st.set_page_config(layout="wide")
st.title("🗺️ Analisis Spasial: Peta Jaringan Observasi Iklim")

# Baca file CSV atau JSON dari direktori lokal
data_path_csv = os.path.join("data", "data.csv")
data_path_json = os.path.join("data", "data.json")

if os.path.exists(data_path_csv):
    df_all = pd.read_csv(data_path_csv)
elif os.path.exists(data_path_json):
    df_all = pd.read_json(data_path_json)
else:
    st.error("File data tidak ditemukan di folder 'data'. Harap pastikan data.csv atau data.json tersedia.")
    st.stop()

# Bersihkan data kosong koordinat
df_all = df_all.dropna(subset=["LINTANG", "BUJUR"])

# Sidebar filter
st.sidebar.header("🔍 Filter")
jaringan_list = df_all["JARINGAN"].unique().tolist()
provinsi_list = df_all["PROVINSI"].dropna().unique().tolist()

selected_jaringan = st.sidebar.multiselect("Jenis Jaringan", jaringan_list, default=jaringan_list)
selected_provinsi = st.sidebar.multiselect("Provinsi", provinsi_list, default=provinsi_list)

df_filtered = df_all[
    (df_all["JARINGAN"].isin(selected_jaringan)) &
    (df_all["PROVINSI"].isin(selected_provinsi))
]

st.markdown(f"### Jumlah titik yang ditampilkan: `{len(df_filtered)}`")
# st.markdown(f"### Jenis Peralatan: `{selected_jaringan}`")

# Tetapkan warna unik untuk setiap provinsi
provinsi_colors = {prov: f"#{random.randint(0, 0xFFFFFF):06x}" for prov in provinsi_list}

# Tetapkan ikon emoji untuk setiap jenis jaringan
jaringan_icons = {
    'PHOBS': '☂',
    'ARG': '🌧️',
    'AWS': '🌤️',
    'AAWS': '♣',
    'ASRS': '🌡️',
    'IKLIMMIKRO': '★',
    'SOIL': '⚑'
}

# Buat peta dasar
m = folium.Map(location=[-2.5, 118], zoom_start=5)

for _, row in df_filtered.iterrows():
    prov = row['PROVINSI']
    color = provinsi_colors.get(prov, 'gray')
    icon_text = jaringan_icons.get(row['JARINGAN'], '☂')

    folium.Marker(
        location=[row["LINTANG"], row["BUJUR"]],
        icon=folium.DivIcon(html=f"<div style='font-size:18px; color:{color};'>{icon_text}</div>"),
        popup=f"{row['NO STASIUN']} ({row['JARINGAN']})<br>{row['KAB/KOTA']}, {prov}"
    ).add_to(m)

folium.LayerControl(collapsed=False).add_to(m)

st.subheader("🗺️ Peta Interaktif")
st_folium(m, width=1000, height=600)
st.markdown(jaringan_icons)

# # Scatter plot koordinat
# st.subheader("📊 Scatter Plot Longitude vs Latitude")
# st.scatter_chart(df_filtered[["BUJUR", "LINTANG"]])

# Tabel data
st.subheader("📋 Tabel Data")
st.dataframe(df_filtered.reset_index(drop=True))

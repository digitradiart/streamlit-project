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

# Tetapkan warna unik untuk setiap provinsi
provinsi_colors = {prov: f"#{random.randint(0, 0xFFFFFF):06x}" for prov in provinsi_list}

# Tetapkan ikon emoji untuk setiap jenis jaringan
jaringan_icons = {
    'PHOBS': '💧',
    'ARG': '🌧️',
    'AWS': '☁️',
    'AAWS': '🌤️',
    'ASRS': '🌡️',
    'IKLIMMIKRO': '🍃',
    'SOIL': '🪨'
}

# Buat peta dasar
m = folium.Map(location=[-2.5, 118], zoom_start=5)

# Tampilkan marker provinsi dulu
for prov in selected_provinsi:
    df_prov = df_filtered[df_filtered['PROVINSI'] == prov]
    if df_prov.empty:
        continue

    # Titik rata-rata untuk marker provinsi
    lat_center = df_prov['LINTANG'].mean()
    lon_center = df_prov['BUJUR'].mean()
    color = provinsi_colors.get(prov, 'gray')
    total = len(df_prov)

    # Popup dengan link ekspansi (layer detail)
    html_popup = f"""
    <b>{prov}</b><br>
    Total alat: {total}<br>
    Klik tombol di bawah untuk menampilkan semua alat.<br>
    <button onclick=\"document.getElementById('{prov}').style.display='block'\">Lihat alat</button>
    """

    folium.Marker(
        location=[lat_center, lon_center],
        icon=folium.Icon(color="blue", icon="info-sign"),
        popup=folium.Popup(html_popup, max_width=300)
    ).add_to(m)

    # Buat FeatureGroup tersembunyi untuk alat di provinsi ini
    fg = folium.FeatureGroup(name=prov, show=False)
    for _, row in df_prov.iterrows():
        icon_text = jaringan_icons.get(row['JARINGAN'], '📍')
        folium.Marker(
            location=[row["LINTANG"], row["BUJUR"]],
            icon=folium.DivIcon(html=f"<div style='font-size:18px; color:{color};'>{icon_text}</div>"),
            popup=f"{row['NO STASIUN']} ({row['JARINGAN']})<br>{row['KAB/KOTA']}, {prov}"
        ).add_to(fg)
    m.add_child(fg)

folium.LayerControl(collapsed=False).add_to(m)

st.subheader("🗺️ Peta Interaktif")
st_folium(m, width=1000, height=600)

# Scatter plot koordinat
st.subheader("📊 Scatter Plot Longitude vs Latitude")
st.scatter_chart(df_filtered[["BUJUR", "LINTANG"]])

# Tabel data
st.subheader("📋 Tabel Data")
st.dataframe(df_filtered.reset_index(drop=True))
import streamlit as st
import pandas as pd
import os
import folium
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


st.set_page_config(layout="wide")
st.title("🗺️ Peta Sebaran Peralatan Observasi Iklim")

# Load data
data_path = os.path.join("data", "data.csv")
df = pd.read_csv(data_path)
df = df.dropna(subset=["LINTANG", "BUJUR"])

# Buat list provinsi dan jaringan unik
provinsi_list = sorted(df["PROVINSI"].dropna().unique())
jaringan_list = sorted(df["JARINGAN"].dropna().unique())

# Generate warna unik untuk setiap provinsi
color_list = list(mcolors.TABLEAU_COLORS.values()) + list(mcolors.CSS4_COLORS.values())
provinsi_colors = {prov: color_list[i % len(color_list)] for i, prov in enumerate(provinsi_list)}

# Simbol/icon berdasarkan jenis jaringan (disederhanakan untuk beberapa)
jaringan_icons = {
    'PHOBS': '■',        
    'ARG': '☂️',
    'AWS': '☁',
    'AAWS': '🌤️',
    'ASRS': '🌡️',
    'IKLIMMIKRO': '⬤',    
    'SOIL': '▲'           
}

# Sidebar filter
st.sidebar.header("Filter")
selected_prov = st.sidebar.multiselect("Pilih Provinsi", provinsi_list, default=provinsi_list)
selected_jaringan = st.sidebar.multiselect("Pilih Jenis Alat", jaringan_list, default=jaringan_list)

# Filter data
df_filtered = df[df["PROVINSI"].isin(selected_prov) & df["JARINGAN"].isin(selected_jaringan)]

# Inisialisasi peta
m = folium.Map(location=[-2, 118], zoom_start=5, tiles='cartodbpositron')

# Tambahkan marker
for _, row in df_filtered.iterrows():
    prov = row['PROVINSI']
    jenis = row['JARINGAN']
    color = provinsi_colors.get(prov, 'gray')
    icon_text = jaringan_icons.get(jenis, '📍')

    folium.Marker(
        location=[row['LINTANG'], row['BUJUR']],
        icon=folium.DivIcon(
            html=f"<div style='font-size:18px; color:{color}'>{icon_text}</div>"
        ),
        popup=f"<b>{jenis}</b><br>{row['NO STASIUN']}<br>{row['KAB/KOTA']}, {prov}"
    ).add_to(m)

# Tampilkan peta
folium_static(m, width=1200, height=700)

# Tampilkan legenda
with st.expander("📘 Lihat Legenda Warna & Simbol"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🎨 Warna per Provinsi")
        for prov in selected_prov:
            st.markdown(f"<div style='color:{provinsi_colors[prov]}; font-weight:bold;'>⬤ {prov}</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("### 🔣 Simbol per Jenis Alat")
        for jenis, icon in jaringan_icons.items():
            st.markdown(f"<div style='font-size:18px;'>{icon} = {jenis}</div>", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import os
import altair as alt

st.set_page_config(layout="wide")
st.title("📍 Analisis Per Provinsi")

# Load data
data_path = os.path.join("data", "data.csv")
if not os.path.exists(data_path):
    st.error("File data.csv tidak ditemukan dalam folder data.")
    st.stop()

# Baca dan bersihkan data
df = pd.read_csv(data_path)
df = df.dropna(subset=["LINTANG", "BUJUR"])
provinsi_list = sorted(df["PROVINSI"].dropna().unique().tolist())

# Sidebar untuk memilih provinsi
selected_prov = st.sidebar.selectbox("Pilih Provinsi", provinsi_list)
df_prov = df[df["PROVINSI"] == selected_prov]

st.header(f"📊 Statistik untuk Provinsi: {selected_prov}")

# Jumlah alat per jenis jaringan
st.subheader("Jumlah Alat per Jenis Jaringan")
jaringan_counts = df_prov["JARINGAN"].value_counts().reset_index()
jaringan_counts.columns = ["Jenis Jaringan", "Jumlah"]
st.dataframe(jaringan_counts)

bar = alt.Chart(jaringan_counts).mark_bar().encode(
    x=alt.X("Jumlah:Q", title="Jumlah Alat"),
    y=alt.Y("Jenis Jaringan:N", sort='-x'),
    color=alt.Color("Jenis Jaringan:N"),
    tooltip=["Jenis Jaringan", "Jumlah"]
)
st.altair_chart(bar, use_container_width=True)

# Sebaran kabupaten/kota
st.subheader("Jumlah Alat per Kabupaten/Kota")
kab_counts = df_prov["KAB/KOTA"].value_counts().reset_index()
kab_counts.columns = ["Kabupaten/Kota", "Jumlah"]
st.dataframe(kab_counts)

bar2 = alt.Chart(kab_counts).mark_bar().encode(
    x=alt.X("Jumlah:Q", title="Jumlah Alat"),
    y=alt.Y("Kabupaten/Kota:N", sort='-x'),
    tooltip=["Kabupaten/Kota", "Jumlah"]
).properties(height=600)
st.altair_chart(bar2, use_container_width=True)

# Tabel data mentah per provinsi
st.subheader("📋 Data Detail")
st.dataframe(df_prov.reset_index(drop=True))

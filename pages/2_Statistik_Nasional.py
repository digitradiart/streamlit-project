import streamlit as st
import pandas as pd
import os
import altair as alt

st.title("📈 Statistik Deskriptif Peralatan Observasi Iklim")

# Load data
data_path = os.path.join("data", "data.csv")
df = pd.read_csv(data_path)

# Filter data valid
df = df.dropna(subset=["LINTANG", "BUJUR"])

# Jumlah alat per provinsi
st.subheader("Jumlah Alat per Provinsi")
prov_counts = df["PROVINSI"].value_counts().reset_index()
prov_counts.columns = ["Provinsi", "Jumlah"]
st.dataframe(prov_counts)
# st.header(len(prov_counts))

bar = alt.Chart(prov_counts).mark_bar().encode(
    x=alt.X("Jumlah:Q", title="Jumlah Alat"),
    y=alt.Y("Provinsi:N", sort='-x'),
    tooltip=["Provinsi", "Jumlah"]
).properties(height=600)
st.altair_chart(bar, use_container_width=True)

# Jumlah alat per jenis jaringan
st.subheader("Jumlah Alat per Jenis Jaringan")
jenis_counts = df["JARINGAN"].value_counts().reset_index()
jenis_counts.columns = ["Jenis Jaringan", "Jumlah"]
st.dataframe(jenis_counts)

pie = alt.Chart(jenis_counts).mark_arc().encode(
    theta="Jumlah:Q",
    color="Jenis Jaringan:N",
    tooltip=["Jenis Jaringan", "Jumlah"]
)
st.altair_chart(pie, use_container_width=True)

# Tabel ringkasan gabungan
st.subheader("Rekap Jumlah Alat per Provinsi dan Jenis")
pivot = pd.pivot_table(df, index="PROVINSI", columns="JARINGAN", aggfunc="size", fill_value=0)
pivot["TOTAL"] = pivot.sum(axis=1)
st.dataframe(pivot)

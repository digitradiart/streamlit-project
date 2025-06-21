import streamlit as st
import pandas as pd

st.title("📈 Analisis Temporal")

uploaded_file = st.file_uploader("Upload file Excel", type=["xlsx"])

if uploaded_file:
    xls = pd.ExcelFile(uploaded_file)
    sheet_names = xls.sheet_names
    df_all = pd.DataFrame()

    for sheet in sheet_names:
        df = xls.parse(sheet)
        df["JARINGAN"] = sheet
        df_all = pd.concat([df_all, df], ignore_index=True)

    # Misal kamu punya kolom 'TAHUN' atau 'TANGGAL PASANG'
    if "TAHUN" in df_all.columns:
        df_count = df_all.groupby(["TAHUN", "JARINGAN"]).size().unstack().fillna(0)
        st.line_chart(df_count)
    else:
        st.warning("Kolom waktu (seperti TAHUN atau TANGGAL PASANG) tidak ditemukan.")

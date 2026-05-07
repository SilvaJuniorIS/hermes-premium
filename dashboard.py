import streamlit as st
import sqlite3
import pandas as pd

st.title("🚀 HERMES DASHBOARD")

conn = sqlite3.connect("data/hermes.sqlite3")

df = pd.read_sql_query("SELECT * FROM licitacoes", conn)

if df.empty:
    st.warning("Sem dados ainda")
else:
    st.dataframe(df)

    st.subheader("🔥 TOP OPORTUNIDADES")
    top = df.sort_values(by="valor_estimado_num", ascending=False).head(10)
    st.table(top)
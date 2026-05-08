import sqlite3

import pandas as pd
import streamlit as st

from src.config import DB_PATH
from src.hermes_db import init_db


st.set_page_config(page_title="Hermes Dashboard", layout="wide")
st.title("Hermes Dashboard")

init_db()

with sqlite3.connect(DB_PATH) as conn:
    df = pd.read_sql_query(
        """
        SELECT
            objeto,
            estado,
            municipio,
            valor_estimado_num,
            score,
            classificacao,
            oportunidade,
            data_abertura,
            last_seen_at
        FROM licitacoes
        ORDER BY score DESC, valor_estimado_num DESC, last_seen_at DESC
        LIMIT 500
        """,
        conn,
    )

if df.empty:
    st.warning("Sem dados ainda. Rode uma coleta pela API ou com python -m src.main.")
else:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Registros", len(df))
    col2.metric("Score medio", round(df["score"].fillna(0).mean(), 1))
    col3.metric("Maior valor", f"R$ {df['valor_estimado_num'].fillna(0).max():,.2f}")
    col4.metric("Alta prioridade", int((df["classificacao"] == "ALTA").sum()))

    st.dataframe(df, width="stretch", hide_index=True)

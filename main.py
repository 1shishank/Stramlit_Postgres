import streamlit as st
import pandas as pd
from connection import get_connection

st.title("Employee Dashboard")

conn = get_connection()

if conn:

    query = "SELECT * FROM employees"

    df = pd.read_sql(query, conn)

    st.success("Database Connected Successfully")

    st.subheader("Employee Records")

    st.dataframe(df)

    conn.close()

else:
    st.error("Failed to connect to PostgreSQL")

##python -m streamlit run app.py
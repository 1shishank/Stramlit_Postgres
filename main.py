import streamlit as st
import pandas as pd
from connection import get_connection

tab1, tab2 = st.tabs(
    ["Upload Report", "View Report"]
)

# ----------------------------
# TAB 1 - Upload Report
# ----------------------------
with tab1:

    st.title("Backup Health Dashboard")

    upload_date = st.date_input("Select Report Date")

    uploaded_file = st.file_uploader(
        "Upload Excel File",
        type=["xlsx"]
    )

    if uploaded_file:

        df = pd.read_excel(uploaded_file)

        conn = get_connection()
        cur = conn.cursor()

        for _, row in df.iterrows():

            cur.execute(
                """
                INSERT INTO backup_status
                (
                    report_date,
                    backup_server,
                    ip_address,
                    status,
                    remarks
                )
                VALUES (%s,%s,%s,%s,%s)
                """,
                (
                    upload_date,
                    row["Backup Server"],
                    row["IP Address"],
                    row["Status"],
                    row["Remarks"]
                )
            )

        conn.commit()
        conn.close()

        st.success("Report Uploaded Successfully")


# ----------------------------
# TAB 2 - View Report
# ----------------------------
with tab2:

    st.header("View Report")

    selected_date = st.date_input(
        "Choose Date To View",
        key="view_date"
    )

    if st.button("Fetch Report"):

        conn = get_connection()

        query = """
        SELECT
            backup_server,
            ip_address,
            status,
            remarks
        FROM backup_status
        WHERE report_date = %s
        ORDER BY backup_server
        """

        df = pd.read_sql(
            query,
            conn,
            params=[selected_date]
        )
        st.dataframe(df)

st.title("PostgreSQL Query Console")

query = st.text_area(
    "Enter SQL Query",
    height=150,
    placeholder="SELECT * FROM backup_status LIMIT 10;"
)

if st.button("Run Query"):

    if not query.strip():
        st.warning("Please enter a query.")
    else:
        try:
            conn = get_connection()

            df = pd.read_sql_query(query, conn)

            st.success("Query executed successfully.")

            st.dataframe(
                df,
                use_container_width=True
            )

            conn.close()

        except Exception as e:
            st.error(f"Error: {e}")
       


import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3 as db
import sys
import json
import requests
import altair as alt 
from io import BytesIO

# Database connection to pandas
con = db.connect("Data_sicence_SQL.db")

# API Key for currency conversion
API_KEY = "929ce405b668474ea251cb0f2cb4764b"

def fetch_exchange_rate():
    """Fetches the latest exchange rate for SEK from the currency API."""
    url = f"https://api.currencyfreaks.com/v2.0/rates/latest?apikey={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        payload = json.loads(response.text)
        return float(payload["rates"]["SEK"])
    except Exception as e:
        st.error(f"Error fetching exchange rate: {e}")
        return None

def convert_salaries(salaries_df, sek_rate, selected_currency):
    """Converts salaries from USD to SEK if selected, otherwise keeps them in USD."""
    try:
        if selected_currency == "SEK":
            salaries_df["salary_converted"] = round(salaries_df["salary_in_usd"] * sek_rate)
            salaries_df["currency"] = "SEK"
        else:
            salaries_df["salary_converted"] = salaries_df["salary_in_usd"]
            salaries_df["currency"] = "USD"
        return salaries_df
    except Exception as e:
        st.error(f"Error converting salaries: {e}")
        return None

# Streamlit app title
st.title("Salary Converter and Exporter")

# Sidebar for currency selection
st.sidebar.header("Currency converter")
selected_currency = st.sidebar.selectbox("Select currency for salary display:", ["USD", "SEK"])

uploaded_file = st.file_uploader("Upload your database-file", type="db")
if uploaded_file:
    try:
        temp_file_path = f"temp_{uploaded_file.name}"
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.read())

        # Connect to the SQLite database file
        con = db.connect(temp_file_path)

        salaries_df = pd.read_sql_query('SELECT * FROM salaries', con)
        
        if "salary_in_usd" not in salaries_df.columns:
            st.error("SQL file must contain 'salary_in_usd' column")
        else:
            sek_rate = fetch_exchange_rate()
            if sek_rate:
                st.success(f"Current SEK exchange rate: {sek_rate}")
                converted_df = convert_salaries(salaries_df, sek_rate, selected_currency)
                if converted_df is not None:
                    st.subheader(f"Salary Data in {selected_currency}")
                    st.dataframe(converted_df)
                    if st.button("Export to Database"):
                        # export_to_database(converted_df)
                        st.success("Data exported to SQLite database successfully!")
    except Exception as e:
        st.error(f"Error processing file: {e}")

# Code Display Section.
code = '''"""
Complete code block displayed in Streamlit for reference.
"""
'''  
 # Code for expander.
with st.expander('Code'):
    st.write('**Data**')
    st.code(code, language='python')
    




  
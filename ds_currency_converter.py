import streamlit as st
import pandas as pd
import sqlite3 as db
import requests
import json

API_KEY = "929ce405b668474ea251cb0f2cb4764b"

def fetch_exchange_rate():
    url = f"https://api.currencyfreaks.com/v2.0/rates/latest?apikey={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        payload = json.loads(response.text)
        return float(payload["rates"]["SEK", "EUR""])
    except Exception as e:
        st.error(f"Error fetching exchange rate: {e}")
        return None

def convert_salaries(salaries_df, sek_rate, selected_currency):
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

def export_to_database(df):
    try:
        con = db.connect("ds_salaries.db")
        df.to_sql("salaries", con, if_exists="replace", index=False)
        con.close()
    except Exception as e:
        st.error(f"Error exporting to database: {e}")

# Streamlit app
st.title("Salary Converter and Exporter")

# Sidebar for currency selection
st.sidebar.header("Settings")
selected_currency = st.sidebar.selectbox("Select currency for salary display:", ["USD", "SEK"])

uploaded_file = st.file_uploader("Upload your CSV file", type="csv")
if uploaded_file:
    try:
        salaries_df = pd.read_csv(uploaded_file)
        if "salary_in_usd" not in salaries_df.columns:
            st.error("CSV file must contain 'salary_in_usd' column")
        else:
            sek_rate = fetch_exchange_rate()
            if sek_rate:
                st.success(f"Current SEK exchange rate: {sek_rate}")
                converted_df = convert_salaries(salaries_df, sek_rate, selected_currency)
                if converted_df is not None:
                    st.subheader(f"Salary Data in {selected_currency}")
                    st.dataframe(converted_df)
                    if st.button("Export to Database"):
                        export_to_database(converted_df)
                        st.success("Data exported to SQLite database successfully!")
    except Exception as e:
        st.error(f"Error processing file: {e}")

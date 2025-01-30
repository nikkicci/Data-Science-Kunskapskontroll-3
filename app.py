import pandas as pd
import streamlit as st
import numpy as np
import matplotlib as mpl
import sqlite3 as db
import matplotlib.pyplot as plt
import requests
import sys
import json
import logging

con = db.connect('ds_salaries.db')

try:
    con = db.connect('ds_salaries.db')
    print("Anslutning lyckades!")
except db.Error as e:
    print(f"Fel vid anslutning: {e}")
#finally:
    #if 'con' in locals():
    #con.close()

# omvandla valuta från USD till SEK samt skapa ny kolumn och loggfil
API_KEY = "929ce405b668474ea251cb0f2cb4764b"  

def fetch_exchange_rate():
    url = f"https://api.currencyfreaks.com/v2.0/rates/latest?apikey={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        payload = json.loads(response.text)
        return float(payload["rates"]["SEK", "EUR"])
    except Exception as e:
        st.error(f"Error fetching exchange rate: {e}")
        return None

def bail(message):
    logger.error(message)
    sys.exit(1)

def fetch_exchange_rate():
    url = f"https://api.currencyfreaks.com/v2.0/rates/latest?apikey={API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch currencies: {response.text}")
    except Exception as e:
        raise Exception(f"Failed to fetch currencies: {str(e)}")
    
    payload = json.loads(response.text)
    try:
        sek_rate = float(payload["rates"]["SEK"])  # Hämta SEK-växelkursen
    except KeyError:
        raise Exception("SEK rate not found in API response")
    
    return sek_rate

def convert_salaries_to_sek(salaries_df, sek_rate):
    try:
        # Lägg till en ny kolumn med omvandlade löner
        salaries_df["salary_in_sek"] = round(salaries_df["salary_in_usd"] * sek_rate)
    except Exception as e:
        raise Exception(f"Failed to convert salaries: {str(e)}")
    return salaries_df

def export_to_database(df):
    try:
        con = db.connect("ds_salaries.db")
        df.to_sql("salaries", con, if_exists="replace", index=False)
        con.close()
    except Exception as e:
        raise Exception(f"Failed to export to database: {str(e)}")

if __name__ == "__main__":
    logging.basicConfig(filename="salaries.log", level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
    logger = logging.getLogger()
    
    try:
        # Steg 1: Hämta SEK-växelkursen
        sek_rate = fetch_exchange_rate()
        logger.info(f"Fetched SEK exchange rate: {sek_rate}")
        
        # Steg 2: Läs in löner från CSV
        salaries_df = pd.read_csv("ds_salaries.csv")
        if "salary_in_usd" not in salaries_df.columns:
            raise Exception("CSV file must contain 'salary_in_usd' column")
        
        # Steg 3: Omvandla löner till SEK
        salaries_df = convert_salaries_to_sek(salaries_df, sek_rate)
        
        # Steg 4: Exportera data till SQLite-databas
        export_to_database(salaries_df)
        
        logger.info("Salaries converted and exported successfully")
    except Exception as e:
        bail(str(e))


st.title('💸 Data Scientists Salaries 💸')

st.write('This is an app for data scientists salaries with analysis and a currency converter for USD to SEK')

st.sidebar.header('Input Options')

## Sidebar - Currency price unit
currency_list = ['SEK', 'USD']
base_price_unit = st.sidebar.selectbox('Select base currency for conversion', currency_list)
symbols_price_unit = st.sidebar.selectbox('Select target currency to convert to', currency_list)

with st.expander('Data'):
  st.write('**Raw data**')
  df = pd.read_csv('ds_salaries.csv')
  df
  

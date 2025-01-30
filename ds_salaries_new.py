import pandas as pd
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



# df = pd.read_csv(r'C:\Users\kolcz\Documents\data_science_kunskapskontroll_3_salaries\ds_salaries.csv')

# df.to_sql('ds_salaries', con, if_exists = 'replace', index=False)

# print(df)

# df.columns
 
# df['employee_residence'] = df['employee_residence'].replace({"ES": "Spain", "US": "United States", "CA": "Canada", "DE": "Germany", "GB": "Great Britain", "NG": "Nigeria", "IN": "India", "HK": "Hong Kong", "PT": "Portugal", "NL": "Netherlands", "CH": "Switzerland", "CF": "Central African Republic", "FI": "Finland", "UA": "Uruguay", "IE": "Republic of Ireland", "IL": "Israel", "GH": "Ghana", "AT": "Austria", "CO":"Colombia", "SG":"Singapore", "SE": "Sweden", "SI": "Slovenia", "MX": "Mexico", "UZ": "Uzbekistan", "HR": "Croatia", "PL": "Poland", "KW": "Kuwait", "VN": "Vietnam", "CY": "Cypern", "AR": "Argentina", "AM": "Armenia", "BA": "BosniaandHerzegovina", "KE": "Kenya", "GR": "Greece", "MK": "NorthMacedonia", "LV": "Latvia", "IT": "Italy", "MA": "Morocco", "LT": "Lithuania", "BE": "Belgium", "AS": "AmericanSamoa", "IR":"Iran", "HU": "Hungary", "SK": "Slovakia", "CN": "China", "CZ": "CzechRepublic", "CR": "CostaRica", "TR": "Turkey", "DK": "Denmark", "BO": "Bolivia", "PH": "Philippines", "DO": "DominicanRepublic", "EG": "Egypt", "ID": "Indonesia", "AE": "UnitedArabEmirates", "MY": "Malaysia", "JP": "Japan", "EE": "Estonia", "HN": "Honduras", "TN": "Tunisia", "IQ": "Iraq", "BG": "Bulgaria", "JE": "Jordanien", "RS": "Serbia", "NZ": "NewZealand", "MD": "Moldova", "LU": "Luxenbourg", "MT": "Malta"})
 
# new_df = df.to_sql("ds_salaries.csv", con, if_exists="replace")
 
# print(new_df)
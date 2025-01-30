import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3 as db  
import json
import requests


# Connect databas with pandas.
con = db.connect("Data_sicence_SQL.db")

# Set the title for the Streamlit app
st.title("Christian's Analytics")

### Plot 1: Number of Data Scientists per Country ###
st.header("Plot nr 1")

# SQL query to get the top 6 countries with the most Data Scientists
query = '''SELECT employee_residence, COUNT(*) AS OCCURRENCE
FROM salaries
WHERE job_title='Data Scientist'
GROUP BY employee_residence
ORDER BY OCCURRENCE DESC
LIMIT 6;'''

# Fetch data into a DataFrame
df = pd.read_sql(query, con)

# Create a bar plot
plt.figure(figsize=(10, 6))
df.plot(kind="bar", x="employee_residence", rot=45)
plt.xlabel("Employee Residence", fontsize=14)
plt.ylabel("Data Scientists", fontsize=14)
plt.title("Top 6 Number of Data Scientists per Country", fontsize=16)

# Display plot in Streamlit
st.pyplot(plt)

### Plot 2: Number of Job Listings per Country ###
st.header("Plot nr 2")

# SQL query to get the top 5 countries with the most job listings
query = '''SELECT company_location, COUNT(*) AS job_count
FROM Salaries
GROUP BY company_location
ORDER BY job_count DESC
LIMIT 5;'''

# Fetch data into a DataFrame
df = pd.read_sql(query, con)

# Create a bar plot with dark background
plt.figure(figsize=(10, 6))
plt.style.use("dark_background")
df.plot(kind="bar", x="company_location", rot=45)
plt.xlabel("Company Location", fontsize=14)
plt.ylabel("Number of Jobs", fontsize=14)
plt.title("Top 5 Number of Jobs per Country", fontsize=16)

# Display plot in Streamlit
st.pyplot(plt)

### Plot 3: Salary Data with Currency Conversion ###
st.header("Plot nr 3")

API_KEY = "929ce405b668474ea251cb0f2cb4764b"

def fetch_exchange_rate():
    """Fetch the exchange rate for SEK from an API."""
    url = f"https://api.currencyfreaks.com/v2.0/rates/latest?apikey={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        payload = json.loads(response.text)
        return float(payload["rates"]["SEK"])
    except Exception as e:
        st.error(f"Error fetching exchange rate: {e}")
        return None

def fetch_salaries_from_db(currency="USD"):
    """Fetch average salary data from the database in the selected currency."""
    try:
        con = db.connect("Data_sicence_SQL.db")
        if currency == "SEK":
            query = '''SELECT company_size, AVG(salary_in_sek) AS avg_salary, 'SEK' AS currency
                       FROM salaries GROUP BY company_size'''
        else:
            query = '''SELECT company_size, AVG(salary_in_usd) AS avg_salary, 'USD' AS currency
                       FROM salaries GROUP BY company_size'''
        return pd.read_sql_query(query, con)
    except Exception as e:
        st.error("Error fetching salary data")
        return pd.DataFrame()

with st.sidebar:
    st.header("Currency Settings")
    selected_currency = st.radio("Select Currency:", ["USD", "SEK"], index=0)

salaries_df = fetch_salaries_from_db(selected_currency)

if salaries_df.empty:
    st.stop()

# Plot salary data
st.subheader(f"Salary Bar Chart in {selected_currency}")
fig, ax = plt.subplots(figsize=(10, 6))
salaries_df.plot(kind="bar", x="company_size", y="avg_salary", ax=ax, color="skyblue", legend=False, rot=0)
ax.set_title(f"Average Salaries in {selected_currency}")
ax.set_ylabel(f"Salary ({selected_currency})")
ax.set_xlabel("Company Size")
plt.tight_layout()
st.pyplot(fig)

# Code display section
code = '''(same code as above)'''
with st.expander("Code"):
    st.write("**Data**")
    st.code(code, language="python")











        










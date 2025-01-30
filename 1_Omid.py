import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3 as db
import sys
import json
import requests
import logging

con = db.connect("Data_sicence_SQL.db")

st.title("Omid's analytics")

query = '''SELECT job_title, salary_in_usd AS salary_data_analyst, work_year
FROM salaries
WHERE job_title = 'Data Analyst'
AND work_year IN ('2021', '2022', '2023')
GROUP BY job_title, salary_in_usd, work_year
ORDER BY salary_in_usd, work_year DESC
LIMIT 20;'''
 
df = pd.read_sql(query, con)
 
df.plot(kind="bar",title="Top 20 'Data analyst' salaries between 2021 - 2023", y="salary_data_analyst", x="work_year", rot=60)
plt.xlabel("work_year")
plt.ylabel("salary_data_analyst")

st.pyplot(plt)



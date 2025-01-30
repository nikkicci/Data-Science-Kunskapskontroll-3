import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3 as db


# Create a title for the Streamlit app
st.title("Milan's Analytics")

# Establish a connection to the database
con = db.connect('Data_sicence_SQL.db')

### Plot 1: Average Salary Per Job Title ###
st.header("Plot nr 1")

# SQL query to fetch the top 5 job titles with the highest average salary
query = """
SELECT job_title, AVG(salary_in_usd) AS average_salary_per_title
FROM Salaries
GROUP BY job_title
ORDER BY average_salary_per_title DESC
LIMIT 5;
"""

# Retrieve the data and store it in a Pandas DataFrame
df = pd.read_sql(query, con)

# Create a figure for the plot
plt.figure(figsize=(12, 6))

# Create a bar chart with job titles on the x-axis and average salary on the y-axis
df.plot(kind="bar", x="job_title", color="white")

# Apply a dark background style
plt.style.use("dark_background")

# Customize plot title and labels
plt.title('Average Salary per Job Title', fontsize=16)
plt.xlabel('Job Title', fontsize=14)
plt.ylabel('Average Salary (USD)', fontsize=14)

# Adjust font size and rotation of tick labels
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)

# Display the plot in Streamlit
st.pyplot(plt)


### Plot 2: Average Salary Per Country ###
st.header("Plot nr 2")

# SQL query to fetch the top 5 countries with the highest average salary
query = """
SELECT company_location, AVG(salary_in_usd) AS average_salary
FROM Salaries
GROUP BY company_location
ORDER BY average_salary DESC
LIMIT 5;
"""

# Retrieve the data and store it in a Pandas DataFrame
df = pd.read_sql(query, con)

# Create a figure for the plot
plt.figure(figsize=(15, 8))

# Create a bar chart with countries on the x-axis and average salary on the y-axis
df.plot(kind="bar", x="company_location", rot=45)

# Customize plot title and labels
plt.title('Tech Salaries per Country')
plt.xlabel('Country', fontsize=10)
plt.ylabel('Salary (USD)', fontsize=10)

# Display the plot in Streamlit
st.pyplot(plt)


### Plot 3: Most Common Job Titles ###
st.header("Plot nr 3")

# SQL query to fetch the 10 most common job titles
query = """
SELECT job_title, COUNT(*) AS flest_förekommande
FROM Salaries
GROUP BY job_title
ORDER BY flest_förekommande DESC
LIMIT 10;
"""

# Retrieve the data and store it in a Pandas DataFrame
df = pd.read_sql(query, con)

# Create a figure for the plot
plt.figure(figsize=(15, 8))

# Create a bar chart with job titles on the x-axis and their occurrence on the y-axis
df.plot(kind="bar", x="job_title", color="blue")

# Customize plot title and labels
plt.title('Most Common Tech Titles', fontsize=16)
plt.xlabel('Job Title', fontsize=10)
plt.ylabel('Occurrence', fontsize=10)

# Adjust font size and rotation of tick labels
plt.xticks(rotation=30, fontsize=10)
plt.yticks(fontsize=10)

# Display the plot in Streamlit
st.pyplot(plt)






import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3 as db



# connection to SQL_databas
con= db.connect('Data_sicence_SQL.db')
df = pd.read_sql("select * from salaries", con)


# Title,image and description on front page.  
st.title("Salaries within the data sphere💸")

st.write("This is our project based on dataset Data Scientists salaries 2023 ")

st.audio(r"C:\Users\Max\Downloads\shane-mcmahon-here-comes-the-money-entrance-theme-128-ytshorts.savetube.me.mp3")

st.image(r"C:\Users\Max\Downloads\Leo wolf.jpg")

st.title("Agenda")

st.header("+ Introduktion")
st.header("+ Analys")
st.header("+ Avslutning")

















import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3 as db
import altair as alt
import pydeck as pdk


con= db.connect('Data_sicence_SQL.db')

query = """
SELECT work_year, COUNT(remote_ratio) as remote_workers
FROM salaries
WHERE work_year BETWEEN 2020 AND 2023
AND remote_ratio is not null AND remote_ratio > 50
GROUP BY work_year
ORDER BY work_year
"""
df = pd.read_sql_query(query, con)


st.title("Max's Analytics")

st.header("Kan man se en ökning på hur många som arbetar hemma mellan 2020-2023? ")


chart = alt.Chart(df).mark_line().encode(
    x = alt.X('work_year:O', axis = alt.Axis(labelAngle=-360)),
    y ='remote_workers:Q',
    tooltip=["work_year", "remote_workers"]
).properties(
    title ="Ökning av antalet som arbetar hemma"
)

st.altair_chart(chart, use_container_width=True)


st.header("Employee residence over the world")

# Skapa dataset med latitud, longitud och storlek för alla länder
countries_coords = {
    "ES": {"country": "Spain", "lat": 40.4637, "lon": -3.7492, "size": 3000},
    "US": {"country": "United States", "lat": 37.7749, "lon": -122.4194, "size": 3000},
    "CA": {"country": "Canada", "lat": 45.4215, "lon": -75.6992, "size": 3000},
    "DE": {"country": "Germany", "lat": 52.52, "lon": 13.4050, "size": 3000},
    "GB": {"country": "Great Britain", "lat": 51.5074, "lon": -0.1278, "size": 3000},
    "NG": {"country": "Nigeria", "lat": 9.0820, "lon": 8.6753, "size": 3000},
    "IN": {"country": "India", "lat": 28.6139, "lon": 77.2090, "size": 3000},
    "HK": {"country": "Hong Kong", "lat": 22.3193, "lon": 114.1694, "size": 3000},
    "PT": {"country": "Portugal", "lat": 38.7369, "lon": -9.1395, "size": 3000},
    "NL": {"country": "Netherlands", "lat": 52.3676, "lon": 4.9041, "size": 3000},
    "CH": {"country": "Switzerland", "lat": 46.8182, "lon": 8.2275, "size": 3000},
    "CF": {"country": "Central African Republic", "lat": 4.3947, "lon": 18.5582, "size": 3000},
    "FI": {"country": "Finland", "lat": 60.1695, "lon": 24.9354, "size": 3000},
    "UA": {"country": "Uruguay", "lat": -34.9011, "lon": -56.1645, "size": 3000},
    "IE": {"country": "Republic of Ireland", "lat": 53.3498, "lon": -6.2603, "size": 3000},
    "IL": {"country": "Israel", "lat": 31.7683, "lon": 35.2137, "size": 3000},
    "GH": {"country": "Ghana", "lat": 5.6037, "lon": -0.1870, "size": 3000},
    "AT": {"country": "Austria", "lat": 48.2082, "lon": 16.3738, "size": 3000},
    "CO": {"country": "Colombia", "lat": 4.7110, "lon": -74.0721, "size": 3000},
    "SG": {"country": "Singapore", "lat": 1.3521, "lon": 103.8198, "size": 3000},
    "SE": {"country": "Sweden", "lat": 59.3293, "lon": 18.0686, "size": 3000},
    "SI": {"country": "Slovenia", "lat": 46.0511, "lon": 14.5051, "size": 3000},
    "MX": {"country": "Mexico", "lat": 19.4326, "lon": -99.1332, "size": 3000},
    "UZ": {"country": "Uzbekistan", "lat": 41.2995, "lon": 69.2401, "size": 3000},
    "HR": {"country": "Croatia", "lat": 45.1, "lon": 15.2, "size": 3000},
    "PL": {"country": "Poland", "lat": 52.2298, "lon": 21.0118, "size": 3000},
    "KW": {"country": "Kuwait", "lat": 29.3759, "lon": 47.9774, "size": 3000},
    "VN": {"country": "Vietnam", "lat": 21.0285, "lon": 105.8542, "size": 3000},
    "CY": {"country": "Cyprus", "lat": 35.1264, "lon": 33.4299, "size": 3000},
    "AR": {"country": "Argentina", "lat": -34.6037, "lon": -58.3816, "size": 3000},
    "AM": {"country": "Armenia", "lat": 40.1792, "lon": 44.4991, "size": 3000},
    "BA": {"country": "Bosnia and Herzegovina", "lat": 43.8486, "lon": 18.3564, "size": 3000},
    "KE": {"country": "Kenya", "lat": -1.2867, "lon": 36.8172, "size": 3000},
    "GR": {"country": "Greece", "lat": 37.9838, "lon": 23.7275, "size": 3000},
    "MK": {"country": "North Macedonia", "lat": 41.6086, "lon": 21.7453, "size": 3000},
    "LV": {"country": "Latvia", "lat": 56.946, "lon": 24.1059, "size": 3000},
    "IT": {"country": "Italy", "lat": 41.9028, "lon": 12.4964, "size": 3000},
    "MA": {"country": "Morocco", "lat": 34.0209, "lon": -6.8416, "size": 3000},
    "LT": {"country": "Lithuania", "lat": 54.6892, "lon": 25.2798, "size": 3000},
    "BE": {"country": "Belgium", "lat": 50.8503, "lon": 4.3517, "size": 3000},
    "AS": {"country": "American Samoa", "lat": -14.2700, "lon": -170.1324, "size": 3000},
    "IR": {"country": "Iran", "lat": 35.6892, "lon": 51.3890, "size": 3000},
    "HU": {"country": "Hungary", "lat": 47.4979, "lon": 19.0402, "size": 3000},
    "SK": {"country": "Slovakia", "lat": 48.1482, "lon": 17.1067, "size": 3000},
    "CN": {"country": "China", "lat": 39.9042, "lon": 116.4074, "size": 3000},
    "CZ": {"country": "Czech Republic", "lat": 50.0755, "lon": 14.4378, "size": 3000},
    "CR": {"country": "Costa Rica", "lat": 9.9281, "lon": -84.0907, "size": 3000},
    "TR": {"country": "Turkey", "lat": 41.0082, "lon": 28.9784, "size": 3000},
    "DK": {"country": "Denmark", "lat": 55.6761, "lon": 12.5683, "size": 3000},
    "BO": {"country": "Bolivia", "lat": -16.5000, "lon": -68.1193, "size": 3000},
    "PH": {"country": "Philippines", "lat": 14.5995, "lon": 120.9842, "size": 3000},
    "DO": {"country": "Dominican Republic", "lat": 18.7357, "lon": -70.1627, "size": 3000},
    "EG": {"country": "Egypt", "lat": 30.0444, "lon": 31.2357, "size": 3000},
    "ID": {"country": "Indonesia", "lat": -6.2088, "lon": 106.8456, "size": 3000},
    "AE": {"country": "United Arab Emirates", "lat": 25.276987, "lon": 55.296249, "size": 3000},
    "MY": {"country": "Malaysia", "lat": 3.1390, "lon": 101.6869, "size": 3000},
    "JP": {"country": "Japan", "lat": 35.6762, "lon": 139.6503, "size": 3000},
    "EE": {"country": "Estonia", "lat": 59.4370, "lon": 24.7535, "size": 3000},
    "HN": {"country": "Honduras", "lat": 13.9671, "lon": -77.0215, "size": 3000},
    "TN": {"country": "Tunisia", "lat": 36.8065, "lon": 10.1815, "size": 3000},
    "IQ": {"country": "Iraq", "lat": 33.3152, "lon": 44.3661, "size": 3000},
    "BG": {"country": "Bulgaria", "lat": 42.6977, "lon": 23.3219, "size": 3000},
    "JE": {"country": "Jordan", "lat": 31.9634, "lon": 35.9304, "size": 3000},
    "RS": {"country": "Serbia", "lat": 44.8176, "lon": 20.4633, "size": 3000},
    "NZ": {"country": "New Zealand", "lat": -36.8485, "lon": 174.7633, "size": 3000},
    "MD": {"country": "Moldova", "lat": 47.0105, "lon": 28.8638, "size": 3000},
    "LU": {"country": "Luxembourg", "lat": 49.6117, "lon": 6.13, "size": 3000},
    "MT": {"country": "Malta", "lat": 35.8997, "lon": 14.5147, "size": 3000}
}

# Omvandla till DataFrame för pydeck
df = pd.DataFrame.from_dict(countries_coords, orient='index')

# Skapa pydeck visualisering
deck = pdk.Deck(
    initial_view_state=pdk.ViewState(
        latitude=20, longitude=0, zoom=2, pitch=0
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            df,
            get_position=['lon', 'lat'],
            get_radius='size',
            get_fill_color=[0, 0, 255], 
            radius_min_pixels=10,
        ),
    ],
)

# Visa kartan
st.pydeck_chart(deck)





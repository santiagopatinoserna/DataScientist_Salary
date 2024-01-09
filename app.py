import streamlit as st
import pandas as pd
import requests
from io import StringIO
import plotly.graph_objs as go
import plotly.express as px
import numpy as np

# Titulo de la aplicacion
st.title('Global Data Jobs: Analyzing Salaries by Title and Company Size')

# Cargar y preparar los datos
@st.cache
def load_data():
    url = "https://drive.google.com/uc?export=download&id=1KYTSG4N91q8OUg4N0Z-BclO5Hm9jvL12"
    response = requests.get(url)
    content = StringIO(response.text)
    df = pd.read_csv(content)

    # Limpieza y preparacion de datos
    df = df.drop(columns=['Unnamed: 0'])
    df[["work_year", "salary", "salary_in_usd", "remote_ratio"]] = df[["work_year", "salary", "salary_in_usd", "remote_ratio"]].astype(int)

    # Mapeo de nombres de paises
    country_name_mapping = { ... }  # mismo mapeo que proporcionaste
    df['company_location'] = df['company_location'].map(country_name_mapping)

    # Agrupar y calcular el salario medio
    clustered_data = df.groupby(['company_location', 'company_size', 'job_title'])['salary_in_usd'].mean().reset_index()
    clustered_data['salary_in_usd'] = np.round(clustered_data['salary_in_usd'] / 1000, 0)
    return clustered_data

# Cargar datos
clustered_data = load_data()

# Crear el gráfico
def create_figure(data):
    # Resto del código de plotly que proporcionaste...

    return fig

# Mostrar el gráfico
fig = create_figure(clustered_data)
st.plotly_chart(fig, use_container_width=True)

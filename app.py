import streamlit as st
import pandas as pd
import requests
from io import StringIO
import numpy as np  
import streamlit as st
import plotly.graph_objs as go
import plotly.express as px

#Functions
#get data
def get_data():
    url = "https://drive.google.com/uc?export=download&id=1KYTSG4N91q8OUg4N0Z-BclO5Hm9jvL12"
    response = requests.get(url)
    content = StringIO(response.text)
    df = pd.read_csv(content)
    return df  # Return the DataFrame

def format(df):
    #Give format
    #Drop not necesary cols
    df=df.drop(columns=['Unnamed: 0'])
    #INt
    df[["work_year","salary","salary_in_usd","remote_ratio"]]=df[["work_year","salary","salary_in_usd","remote_ratio"]].astype(int)
    #Completing country names:
    country_name_mapping = {
        'DE': 'Germany',    'JP': 'Japan',    'GB': 'United Kingdom',    'HN': 'Honduras',    'US': 'United States',    'HU': 'Hungary',    'NZ': 'New Zealand',    'FR': 'France',    'IN': 'India',
        'PK': 'Pakistan',    'CN': 'China',    'GR': 'Greece',    'AE': 'United Arab Emirates',    'NL': 'Netherlands',    'MX': 'Mexico',    'CA': 'Canada',    'AT': 'Austria',    'NG': 'Nigeria',
        'ES': 'Spain',    'PT': 'Portugal',    'DK': 'Denmark',    'IT': 'Italy',    'HR': 'Croatia',    'LU': 'Luxembourg',    'PL': 'Poland',    'SG': 'Singapore',    'RO': 'Romania',    'IQ': 'Iraq',
        'BR': 'Brazil',    'BE': 'Belgium',    'UA': 'Ukraine',    'IL': 'Israel',    'RU': 'Russia',    'MT': 'Malta',    'CL': 'Chile',    'IR': 'Iran',    'CO': 'Colombia',    'MD': 'Moldova',
        'KE': 'Kenya',    'SI': 'Slovenia',    'CH': 'Switzerland',    'VN': 'Vietnam',    'AS': 'American Samoa',    'TR': 'Turkey',    'CZ': 'Czech Republic',    'DZ': 'Algeria',    'EE': 'Estonia',
        'MY': 'Malaysia',    'AU': 'Australia',    'IE': 'Ireland'}
    df['company_location'] = df['company_location'].map(country_name_mapping)
    return df

def clustering_data(df):
    # Prepare the data for plotting
    clustered_data = df.groupby(['company_location', 'company_size', 'job_title'])['salary_in_usd'].mean().reset_index()
    # Round the salaries to the nearest thousand
    clustered_data['salary_in_usd'] = np.round(clustered_data['salary_in_usd'] / 1000, 0)
    return clustered_data

def create_salary_scatter_plot(clustered_data):
    # Create mappings
    size_mapping = {'S': 'Small', 'M': 'Medium', 'L': 'Large'}
    unique_countries = clustered_data['company_location'].unique()
    country_colors = px.colors.qualitative.Plotly
    color_map = {country: country_colors[i % len(country_colors)] for i, country in enumerate(unique_countries)}
    marker_mapping = {'S': 'circle', 'M': 'square', 'L': 'diamond'}

    # Create the main scatter plot
    fig = go.Figure()

    # Add scatter plot for each company size
    for size in clustered_data['company_size'].unique():
        df_subset = clustered_data[clustered_data['company_size'] == size]
        fig.add_trace(go.Scatter(
            x=df_subset['job_title'],
            y=df_subset['salary_in_usd'],
            mode='markers',
            marker=dict(
                symbol=marker_mapping[size],
                size=10,
                color=[color_map[loc] for loc in df_subset['company_location']]
            ),
            name=size,
            hovertemplate="<b>%{text}</b><br>Company Location=%{customdata[0]}<br>Company Size=%{customdata[1]}<br>Average Salary (K USD)=%{y}",
            text=df_subset['job_title'],  # Job Title
            customdata=df_subset[['company_location', 'company_size']].values,  # Company Location and Size
            legendgroup='size',
            showlegend=False
        ))

    # Define the gray color for the legend markers
    gray_color = 'gray'


    # Add custom entries to the legend for country colors
    for country, color in color_map.items():
        fig.add_trace(go.Scatter(
            x=[None],
            y=[None],
            mode='markers',
            marker=dict(color=color, size=10),
            name=country,
            legendgroup='country'
        ))

    # Update the layout to adjust the appearance
    fig.update_layout(
        #title="<b>💼 Global Data Jobs:</b> <br><span style='font-size:22px;'>Analyzing Salaries by Title and Company Size 📊</span>",
        #title_x=0.5,
        #title_font=dict(size=24),
        xaxis=dict(title="Job Title", tickangle=-45),
        yaxis=dict(title="Average Salary in Thousands of USD"),
        legend=dict(
            title_font_size=16,
            font_size=12,
            itemsizing='constant',
            traceorder='grouped',
            groupclick="toggleitem"
        ),
        height=800,
        width=1200,
        
    )

    return fig

def main():
    st.set_page_config(layout="wide")
    # Define título y subtítulo
    title = "💼 Global Data Jobs"
    subtitle = "Analyzing Salaries by Title and Company Size"

    # Uso de marcado para título y subtítulo
    st.markdown(f"<h1 style='text-align: center;'>{title}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>{subtitle} 📊</h3>", unsafe_allow_html=True)

    df = get_data()
    df=get_data()
    df=format(df)
    clustered_data=clustering_data(df)
    #st.dataframe(clustered_data)
    # Create the plot
    fig = create_salary_scatter_plot(clustered_data)

    # Display the plot in the Streamlit app
    st.plotly_chart(fig, use_container_width=True)
    
    
    
if __name__ == '__main__':
    main()
    

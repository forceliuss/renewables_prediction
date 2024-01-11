import time
import streamlit as st
import pandas as pd
from pandas.api.types import CategoricalDtype
import plotly.express as px

import warnings
warnings.filterwarnings('ignore')

from src.cleaning import *

#Page Setup
st.set_page_config(
    page_title="Renewable Prediction",
    page_icon=":infinity:",
    layout="wide",
    initial_sidebar_state="expanded"
)

hide_st_style="""
            <style>
            #MainMenu {visibility:hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)

#Main dataframe
df = renewable_by_country()
pop = population_by_country()
dem = demand_by_country()
lcoe = lcoe_by_country()
fin = investment_by_country()

#Sidebar
st.sidebar.title('Menu')

#Selecting the Region
region_select = st.sidebar.selectbox("Region:",df['Region'].unique())

df = df.query('Region == @region_select')

#Selecting the Country
cntry_select = st.sidebar.selectbox("Country:",df['Country'].unique())


df = df.query('Country == @cntry_select')
pop = pop.query('Country == @cntry_select')
dem = dem.query('Country == @cntry_select')
lcoe = lcoe.query('Country == @cntry_select')
fin = fin.query('Country == @cntry_select')

#Selecting the year
yr_select = str(st.sidebar.slider('Year:', 2000, 2021, 2000))

df_select = df[['Country','Region','Technology',yr_select]]
pop_select = pop[['Country','Region',yr_select]]
dem_select = dem[['Country','Region',yr_select]]
yr_fin = int(yr_select)
fin_select = fin.query('Year == @yr_fin')

#Main Body
st.title(f':bar_chart: Renewable Production in {cntry_select}')


#Section 1
sec_1 = st.container()
sec_1.header(f'Annual Report - {yr_select}', divider='gray')


#KPIs Calculations
if pop_select!=0 or df_select!=0 or df!=0:
    population_total = pop_select[yr_select].sum()
    total_production = df_select[yr_select].sum()
    production_percap = total_production/population_total
    growth_production = (float(df['2021'].sum())-float(df['2000'].sum()))/float(df['2000'].sum())
    production_rate = growth_production/(2021-2000)

    total_demand = dem_select[yr_select].sum()
    hab_demand = (total_production)/(population_total)
    growth_demand = (float(dem['2021'])-float(dem['2000']))/float(dem['2000'])
    growth_rate = growth_demand/(2021-2000)

    fin_percap = (fin_select['Investment_M_USD'].sum())/population_total

    df_select['Percentage'] = round((df[yr_select]/total_production),2)

    if yr_select != '2000':
        yr = int(yr_select)
        prev_yr = str(yr-1)
        prev_production = df[prev_yr].sum()
        delta_production = ((total_production-prev_production)/total_production)
        prev_demand = dem[prev_yr].sum()
        delta_demand = ((total_demand-prev_demand)/total_demand)
    else:
        delta_production = 0
        delta_demand = 0

    #KPIs classification

    if production_percap >= 1000:
        tag = 'Very Hight'
        tag_color = 'normal'
    elif production_percap >= 500:
        tag = 'Hight'
        tag_color = 'normal'
    elif production_percap >= 250:
        tag = 'Medium'
        tag_color = 'off'
    elif production_percap >= 100:
        tag = 'Low'
        tag_color = 'inverse'
    else:
        tag = 'Very Low'
        tag_color = 'inverse'
    
    
    #Section layout section 1
    col1_s1, col2_s1, col3_s1 = sec_1.columns(3, gap='large')
    
    #Printing the metrics
    col1_s1.metric(
        label="Renewable Production:",
        value=f'{round(total_production/1000,2)} TWh',
        delta=f'{round(delta_production*100,2)} %'
    )


    col2_s1.metric(
        label="Energy Demand:",
        value=f'{round(total_demand,1)} TWh',
        delta=f'{round(delta_demand*100,2)} %'
    )

    col3_s1.metric(
        label="Population:",
        value=f'{round(population_total,1)} Millions'
    )
    st.divider()

    #Subsection 1
    sub_1 = st.container()
    sub_1.subheader(':grey[KPIs]')

    #Subsection layout subsection 1
    col1_sub1, col2_sub1 = sub_1.columns([1,2], gap='large')

    #Printing the KPIs
    col1_sub1.metric(
        label="Annual renewable (GWh / hab)",
        value=f'{round(production_percap,2)}',
        delta=tag,
        delta_color=tag_color
    )

    col1_sub1.metric(
        label="Annual investment (millions USD / hab)",
        value=f'$ {round(fin_percap,2)}'
    )

    col1_sub1.divider()
    col1_sub1.caption('(2000 - 2021)')

    col1_sub1.metric(
        label="Average energy demand growth",
        value=f'{round(growth_rate*100,2)} %'
    )


    col1_sub1.metric(
        label="Average renewable production growth",
        value=f'{round(production_rate*100,2)} %'
    )

    #Ploting the percentage of each source
    perc_fig = px.pie(
        df_select, 
        values='Percentage', 
        names='Technology',
        title='Production by source (%)',
        color_discrete_sequence=px.colors.qualitative.G10
    )
    perc_fig.update_traces(sort=False) 
    col2_sub1.plotly_chart(
        perc_fig,
        use_container_width=True
    )

    #Section 2
    sec_2 = st.container()
    sec_2.header('Overview', divider='gray')

    #Section layout section 2
    col1_s2, col2_s2 = sec_2.columns(2, gap='small')

    #Comparing the renewable production and the demand
    prod = df.drop(['Region','Technology'], axis=1)
    prod = prod.groupby('Country').sum()\
        .transpose()\
        .reset_index()\
        .rename(columns={
            'index':'Year',
            cntry_select : 'Production'
        })

    dex = dem.drop('Region', axis=1)
    dex = dex.groupby('Country').sum()*1000
    dex = dex.transpose()\
        .reset_index()\
        .rename(columns={
            'index':'Year',
            cntry_select : 'Demand'
        })

    prod_dex = pd.merge(prod, dex, left_on='Year', right_on='Year', how='left')

    #Ploting the production x demand
    dem_fig = px.line(
        prod_dex,
        x='Year',
        y=['Production','Demand'],
        title=f'Production x Demand (GWh) (2000 - 2021) ',
        color_discrete_sequence=px.colors.qualitative.G10,
        labels={
            'Year':'Year',
            'value' :'Energy (GWh)',
            'variable':''
        }
    )
    col1_s2.plotly_chart(
        dem_fig,
        use_container_width=True
    )


    fig = df.drop(columns={'Country','Region'})\
        .set_index('Technology')\
        .transpose()
    fig['Year'] = fig.index

    #Ploting the total Energy Production
    plot_fig = px.area(
        fig,
        x='Year',
        y=['Hydropower','Onshore wind','Offshore wind','Solar','Solar photovoltaic'],
        title=f'Total Energy Production (2000 - 2021) ',
        color_discrete_sequence=px.colors.qualitative.G10,
        labels={
            'Year':'Year',
            'value' :'Energy Production (GWh)' ,
            'variable':'Technology'
        }
    )
    col2_s2.plotly_chart(
        plot_fig,
        use_container_width=True
    )

    #Section 3
    sec_3 = st.container()

    #Section 4
    sec_4 = st.container()

    #Section layout
    col1_s4, col2_s4 = sec_4.columns(2,gap='large')

    fin_plt = fin.pivot_table(values='Investment_M_USD', index='Year', columns=['Technology'], aggfunc='first')\
        .reset_index()

    #Ploting the total Investment by Technology
    fin_fig = px.bar(
        fin_plt,
        x='Year',
        y=['Hydropower','Onshore wind','Offshore wind','Solar','Solar photovoltaic'],
        title=f'Investment by Technology (2000 - 2021) ',
        color_discrete_sequence=px.colors.qualitative.G10,
        labels={
            'Year':'Year',
            'value' :'Millions in investment (USD)',
            'variable':'Technology'
        }
    )
    col1_s4.plotly_chart(
        fin_fig,
        use_container_width=True
    )

    #Ploting the total Levelized cost of energy
    lcoe_fig = px.line(
        lcoe,
        x='Year',
        y=['Hydropower LCOE','Onshore wind LCOE','Offshore wind LCOE','Solar LCOE','Solar photovoltaic LCOE'],
        title=f'Levelized cost of energy (1990 - 2021) ',
        color_discrete_sequence=px.colors.qualitative.G10,
        labels={
            'Year':'Year',
            'value' :'LCOE ($/GWh)',
            'variable':'Technology'
        }
    )
    col2_s4.plotly_chart(
        lcoe_fig,
        use_container_width=True
    )

else:
    sec_1.subheader('Data not found.')

import pandas as pd
from pandas.api.types import CategoricalDtype

import numpy as np

import warnings
warnings.filterwarnings('ignore')

#Cleaning renewable dataset
def renewable_by_country():
    df = pd.read_csv('./input/renewable_dataset.csv', sep=';')
    df = df[~df['Region'].isna()]
    
    df['Technology'].replace(['Onshore wind energy','Offshore wind energy'], ['Onshore wind','Offshore wind'], inplace=True)
    
    technology = df['Technology'].unique()
    source = CategoricalDtype(categories=technology, ordered=True)
    df['Technology'] = df['Technology'].astype(source)
    
    sources = ['Hydropower','Onshore wind','Offshore wind','Solar','Solar photovoltaic']
    df = df[df['Technology'].isin(sources)]

    
    return df

def renewable_by_region():
    df = pd.read_csv('./input/renewable_dataset.csv', sep=';')
    df = df[df['Region'].isna()]
    
    df['Technology'].replace(['Onshore wind energy','Offshore wind energy'], ['Onshore wind','Offshore wind'], inplace=True)
    
    technology = df['Technology'].unique()
    source = CategoricalDtype(categories=technology, ordered=True)
    df['Technology'] = df['Technology'].astype(source)
    
    #Dropping the region sub section
    df = df.dropna(axis=1)\
        .rename(columns={'Country':'Region'})
    
    return df

#Creating a dataframe with the countryies and regions
def country_region():
    df = pd.read_csv('./input/renewable_dataset.csv', sep=';')
    df = df[~df['Region'].isna()]
    df = df[['Country','Region']]\
        .drop_duplicates()
    return df

def population_by_country():
    #Calling country_region
    df = country_region()
    
    #Importing and renaming
    pop = pd.read_csv('./input/popultion_dataset.csv', sep=',') #Values in millions
    pop = pop.rename(columns={
        'Economy_Label':'Country',
        '2000_Absolute_value_in_millions_Value':'2000',
        '2001_Absolute_value_in_millions_Value':'2001',
        '2002_Absolute_value_in_millions_Value':'2002',
        '2003_Absolute_value_in_millions_Value':'2003',
        '2004_Absolute_value_in_millions_Value':'2004',
        '2005_Absolute_value_in_millions_Value':'2005',
        '2006_Absolute_value_in_millions_Value':'2006',
        '2007_Absolute_value_in_millions_Value':'2007',
        '2008_Absolute_value_in_millions_Value':'2008',
        '2009_Absolute_value_in_millions_Value':'2009',
        '2010_Absolute_value_in_millions_Value':'2010',
        '2011_Absolute_value_in_millions_Value':'2011',
        '2012_Absolute_value_in_millions_Value':'2012',
        '2013_Absolute_value_in_millions_Value':'2013',
        '2014_Absolute_value_in_millions_Value':'2014',
        '2015_Absolute_value_in_millions_Value':'2015',
        '2016_Absolute_value_in_millions_Value':'2016',
        '2017_Absolute_value_in_millions_Value':'2017',
        '2018_Absolute_value_in_millions_Value':'2018',
        '2019_Absolute_value_in_millions_Value':'2019',
        '2020_Absolute_value_in_millions_Value':'2020',
        '2021_Absolute_value_in_millions_Value':'2021',
        '2022_Absolute_value_in_millions_Value':'2022',
        '2023_Absolute_value_in_millions_Value':'2023',
        '2024_Absolute_value_in_millions_Value':'2024',
        '2025_Absolute_value_in_millions_Value':'2025',
        '2026_Absolute_value_in_millions_Value':'2026'})
    pop = pop[pop['Country'] != 'Individual economies']
    
    
    pop = pd.merge(df, pop, left_on='Country', right_on='Country', how='left')
    pop = pop.fillna(0)
    
    return pop

def demand_by_country():
    df = country_region()
    
    dem = pd.read_csv('./input/electricity_demand_dataset.csv', sep=',')
    dem = dem[~dem['Code'].isna()]
    dem['Year'] = dem['Year'].astype(str)
    
    dem = dem.pivot_table(values='Electricity demand - TWh', index='Entity', columns=['Year'], aggfunc='first')\
        .fillna(0)\
        .reset_index()\
        .rename(columns={'Entity':'Country'})

    dem = dem[['Country','2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', 
               '2016', '2017', '2018', '2019', '2020', '2021', '2022']]
    dem = pd.merge(df, dem, left_on='Country', right_on='Country', how='left')
    
    return dem

def lcoe_by_country():
    df = country_region()
    
    lcoe = pd.read_csv('./input/LCOE_dataset.csv', sep=',')
    lcoe = lcoe.rename(columns={
        'Entity':'Country',
        'Bioenergy levelized cost of energy':'Bioenergy LCOE',
        'Geothermal levelized cost of energy':'Geothermal LCOE',
        'Offshore wind levelized cost of energy': 'Offshore wind LCOE',
        'Solar photovoltaic levelized cost of energy': 'Solar photovoltaic LCOE',
        'Concentrated solar power levelized cost of energy' : 'Solar LCOE',
        'Hydropower levelized cost of energy' : 'Hydropower LCOE',
        'Onshore wind levelized cost of energy' : 'Onshore wind LCOE'
    })
    
    
    lcoe = lcoe.drop('Code', axis=1)\
        .fillna(0).sort_values('Year')
        
    lcoe = pd.merge(df, lcoe, left_on='Country', right_on='Country', how='left')
    
    return lcoe

def investment_by_country():
    invst = pd.read_csv('./input/investment_dataset.csv', sep=',')
    invst = invst.rename(columns={
        'Country/area':'Country',
        'Public Investments (2020 million USD)':'Investment_M_USD'
    })
    invst['Technology'].replace(['On-grid Solar photovoltaic', 'Off-grid Solar photovoltaic'], 'Solar photovoltaic', inplace=True)
    invst['Technology'].replace(['Onshore wind energy', 'Offshore wind energy'], ['Onshore wind','Offshore wind'], inplace=True)
    invst['Technology'].replace(['Concentrated solar power'], 'Solar', inplace=True)
    invst['Technology'].replace(['Renewable hydropower'], 'Hydropower', inplace=True)
    
    return invst
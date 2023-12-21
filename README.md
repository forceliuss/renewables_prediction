# Renewable Predigtion (2/3)
## Predigtion of renewable energy analysis dashboard

This is an experimental project!! The main objective of this project is to create a dashboard to analyze the data from several sources and develop a common place for these insights.This is a part of a bigger project, to check more about the first part. (links below)

## Medium Article
Check the part 1 here:
<a href='https://medium.com/@forceliuss/renewable-insight-eda-with-streamlit-006a4a0c7b6c' target='_blank'>Renewable Insights — EDA with Streamlit</a>

## Datasets

* Renewable Energy Production by Country (2000 - 2021)
<a href='https://pxweb.irena.org/pxweb/en/IRENASTAT/IRENASTAT__Power%20Capacity%20and%20Generation/REGEN_2023_cycle2.px/' target='_blank'>IRENA</a>

* Investment in Renewable by Source (1960 - 2022)
<a href='https://ourworldindata.org/grapher/investment-in-renewable-energy-by-technology?facet=none' target='_blank'>Our World in Data</a>


## Code objectives

 - Import and clear the data from the datasets
 - Combine all the different sources into a main dataframe
 - Analyze the dataframe and create metrics
 - Create a local dashboard (StreamLit)
 - Sort the global datasets by countries

## Libraries

* Pandas -`pip install pandas`
* Numpy -`pip install numpy`
* StreamLit -`pip install streamlit`
* Matplotlib -`pip install matplotlib`
* Plotly Express - `pip install plotly`

## How to run

1. Clone this project 
2. Run your python kernel
3. Install all the libraries above
4. Run `main.py` through the streamlit command `streamlit run main.py`

import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt

topo = ['Date',
'Time',
'Temp OUT',
'Hi temp',
'Low Temp',
'Out Hum',
'Dew Pt.',
'Wind Speed',
'Wind Dir',
'Wind Run',
'Hi Speed',
'Hi Dir',
'Wind Chill',
'Heat Index',
'THW Index',
'THSW Index',
'Bar',
'Rain',
'Rain Rate',
'Solar Rad',
'Solar Energy',
'Hi Solar Rad',
'UV Index',
'UV Dose',
'Hi UV',
'Heat D-D',
'Cool D-D',
'In Temp',
'In Hum',
'In Dew',
'In Heat',
'In EMC',
'In Air Density',
'ET',
'Wind Samp',
'Wind TX',
'ISS Recept',
'Arc Int.']
if 1!=2:
    dados='c:/AVELL/Davis/dall.txt'
    dados='c:/Users/LAVAT/Desktop/davis_teste_dash.txt'
    #c:\Users\LAVAT\Desktop\

    
    davis = pd.read_csv(dados, sep='\t', dtype={'Temp OUT': float, 'Out Hum': float, 'Rain': float, 'UV Index': float,'UV Dose':float,'Bar':float,'Dew Pt.':float,'Heat Index':float}, na_values=['---','------'], header=1,names=topo)

    davis=davis.sort_values(by='Date')
    davis["Date"] = pd.to_datetime(davis["Date"])
    davis['Year']=davis['Date'].dt.year
    davis['Month']=davis['Date'].dt.month
    davis['Year']= pd.to_numeric(davis['Year'], errors='coerce')
    bar_avg=davis[['Bar','Year']].groupby('Year').mean()
    

    davis_2024=davis[davis['Year']==2024]
    
    
    #davis = davis[davis['Year'] != 2018]
import dash

from dash import dcc, html
numeric_columns = ['Year', 'Rain','Temp OUT', 'Out Hum','UV Index','UV Dose','Wind Speed','Dew Pt.','Heat Index']
davis = davis[numeric_columns]



davis_mean = davis.groupby('Year').agg({'Rain': 'sum','Temp OUT': 'mean','Out Hum': 'mean','UV Index':'max','UV Dose':'max','Wind Speed':'mean','Dew Pt.':'mean','Heat Index':'mean'}).reset_index()



app = dash.Dash(__name__)

font_family = 'Arial, sans-serif'
title_font_size = '30px'
subtitle_font_size = '24px'
font_color = '#333'


app.layout = html.Div(children=[
    html.H1(children='Dashboard Meteorológico - Davis Vantage Pro 2', style={'font-family': font_family, 'font-size': title_font_size}),

    html.Div(children='''
        Dados da Estação Davis
    ''', style={'font-family': font_family, 'font-size': subtitle_font_size}),

     dcc.Graph(
        id='rain-natal',
        figure=px.line(davis_mean, x='Year', y='Rain', title='Rain - Natal Station', labels={'Rain': 'Rain (mm/Year)'}).update_xaxes(categoryorder="total ascending")
    ),

    dcc.Graph(
        id='bar-natal',
        figure=px.line(bar_avg, x=bar_avg.index, y='Bar', title='Pressure - Natal Station', labels={'Bar': 'Atm Pressure (hPa)'})    ),

   
   
    

    

    
    dcc.Graph(
        id='temp-out-natal',
        figure=px.line(davis_mean, x='Year', y='Temp OUT', title='Temp Out Mean - Natal Station', labels={'Temp OUT': 'Temp OUT (°C)'}).update_xaxes(categoryorder="total ascending")
    ),

    dcc.Graph(
        id='out-hum-natal',
        figure=px.line(davis_mean, x='Year', y='Out Hum', title='Out Hum Mean - Natal Station', labels={'Out Hum': 'Out Hum (%)'}).update_xaxes(categoryorder="total ascending")
    ),

    dcc.Graph(
        id='Dew Point-natal',
        figure=px.line(davis_mean, x='Year', y='Dew Pt.', title='Dew Pt. Mean - Natal Station', labels={'Dew Pt.': 'Dew Point (°C)'}).update_xaxes(categoryorder="total ascending")
    ),



    dcc.Graph(
        id='heat-index-natal',
        figure=px.line(davis_mean, x='Year', y='Heat Index', title='Heat Index - Natal Station', labels={'Temp OUT': 'Temp OUT (°C)'}).update_xaxes(categoryorder="total ascending")
    ),

    
    

   

    dcc.Graph(
        id='uv-index-natal',
        figure=px.line(davis_mean, x='Year', y='UV Index', title='UV Index Max - Natal Station', labels={'UV Index': 'UV Index'}).update_xaxes(categoryorder="total ascending")
    ),
    dcc.Graph(
        id='uv-dose-natal',
        figure=px.line(davis_mean, x='Year', y='UV Dose', title='UV Dose Max - Natal Station', labels={'UV Dose': 'UV Dose'}).update_xaxes(categoryorder="total ascending")
    ),
    dcc.Graph(
        id='Wind Speed',
        figure=px.line(davis_mean, x='Year', y='Wind Speed', title='Wind Speed Mean- Natal Station', labels={'Wind Speed': 'Wind Speed (m/s)'}).update_xaxes(categoryorder="total ascending")
    ),
    
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)  
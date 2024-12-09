import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados
topo = ['Date', 'Time', 'Temperatura', 'Hi temp', 'Low Temp', 'Umidade', 'Dew Pt.', 'Velocidade do Vento', 'Wind Dir', 'Wind Run', 'Hi Speed', 'Hi Dir', 'Wind Chill', 'Heat Index', 'THW Index', 'THSW Index', 'Pressão Atm.', 'Precipitação', 'Rain Rate', 'Solar Rad', 'Solar Energy', 'Hi Solar Rad', 'UVI', 'UV Dose', 'Hi UV', 'Heat D-D', 'Cool D-D', 'In Temp', 'In Hum', 'In Dew', 'In Heat', 'In EMC', 'In Air Density', 'ET', 'Wind Samp', 'Wind TX', 'ISS Recept', 'Arc Int.']
dados = 'd11.txt'

davis = pd.read_csv(dados, sep='\t', dtype={'Temp OUT': float, 'Out Hum': float, 'Rain': float, 'UV Index': float, 'UV Dose': float, 'Bar': float, 'Dew Pt.': float, 'Heat Index': float}, na_values=['---', '------'], header=1, names=topo)
davis["Date"] = pd.to_datetime(davis["Date"])
davis['Dia'] = davis['Date'].dt.day
davis['Year'] = davis['Date'].dt.year
davis['Mês'] = davis['Date'].dt.month

# Definindo as variáveis para as opções no Streamlit
anos_lista = list(davis['Year'].unique())
meses_lista = list(davis['Mês'].unique())

# Streamlit UI
st.title('Dashboard de Dados Meteorológicos - Estação Davis')

# Seleção de ano e mês
ano_selecionado = st.selectbox('Selecione o ano', anos_lista, index=0)
mes_selecionado = st.selectbox('Selecione o mês', meses_lista, index=0)

# Filtrando os dados
davis_selecionado = davis[(davis['Year'] == ano_selecionado) & (davis['Mês'] == mes_selecionado)]

# Exibindo gráfico
fig = px.scatter(davis_selecionado, x='Date', y='Temperatura', title='Temperatura ao longo do mês')
st.plotly_chart(fig)

# Exibindo tabela
st.write(davis_selecionado[['Date', 'Temperatura', 'Precipitação']])


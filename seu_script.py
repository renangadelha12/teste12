import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
# Carregar os dados
topo = ['Date', 'Time', 'Temperatura', 'Hi temp', 'Low Temp', 'Umidade', 'Dew Pt.', 'Velocidade do Vento', 'Wind Dir', 'Wind Run', 'Hi Speed', 'Hi Dir', 'Wind Chill', 'Heat Index', 'THW Index', 'THSW Index', 'Pressão Atm.', 'Precipitação', 'Rain Rate', 'Solar Rad', 'Solar Energy', 'Hi Solar Rad', 'UVI', 'UV Dose', 'Hi UV', 'Heat D-D', 'Cool D-D', 'In Temp', 'In Hum', 'In Dew', 'In Heat', 'In EMC', 'In Air Density', 'ET', 'Wind Samp', 'Wind TX', 'ISS Recept', 'Arc Int.']
dados = 'dall.txt'

davis = pd.read_csv(dados, sep='\t', dtype={'Temp OUT': float, 'Out Hum': float, 'Rain': float, 'UV Index': float, 'UV Dose': float, 'Bar': float, 'Dew Pt.': float, 'Heat Index': float}, na_values=['---', '------'], header=1, names=topo)
davis["Date"] = pd.to_datetime(davis["Date"])
davis['Dia'] = davis['Date'].dt.day
davis['Year'] = davis['Date'].dt.year
davis['Mês'] = davis['Date'].dt.month
davis['Time'] = pd.to_datetime(davis['Time'], format='%H:%M').dt.time


# Definindo as variáveis para as opções no Streamlit
anos_lista = list(davis['Year'].unique())
meses_lista = list(davis['Mês'].unique())
dias_lista=list(davis['Date'].unique())

# Streamlit UI
st.title('Dashboard de Dados Meteorológicos')

# Seleção de ano , mês e dia
ano_selecionado = st.selectbox('Selecione o ano', anos_lista, index=0)
mes_selecionado = st.selectbox('Selecione o mês', meses_lista, index=0)
dia_selecionado = st.selectbox('Selecione o dia',dias_lista,index=0)

# Filtrando os dados
davis_selecionado = davis[(davis['Year'] == ano_selecionado) & (davis['Mês'] == mes_selecionado)]
davis_selecionado1 = davis[davis['Date'] == dia_selecionado]
#    dia_escholido_dropdown=davis[davis['Data'] == s_day]

# Exibindo gráfico com Altair
chart = alt.Chart(davis_selecionado1).mark_line().encode(
    x='Time:T',
    y='Temperatura:Q',
    tooltip=['Time:T', 'Temperatura:Q']
).properties(
    title='Temperatura ao longo do mês'
)

st.altair_chart(chart, use_container_width=True)

# Exibindo tabela com os dados selecionados
st.write(davis_selecionado1[['Time', 'Temperatura', 'Precipitação']])

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


# Definindo as variáveis para as opções no Streamlit
#anos_lista = list(davis['Year'].unique())
#meses_lista = list(davis['Mês'].unique())
dias_lista=list(davis['Date'].unique())

# Usando HTML para estilizar o título
st.markdown('<h1 style="color:green">Dashboard de Dados Meteorológicos</h1>', unsafe_allow_html=True)


# Seleção de ano , mês e dia
#ano_selecionado = st.selectbox('Selecione o ano', anos_lista, index=0)
#mes_selecionado = st.selectbox('Selecione o mês', meses_lista, index=0)
dia_selecionado = st.selectbox('Selecione o dia',dias_lista,index=0)

# Filtrando os dados
#davis_selecionado = davis[(davis['Year'] == ano_selecionado) & (davis['Mês'] == mes_selecionado)]
davis_selecionado1 = davis[davis['Date'] == dia_selecionado]
davis_selecionado1['Hora'] = davis_selecionado1['Time']
davis_selecionado1['Hi Dir'] = davis_selecionado1['Hi Dir'].replace({'N': 0, 'NNE': 22.5, 'NE': 45.0, 'ENE': 67.5, 'E': 90.0, 'ESE': 112.5,
                                         'SE': 135.0, 'SSE': 157.5, 'S': 180, 'SSW': 202.5, 'SW': 225.0, 'WSW': 247.5,
                                         'W': 270, 'WNW': 292.5, 'NW': 315, 'NNW': 337.5})

davis_selecionado1['Wind Dir'] = davis_selecionado1['Wind Dir'].replace({'N': 0, 'NNE': 22.5, 'NE': 45.0, 'ENE': 67.5, 'E': 90.0, 'ESE': 112.5,
                                              'SE': 135.0, 'SSE': 157.5, 'S': 180, 'SSW': 202.5, 'SW': 225.0, 'WSW': 247.5,
                                              'W': 270, 'WNW': 292.5, 'NW': 315, 'NNW': 337.5})

# Exibindo gráfico com Altair
chart = alt.Chart(davis_selecionado1).mark_line().encode(
    x=alt.X('Hora', title='Hora do Dia'),  # Agora 'Hora' é do tipo temporal
    y=alt.Y('Temperatura', title='Temperatura (°C)'),
    tooltip=['Hora', 'Temperatura:Q']  # Exibindo hora e temperatura no tooltip
).properties(
    title='Temperatura ao longo do dia selecionado'
)

# Exibindo o gráfico no Streamlit
st.altair_chart(chart, use_container_width=True)


wind_rose = alt.Chart(davis_selecionado1).mark_bar().encode(
    theta=alt.Theta(field="Wind Dir", type="quantitative", bin=alt.Bin(maxbins=16)),  # Direção do vento no eixo angular (dividido em 16 bins)
    radius=alt.Radius(field="Velocidade do Vento", type="quantitative"),  # Intensidade do vento no eixo radial
    color=alt.Color(field="Wind Dir", type="quantitative", scale=alt.Scale(scheme='category20c')),  # Cor por direção
    tooltip=["Wind Dir", "Velocidade do Vento:Q"]  # Tooltip para mostrar direção e velocidade
).properties(
    title='Rosa dos Ventos - Dia Selecionado',
    width=500,
    height=500
).configure_view(
    stroke=None  # Remover bordas do gráfico
)

# Exibindo o gráfico no Streamlit
st.altair_chart(wind_rose, use_container_width=True)

# Exibindo os dados em formato de tabela
st.write(davis_selecionado1[['Hora', 'Temperatura', 'Precipitação','Wind Dir','Velocidade do Vento']])



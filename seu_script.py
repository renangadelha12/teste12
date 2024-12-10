import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
# Carregar os dados
st.set_page_config(page_title="Dashboard de Dados Meteorológicos", layout="wide")
st.markdown(
    """
    <style>
    /* Controlar largura do conteúdo */
    .main {
        max-width: 90%; /* Define a largura máxima */
        margin: 0 auto; /* Centraliza horizontalmente */
        background-color: #e6f7ff; /* Azul claro */
        padding: 20px; /* Adiciona espaço interno */
        border-radius: 10px; /* Suaviza bordas */
    }
    /* Alterar fundo de toda a página */
    body {
        background-color: #e6f7ff; /* Azul claro */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Seu código do dashboard continua aqui
st.markdown('<h1 style="color:green">Dashboard de Dados Meteorológicos - Vantage Pro 2</h1>', unsafe_allow_html=True)
topo = ['Date', 'Time', 'Temperatura', 'Hi temp', 'Low Temp', 'Umidade', 'Dew Pt.', 'Velocidade do Vento', 'Wind Dir', 'Wind Run', 'Hi Speed', 'Hi Dir', 'Wind Chill', 'Heat Index', 'THW Index', 'THSW Index', 'Pressão Atm.', 'Precipitação', 'Rain Rate', 'Solar Rad', 'Solar Energy', 'Hi Solar Rad', 'UVI', 'UV Dose', 'Hi UV', 'Heat D-D', 'Cool D-D', 'In Temp', 'In Hum', 'In Dew', 'In Heat', 'In EMC', 'In Air Density', 'ET', 'Wind Samp', 'Wind TX', 'ISS Recept', 'Arc Int.']
dados = 'dall.txt'

davis = pd.read_csv(dados, sep='\t', dtype={'Temp OUT': float, 'Out Hum': float, 'Rain': float, 'UV Index': float, 'UV Dose': float, 'Bar': float, 'Dew Pt.': float, 'Heat Index': float}, na_values=['---', '------'], header=1, names=topo)
davis["Date"] = pd.to_datetime(davis["Date"])
davis['Dia'] = davis['Date'].dt.day
davis['Year'] = davis['Date'].dt.year
davis['Mês'] = davis['Date'].dt.month


# Definindo as variáveis para as opções no Streamlit
anos_lista = list(davis['Year'].unique())
meses_lista = list(davis['Mês'].unique())
dias_lista=list(davis['Date'].unique())
variaveis=list(topo)
# Usando HTML para estilizar o título
st.markdown('<h1 style="color:green">Dashboard de Dados Meteorológicos - Vantage Pro 2</h1>', unsafe_allow_html=True)


# Seleção de ano , mês e dia
ano_selecionado = st.selectbox('Selecione o ano', anos_lista, index=0)
#mes_selecionado = st.selectbox('Selecione o mês', meses_lista, index=0)
dia_selecionado = st.selectbox('Selecione o dia',dias_lista,index=0)
variavel_grafico=st.selectbox('Selecione a variavel para graficar',variaveis,index=0)

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
davis_selecionado1['Hora'] = pd.to_datetime(davis_selecionado1['Hora'], format='%H:%M').dt.strftime('%H:%M')

chart = alt.Chart(davis_selecionado1).mark_line().encode(
    x=alt.X('Hora:O', title='Hora do Dia'),
    y=alt.Y(f'{variavel_grafico}:Q', title=f'{variavel_grafico}'), 
    tooltip=['Hora', 'Temperatura:Q']
).properties(
    title='Temperatura ao longo do dia selecionado'
)

st.altair_chart(chart, use_container_width=True)

davis_selecionado_ano = davis[davis['Year'] == ano_selecionado]

precipitacao_por_mes = davis_selecionado_ano.groupby('Mês')['Precipitação'].sum().reset_index()

# Calculando o total de precipitação no ano
total_precipitacao_ano = precipitacao_por_mes['Precipitação'].sum()

# Calculando a proporção de precipitação para cada mês
precipitacao_por_mes['Proporcao'] = precipitacao_por_mes['Precipitação'] / total_precipitacao_ano * 100

# Criando o gráfico setorial de distribuição de precipitação mensal
chart_rain = alt.Chart(precipitacao_por_mes).mark_arc().encode(
    theta=alt.Theta('Proporcao:Q', title='Proporção de Precipitação no Ano (%)'),
    color=alt.Color('Mês:O', scale=alt.Scale(scheme='accent'), title='Mês'),  
    tooltip=['Mês:O', 'Precipitação:Q', 'Proporcao:Q']
).properties(
    title=f'Distribuição da Precipitação no Ano {ano_selecionado}'
)

# Exibindo o gráfico no Streamlit
st.altair_chart(chart_rain, use_container_width=True)

# Exibindo os dados em formato de tabela
#st.write(davis_selecionado1[['Hora', 'Temperatura', 'Precipitação','Wind Dir','Velocidade do Vento']])



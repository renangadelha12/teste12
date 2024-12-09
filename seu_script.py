import streamlit as st  # Por convenção, vamos apelidar o streamlit de st
import pandas as pd  # Importando a biblioteca Pandas

# Aqui definimos o título da página e o layout como wide
st.set_page_config(page_title="Meu Dashboard", layout="wide")

# Título do seu dashboard
st.write("""
# Meu primeiro Dashboard
Abaixo veremos a tabela de dados carregada do arquivo CSV
""")

# Importando a base de dados e transformando em um DataFrame do pandas
df = pd.read_csv('NSE-TATAGLOBAL11.csv', sep=',') 

# Exibindo o DataFrame na interface do Streamlit
st.dataframe(df)  # ou st.write(df) para exibir de outra forma

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Ler o arquivo CSV
data = pd.read_csv('/content/age_gender.csv')

# Exibir o gráfico no Streamlit
st.title('Gráfico a partir de um arquivo CSV')
st.line_chart(data)

# Exibir a tabela de dados
st.subheader('Dados')
st.write(data)

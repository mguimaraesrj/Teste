import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Ler o arquivo CSV
data = pd.read_csv('caminho/para/o/arquivo.csv')

# Exibir o gráfico no Streamlit
st.title('Gráfico de Pizza a partir de um arquivo CSV')
fig, ax = plt.subplots()
ax.pie(data['Valores'], labels=data['Categorias'], autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Equal aspect ratio garante um gráfico de pizza circular
st.pyplot(fig)

# Exibir a tabela de dados
st.subheader('Dados')
st.write(data)

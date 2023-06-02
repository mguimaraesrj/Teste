import streamlit as st
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd

def obter_informacoes_commodity(commodity):
    url = f"https://www.noticiasagricolas.com.br/cotacoes/{commodity}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Obter o título
    titulo = soup.find('a', {'href': f'/cotacoes/{commodity}'}).text
    st.write("Título:", titulo)

    # Obter as informações na segunda coluna (td) da segunda linha (tr)
    linha_tabela = soup.find_all('tr')[1]
    dados_tabela = linha_tabela.find_all('td')[1].text
    st.write("Informação:", dados_tabela)

    link_histórico = soup.find('a', {"class": "mostrar-historico"})["href"]
    st.write("Link do histórico:", link_histórico)

    # Acessar o link do histórico e raspar os dados da página
    url_hist = f"https://www.noticiasagricolas.com.br{link_histórico}"
    response_hist = requests.get(url_hist)
    soup_hist = BeautifulSoup(response_hist.text, 'html.parser')

    # Realizar o scraping dos dados da página histórico
    dados_td = soup_hist.find_all('td')
    historico_dados = []
    for i, td in enumerate(dados_td):
        if i < 30:
            historico_dados.append(float(td.text.replace(',', '.')))
        else:
            break

    st.subheader("Dados do histórico (Últimos 30 dias)")
    st.write(historico_dados)

    # Criar um DataFrame com os dados históricos
    df = pd.DataFrame(historico_dados, columns=["Preço"])
    df.index = pd.date_range(end=pd.Timestamp.now().date(), periods=len(df), freq='D')

    # Plotar o gráfico de linha
    st.subheader("Variação do Preço (Últimos 30 dias)")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df.index, df['Preço'], marker='o', linestyle='-')
    ax.set_xlabel('Data')
    ax.set_ylabel('Preço')
    ax.set_xticklabels(df.index, rotation=45)
    st.pyplot(fig)

# Título da página
st.title("Obter Informações de Commodity")

# Obter a commodity desejada do usuário
commodity = st.text_input("Digite o nome da commodity").lower().replace(' ', '-')

# Verificar se o usuário digitou uma commodity
if commodity:
    # Chamar a função com a commodity fornecida pelo usuário
    obter_informacoes_commodity(commodity)

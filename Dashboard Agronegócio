import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
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

    # Armazenar os valores dos dados em uma lista, ignorando os resultados indesejados
    valores = []
    for td in dados_td:
        texto = td.text.strip()
        if "/" not in texto and "%" not in texto:
            match = re.search(r'\d+\.\d+', texto)
            if match:
                valor = float(match.group())
                valores.append(valor)

    # Criar um DataFrame com os valores e a data como índice
    df = pd.DataFrame(valores, columns=["Preço"])
    df.index = pd.date_range(start='01/01/2023', periods=len(df), freq='D')

    # Plotar o gráfico de variação do preço para os últimos 30 dias
    st.subheader("Variação do Preço (Últimos 30 dias)")
    plt.figure(figsize=(10, 6))
    plt.plot(df.index[-30:], df['Preço'][-30:], marker='o', linestyle='-')
    plt.xlabel('Data')
    plt.ylabel('Preço')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot()

# Título da página
st.title("Obter Informações de Commodity")

# Obter a commodity desejada do usuário
commodity = st.text_input("Digite o nome da commodity").lower().replace(' ', '-')

# Verificar se o usuário digitou uma commodity
if commodity:
    # Chamar a função com a commodity fornecida pelo usuário
    obter_informacoes_commodity(commodity)

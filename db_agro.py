import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime

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

    # Para obter o histórico de preços do produto
    link_historico = soup.find('a', {"class": "mostrar-historico"})["href"]
    st.write("Link do histórico:", link_historico)

    # Acessar o novo link gerado por "link_historico"
    novo_link = f"https://www.noticiasagricolas.com.br{link_historico}"
    novo_response = requests.get(novo_link)
    novo_soup = BeautifulSoup(novo_response.text, 'html.parser')

    # Encontrar todas as informações com a tag <td> na nova página
    resultados = novo_soup.find_all('td')

    # Organizar os resultados em listas separadas para cada coluna
    tipo_resultado = 0
    datas = []
    precos = []

    for resultado in resultados:
        texto = resultado.text.strip()

        if tipo_resultado == 0:
            datas.append(texto)
        elif tipo_resultado == 1:
            precos.append(float(texto))

        tipo_resultado += 1
        if tipo_resultado == 3:
            tipo_resultado = 0

        if len(datas) >= 11:
            break

    # Verificar se as listas têm o mesmo tamanho
    tamanho = min(len(datas), len(precos))

    # Converter as datas para o formato correto
    datas_formatadas = [datetime.strptime(data, "%d/%m/%Y") for data in datas[:tamanho]]

    # Criar um dataframe com as colunas "Datas" e "Preços"
    df = pd.DataFrame({"Datas": datas_formatadas, "Preços": precos[:tamanho]})

    # Ordenar o dataframe por preço em ordem crescente
    df = df.sort_values(by="Preços")

    # Exibir o dataframe
    st.write(df)

    # Plotar o gráfico
    fig, ax = plt.subplots()
    ax.plot(df["Datas"], df["Preços"])
    ax.set_xlabel("Datas")
    ax.set_ylabel("Preços")
    ax.set_title("Histórico de Preços")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

# Cabeçalho do aplicativo
st.title("Histórico de Preços de Commodity")

# Obter a commodity desejada do usuário
commodity = st.text_input("Digite o nome da commodity")

# Converter a commodity para letras minúsculas
commodity = commodity.lower()

# Chamar a função com a commodity fornecida pelo usuário
if st.button("Obter Informações"):
    obter_informacoes_commodity(commodity)

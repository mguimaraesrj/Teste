import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

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
    datas = []
    precos = []

    for resultado in resultados:
        if len(datas) >= 11:
            break

        texto = resultado.text.strip()

        if len(texto) > 0:
            if len(datas) % 3 == 0:
                datas.append(texto)
            elif len(datas) % 3 == 1:
                precos.append(texto)

    # Criar um dataframe com as colunas "Datas" e "Preços"
    df = pd.DataFrame({"Datas": datas, "Preços": precos})

    # Exibir o dataframe
    st.write(df)

# Obter a commodity desejada do usuário
commodity = input("Digite o nome da commodity: ").lower().replace(' ', '-')

# Chamar a função com a commodity fornecida pelo usuário
obter_informacoes_commodity(commodity)

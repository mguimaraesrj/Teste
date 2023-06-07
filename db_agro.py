import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt


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
            precos.insert(0, texto)  # Inverter a ordem dos preços, inserindo-os no início da lista

        tipo_resultado += 1
        if tipo_resultado == 3:
            tipo_resultado = 0

        if len(datas) >= 11:
            break

    # Verificar se as listas têm o mesmo tamanho
    tamanho = min(len(datas), len(precos))

    # Criar um dataframe com as colunas "Datas" e "Preços"
    df = pd.DataFrame({"Datas": datas[:tamanho], "Preços": precos[:tamanho]})

    # Inverter a ordem das datas
    df = df.iloc[::-1]

    # Exibir o dataframe
    st.write(df)

    # Plotar o gráfico
    plt.plot(df["Datas"], df["Preços"])
    plt.xlabel("Datas")
    plt.ylabel("Preços")
    plt.title("Histórico de Preços")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot()


# Título do aplicativo
st.title("Histórico de Preços de Commodities")

# Obter a commodity desejada do usuário
commodity = st.text_input("Digite o nome da commodity").lower().replace(' ', '-')

# Verificar se o usuário digitou uma commodity
if commodity:
    # Chamar a função com a commodity fornecida pelo usuário
    obter_informacoes_commodity(commodity)

import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import plotly.express as px

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
    variacoes = []

    for i, resultado in enumerate(resultados):
        texto = resultado.text.strip()

        if len(texto) > 0:
            if i % 3 == 0:
                datas.append(texto)
            elif i % 3 == 1:
                precos.append(texto)
            else:
                variacoes.append(texto)

    # Verificar se as listas têm o mesmo comprimento
    min_length = min(len(datas), len(precos), len(variacoes))
    datas = datas[:min_length]
    precos = precos[:min_length]
    variacoes = variacoes[:min_length]

    # Criar um dataframe com as colunas "Datas", "Preços" e "Variação %"
    df = pd.DataFrame({"Datas": datas, "Preços": precos, "Variação %": variacoes})

    # Converter a coluna de preços para numérico
    df["Preços"] = pd.to_numeric(df["Preços"], errors="coerce")

    # Exibir o dataframe
    st.write(df)

    # Verificar se há dados suficientes para plotar o gráfico
    if len(df) >= 2:
        # Criar um gráfico de linha interativo com base nos preços históricos usando a biblioteca plotly
        fig = px.line(df, x="Datas", y="Preços", title="Histórico de Preços")
        st.plotly_chart(fig)
    else:
        st.write("Não há dados suficientes para plotar o gráfico.")

# Criar a interface do Streamlit
st.title("Obter Informações de Commodity")
commodity = st.text_input("Digite o nome da commodity")
if st.button("Obter Informações"):
    obter_informacoes_commodity(commodity.lower().replace(' ', '-'))

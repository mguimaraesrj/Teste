import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import altair as alt
from datetime import datetime

def obter_informacoes_commodity(commodity):
    url = f"https://www.noticiasagricolas.com.br/cotacoes/{commodity}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Obter o título
    titulo = soup.find('a', {'href': f'/cotacoes/{commodity}'}).text

    # Obter as informações na segunda coluna (td) da segunda linha (tr)
    linha_tabela = soup.find_all('tr')[1]
    dados_tabela = linha_tabela.find_all('td')[1].text

    # Exibir a cotação atual
    st.sidebar.write("**Cotação atual:** R$", dados_tabela)

    # Para obter o histórico de preços do produto
    link_historico = soup.find('a', {"class": "mostrar-historico"})["href"]
    link_historico_completo = f"https://www.noticiasagricolas.com.br{link_historico}"

    # Acessar o novo link gerado por "link_historico_completo"
    novo_response = requests.get(link_historico_completo)
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
            precos.append(texto)

        tipo_resultado += 1
        if tipo_resultado == 3:
            tipo_resultado = 0

        if len(datas) >= 11:
            break

    # Reverter a ordem dos preços
    precos.reverse()

    # Verificar se as listas têm o mesmo tamanho
    tamanho = min(len(datas), len(precos))

    # Converter as datas para o formato correto
    datas_formatadas = [datetime.strptime(data, "%d/%m/%Y").strftime("%d/%m/%Y") for data in datas[:tamanho]]

    # Criar um dataframe com as colunas "Datas" e "Preços"
    df = pd.DataFrame({"Datas": datas_formatadas, "Preços": precos[:tamanho]})

    # Ordenar o dataframe por data
    df = df.sort_values(by="Datas")

    # Exibir o título "Histórico de Preços"
    st.subheader("Histórico de Preços")
    st.markdown(link_historico_completo)

    # Exibir o dataframe com as colunas "Datas" e "Preços" apenas se o botão "Exibir Tabela" for clicado
    if st.button("Exibir Tabela"):
        st.write(df[["Datas", "Preços"]])

    # Plotar o gráfico
    plotar_grafico(df)

    # Exibir a frase após o gráfico, se a commodity for "Boi Gordo"
    if commodity == "boi-gordo":
        st.markdown("**Não é à toa que o PIB começa com P de Pecuária! - Léo & Raphael**")


def plotar_grafico(df):
    # Configurar a faixa de valores do eixo x e y
    x_range = [df["Datas"].min(), df["Datas"].max()]
    y_range = [df["Preços"].min(), df["Preços"].max()]

    # Plotar o gráfico usando Altair
    chart = alt.Chart(df).mark_line().encode(
        x='Datas',
        y='Preços'
    ).properties(
        width=600,
        height=300
    ).interactive()

    # Exibir o gráfico usando Streamlit
    st.altair_chart(chart, use_container_width=True)


# Estilo do título
title_html = """
    <style>
        .title h1 {
            color: #FFFFFF;
            background-color: #00C851;
            padding: 20px;
            font-size: 48px; /* Aumente o tamanho da fonte para 48px */
            margin: 0;
        }
    </style>
"""

# Cabeçalho do aplicativo
st.markdown(title_html, unsafe_allow_html=True)
st.markdown('<div class="title"><h2>Agroboard - Dashboard Agro 🌱</h2></div>', unsafe_allow_html=True)

# Restante do código...

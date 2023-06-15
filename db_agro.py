import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
from datetime import datetime

def obter_informacoes_commodity(commodity):
    # ... código anterior ...

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

    # Reverter a ordem dos preços
    precos.reverse()

    # Verificar se as listas têm o mesmo tamanho
    tamanho = min(len(datas), len(precos))

    # Converter as datas para o formato correto
    datas_formatadas = [datetime.strptime(data, "%d/%m/%Y").strftime("%d/%m/%Y") for data in datas[:tamanho]]

    # Criar um dataframe com as colunas "Datas" e "Preços"
    df = pd.DataFrame({"Datas": datas_formatadas, "Preços": precos[:tamanho]})

    # Ordenar o dataframe por preço
    df = df.sort_values(by="Preços")

    # Exibir o título "Histórico de Preços"
    st.subheader("Histórico de Preços")
    st.markdown(link_historico_completo)

    # Exibir o dataframe com as colunas "Datas" e "Preços" apenas se o botão "Exibir Tabela" for clicado
    if st.button("Exibir Tabela"):
        st.write(df[["Datas", "Preços"]])

    # Plotar o gráfico ordenado por preço
    chart = st.line_chart(df.set_index("Datas"))
    chart.x_range = [df["Datas"].min(), df["Datas"].max()]  # Configurar a faixa de valores do eixo x


# Restante do código permanece o mesmo...

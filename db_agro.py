import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
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
            precos.insert(0, texto)  # Inverter a ordem dos preços, inserindo-os no início da lista

        tipo_resultado += 1
        if tipo_resultado == 3:
            tipo_resultado = 0

        if len(datas) >= 11:
            break

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
    chart = st.line_chart(df.set_index("Datas"))
    chart.x_range = [df["Datas"].min(), df["Datas"].max()]  # Configurar a faixa de valores do eixo x


# Estilo do título
title_html = """
    <style>
        .title h1 {
            color: #FFFFFF;
            background-color: #00C851;
            padding: 20px;
            font-size: 32px;
            margin: 0;
        }
    </style>
"""

# Cabeçalho do aplicativo
st.markdown(title_html, unsafe_allow_html=True)
st.markdown('<div class="title"><h1>Agroboard 🐂 🌱</h1></div>', unsafe_allow_html=True)

# Dicionário de correlação entre a chave (opção selecionada) e o valor (commodity correspondente)
commodity_correlacao = {
    "Boi Gordo 🐂": "boi-gordo",
    "Soja 🌱": "soja",
    "Café ☕": "cafe",
    "Frango 🐥": "frango",
    "Laranja 🍊": "laranja",
    "Milho 🌽": "milho"
}

# Selecionar a commodity desejada do usuário na barra lateral
commodity_selecionada = st.sidebar.selectbox("Categorias (Commodities)", list(commodity_correlacao.keys()))

# Verificar se a opção selecionada tem uma correspondência
if commodity_selecionada in commodity_correlacao:
    # Obter o valor correspondente no dicionário de correlação
    commodity = commodity_correlacao[commodity_selecionada]

    # Chamada da função com a commodity correlacionada
    obter_informacoes_commodity(commodity)
else:
    st.write("Não foi encontrada uma correspondência para a commodity selecionada.")

# Resumo do projeto
st.sidebar.markdown("---")
st.sidebar.markdown("**Projeto Agroboard**")
st.sidebar.write("O Agroboard - o dashboard agro, tem como objetivo facilitar informações importantes aos empresários do agronegócio. Sendo assim, a plataforma disponibiliza aos seus usuários as cotações atualizadas dos principais produtos agrícolas que movimentam a economia no território brasileiro. Desta forma, facilitamos o processo de comunicação entre os órgãos reguladores e os demais membros da comunidade agrícola.")
st.sidebar.write("O projeto foi realizado pelo aluno Matheus Guimarães, submetido como trabalho final na disciplina de Introdução à Programação em 2023.1.")

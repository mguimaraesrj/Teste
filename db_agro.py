import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
from datetime import datetime
import streamlit.components.v1 as components

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

    # Resto do código omitido para maior clareza

def plotar_grafico(df):
    # Configurar a faixa de valores do eixo x e y
    x_range = [df["Datas"].min(), df["Datas"].max()]
    y_range = [df["Preços"].min(), df["Preços"].max()]

    # Plotar o gráfico
    chart = st.line_chart(df.set_index("Datas"), use_container_width=True)
    chart.x_range = x_range
    chart.y_range = y_range

# Estilo do título
barra_verde = """
<style>
.barra-verde {
    background-color: #00C851;
    height: 10px;
}
</style>
"""

# Cabeçalho do aplicativo
components.html(barra_verde)
st.markdown('<div class="title"><h2 class="barra-verde">Agroboard - Dashboard Agro 🌱</h2></div>', unsafe_allow_html=True)

# Restante do código existente

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

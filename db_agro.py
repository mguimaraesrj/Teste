import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import emoji
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
            precos.insert(0, texto)  # Inverter a ordem dos preços, inserindo-os no início da lista

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

    # Ordenar o dataframe por data
    df = df.sort_values(by="Datas")

    # Exibir o dataframe
    st.write(df)

    # Plotar o gráfico
    chart = st.line_chart(df.set_index("Datas"))
    chart.x_range = [df["Datas"].min(), df["Datas"].max()]  # Configurar a faixa de valores do eixo x

    st.text("Não deixe de ouvir este som! Acesse:" "https://www.youtube.com/watch?v=aFk363XM-N8")


# Cabeçalho do aplicativo
st.title("Agroboard - o dashboard Agro")

# Dicionário de correlação entre a chave (opção selecionada) e o valor (commodity correspondente)
commodity_correlacao = {
    "Boi Gordo": "boi-gordo",
    "Soja": "soja",
    "Café": "cafe",
    "Trigo": "trigo",
    "Frango": "frango",
    "Laranja": "laranja",
    "Milho": "milho"
}

# Selecionar a commodity desejada do usuário
commodity_selecionada = st.sidebar.selectbox(
    "Selecione uma commodity",
    list(commodity_correlacao.keys()),
    format_func=lambda x: emoji.emojize(f"{x} :{commodity_correlacao[x]}:", use_aliases=True)
)

# Verificar se a opção selecionada tem uma correspondência
if commodity_selecionada in commodity_correlacao:
    # Obter o valor correspondente no dicionário de correlação
    commodity = commodity_correlacao[commodity_selecionada]

    # Chamada da função com a commodity correlacionada
    obter_informacoes_commodity(commodity)
else:
    st.write("Não foi encontrada uma correspondência para a commodity selecionada.")

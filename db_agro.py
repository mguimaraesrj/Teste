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


# Cabeçalho do aplicativo
st.title("Agroboard - o dashboard Agro")

# Opções pré-estabelecidas para o usuário selecionar
commodity_opcoes = ["Boi Gordo", "Soja", "Café", "Trigo", "Frango", "Laranja", "Milho"]
commodity_opcoes_correlacionadas = ["boi Gordo", "soja", "cafe", "trigo", "frango", "laranja", "milho"]

# Criar o dicionário de correlação
correlacao = dict(zip(commodity_opcoes, commodity_opcoes_correlacionadas))

# Selecionar a commodity desejada do usuário
commodity_selecionada = st.selectbox("Selecione uma commodity", commodity_opcoes)

# Substituir a opção selecionada pelo usuário pela opção correlacionada
commodity_correlacionada = correlacao.get(commodity_selecionada)

# Verificar se a opção selecionada tem uma correspondência
if commodity_correlacionada:
    # Atualizar a variável commodity com a opção correlacionada
    commodity = commodity_correlacionada
    
    # Chamada da função com a commodity correlacionada
    obter_informacoes_commodity(commodity)
else:
    st.write("Não foi encontrada uma correspondência para a commodity selecionada.")

import pandas as pd
import streamlit as st

# Carregar o arquivo CSV
file_path = st.file_uploader("Selecione o arquivo CSV", type="csv")

if file_path is not None:
    data = pd.read_csv(file_path)

    # Opção para selecionar a quantidade de linhas a exibir
    num_rows = st.slider("Quantidade de linhas a exibir", 1, len(data), 10)
    st.write(data.head(num_rows))

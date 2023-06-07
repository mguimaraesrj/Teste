import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

data = pd.read_csv("allJobs.csv")

plt.plot(data["x"], data["y"])
plt.xlabel("Valores de X")
plt.ylabel("Valores de Y")
plt.title("Gráfico de Linhas")

st.pyplot()

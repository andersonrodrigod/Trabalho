import pandas as pd


arquivo_csv = "data/processed/coluna_1.csv"

# verificar os tipos de colunas 
df = pd.read_csv(arquivo_csv, sep=",", encoding="utf-8")


df_resultado =  df[(df["p1"] == 1) & (df["elogio_ou_queixa"] == "QUEIXA")] 

print(df_resultado)
import pandas as pd


arquivo_csv = "data/processed/comentarios_processados_full.csv"

# verificar os tipos de colunas 
df = pd.read_csv(arquivo_csv, sep=",", encoding="utf-8")


# verificar os nomes das classificações tem na coluna grupo
print(df["grupo"].unique())

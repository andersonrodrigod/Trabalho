import pandas as pd


df = pd.read_excel("dados.xlsx", dtype=str)

df = df["Telefone 2"].dropna().apply(lambda x: "55" + str(x))

print(df)
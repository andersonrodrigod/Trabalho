import pandas as pd

df1 = pd.read_excel("arquivo1.xlsx")
df2 = pd.read_excel("arquivo2.xlsx")

df_final = pd.concat([df1, df2], ignore_index=True)

df_final.to_excel("arquivo_unido.xlsx", index=False)

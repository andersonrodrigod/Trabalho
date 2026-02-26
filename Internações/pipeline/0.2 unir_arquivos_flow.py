import pandas as pd

df1 = pd.read_excel("eletivo.xlsx")
df2 = pd.read_excel("internacao.xlsx")

df_final = pd.concat([df1, df2], ignore_index=True)

df_final.to_excel("status_resposta.xlsx", index=False)

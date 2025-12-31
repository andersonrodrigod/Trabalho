import pandas as pd

df = pd.read_excel("NOVEMBRO GERAL.xlsx", sheet_name="BASE")

print(df.columns)

df_base = df[df["BASE"] == "CCG"][["COD USUARIO", "USUARIO", "DT AUTORIZACAO", "DT INTERNACAO"]]


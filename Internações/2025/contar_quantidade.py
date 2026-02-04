import pandas as pd

# 1. Ler os arquivos
df_main = pd.read_excel("BASE DEZEMBRO INTERNACAO MAIN.xlsx")
df_senhas = pd.read_csv("telefone_senha_dezembro.csv")

# 2. Garantir que as colunas estão no mesmo tipo (muito importante)
df_main["SENHA"] = df_main["SENHA"].astype(str)
df_senhas["CD_SENHA"] = df_senhas["CD_SENHA"].astype(str)

# 3. Verificar quais SENHAS do main existem no CSV
df_main["ENCONTROU"] = df_main["SENHA"].isin(df_senhas["CD_SENHA"])

# 4. Contar quantas foram encontradas
total_encontradas = df_main["ENCONTROU"].sum()

print("Total de SENHAS encontradas:", total_encontradas)

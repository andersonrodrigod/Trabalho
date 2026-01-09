import pandas as pd


df = pd.read_excel("NOVEMBRO.xlsx")

codigo_carteira = df[df["CD_USUARIO"].duplicated(keep=False)]

codigo_carteira_nao_duplicados = df[~df["CD_USUARIO"].duplicated(keep=False)]

print("Duplicados:")
print(codigo_carteira)
print("\nNão Duplicados:")
print(codigo_carteira_nao_duplicados)

codigo_carteira.to_excel("NOVEMBRO_DUPLICADOS.xlsx", index=False)
codigo_carteira_nao_duplicados.to_excel("NOVEMBRO_UNIQUES.xlsx", index=False)



    
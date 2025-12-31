import pandas as pd


df = pd.read_excel("SETEMBRO.xlsx")

codigo_carteira = df[df["CD_USUARIO"].duplicated(keep=False)]

codigo_carteira_nao_duplicados = df[~df["CD_USUARIO"].duplicated(keep=False)]

print("Duplicados:")
print(codigo_carteira)
print("\nNão Duplicados:")
print(codigo_carteira_nao_duplicados)

codigo_carteira.to_excel("SETEMBRO_DUPLICADOS.xlsx", index=False)
codigo_carteira_nao_duplicados.to_excel("SETEMBRO_UNIQUES.xlsx", index=False)



    
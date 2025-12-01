import pandas as pd
from collections import Counter

arquivo = "tests/coluna_1_grupo.csv"


df = pd.read_csv(arquivo, sep=",")

# Filtrar somente os casos de RECEPÇAO
df_recep = df[df["grupo"] == "ADMINISTRATIVO"]
df_recep = df[(df["grupo"] == "ADMINISTRATIVO") & (df["comentario_p1"].str.contains("recepc", case=False))]

df_recep.to_csv("tests/contem_recepcao.csv", index=False)

# Quantidade de casos do grupo RECEPÇAO
total_casos = len(df_recep)
print(total_casos)


# quantidade das palavras recepcionista e recepcao
df_recepcionista = df_recep["comentario_p1"].str.contains("recepcepcionista", case=False)
df_recepcao = df_recep["comentario_p1"].str.contains("recepcao", case=False)


#print(df_recepcionista)
#print(df_recepcao)


# Quantidade que citam recepcionista e não citam recepção 
qtd_recepcionista = (df_recepcionista & ~df_recepcao).sum()

# Quantidade que citam recepção e não citam recepcionista
qtd_recepcao = (~df_recepcionista & df_recepcao).sum()

#print(qtd_recepcao)
#print(qtd_recepcionista)



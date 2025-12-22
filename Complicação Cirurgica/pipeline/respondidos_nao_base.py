import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

abas_respostas = pd.read_excel("resposta.xlsx", sheet_name=None, engine="openpyxl", dtype=str)
abas_novembro = pd.read_excel("NOVEMBRO GERAL.xlsx", sheet_name=None, engine="openpyxl", dtype=str)

df_respostas = abas_respostas["p1"]
df_base = abas_novembro["BASE"]

df_resposta_separador = df_respostas["Nome"].str.split("_", expand=True).copy()

df_resposta_separador["nome_manipulado"] = df_resposta_separador[0]
df_resposta_separador["procedimento"] = df_resposta_separador[1]
df_resposta_separador["prestador"] = df_resposta_separador[2]

cond_nao_respondidas = ((df_base["P1"].isna()) | (df_base["P1"].astype(str).str.strip() == ""))
df_base_nao_respondidos = df_base[cond_nao_respondidas].copy()
df_base_nao_respondidos["status_resposta"] = "Não Respondido"

print(len(df_base["P1"]))
print(len(df_base[df_base["P1"] == "Sim"]))
print(len(df_base_nao_respondidos))

df_merge = df_base_nao_respondidos.merge(
    df_resposta_separador,
    left_on=["USUARIO", "PROCEDIMENTO", "PRESTADOR"],
    right_on=["nome_manipulado", "procedimento", "prestador"],
    how="left",
    indicator=True
)

df_merge_nome = df_base_nao_respondidos.merge(
    df_resposta_separador,
    left_on=["USUARIO"],
    right_on=["nome_manipulado"],
    how="left",
    indicator=True
)

print(df_merge["_merge"].value_counts())
print(df_merge_nome["_merge"].value_counts())

df_estao_repondidos = df_merge[df_merge["_merge"] == "both"].copy()
print(df_estao_repondidos["CHAVE"])

df_estao_repondidos_nome_igual = df_merge_nome[df_merge_nome["_merge"] == "both"].copy()
print(df_estao_repondidos_nome_igual["CHAVE"])

with pd.ExcelWriter("estao_respondidos_nao_base.xlsx", engine="openpyxl") as writer:
    df_estao_repondidos.to_excel(writer, sheet_name="respondidos_nao_base", index=False)
    df_estao_repondidos_nome_igual.to_excel(writer,sheet_name="respondidos_nome_igual", index=False)



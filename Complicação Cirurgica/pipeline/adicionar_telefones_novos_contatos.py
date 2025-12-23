import pandas as pd

df_novos_numeros = pd.read_excel("TOTAL_SEGUNDO_NOVEMBRO.xlsx")
df_novos_abas = pd.read_excel("novos_contatos 22.12.xlsx", sheet_name=None)

df_novos_contatos = df_novos_abas["usuarios"]

df_novos_numeros = df_novos_numeros[df_novos_numeros["STATUS BOT"] == "NOVO CONTATO"]


df_merge = df_novos_contatos.merge(
    df_novos_numeros[["CHAVE RELATORIO", "TELEFONE 1"]],
    on="CHAVE RELATORIO",
    how="left",
    suffixes=("", "_NOVO")
)

mask_vazio = df_merge["TELEFONE 1"].isna() | (df_merge["TELEFONE 1"] == "")


df_merge.loc[mask_vazio, "TELEFONE 1"] = df_merge.loc[mask_vazio, "TELEFONE 1_NOVO"]

df_merge.drop(columns=["TELEFONE 1_NOVO"], inplace=True)

df_novos_abas["usuarios"] = df_merge

with pd.ExcelWriter("novos_contatos 22.12 atualizados.xlsx", engine="xlsxwriter") as writer:
    for nome_aba, df in df_novos_abas.items():
        df.to_excel(writer, sheet_name=nome_aba, index=False)


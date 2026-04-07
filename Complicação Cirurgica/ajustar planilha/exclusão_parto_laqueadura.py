import pandas as pd


arquivo_entrada = "complicacao.xlsx"
aba = "BASE"
arquivo_saida = "BASE_SEM_PARTO_LAQUEADURA.xlsx"
arquivo_excluidos = "LINHAS_EXCLUIDAS_PARTO_LAQUEADURA.xlsx"


abas = pd.read_excel(arquivo_entrada, sheet_name=None)
df = abas[aba]

procedimento = df["PROCEDIMENTO"].fillna("").astype(str).str.upper().str.strip()
mascara_excluir = procedimento.str.contains("PARTO|LAQUEADURA", na=False)

df_filtrado = df[~mascara_excluir].copy()
df_excluidos = df[mascara_excluir].copy()

abas[aba] = df_filtrado

with pd.ExcelWriter(arquivo_saida, engine="openpyxl") as writer:
    for nome_aba, df_aba in abas.items():
        df_aba.to_excel(writer, sheet_name=nome_aba, index=False)

df_excluidos.to_excel(arquivo_excluidos, index=False)

print("Processo finalizado.")
print("Linhas mantidas:", len(df_filtrado))
print("Linhas excluidas:", len(df_excluidos))
print("Arquivo final:", arquivo_saida)
print("Arquivo com excluidas:", arquivo_excluidos)

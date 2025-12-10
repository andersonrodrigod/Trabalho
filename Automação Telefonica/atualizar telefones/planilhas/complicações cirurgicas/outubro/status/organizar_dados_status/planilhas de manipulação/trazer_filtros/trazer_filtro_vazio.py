import pandas as pd

print("📘 Lendo o arquivo MES OUTUBRO GERAL.xlsx...")
df = pd.read_excel("MES OUTUBRO GERAL.xlsx", sheet_name="BASE")

print("🔍 Criando filtros...")

# Filtros booleanos (True/False)
filtro_nao_lidas = df["STATUS"].isna() | (df["STATUS"].astype(str).str.strip() == "")

filtro_lidas_nao_respondidas = (
    (df["STATUS"].astype(str).str.strip() == "Lida") &
    (
        df["P1"].isna() |
        (df["P1"].astype(str).str.strip() == "")
    )
)


# Aplicando os filtros
df_nao_lidas = df.loc[filtro_nao_lidas, ["COD USUARIO", "USUARIO", "PRESTADOR", "CHAVE"]]

df_lidas_nao_respondidads = df.loc[filtro_lidas_nao_respondidas, ["COD USUARIO", "USUARIO", "PRESTADOR", "CHAVE"]]

print(f"✅ Registros lidas e não respondidas: {len(df_lidas_nao_respondidads)}")
print(f"✅ Registros não lidos: {len(df_nao_lidas)}")

print("💾 Salvando arquivos...")
df_lidas_nao_respondidads.to_excel("lidas_nao_respondidas.xlsx", index=False)
df_nao_lidas.to_excel("nao_lidas.xlsx", index=False)


#df_vazios.to_excel("status_vazio_resultado.xlsx", index=False)
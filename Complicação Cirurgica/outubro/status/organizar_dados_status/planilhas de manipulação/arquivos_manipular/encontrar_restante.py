import pandas as pd

print("📘 Lendo os arquivos...")

df_nomes = pd.read_excel("Nomes_tratados_status.xlsx")
df_p1 = pd.read_excel("status_vazio_resultado_unicos.xlsx")

print("🔎 Normalizando textos...")

# Normaliza texto para evitar erros de espaço
nomes_col = df_nomes["nome_manipulado"].astype(str).str.strip()
usuarios_col = df_p1["USUARIO"].astype(str).str.strip()

print("🔧 Criando filtro de correspondência...")

# Filtra as linhas do P1 onde USUARIO existe em Nomes
mask = usuarios_col.isin(nomes_col)

df_resultado = df_p1.loc[mask, ["COD USUARIO", "USUARIO", "CHAVE"]]

print(f"✅ Registros encontrados: {len(df_resultado)}")

print("💾 Salvando nova planilha...")

df_resultado.to_excel("Usuarios_encontrados_STATUS.xlsx", index=False)

print("🎉 Concluído! Arquivo gerado: Usuarios_encontrados_STATUS.xlsx")
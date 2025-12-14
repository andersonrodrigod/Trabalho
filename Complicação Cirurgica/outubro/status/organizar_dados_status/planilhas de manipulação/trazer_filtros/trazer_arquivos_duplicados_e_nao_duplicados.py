import pandas as pd

print("📘 Lendo arquivos...")

# Base de comparação
df_base = pd.read_excel("usuarios_duplicados_BASE.xlsx")
base_col = df_base["USUARIO"].astype(str).str.strip()

# Arquivo 1
df_nomes = pd.read_excel("Nomes_tratados_status.xlsx")
nomes_col = df_nomes["nome_manipulado"].astype(str).str.strip()

# Arquivo 2
df_p1 = pd.read_excel("status_vazio_resultado.xlsx")
p1_col = df_p1["USUARIO"].astype(str).str.strip()

print("🔎 Separando registros...")

# --- Nomes_tratados_p1 ---
mask_nomes = nomes_col.isin(base_col)

df_nomes_duplicados = df_nomes[mask_nomes]
df_nomes_unicos    = df_nomes[~mask_nomes]

# --- P1_vazio_resultado ---
mask_p1 = p1_col.isin(base_col)

df_p1_duplicados = df_p1[mask_p1]
df_p1_unicos     = df_p1[~mask_p1]

print("💾 Salvando resultados...")

# Nomes_tratados_p1
df_nomes_duplicados.to_excel("Nomes_tratados_status_duplicados.xlsx", index=False)
df_nomes_unicos.to_excel("Nomes_tratados_status_unicos.xlsx", index=False)

# P1_vazio_resultado
df_p1_duplicados.to_excel("status_vazio_resultado_duplicados.xlsx", index=False)
df_p1_unicos.to_excel("status_vazio_resultado_unicos.xlsx", index=False)

print("🎉 Concluído! Arquivos gerados com todas as colunas.")

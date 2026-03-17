import pandas as pd

# 1. Ler o arquivo
df = pd.read_excel("BASE_FINAL_ORGANIZADA.xlsx")

# 2. Garantir tipo correto
df["CD_USUARIO"] = df["CD_USUARIO"].astype(str).str.strip()
df["PROCEDIMENTO"] = df["PROCEDIMENTO"].astype(str).str.upper()

# 3. Identificar duplicados de CD_USUARIO
df["DUPLICADO"] = df["CD_USUARIO"].duplicated(keep=False)

# 4. Filtrar apenas os duplicados
df_dup = df[df["DUPLICADO"] == True]

# 5. Marcar quais são INTERNACAO CLINICA
df_dup["INTERNACAO_CLINICA"] = df_dup["PROCEDIMENTO"].str.contains(
    "INTERNACAO CLINICA",
    na=False
)

# 6. Contar quantas internações clínicas existem por CD_USUARIO
internacao_por_usuario = (
    df_dup[df_dup["INTERNACAO_CLINICA"] == True]
    .groupby("CD_USUARIO")
    .size()
    .reset_index(name="QTD_INTERNACAO_CLINICA")
)

# 7. Totais gerais
total_duplicados = df_dup.shape[0]
total_internacao_clinica = df_dup["INTERNACAO_CLINICA"].sum()

print("Total de registros duplicados:", total_duplicados)
print("Total de INTERNACAO CLINICA dentro dos duplicados:", total_internacao_clinica)

print("\nQuantidade de INTERNACAO CLINICA por CD_USUARIO:")
print(internacao_por_usuario.head(10))

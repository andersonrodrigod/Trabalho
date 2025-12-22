import pandas as pd

# ==================================================
# LEITURA DOS ARQUIVOS
# ==================================================
print("📘 Lendo MES OUTUBRO GERAL.xlsx (BASE)...")
df_base = pd.read_excel(
    "MES OUTUBRO GERAL.xlsx",
    sheet_name="BASE"
)

print("📗 Lendo UF.xlsx (Planilha1)...")
df_uf = pd.read_excel(
    "UF.xlsx",
    sheet_name="Planilha1"
)

# ==================================================
# NORMALIZAÇÃO (ESSENCIAL)
# ==================================================
print("🧽 Normalizando colunas...")

df_base["PRESTADOR"] = df_base["PRESTADOR"].astype(str).str.strip()
df_uf["PRESTADOR"] = df_uf["PRESTADOR"].astype(str).str.strip()

df_base["COD PROCEDIMENTO"] = df_base["COD PROCEDIMENTO"].astype(str).str.strip()
df_uf["COD PROCEDIMENTO"] = df_uf["COD PROCEDIMENTO"].astype(str).str.strip()

# ==================================================
# 1) MERGE PELO PRESTADOR → SIGLA / ESTADOS
#    (garantindo unicidade)
# ==================================================
print("🧹 Tratando duplicados de PRESTADOR na BASE...")

df_base_prestador = (
    df_base[["PRESTADOR", "SIGLA", "ESTADOS"]]
    .drop_duplicates(subset=["PRESTADOR"])
)

print("🔗 Vinculando SIGLA e ESTADOS pelo PRESTADOR...")

df_uf = df_uf.merge(
    df_base_prestador,
    on="PRESTADOR",
    how="left",
    validate="many_to_one"
)

# ==================================================
# 2) MERGE PELO COD PROCEDIMENTO → ESPECIALISTA
# ==================================================
print("🧹 Tratando duplicados de COD PROCEDIMENTO na BASE...")

df_base_proc = (
    df_base[["COD PROCEDIMENTO", "ESPECIALISTA"]]
    .drop_duplicates(subset=["COD PROCEDIMENTO"])
)

print("🔗 Vinculando ESPECIALISTA pelo COD PROCEDIMENTO...")

df_uf = df_uf.merge(
    df_base_proc,
    on="COD PROCEDIMENTO",
    how="left",
    validate="many_to_one"
)

# ==================================================
# SALVAR RESULTADO
# ==================================================
print("💾 Salvando UF_atualizado.xlsx ...")

df_uf.to_excel(
    "UF_atualizado.xlsx",
    index=False
)

print("✅ Processo finalizado com sucesso!")

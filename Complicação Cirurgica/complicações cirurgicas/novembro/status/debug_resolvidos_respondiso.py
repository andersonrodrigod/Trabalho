import pandas as pd

print("\n================ AUDITORIA RESPONDIDOS x RESOLVIDOS ================\n")

# --------------------------------------------------
# 1) Ler somente as abas necessárias
# --------------------------------------------------
df_abas = pd.read_excel("novos_contatos_atualizado.xlsx", sheet_name=None)

df_respondidos = df_abas["usuarios_respondidos"].copy()
df_resolvidos = df_abas["usuarios_resolvidos"].copy()

# --------------------------------------------------
# 2) Função de chave lógica (mesma do ETL!)
# --------------------------------------------------
def normalizar_chave(df):
    return (
        df["COD USUARIO"].fillna("").astype(str).str.strip() + "|" +
        df["USUARIO"].fillna("").astype(str).str.strip().str.upper() + "|" +
        df["PRESTADOR"].fillna("").astype(str).str.strip().str.upper() + "|" +
        df["PROCEDIMENTO"].fillna("").astype(str).str.strip().str.upper()
    )

# --------------------------------------------------
# 3) Criar chaves
# --------------------------------------------------
ch_resp = df_respondidos["CHAVE RELATORIO"].astype(str).str.strip()
ch_resol = df_resolvidos["CHAVE RELATORIO"].astype(str).str.strip()

ch_log_resp = normalizar_chave(df_respondidos)
ch_log_resol = normalizar_chave(df_resolvidos)

# --------------------------------------------------
# 4) Verificar presença
# --------------------------------------------------
mask_por_chave = ch_resp.isin(ch_resol)
mask_por_logica = ch_log_resp.isin(ch_log_resol)

mask_nao_resolvidos = ~(mask_por_chave | mask_por_logica)

df_problema = df_respondidos[mask_nao_resolvidos].copy()

# --------------------------------------------------
# 5) Resultado
# --------------------------------------------------
print(f"Total em usuarios_respondidos: {len(df_respondidos)}")
print(f"Total em usuarios_resolvidos: {len(df_resolvidos)}")
print(f"🚨 Respondidos que NÃO estão em resolvidos: {len(df_problema)}")

if len(df_problema) > 0:
    print("\n🔎 Primeiros casos problemáticos:")
    print(df_problema[[
        "CHAVE RELATORIO",
        "COD USUARIO",
        "USUARIO",
        "PRESTADOR",
        "PROCEDIMENTO"
    ]].head(10))

    df_problema.to_excel(
        "auditoria_respondidos_nao_resolvidos.xlsx",
        index=False
    )

    print("\n📁 Arquivo 'auditoria_respondidos_nao_resolvidos.xlsx' gerado.")
else:
    print("\n✅ Nenhuma inconsistência encontrada.")

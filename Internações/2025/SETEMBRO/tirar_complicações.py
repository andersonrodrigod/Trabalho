import pandas as pd

# =====================================================
# 1. Ler os arquivos
# =====================================================
df_janeiro = pd.read_excel("INTERNACOES_OUTUBRO.xlsx")

df_comp = pd.read_excel(
    "OUTUBRO COMPLICA.xlsx",
)

# =====================================================
# 2. Padronizar colunas
# =====================================================
# Janeiro
df_janeiro["CD_CARTEIRINHA_USUARIO"] = (
    df_janeiro["CD_CARTEIRINHA_USUARIO"].astype(str).str.strip()
)

df_janeiro["NM_BENEFICIARIO"] = (
    df_janeiro["NM_BENEFICIARIO"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# Complicação
df_comp["COD USUARIO"] = (
    df_comp["COD USUARIO"].astype(str).str.strip()
)

df_comp["USUARIO"] = (
    df_comp["USUARIO"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# =====================================================
# 3. Criar chave composta (ÚNICA REGRA)
# =====================================================
df_janeiro["CHAVE_USUARIO"] = (
    df_janeiro["CD_CARTEIRINHA_USUARIO"] + "|" +
    df_janeiro["NM_BENEFICIARIO"]
)

df_comp["CHAVE_USUARIO"] = (
    df_comp["COD USUARIO"] + "|" +
    df_comp["USUARIO"]
)

# =====================================================
# 4. Máscara de exclusão (FORMA CORRETA)
# =====================================================
excluir_final = df_janeiro["CHAVE_USUARIO"].isin(
    df_comp["CHAVE_USUARIO"]
)

# =====================================================
# 5. Resultados
# =====================================================
df_excluidos = df_janeiro[excluir_final].copy()
df_limpo = df_janeiro[~excluir_final].copy()

print("Total de linhas excluídas:", df_excluidos.shape[0])
print(
    "Total de indivíduos distintos excluídos:",
    df_excluidos["CD_CARTEIRINHA_USUARIO"].nunique()
)

# =====================================================
# 6. Limpeza opcional (remover chave técnica)
# =====================================================
df_excluidos = df_excluidos.drop(columns=["CHAVE_USUARIO"])
df_limpo = df_limpo.drop(columns=["CHAVE_USUARIO"])

# =====================================================
# 7. Salvar arquivos
# =====================================================
df_limpo.to_excel(
    "OUTUBRO_INTERNAÇOES_LIMPO.xlsx",
    index=False
)

df_excluidos.to_excel(
    "OUTUBRO_INTERNAÇOES_EXCLUIDOS.xlsx",
    index=False
)

import pandas as pd

# =====================================================
# 1. Ler arquivo
# =====================================================
df = pd.read_excel("JANEIRO_INTERNAÇOES.xlsx")

# Padronizar colunas
df["CD_USUARIO"] = df["CD_USUARIO"].astype(str).str.strip()
df["NOME_PROCEDIMENTO"] = df["NOME_PROCEDIMENTO"].astype(str).str.upper()

# =====================================================
# 2. Separar duplicados
# =====================================================
duplicados = df[df["CD_USUARIO"].duplicated(keep=False)]
nao_duplicados = df[~df["CD_USUARIO"].duplicated(keep=False)]

mantidos = []
excluidos = []

# =====================================================
# 3. Processar cada código duplicado (REGRAS ORIGINAIS)
# =====================================================
for codigo, grupo in duplicados.groupby("CD_USUARIO"):

    # --- REGRA 3: CESARIANA ---
    if grupo["NOME_PROCEDIMENTO"].str.contains("CESARIANA", na=False).any():
        manter = grupo[grupo["NOME_PROCEDIMENTO"].str.contains("CESARIANA", na=False)]
        excluir = grupo.drop(manter.index)

    # --- REGRA 2: PARTO VIA VAGINAL ---
    elif grupo["NOME_PROCEDIMENTO"].str.contains("PARTO \\(VIA VAGINAL\\)", na=False).any():
        manter = grupo[grupo["NOME_PROCEDIMENTO"].str.contains("PARTO \\(VIA VAGINAL\\)", na=False)]
        excluir = grupo.drop(manter.index)

    # --- REGRA 1: INTERNACAO (misto) ---
    elif grupo["NOME_PROCEDIMENTO"].str.contains("INTERNACAO", na=False).any():
        manter = grupo[~grupo["NOME_PROCEDIMENTO"].str.contains("INTERNACAO", na=False)]
        excluir = grupo.drop(manter.index)

        # Se todos forem internação, mantém todos (por enquanto)
        if manter.empty:
            manter = grupo
            excluir = grupo.iloc[0:0]

    else:
        manter = grupo
        excluir = grupo.iloc[0:0]

    mantidos.append(manter)
    excluidos.append(excluir)

# =====================================================
# 4. Consolidar após regras principais
# =====================================================
df_mantidos = pd.concat(mantidos + [nao_duplicados], ignore_index=True)
df_excluidos = pd.concat(excluidos, ignore_index=True)

# =====================================================
# 5. REGRA FINAL — duplicados restantes só com INTERNACAO
# =====================================================
duplicados_finais = df_mantidos[
    df_mantidos["CD_USUARIO"].duplicated(keep=False)
]

for codigo, grupo in duplicados_finais.groupby("CD_USUARIO"):

    # Se TODOS os procedimentos forem INTERNACAO
    if grupo["NOME_PROCEDIMENTO"].str.contains("INTERNACAO", na=False).all():

        # Manter apenas 1 (o primeiro)
        manter_um = grupo.iloc[[0]]
        excluir_restante = grupo.iloc[1:]

        # Atualizar mantidos e excluídos
        df_mantidos = df_mantidos.drop(excluir_restante.index)
        df_excluidos = pd.concat(
            [df_excluidos, excluir_restante],
            ignore_index=True
        )

# =====================================================
# 6. Salvar arquivos finais
# =====================================================
df_mantidos.to_excel("REGISTROS_MANTIDOS.xlsx", index=False)
df_excluidos.to_excel("REGISTROS_EXCLUIDOS.xlsx", index=False)

print("Processo finalizado.")
print("Mantidos:", df_mantidos.shape[0])
print("Excluídos:", df_excluidos.shape[0])

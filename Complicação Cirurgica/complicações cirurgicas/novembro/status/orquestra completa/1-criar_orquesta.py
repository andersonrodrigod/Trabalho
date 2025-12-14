import pandas as pd

# ==========================================================
# 1) LEITURA DO ARQUIVO
# ==========================================================
print("📘 Lendo arquivo NOVEMBRO GERAL.xlsx aba BASE...")
df = pd.read_excel("NOVEMBRO GERAL 13.12.xlsx", sheet_name="BASE")

print("🧽 Normalizando colunas...")
df.columns = df.columns.str.strip()


# ==========================================================
# 2) IDENTIFICAR DUPLICADOS (ANTES DE TUDO)
# ==========================================================
print("🔍 Identificando duplicados por COD USUARIO...")

mask_duplicados = df.duplicated(subset=["COD USUARIO"], keep=False)

df_duplicados_raw = df[mask_duplicados]
df_sem_duplicados = df[~mask_duplicados]

print(f"   ➜ Total duplicados: {len(df_duplicados_raw)}")
print(f"   ➜ Total sem duplicados: {len(df_sem_duplicados)}")


# ==========================================================
# 3) COLUNAS FINAIS PADRÃO
# ==========================================================
colunas_finais = [
    'STATUS BOT', 'BASE', 'COD USUARIO', 'USUARIO', 'TELEFONE RELATORIO',
    'TELEFONE 1', 'TELEFONE 2', 'TELEFONE 3', 'TELEFONE 4', 'TELEFONE 5',
    'PRESTADOR', 'PROCEDIMENTO', 'TP ATENDIMENTO', 'DT INTERNACAO', 'ENVIO',
    'ULTIMO STATUS DE ENVIO','RESPONDIDO', 'LIDA', 'ENTREGUE', 'ENVIADA',
    'NAO_ENTREGUE_META', 'MENSAGEM_NAO_ENTREGUE', 'EXPERIMENTO',
    'OPT_OUT', 'TELEFONE ENVIADO', 'CHAVE RELATORIO', 'CHAVE STATUS',
    'STATUS TELEFONE', 'STATUS CHAVE', 'QT TELEFONE', 'QT LIDA',
    'QT ENTREGUE', 'QT ENVIADA', 'QT NAO_ENTREGUE_META',
    'QT MENSAGEM_NAO_ENTREGUE', 'QT EXPERIMENTO', 'QT OPT_OUT'
]


# ==========================================================
# 4) FUNÇÃO PADRÃO PARA MONTAR DATAFRAME FINAL
# ==========================================================
def montar_df_final(df_base):
    df_final = pd.DataFrame(columns=colunas_finais)

    if 'BASE' in df_base: df_final['BASE'] = df_base['BASE']
    if 'COD USUARIO' in df_base: df_final['COD USUARIO'] = df_base['COD USUARIO']
    if 'USUARIO' in df_base: df_final['USUARIO'] = df_base['USUARIO']
    if 'TELEFONE' in df_base: df_final['TELEFONE RELATORIO'] = df_base['TELEFONE']
    if 'PRESTADOR' in df_base: df_final['PRESTADOR'] = df_base['PRESTADOR']
    if 'PROCEDIMENTO' in df_base: df_final['PROCEDIMENTO'] = df_base['PROCEDIMENTO']
    if 'TP ATENDIMENTO' in df_base: df_final['TP ATENDIMENTO'] = df_base['TP ATENDIMENTO']
    if 'DT INTERNACAO' in df_base: df_final['DT INTERNACAO'] = df_base['DT INTERNACAO']
    if 'DT ENVIO' in df_base: df_final['ENVIO'] = df_base['DT ENVIO']
    if 'CHAVE' in df_base: df_final['CHAVE RELATORIO'] = df_base['CHAVE']

    for col in colunas_finais:
        if col not in df_final.columns:
            df_final[col] = ""

    return df_final


# ==========================================================
# 5) ABA USUARIOS (BASE MESTRA — SEM DUPLICADOS)
# ==========================================================
print("📌 Criando aba usuarios (sem duplicados)...")
df_usuarios = montar_df_final(df_sem_duplicados)


# ==========================================================
# 6) ABAS DERIVADAS (SEMPRE A PARTIR DE df_sem_duplicados)
# ==========================================================

# --- usuarios_nao_lidos
filtro_nao_lidos = (
    df_sem_duplicados['STATUS'].isna() |
    (df_sem_duplicados['STATUS'].astype(str).str.strip() == "")
)
df_usuarios_nao_lidos = montar_df_final(df_sem_duplicados[filtro_nao_lidos])

# --- usuarios_lidos
status_validos = ["Lida", "Não quis", "Óbito"]
df_lidos = montar_df_final(
    df_sem_duplicados[df_sem_duplicados['STATUS'].isin(status_validos)]
)

# --- respondidos / nao respondidos P1
df_respondidos_p1 = montar_df_final(
    df[df['P1'].notna()]
)

df_nao_respondidos_p1 = montar_df_final(
    df[df['P1'].isna()]
)

print(len(df_respondidos_p1))
print(len(df_nao_respondidos_p1))
# ==========================================================
# 7) ABA USUARIOS DUPLICADOS (ISOLADA)
# ==========================================================
print("📌 Criando aba usuarios_duplicados...")
df_duplicados = montar_df_final(df_duplicados_raw)


# ==========================================================
# 8) ABAS VAZIAS PADRÃO
# ==========================================================
df_vazio = pd.DataFrame(columns=colunas_finais)

abas_vazias = {
    "usuarios_lidos_nao_respondidos": df_vazio,
    "segundo_envio_lidos": df_vazio,
    "usuarios_resolvidos": df_vazio,
    "usuarios_defeituosos": df_vazio,
    "trocar_contato_lida": df_vazio,
    "HAP": df_vazio,
    "NDI SP": df_vazio,
    "NDI MINAS": df_vazio,
    "CLINIPAN": df_vazio,
    "CCG": df_vazio
}


# ==========================================================
# 9) SALVAR ARQUIVO FINAL
# ==========================================================
print("💾 Salvando arquivo final novos_contatos.xlsx ...")

with pd.ExcelWriter("novos_contatos.xlsx", engine="openpyxl") as writer:
    df_usuarios.to_excel(writer, sheet_name="usuarios", index=False)
    df_usuarios_nao_lidos.to_excel(writer, sheet_name="usuarios_nao_lidos", index=False)
    df_lidos.to_excel(writer, sheet_name="usuarios_lidos", index=False)
    df_respondidos_p1.to_excel(writer, sheet_name="usuarios_respondidos", index=False)
    df_nao_respondidos_p1.to_excel(writer, sheet_name="usuarios_nao_respondidos_p1", index=False)
    df_duplicados.to_excel(writer, sheet_name="usuarios_duplicados", index=False)

    for aba, tabela in abas_vazias.items():
        tabela.to_excel(writer, sheet_name=aba, index=False)

print("✅ Arquivo criado com sucesso!")

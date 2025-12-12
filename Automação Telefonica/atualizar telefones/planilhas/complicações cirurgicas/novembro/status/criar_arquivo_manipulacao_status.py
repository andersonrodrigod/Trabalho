import pandas as pd

print("📘 Lendo arquivo NOVEMBRO GERAL.xlsx aba BASE...")
df = pd.read_excel("NOVEMBRO GERAL.xlsx", sheet_name="BASE")

print("🧽 Normalizando colunas...")
df.columns = df.columns.str.strip()

# -------------------------
# COLUNAS FINAIS A SEREM CRIADAS
# -------------------------
colunas_finais = [
    'STATUS BOT', 'BASE', 'COD USUARIO', 'USUARIO', 'TELEFONE RELATORIO', 'TELEFONE 1', 
    'TELEFONE 2', 'TELEFONE 3', 'TELEFONE 4', 'TELEFONE 5', 'PRESTADOR', 
    'PROCEDIMENTO', 'TP ATENDIMENTO', 'DT INTERNACAO', 'ENVIO', 
    'ULTIMO STATUS DE ENVIO', 'LIDA', 'ENTREGUE', 'ENVIADA', 
    'NAO_ENTREGUE_META', 'MENSAGEM_NAO_ENTREGUE', 'EXPERIMENTO', 
    'OPT_OUT', 'TELEFONE ENVIADO', 'CHAVE RELATORIO', 'CHAVE STATUS', 
    'STATUS TELEFONE', 'STATUS CHAVE', 'QT TELEFONE', 'QT LIDA', 'QT ENTREGUE', 'QT ENVIADA', 
    'QT NAO_ENTREGUE_META', 'QT MENSAGEM_NAO_ENTREGUE', 'QT EXPERIMENTO', 
    'QT OPT_OUT'
]

# -------------------------
# FUNÇÃO PARA PADRONIZAR E CRIAR AS COLUNAS
# -------------------------
def montar_df_final(df_base):
    df_final = pd.DataFrame(columns=colunas_finais)

    # Copiando valores existentes
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

    # Criar colunas que não existem (ficam vazias)
    for col in colunas_finais:
        if col not in df_final.columns:
            df_final[col] = ""

    return df_final


# ----------------------------------------------------------
# ABA 1 — usuarios (STATUS vazio ou NaN)
# ----------------------------------------------------------
print("📌 Filtrando usuários com STATUS vazio ou NaN...")
filtro_usuarios = df[df['STATUS'].isna() | (df['STATUS'].astype(str).str.strip() == "")]
df_usuarios = montar_df_final(filtro_usuarios)


# --- NOVA LINHA: criar usuarios_nao_lidos usando o mesmo filtro ---
df_usuarios_nao_lidos = montar_df_final(filtro_usuarios)

# ----------------------------------------------------------
# ABA 2 — usuarios_lidos (STATUS = Lida, Não quis, Óbito)
# ----------------------------------------------------------
status_validos = ["Lida", "Não quis", "Óbito"]

print("📌 Filtrando usuários lidos...")
filtro_lidos = df[df['STATUS'].isin(status_validos)]
df_lidos = montar_df_final(filtro_lidos)


# ----------------------------------------------------------
# ABA 3 — usuarios_lidos_nao_respondidos
# Apenas registros com P1 preenchido (independe do STATUS)
# ----------------------------------------------------------
print("📌 Filtrando usuários que preencheram P1...")

filtro_respondidos_p1 = df[df['P1'].notna()]
filtro_nao_respondidos_p1 = df[df["P1"].isna()]

df_respondidos_p1 = montar_df_final(filtro_respondidos_p1)
df_nao_respondidos_p1 = montar_df_final(filtro_nao_respondidos_p1)


# ----------------------------------------------------------
# ABA — usuarios_duplicados (com todas as informações)
# ----------------------------------------------------------
print("🔍 Verificando duplicados na coluna COD USUARIO...")
duplicados = df[df.duplicated(subset=['COD USUARIO'], keep=False)]
df_duplicados = montar_df_final(duplicados)


# ----------------------------------------------------------
# Criar abas vazias com colunas
# ----------------------------------------------------------
df_vazio = pd.DataFrame(columns=colunas_finais)

abas_vazias = {
    "usuarios_nao_lidos": df_usuarios_nao_lidos,
    "usuarios_lidos_nao_respondidos": df_vazio,
    "segundo_envio_lidos": df_vazio,
    "usuarios_duplicados": df_duplicados,
    "usuarios_resolvidos": df_vazio,
    "HAP": df_vazio,
    "NDI SP": df_vazio,
    "NDI MINAS": df_vazio,
    "CLINIPAN": df_vazio,
    "CCG": df_vazio
}

# ----------------------------------------------------------
# SALVANDO ARQUIVO FINAL
# ----------------------------------------------------------
print("💾 Salvando arquivo final novos_contatos.xlsx ...")

with pd.ExcelWriter("novos_contatos.xlsx", engine="openpyxl") as writer:
    df_usuarios.to_excel(writer, sheet_name="usuarios", index=False)
    df_lidos.to_excel(writer, sheet_name="usuarios_lidos", index=False)
    df_respondidos_p1.to_excel(writer, sheet_name="usuarios_respondidos", index=False)
    df_nao_respondidos_p1.to_excel(writer, sheet_name="usuarios_nao_respondidos", index=False)

    # abas vazias + duplicados
    for aba, tabela in abas_vazias.items():
        tabela.to_excel(writer, sheet_name=aba, index=False)

print("✅ Arquivo criado com sucesso!")

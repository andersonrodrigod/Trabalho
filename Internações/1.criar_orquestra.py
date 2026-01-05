import pandas as pd
import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)

# ==========================================================
# 1) LEITURA DO ARQUIVO
# ==========================================================

df = pd.read_excel("NOVEMBRO GERAL.xlsx", sheet_name="BASE")
df.columns = df.columns.str.strip()

# ==========================================================
# 2) IDENTIFICAR DUPLICADOS (ANTES DE TUDO)
# ==========================================================

mask_duplicados = df.duplicated(subset=["COD USUARIO"], keep=False)

df_duplicados = df[mask_duplicados]
df_nao_duplicados = df[~mask_duplicados]

print(f"   ➜ Total duplicados: {len(df_duplicados)}")
print(f"   ➜ Total sem duplicados: {len(df_nao_duplicados)}")

# ==========================================================
# 3) COLUNAS FINAIS PADRÃO
# ==========================================================

colunas_finais = [
    'STATUS BOT', 'BASE', 'COD USUARIO', 'USUARIO', 'TELEFONE RELATORIO',
    'TELEFONE 1', 'TELEFONE 2', 'TELEFONE 3', 'TELEFONE 4', 'TELEFONE 5',
    'TP ATENDIMENTO', 'DT INTERNACAO', 'ENVIO',
    'ULTIMO STATUS DE ENVIO','IDENTIFICACAO', 'RESPOSTA', 'LIDA', 'ENTREGUE', 'ENVIADA',
    'NAO_ENTREGUE_META', 'MENSAGEM_NAO_ENTREGUE', 'EXPERIMENTO',
    'OPT_OUT', 'TELEFONE ENVIADO', 'CHAVE RELATORIO', 'CHAVE STATUS',
    'STATUS TELEFONE', 'STATUS CHAVE', "PROCESSO", "QT TELEFONE"
]

colunas_envio_telefonico = [
    'BASE',
    'COD USUARIO',
    'USUARIO',
    'PRESTADOR',
    'PROCEDIMENTO',
    'TELEFONE ENVIADO',
    'TIPO TELEFONE',
    'DATA ENVIO',
    'ENVIO_ID',
    'TENTATIVA',
    'ULTIMO STATUS DE ENVIO',
    'LIDA',
    'RESPONDIDO',
    'ENTREGUE',
    'STATUS TELEFONE',
    'STATUS CHAVE',
    'SOMA STATUS',
    'CHAVE RELATORIO',
    'CHAVE STATUS',
    'PROCESSO'
]

# ==========================================================
# 4) FUNÇÃO PADRÃO PARA MONTAR DATAFRAME FINAL
# ==========================================================

def montar_df_final(df):
    df_final = pd.DataFrame(columns=colunas_finais)

    if "BASE" in df: df_final["BASE"] = df["BASE"]
    if "COD USUARIO" in df: df_final["COD USUARIO"] = df["COD USUARIO"]
    if "USUARIO" in df: df_final["USUARIO"] = df["USUARIO"]
    if "TELEFONE" in df: df_final["TELEFONE RELATORIO"] = df["TELEFONE"]
    if 'TP ATENDIMENTO' in df: df_final['TP ATENDIMENTO'] = df['TP ATENDIMENTO']
    if 'DT ENVIO' in df: df_final['ENVIO'] = df['DT ENVIO']
    if 'CHAVE' in df: df_final['CHAVE RELATORIO'] = df['CHAVE']

    for col in colunas_finais:
        if col not in df_final.columns:
            df_final[col] = ""

    return df_final

# ==========================================================
# 5) ABA USUARIOS (BASE MESTRA — SEM DUPLICADOS)
# ==========================================================

df_usuarios = montar_df_final(df_nao_duplicados)

# ==========================================================
# 6) ABAS DERIVADAS (SEMPRE A PARTIR DE df_sem_duplicados)
# ==========================================================

# --- usuarios_nao_lidos

filtro_nao_lidos = (df_nao_duplicados["STATUS"].isna()) | (df_nao_duplicados['STATUS'] == "")
df_usuarios_nao_lidos = montar_df_final(df_nao_duplicados[filtro_nao_lidos])

# --- usuarios_lidos
status_validos = ["Lida", "Não quis", "Óbito"]
df_usuarios_lidos = montar_df_final(df_nao_duplicados[df_nao_duplicados['STATUS'].isin(status_validos)])

# --- respondidos / nao respondidos P1
df_respondidos_p1 = montar_df_final(df[df["P1"].notna()])
df_nao_respondidos_p1 = montar_df_final(df[df["P1"].isna()])

# ==========================================================
# 7) ABA USUARIOS DUPLICADOS (ISOLADA)
# ==========================================================

df_duplicados = montar_df_final(df_duplicados)

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

df_dados_envio_telefonico = pd.DataFrame(columns=colunas_envio_telefonico)

with pd.ExcelWriter("novos_contatos.xlsx", engine="openpyxl") as writer:
    df_usuarios.to_excel(writer, sheet_name="usuarios", index=False)
    df_usuarios_nao_lidos.to_excel(writer, sheet_name="usuarios_nao_lidos", index=False)
    df_usuarios_lidos.to_excel(writer, sheet_name="usuarios_lidos", index=False)
    df_respondidos_p1.to_excel(writer, sheet_name="usuarios_respondidos", index=False)
    df_nao_respondidos_p1.to_excel(writer, sheet_name="usuarios_nao_respondidos", index=False)
    df_duplicados.to_excel(writer, sheet_name="usuarios_duplicados", index=False)
    df_dados_envio_telefonico.to_excel(writer, sheet_name="dados_envio_telefonico", index=False)
    
    for aba, tabela in abas_vazias.items():
        tabela.to_excel(writer, sheet_name=aba, index=False)

print("✅ Arquivo criado com sucesso!")



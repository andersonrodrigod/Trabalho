import pandas as pd
import numpy as np
from controle_usuarios import ingestao_usuarios

print("📘 Lendo NOVEMBRO GERAL.xlsx ...")
df_base = pd.read_excel("NOVEMBRO GERAL 13.12.xlsx", sheet_name="BASE")
df_base.columns = df_base.columns.str.strip()

print("📗 Lendo novos_contatos.xlsx ...")
abas = pd.read_excel("novos_contatos.xlsx", sheet_name=None)

abas = ingestao_usuarios(df_base, abas)

# -------------------------
# COLUNAS FINAIS PADRÃO
# -------------------------
colunas_finais = [
    'STATUS BOT', 'BASE', 'COD USUARIO', 'USUARIO',
    'TELEFONE RELATORIO', 'TELEFONE 1', 'TELEFONE 2', 'TELEFONE 3', 'TELEFONE 4', 'TELEFONE 5',
    'PRESTADOR', 'PROCEDIMENTO', 'TP ATENDIMENTO', 'DT INTERNACAO', 'ENVIO',
    'ULTIMO STATUS DE ENVIO', 'LIDA', 'ENTREGUE', 'ENVIADA',
    'NAO_ENTREGUE_META', 'MENSAGEM_NAO_ENTREGUE', 'EXPERIMENTO', 'OPT_OUT',
    'TELEFONE ENVIADO', 'CHAVE RELATORIO', 'CHAVE STATUS',
    'STATUS TELEFONE', 'STATUS CHAVE',
    'QT TELEFONE', 'QT LIDA', 'QT ENTREGUE', 'QT ENVIADA',
    'QT NAO_ENTREGUE_META', 'QT MENSAGEM_NAO_ENTREGUE',
    'QT EXPERIMENTO', 'QT OPT_OUT'
]

# -------------------------
# Função de padronização
# -------------------------
def montar_df_final(df_base):
    df_final = pd.DataFrame(columns=colunas_finais)

    def copia(origem, destino):
        if origem in df_base:
            df_final[destino] = df_base[origem]
        else:
            df_final[destino] = ""

    copia("BASE", "BASE")
    copia("COD USUARIO", "COD USUARIO")
    copia("USUARIO", "USUARIO")
    copia("TELEFONE", "TELEFONE RELATORIO")
    copia("PRESTADOR", "PRESTADOR")
    copia("PROCEDIMENTO", "PROCEDIMENTO")
    copia("TP ATENDIMENTO", "TP ATENDIMENTO")
    copia("DT INTERNACAO", "DT INTERNACAO")
    copia("DT ENVIO", "ENVIO")
    copia("CHAVE", "CHAVE RELATORIO")

    return df_final

# -------------------------
# ABA usuarios_nao_lidos — STATUS vazio
# -------------------------

print("🔍 Identificando duplicados por COD USUARIO + USUARIO...")

mask_duplicados = df_base.duplicated(
    subset=["COD USUARIO", "USUARIO"],
    keep=False
)

print(f"   ➜ Total de linhas duplicadas (par COD+USUARIO): {mask_duplicados.sum()}")
filtro_nao_lidos = df_base[
    (
        df_base["STATUS"].isna() |
        (df_base["STATUS"].astype(str).str.strip() == "")
    )
    &
    (~mask_duplicados)
]

df_usuarios_nao_lidos = montar_df_final(filtro_nao_lidos)

# -------------------------
# ABA usuarios_lidos — STATUS válido
# -------------------------
status_validos = ["Lida", "Não quis", "Óbito"]
filtro_lidos = df_base[df_base["STATUS"].isin(status_validos)]
df_lidos = montar_df_final(filtro_lidos)

# -------------------------
# usuarios_respondidos — P1 preenchido
# -------------------------
df_respondidos = montar_df_final(df_base[df_base["P1"].notna()])

# -------------------------
# usuarios_nao_respondidos — P1 vazio
# -------------------------
df_nao_respondidos = montar_df_final(df_base[df_base["P1"].isna()])

# -------------------------
# Atualizar SOMENTE AS ABAS necessárias
# -------------------------
abas["usuarios_lidos"] = df_lidos
abas["usuarios_nao_lidos"] = df_usuarios_nao_lidos
abas["usuarios_respondidos"] = df_respondidos
abas["usuarios_nao_respondidos"] = df_nao_respondidos

# NÃO altera:
# - usuarios
# - usuarios_resolvidos
# - usuarios_duplicados
# - segundo_envio_lidos
# - bases (HAP, CCG, etc)

# -------------------------
# SALVAR ARQUIVO FINAL
# -------------------------
print("💾 Salvando novos_contatos_atualizados.xlsx ...")
with pd.ExcelWriter("novos_contatos_atualizados.xlsx", engine="openpyxl") as writer:
    for nome_aba, tabela in abas.items():
        tabela.to_excel(writer, sheet_name=nome_aba, index=False)

print("🎉 Arquivo atualizado com sucesso!")

import pandas as pd
import numpy as np
from controle_usuarios import retornar_registros_para_usuarios

# ============================================================
# LEITURA DOS ARQUIVOS
# ============================================================

print("📘 Lendo a planilha novos_contatos.xlsx ...")
abas = pd.read_excel("novos_contatos.xlsx", sheet_name=None)
abas = retornar_registros_para_usuarios(abas)
df_novos = abas["usuarios"].copy()
print("   ✔ Aba usuarios carregada!\n")

print("📗 Lendo a planilha status.xlsx ...")
df_status = pd.read_excel("status.xlsx")
print("   ✔ Planilha tratada carregada!\n")

# ============================================================
# NORMALIZAÇÃO
# ============================================================

df_novos["USUARIO"] = df_novos["USUARIO"].astype(str).str.strip()
df_status["nome_manipulado"] = df_status["nome_manipulado"].astype(str).str.strip()

# ============================================================
# MAPA DE STATUS
# ============================================================

status_colunas = {
    "Lida": "LIDA",
    "Entregue": "ENTREGUE",
    "Enviada": "ENVIADA",
    "A Meta decidiu não entregar a mensagem": "NAO_ENTREGUE_META",
    "Mensagem não pode ser entregue": "MENSAGEM_NAO_ENTREGUE",
    "Número é parte de um experimento": "EXPERIMENTO",
    "MKT messages": "OPT_OUT"
}

colunas_dados_envio_telefonico = [
    "BASE",
    "COD USUARIO",
    "USUARIO",
    "PRESTADOR",
    "PROCEDIMENTO",
    "TELEFONE ENVIADO",
    "ULTIMO STATUS DE ENVIO",
    "RESPONDIDO",
    "ENVIO",
    "STATUS TELEFONE",
    "STATUS CHAVE",
    "CHAVE RELATORIO",
    "CHAVE STATUS",
]

# ============================================================
# GARANTIR COLUNAS DE STATUS E QT
# ============================================================

for col in status_colunas.values():
    if col not in df_novos.columns:
        df_novos[col] = np.nan

    qt_col = "QT " + col
    if qt_col not in df_novos.columns:
        df_novos[qt_col] = np.nan


# ============================================================
# PRESERVAR STATUS ANTIGO
# ============================================================

df_novos["STATUS_ANTIGO"] = df_novos["ULTIMO STATUS DE ENVIO"]

# ============================================================
# 🔥 EVENTOS REAIS NA status.xlsx (BASE DE DECISÃO)
# ============================================================

df_status["EVENTO_REAL"] = (
    df_status["Contato"].astype(str) + "|" +
    df_status["Telefone"].astype(str) + "|" +
    df_status["Data do envio"].astype(str)
)

df_eventos_status = (
    df_status
    .groupby("Contato")["EVENTO_REAL"]
    .nunique()
    .rename("QT_EVENTOS_STATUS")
    .reset_index()
)

# ============================================================
# PEGAR ÚLTIMO STATUS POR CONTATO
# ============================================================

df_status_last = (
    df_status
    .sort_values(by=df_status.columns.tolist())
    .groupby("Contato")
    .last()
    .reset_index()
)

# ============================================================
# MERGE
# ============================================================

df_merge = df_novos.merge(
    df_status_last[["nome_manipulado", "Status", "Telefone", "Contato", "Respondido", "Data do envio"]],
    left_on="USUARIO",
    right_on="nome_manipulado",
    how="left"
)

df_merge = df_merge.merge(
    df_eventos_status,
    on="Contato",
    how="left"
)

# ============================================================
# ATRIBUIÇÕES
# ============================================================

df_merge["ULTIMO STATUS DE ENVIO"] = df_merge["Status"]
df_merge["TELEFONE ENVIADO"] = df_merge["Telefone"]
df_merge["CHAVE STATUS"] = df_merge["Contato"]
df_merge["RESPONDIDO"] = df_merge["Respondido"]
df_merge["ENVIO"] = df_merge["Data do envio"]

mask_status_recebido = df_merge["ULTIMO STATUS DE ENVIO"].notna()


# ============================================================
# SOMAR STATUS NOVO (REGRA FINAL)
# ============================================================

for status, coluna in status_colunas.items():

    cond_mudou_status = (
        (df_merge["ULTIMO STATUS DE ENVIO"] == status) &
        (df_merge["ULTIMO STATUS DE ENVIO"] != df_merge["STATUS_ANTIGO"])
    )

    cond_mesmo_status_novo_evento = (
        (df_merge["ULTIMO STATUS DE ENVIO"] == status) &
        (df_merge["ULTIMO STATUS DE ENVIO"] == df_merge["STATUS_ANTIGO"]) &
        (df_merge["QT_EVENTOS_STATUS"].fillna(1) > 1)
    )

    cond = cond_mudou_status | cond_mesmo_status_novo_evento

    # coluna principal
    df_merge.loc[cond & df_merge[coluna].isna(), coluna] = 0
    df_merge.loc[cond & df_merge[coluna].notna(), coluna] += 1

    # coluna QT
    qt_col = "QT " + coluna
    df_merge.loc[cond & df_merge[qt_col].isna(), qt_col] = 0
    df_merge.loc[cond, qt_col] += 1

# ============================================================
# VERIFICAÇÕES DE CHAVE E TELEFONE
# ============================================================

df_merge["STATUS CHAVE"] = np.where(
    df_merge["CHAVE STATUS"] == df_merge["CHAVE RELATORIO"],
    "OK",
    "ERRO"
)

telefones_lista = [
    "TELEFONE RELATORIO", "TELEFONE 1", "TELEFONE 2",
    "TELEFONE 3", "TELEFONE 4", "TELEFONE 5"
]

df_merge["STATUS TELEFONE"] = df_merge.apply(
    lambda r: "OK" if r["TELEFONE ENVIADO"] in [r[c] for c in telefones_lista] else "ERRO",
    axis=1
)

# ============================================================
# PROCESSO
# ============================================================

ch_respondidos = set(abas["usuarios_respondidos"]["CHAVE RELATORIO"].astype(str))
ch_lidos = set(abas["usuarios_lidos"]["CHAVE RELATORIO"].astype(str))
ch_nao_lidos = set(abas["usuarios_nao_lidos"]["CHAVE RELATORIO"].astype(str))

def definir_processo(ch):
    if ch in ch_respondidos:
        return "RESPONDIDO"
    elif ch in ch_lidos:
        return "LIDO"
    elif ch in ch_nao_lidos:
        return "NÃO LIDO"
    else:
        return "SEM RESULTADO"

df_merge["PROCESSO"] = df_merge["CHAVE RELATORIO"].astype(str).apply(definir_processo)

# ============================================================
# DADOS DE ENVIO TELEFÔNICO
# ============================================================

df_dados_envio_telefonico = (
    df_merge.loc[mask_status_recebido, colunas_dados_envio_telefonico + ["PROCESSO"]]
    .copy()
)

# ============================================================
# CONCATENAR HISTÓRICO
# ============================================================

if "dados_envio_telefonico" in abas:
    hist = abas["dados_envio_telefonico"].copy()
    hist = hist.reindex(columns=df_dados_envio_telefonico.columns)
    df_dados_envio_telefonico = pd.concat(
        [hist, df_dados_envio_telefonico],
        ignore_index=True
    )

# ============================================================
# LIMPEZA
# ============================================================

df_merge = df_merge.drop(
    columns=[
        "nome_manipulado", "Status", "Contato", "Telefone",
        "Respondido", "Data do envio", "QT_EVENTOS_STATUS"
    ],
    errors="ignore"
)

# ============================================================
# SALVAR
# ============================================================

abas["usuarios"] = df_merge
abas["dados_envio_telefonico"] = df_dados_envio_telefonico

print("💾 Salvando novos_contatos_atualizado.xlsx ...")
with pd.ExcelWriter("novos_contatos_atualizados.xlsx", engine="openpyxl") as writer:
    for nome_aba, df in abas.items():
        df.to_excel(writer, sheet_name=nome_aba, index=False)

print("🎉 Arquivo final criado com sucesso!")

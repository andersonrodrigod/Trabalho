import pandas as pd
import numpy as np
import re
import warnings
from controle_usuarios import retornar_registros_para_usuarios
warnings.simplefilter(action="ignore", category=FutureWarning)

# ============================================================
# LEITURA
# ============================================================

print("📘 Lendo novos_contatos.xlsx ...")
abas = pd.read_excel("novos_contatos.xlsx", sheet_name=None)
abas = retornar_registros_para_usuarios(abas)


if "usuarios" not in abas:
    raise ValueError("Aba 'usuarios' não encontrada")

df_novos = abas["usuarios"].copy()
print("✔ usuarios carregado:", df_novos.shape)

print("\n📗 Lendo status.xlsx ...")
df_status = pd.read_excel("status.xlsx", dtype={"Telefone": str, "Contato": str})
print("✔ status carregado:", df_status.shape)

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

# ============================================================
# NORMALIZAÇÃO STATUS
# ============================================================

df_status["Contato"] = df_status["Contato"].astype(str).str.strip()
df_status["NOME_NORM"] = df_status["nome_manipulado"].astype(str).str.strip().str.upper()
df_status["TELEFONE_NORM"] = df_status["Telefone"].astype(str).str.replace(r"\D", "", regex=True)

df_status["DATA_ENVIO"] = pd.to_datetime(
    df_status["Data de envio"],
    dayfirst=True,
    errors="coerce"
)

df_status["DATA_AGENDAMENTO"] = pd.to_datetime(
    df_status["Data agendamento"],
    dayfirst=True,
    errors="coerce"
).dt.date

df_status["DATA_EVENTO"] = df_status["DATA_ENVIO"].fillna(df_status["DATA_AGENDAMENTO"])

print("⚠️ Registros SEM DATA_EVENTO:",
      df_status["DATA_EVENTO"].isna().sum())

# ============================================================
# ESTADO ATUAL (ÚLTIMO EVENTO)
# ============================================================

df_estado_atual = (
    df_status
    .sort_values("DATA_EVENTO")
    .groupby("Contato", as_index=False)
    .last()
)

# ============================================================
# PREPARAÇÃO USUÁRIOS
# ============================================================

df_novos["CHAVE RELATORIO"] = df_novos["CHAVE RELATORIO"].astype(str).str.strip()
df_novos["NOME_NORM"] = df_novos["USUARIO"].astype(str).str.strip().str.upper()

# ============================================================
# FUNÇÃO DE NORMALIZAÇÃO DE TELEFONE (ROBUSTA)
# ============================================================

def normalizar_tel(v):
    if pd.isna(v):
        return ""
    if isinstance(v, (int, float)):
        v = str(int(v))
    return re.sub(r"\D", "", str(v))

# ============================================================
# VIA CHAVE (PRIORIDADE MÁXIMA)
# ============================================================

map_chave = df_estado_atual.set_index("Contato")
mask_chave = df_novos["CHAVE RELATORIO"].isin(map_chave.index)

df_novos.loc[mask_chave, "ULTIMO STATUS DE ENVIO"] = \
    df_novos.loc[mask_chave, "CHAVE RELATORIO"].map(map_chave["Status"])

df_novos.loc[mask_chave, "TELEFONE ENVIADO"] = \
    df_novos.loc[mask_chave, "CHAVE RELATORIO"].map(map_chave["Telefone"])

df_novos.loc[mask_chave, "IDENTIFICACAO"] = \
    df_novos.loc[mask_chave, "CHAVE RELATORIO"].map(map_chave["Respondido"])

df_novos.loc[mask_chave, "DATA_EVENTO"] = \
    df_novos.loc[mask_chave, "CHAVE RELATORIO"].map(map_chave["DATA_EVENTO"])

df_novos.loc[mask_chave, "RESPOSTA"] = \
    df_novos.loc[mask_chave, "CHAVE RELATORIO"].map(map_chave["Resposta"])

df_novos.loc[mask_chave, "CHAVE STATUS"] = \
    df_novos.loc[mask_chave, "CHAVE RELATORIO"]

print("✔ VIA CHAVE:", mask_chave.sum())

# ============================================================
# FALLBACK (NOME + TELEFONE) — SÓ SE NÃO PEGOU VIA CHAVE
# ============================================================

df_novos["TELEFONE ENVIADO_NORM"] = df_novos["TELEFONE 1"].apply(normalizar_tel)

map_fallback = (
    df_estado_atual
    .dropna(subset=["NOME_NORM", "TELEFONE_NORM"])
    .set_index(["NOME_NORM", "TELEFONE_NORM"])
)

mask_fallback = (
    df_novos["ULTIMO STATUS DE ENVIO"].isna()
    & df_novos.set_index(["NOME_NORM", "TELEFONE ENVIADO_NORM"]).index.isin(map_fallback.index)
)

idx_fb = (
    df_novos.loc[mask_fallback]
    .set_index(["NOME_NORM", "TELEFONE ENVIADO_NORM"])
    .index
)

df_novos.loc[mask_fallback, "ULTIMO STATUS DE ENVIO"] = idx_fb.map(map_fallback["Status"])
df_novos.loc[mask_fallback, "TELEFONE ENVIADO"] = idx_fb.map(map_fallback["Telefone"])
df_novos.loc[mask_fallback, "IDENTIFICACAO"] = idx_fb.map(map_fallback["Respondido"])
df_novos.loc[mask_fallback, "DATA_EVENTO"] = idx_fb.map(map_fallback["DATA_EVENTO"])
df_novos.loc[mask_fallback, "CHAVE STATUS"] = idx_fb.map(map_fallback["Contato"])
df_novos.loc[mask_fallback, "RESPOSTA"] = idx_fb.map(map_fallback["Resposta"])

print("✔ FALLBACK:", mask_fallback.sum())

# ============================================================
# CONTAGEM DE STATUS
# ============================================================

df_status["STATUS_MAP"] = (df_status["Status"].map(status_colunas).fillna("OUTROS"))

contagem_total = (
    df_status
    .groupby(["Contato", "STATUS_MAP"])
    .size()
    .unstack(fill_value=0)
)
    
for col in status_colunas.values():
    qt_col = f"QT {col}"

    if col in contagem_total.columns:
        df_novos[qt_col] = (
            df_novos["CHAVE STATUS"]
            .map(contagem_total[col])
            .fillna(0)
            .astype(int)
        )
    else:
        df_novos[qt_col] = 0


contagem_tel_nome = (
    df_status
    .dropna(subset=["NOME_NORM", "TELEFONE_NORM"])
    .groupby(["NOME_NORM", "TELEFONE_NORM", "STATUS_MAP"])
    .size()
    .unstack(fill_value=0)
)

idx_tel_nome = (
    df_novos
    .set_index(["NOME_NORM", "TELEFONE ENVIADO_NORM"])
    .index
)

for col in status_colunas.values():
    if col in contagem_tel_nome.columns:
        df_novos[col] = (
            idx_tel_nome
            .map(contagem_tel_nome[col])
            .fillna(0)
            .astype(int)
        )
    else:
        df_novos[col] = 0



print("✔ Contagem aplicada")

# ============================================================
# TELEFONE PRIORIDADE
# ============================================================

colunas_tel = ["TELEFONE 1", "TELEFONE 2", "TELEFONE 3", "TELEFONE 4", "TELEFONE 5"]

df_novos["TELEFONE ENVIADO_NORM"] = df_novos["TELEFONE ENVIADO"].apply(normalizar_tel)

for c in colunas_tel:
    df_novos[c + "_NORM"] = df_novos[c].apply(normalizar_tel)

def identificar_prioridade(row):
    tel_env = row["TELEFONE ENVIADO_NORM"]
    if not tel_env:
        return np.nan
    for c in colunas_tel:
        if row[c + "_NORM"] == tel_env:
            return c
    return "NAO_ENCONTRADO"

df_novos["TELEFONE PRIORIDADE"] = df_novos.apply(identificar_prioridade, axis=1)

# ============================================================
# STATUS DE CONSISTÊNCIA
# ============================================================

df_novos["STATUS CHAVE"] = np.where(
    df_novos["CHAVE STATUS"] == df_novos["CHAVE RELATORIO"],
    "OK",
    "ERRO"
)

df_novos["STATUS TELEFONE"] = np.where(
    df_novos["TELEFONE PRIORIDADE"] == "NAO_ENCONTRADO",
    "ERRO",
    "OK"
)

# ============================================================
# EXPORTAÇÃO
# ============================================================

df_export = df_novos.copy()

df_export = df_export.loc[:, ~df_export.columns.str.endswith("_NORM")]
df_export = df_export.drop(columns=["DATA_EVENTO"], errors="ignore")

# colunas originais
df_export[list(status_colunas.values())] = \
    df_export[list(status_colunas.values())].replace(0, np.nan)

# colunas QT
df_export[[f"QT {c}" for c in status_colunas.values()]] = \
    df_export[[f"QT {c}" for c in status_colunas.values()]].replace(0, np.nan)

abas["usuarios"] = df_export

with pd.ExcelWriter("novos_contatos_atualizado.xlsx") as writer:
    for nome, df in abas.items():
        df.to_excel(writer, sheet_name=nome, index=False)

print("\n💾 Arquivo salvo com estrutura preservada")

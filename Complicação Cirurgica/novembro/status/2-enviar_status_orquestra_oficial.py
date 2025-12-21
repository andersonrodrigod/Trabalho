import pandas as pd
import numpy as np
from controle_usuarios import retornar_registros_para_usuarios
import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)

# ============================================================
# LEITURA
# ============================================================

print("📘 Lendo novos_contatos.xlsx ...")
abas = pd.read_excel("novos_contatos.xlsx", sheet_name=None)
abas = retornar_registros_para_usuarios(abas)
df_novos = abas["usuarios"].copy()
print("✔ usuarios carregado:", df_novos.shape)

print("\n📗 Lendo status.xlsx ...")
df_status = pd.read_excel("status.xlsx")
print("✔ status carregado:", df_status.shape)

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
# NORMALIZAÇÃO
# ============================================================

df_novos["CHAVE RELATORIO"] = df_novos["CHAVE RELATORIO"].astype(str).str.strip()

df_status["Contato"] = df_status["Contato"].astype(str).str.strip()
df_status["NOME_NORM"] = df_status["nome_manipulado"].astype(str).str.strip().str.upper()
df_status["TELEFONE_NORM"] = df_status["Telefone"].astype(str).str.replace(r"\D", "", regex=True)

df_status["DATA_ENVIO"] = pd.to_datetime(df_status["Data do envio"], dayfirst=True, errors="coerce")
df_status["DATA_AGENDAMENTO"] = pd.to_datetime(df_status["Data agendamento"], dayfirst=True, errors="coerce")
df_status["DATA_EVENTO"] = df_status["DATA_ENVIO"].fillna(df_status["DATA_AGENDAMENTO"])

# ============================================================
# ESTADO ATUAL (ÚLTIMO EVENTO)
# ============================================================

df_status_sorted = df_status.sort_values("DATA_EVENTO")
df_estado_atual = df_status_sorted.groupby("Contato", as_index=False).last()

# ============================================================
# PREPARAÇÃO USUÁRIOS
# ============================================================

df_novos["NOME_NORM"] = df_novos["USUARIO"].astype(str).str.strip().str.upper()
df_novos["TELEFONE_NORM"] = df_novos["TELEFONE RELATORIO"].astype(str).str.replace(r"\D", "", regex=True)

# ============================================================
# 1. VIA CHAVE
# ============================================================

map_chave = df_estado_atual.set_index("Contato")
mask_chave = df_novos["CHAVE RELATORIO"].isin(map_chave.index)

df_novos.loc[mask_chave, "ULTIMO STATUS DE ENVIO"] = df_novos.loc[mask_chave, "CHAVE RELATORIO"].map(map_chave["Status"])
df_novos.loc[mask_chave, "TELEFONE ENVIADO"]       = df_novos.loc[mask_chave, "CHAVE RELATORIO"].map(map_chave["Telefone"])
df_novos.loc[mask_chave, "RESPONDIDO"]             = df_novos.loc[mask_chave, "CHAVE RELATORIO"].map(map_chave["Respondido"])
df_novos.loc[mask_chave, "DATA_EVENTO"]            = df_novos.loc[mask_chave, "CHAVE RELATORIO"].map(map_chave["DATA_EVENTO"])
df_novos.loc[mask_chave, "CHAVE STATUS"]           = df_novos.loc[mask_chave, "CHAVE RELATORIO"]

print("✔ VIA CHAVE:", mask_chave.sum())

# ============================================================
# 2. FALLBACK (SÓ SE NÃO PREENCHEU)
# ============================================================

map_fallback = (
    df_estado_atual
    .dropna(subset=["NOME_NORM", "TELEFONE_NORM"])
    .set_index(["NOME_NORM", "TELEFONE_NORM"])
)

mask_fallback = (
    df_novos["ULTIMO STATUS DE ENVIO"].isna()
    & df_novos.set_index(["NOME_NORM", "TELEFONE_NORM"]).index.isin(map_fallback.index)
)

idx_fb = df_novos.loc[mask_fallback].set_index(["NOME_NORM", "TELEFONE_NORM"]).index

df_novos.loc[mask_fallback, "ULTIMO STATUS DE ENVIO"] = idx_fb.map(map_fallback["Status"])
df_novos.loc[mask_fallback, "TELEFONE ENVIADO"]       = idx_fb.map(map_fallback["Telefone"])
df_novos.loc[mask_fallback, "RESPONDIDO"]             = idx_fb.map(map_fallback["Respondido"])
df_novos.loc[mask_fallback, "DATA_EVENTO"]            = idx_fb.map(map_fallback["DATA_EVENTO"])
df_novos.loc[mask_fallback, "CHAVE STATUS"]           = idx_fb.map(map_fallback["Contato"])

print("✔ VIA FALLBACK:", mask_fallback.sum())

# ============================================================
# 3. CONTAGEM DE STATUS (SEM QUEBRAR BASE)
# ============================================================

df_status_sorted["STATUS_MAP"] = df_status_sorted["Status"].map(status_colunas)

contagem = (
    df_status_sorted
    .groupby(["Contato", "STATUS_MAP"])
    .size()
    .unstack(fill_value=0)
)

for col in status_colunas.values():
    if col not in df_novos.columns:
        df_novos[col] = 0
    df_novos[col] = df_novos["CHAVE RELATORIO"].map(contagem[col]).fillna(0).astype(int)

print("✔ Contagem aplicada")

# ============================================================
# INSPEÇÕES
# ============================================================


df_novos["STATUS CHAVE"] = np.where(
    df_novos["CHAVE STATUS"] == df_novos["CHAVE RELATORIO"],
    "OK",
    "ERRO"
)

colunas_tel = ["TELEFONE RELATORIO","TELEFONE 1","TELEFONE 2","TELEFONE 3","TELEFONE 4","TELEFONE 5"]

for c in colunas_tel:
    if c in df_novos.columns:
        df_novos[c+"_NORM"] = df_novos[c].astype(str).str.replace(r"\D","",regex=True)

df_novos["TELEFONE ENVIADO_NORM"] = df_novos["TELEFONE ENVIADO"].astype(str).str.replace(r"\D","",regex=True)

def conf_tel(r):
    return "OK" if r["TELEFONE ENVIADO_NORM"] in [r.get(c+"_NORM","") for c in colunas_tel] else "ERRO"

df_novos["STATUS TELEFONE"] = df_novos.apply(conf_tel, axis=1)

print("\n🎨 Ajustando visual: convertendo zeros dos status para vazio (NaN)...")

status_cols = list(status_colunas.values())

df_export = df_novos.copy()

df_export[status_cols] = df_export[status_cols].replace(0, np.nan)

print("✔ Zeros convertidos para NaN apenas na versão de exportação")


# ============================================================
# SALVAR
# ============================================================

abas["usuarios"] = df_export


with pd.ExcelWriter("novos_contatos_atualizado.xlsx") as writer:
    for nome, df in abas.items():
        df.to_excel(writer, sheet_name=nome, index=False)

print("\n💾 Arquivo salvo com estrutura preservada")

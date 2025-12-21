import pandas as pd
import numpy as np
from controle_usuarios import retornar_registros_para_usuarios
import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)

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

df_novos["CHAVE RELATORIO"] = df_novos["CHAVE RELATORIO"].astype(str).str.strip().str.replace(r"\s+", " ", regex=True)
df_status["Contato"] = df_status["Contato"].astype(str).str.strip().str.replace(r"\s+", " ", regex=True)
df_status["DATA_ENVIO"] = pd.to_datetime(df_status["Data do envio"], dayfirst=True, errors="coerce")
df_status["DATA_AGENDAMENTO"] = pd.to_datetime(df_status["Data agendamento"], dayfirst=True, errors="coerce")
df_status["ENVIO"] = df_status["DATA_ENVIO"].fillna(df_status["DATA_AGENDAMENTO"])
df_status["NOME_NORM"] = df_status["nome_manipulado"].astype(str).str.strip().str.upper()
df_status["TELEFONE_NORM"] = df_status["Telefone"].astype(str).str.replace(r"\D", "", regex=True)

print("Datas finais inválidas:", df_status["ENVIO"].isna().sum())

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

colunas_para_atualizar = [
    "CHAVE RELATORIO",
    "LIDA",
    "ENTREGUE",
    "ENVIADA",
    "NAO_ENTREGUE_META",
    "MENSAGEM_NAO_ENTREGUE",
    "EXPERIMENTO",
    "OPT_OUT"
]

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

# ============================================================
# VERIFICAR QUEM ESTÁ NA LISTA DE STATUS
# ============================================================

chaves_usuarios = set(df_novos["CHAVE RELATORIO"])
chaves_status = set(df_status["Contato"])
chaves_comuns = chaves_usuarios & chaves_status



df_status_validos = df_status[df_status["Contato"].isin(chaves_comuns)]
usuarios_sem_chave = df_novos.loc[~df_novos["CHAVE RELATORIO"].isin(chaves_status),["USUARIO", "TELEFONE RELATORIO"]].copy()



df_status_ordenado = df_status_validos.sort_values("ENVIO")
usuarios_sem_chave["NOME_NORM"] = usuarios_sem_chave["USUARIO"].astype(str).str.strip().str.upper()
usuarios_sem_chave["TELEFONE_NORM"] = usuarios_sem_chave["TELEFONE RELATORIO"].astype(str).str.replace(r"\D", "", regex=True)

#print("Sem chave:", usuarios_sem_chave.shape[0])


df_status_fallback = df_status.merge(
    usuarios_sem_chave,
    on=["NOME_NORM", "TELEFONE_NORM"],
    how="inner"
)
df_status_fallback = df_status_fallback[df_status.columns]
print("Colunas fallback:")
print(df_status_fallback.columns)
#print("Fallback matches:", df_status_fallback.shape[0])


df_status_unificado = pd.concat(
    [df_status_validos, df_status_fallback],
    ignore_index=True
).drop_duplicates()

df_status_ordenado = df_status_unificado.sort_values("ENVIO")

df_contagem = (df_status_unificado.groupby(["Contato", "Status"])).size().reset_index(name="QT_STATUS")
df_ultimo_status = (df_status_unificado.groupby("Contato").last().reset_index())

print("STATUS VIA CHAVE:", df_status_validos.shape[0])
print("STATUS VIA FALLBACK:", df_status_fallback.shape[0])
print("STATUS UNIFICADO:", df_status_unificado.shape[0])


df_ultimo_status = df_ultimo_status.rename(columns={
    "Contato": "CHAVE STATUS",
    "Status": "ULTIMO STATUS DE ENVIO",
    "Respondido": "RESPONDIDO",
    "ENVIO": "ENVIO",
    "Telefone": "TELEFONE ENVIADO",
})

df_pivot = (
    df_contagem
    .pivot(index="Contato", columns="Status", values="QT_STATUS")
    .fillna(0)
    .reset_index()
)

df_estado_atual = df_novos.merge(
    df_ultimo_status[
        ["CHAVE STATUS", "ULTIMO STATUS DE ENVIO", "RESPONDIDO", "ENVIO", "TELEFONE ENVIADO"]
    ],
    left_on="CHAVE RELATORIO",
    right_on="CHAVE STATUS",
    how="left"
)
colunas_estado_atual = [
    "ULTIMO STATUS DE ENVIO",
    "CHAVE STATUS",
    "RESPONDIDO",
    "ENVIO",
    "TELEFONE ENVIADO",
]

for col in colunas_estado_atual:
    if col in df_estado_atual.columns:
        df_novos[col] = df_estado_atual[col]

df_usuarios_atualizados = df_novos.merge(
    df_pivot,
    left_on="CHAVE RELATORIO",
    right_on="Contato",
    how="left"
)

for col in colunas_para_atualizar:
    if col in df_usuarios_atualizados.columns:
        df_novos[col] = df_usuarios_atualizados[col]


# ============================================================
# STATUS TELEFONE (INSPEÇÃO)
# ============================================================

colunas_telefones = [
    "TELEFONE RELATORIO",
    "TELEFONE 1",
    "TELEFONE 2",
    "TELEFONE 3",
    "TELEFONE 4",
    "TELEFONE 5",
]

def validar_telefone(row):
    telefone_enviado = str(row["TELEFONE ENVIADO"])
    telefones_usuario = [str(row[col]) for col in colunas_telefones if col in row]
    return "OK" if telefone_enviado in telefones_usuario else "ERRO"

df_novos["STATUS TELEFONE"] = df_novos.apply(validar_telefone, axis=1)

# ============================================================
# STATUS CHAVE (INSPEÇÃO)
# ============================================================

df_novos["STATUS CHAVE"] = np.where(
    df_novos["CHAVE RELATORIO"] == df_novos["CHAVE STATUS"],
    "OK",
    "ERRO"
)
abas["usuarios"] = df_novos
#abas["dados_envio_telefonico"] = df_dados_envio_telefonico

print("💾 Salvando novos_contatos_atualizado.xlsx ...")

with pd.ExcelWriter("novos_contatos_atualizado.xlsx") as writer:
    for nome_aba, df in abas.items():
        df.to_excel(writer, sheet_name=nome_aba, index=False)
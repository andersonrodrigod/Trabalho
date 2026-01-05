import pandas as pd

print("📘 Lendo o arquivo status.xlsx ...")
df = pd.read_excel("status.xlsx")
print("✅ Arquivo carregado com sucesso!\n")

# ============================================================
# 0) ATUALIZAÇÃO DE RESPOSTAS (ANTES DE QUALQUER CORREÇÃO)
#    USANDO CONTATO + DATA DE ATENDIMENTO
# ============================================================

print("🔄 Atualizando coluna 'Resposta' a partir do arquivo status_resposta.xlsx...")

df_resposta = pd.read_excel("status_resposta.xlsx")


# ----------------------------
# NORMALIZAÇÃO DAS CHAVES
# ----------------------------

# contato
df["Contato"] = df["Contato"].astype(str).str.strip()
df_resposta["nom_contato"] = df_resposta["nom_contato"].astype(str).str.strip()

# cria nova coluna só com datas sem horas
df["Data de envio"] = pd.to_datetime(df["Data agendamento"], errors="coerce").dt.date

print(df["Data de envio"].head())

df_resposta["dat_atendimento"] = pd.to_datetime(
    df_resposta["dat_atendimento"], errors="coerce", dayfirst=True
).dt.date

# ----------------------------
# MERGE COM DUAS CHAVES
# ----------------------------

df = df.merge(
    df_resposta[["nom_contato", "dat_atendimento", "resposta"]],
    left_on=["Contato", "Data de envio"],
    right_on=["nom_contato", "dat_atendimento"],
    how="left"
)

# ----------------------------
# AJUSTE FINAL
# ----------------------------

df["Resposta"] = df["resposta"].fillna("Sem resposta")

df.drop(
    columns=["nom_contato", "dat_atendimento", "resposta"],
    inplace=True,
    errors="ignore"
)

print("   ✔ Coluna 'Resposta' atualizada com sucesso!\n")

# ------------------------------------------------------------
# 1) CORREÇÃO DE TEXTOS E CARACTERES SUBSTITUÍDOS
# ------------------------------------------------------------

print("🔧 Corrigindo textos da coluna HSM...")

hsm_antes = df["HSM"].copy()

df["HSM"] = df["HSM"].replace({
    "Pesquisa Complicaτ⌡es Cirurgicas": "Complicações cirurgicas"
})

print("📅 Ajustando coluna 'Data de envio' para conter apenas a data...")


print("   ✔ Coluna 'Data de envio' ajustada com sucesso!\n")

alteracoes_hsm = (hsm_antes != df["HSM"]).sum()
print(f"   ✔ Correções na coluna HSM concluídas. Alterações feitas: {alteracoes_hsm}\n")

# ------------------------------------------------------------

print("🔧 Corrigindo textos da coluna Status...")

status_antes = df["Status"].copy()

df["Status"] = df["Status"].replace({
    "A Meta decidiu nπo entregar a mensagem": "A Meta decidiu não entregar a mensagem",
    "N·mero Θ parte de um experimento": "Número é parte de um experimento",
    "Usußrio decidiu nπo receber MKT messages": "MKT messages",
    "Mensagem nπo pode ser entregue": "Mensagem não pode ser entregue"
})

alteracoes_status = (status_antes != df["Status"]).sum()
print(f"   ✔ Correções na coluna Status concluídas. Alterações feitas: {alteracoes_status}\n")

# ------------------------------------------------------------

print("🔧 Corrigindo textos da coluna Respondido...")

resp_antes = df["Respondido"].copy()

df["Respondido"] = df["Respondido"].replace({
    "Nπo": "Não"
})

df["Resposta"] = df["Resposta"].replace({
    "Nπo": "Não"
})


alteracoes_resp = (resp_antes != df["Respondido"]).sum()
print(f"   ✔ Correções na coluna Respondido concluídas. Alterações feitas: {alteracoes_resp}\n")

# ------------------------------------------------------------
# 2) EXCLUSÃO DE LINHAS ESPECÍFICAS NA COLUNA HSM
# ------------------------------------------------------------

print("🗑 Excluindo linhas específicas da coluna HSM...")

linhas_antes = len(df)

df = df[df["HSM"] != "Pesquisa_Pos_cir_urg_intern"]
df = df[df["HSM"] != "Pesquisa_Pos_cir_eletivo"]

linhas_deletadas = linhas_antes - len(df)
print(f"   ✔ Linhas indesejadas removidas. Total excluídas: {linhas_deletadas}\n")

# ------------------------------------------------------------
# 3) SE RESPONDIDO == 'Sim', ENTÃO STATUS = 'Lida'
# ------------------------------------------------------------

print("📌 Ajustando Status para 'Lida' quando Respondido = 'Sim'...")

status_antes2 = df["Status"].copy()
df.loc[df["Respondido"] == "Sim", "Status"] = "Lida"
alteracoes_lida = (status_antes2 != df["Status"]).sum()

print(f"   ✔ Coluna Status ajustada para quem respondeu 'Sim'. Alterações feitas: {alteracoes_lida}\n")

#------------------------------------------------------------
# 4) TRATAR A COLUNA CONTATO – REMOVER TUDO APÓS O PRIMEIRO "_"
# ------------------------------------------------------------

print("✂ Limpando texto da coluna Contato...")

contato_antes = df["Contato"].astype(str).copy()

df["nome_manipulado"] = df["Contato"].astype(str).str.split("_").str[0]

alteracoes_contato = (contato_antes != df["nome_manipulado"]).sum()

print(f"   ✔ Coluna Contato tratada. Alterações feitas: {alteracoes_contato}\n")

df[["Conta", "Mensagem", "Categoria", "Template", "Template", "Protocolo", "Status agendamento", "Agente"]] = pd.NA


# ------------------------------------------------------------
# 5) SALVAR O RESULTADO
# ------------------------------------------------------------

print("💾 Salvando arquivo final tratado como status.xlsx ...")

df.to_excel("status.xlsx", index=False)

print("\n🎉 Processo concluído com sucesso!")

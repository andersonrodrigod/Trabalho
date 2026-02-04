import pandas as pd

df = pd.read_excel("status.xlsx")


# ============================================================
# 0) ATUALIZAÇÃO DE RESPOSTAS (ANTES DE QUALQUER CORREÇÃO)
#    USANDO CONTATO + DATA DE ATENDIMENTO
# ============================================================

df_resposta = pd.read_excel("status_resposta.xlsx")

# ----------------------------
# NORMALIZAÇÃO DAS CHAVES
# ----------------------------

# Contato
df["Contato"] = df["Contato"].astype(str).str.strip()
df_resposta["nom_contato"] = df_resposta["nom_contato"].astype(str).str.strip()

# Cria nova coluna só com datas sem horas
df["Data de envio"] = pd.to_datetime(df["Data agendamento"], errors="coerce", dayfirst=True).dt.date

df_resposta["dat_atendimento"] = pd.to_datetime(df_resposta["dat_atendimento"], errors="coerce", dayfirst=True).dt.date

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


df["Resposta"] =  df["resposta"].fillna("Sem Resposta")

df.drop(columns=["nom_contato", "dat_atendimento", "resposta"], inplace=True, errors="ignore")

# ------------------------------------------------------------
# 1) CORREÇÃO DE TEXTOS E CARACTERES SUBSTITUÍDOS
# ------------------------------------------------------------

df["HSM"] = df["HSM"].replace({"Pesquisa Complicaτ⌡es Cirurgicas": "Complicações cirurgicas"})

df["Status"] = df["Status"].replace({
    "A Meta decidiu nπo entregar a mensagem": "A Meta decidiu não entregar a mensagem",
    "N·mero Θ parte de um experimento": "Número é parte de um experimento",
    "Usußrio decidiu nπo receber MKT messages": "MKT messages",
    "Mensagem nπo pode ser entregue": "Mensagem não pode ser entregue"
})

df["Respondido"] = df["Respondido"].replace({
    "Nπo": "Não"
})

df["Resposta"] = df["Resposta"].replace({
    "Nπo": "Não"
})

# ------------------------------------------------------------
# 2) EXCLUSÃO DE LINHAS ESPECÍFICAS NA COLUNA HSM
# ------------------------------------------------------------

df = df[df["HSM"] != "Pesquisa_Pos_cir_urg_intern"]
df = df[df["HSM"] != "Pesquisa_Pos_cir_eletivo"]

# ------------------------------------------------------------
# 3) SE RESPONDIDO == 'Sim', ENTÃO STATUS = 'Lida'
# ------------------------------------------------------------

df.loc[df["Respondido"] == "Sim", "Status"] = "Lida"

#------------------------------------------------------------
# 4) TRATAR A COLUNA CONTATO – REMOVER TUDO APÓS O PRIMEIRO "_"
# ------------------------------------------------------------

df["nome_manipulado"] = df["Contato"].astype(str).str.split("_").str[0]

df[["Conta", "Mensagem", "Categoria", "Template", "Template", "Protocolo", "Status agendamento", "Agente"]] = pd.NA

df.to_excel("status.xlsx", index=False)

print("\n🎉 Processo concluído com sucesso!")
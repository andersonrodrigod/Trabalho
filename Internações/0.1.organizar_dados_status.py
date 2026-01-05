import pandas as pd

df = pd.read_excel("status.xlsx")

# 1) CORREÇÃO DE TEXTOS E CARACTERES SUBSTITUÍDOS

df["HSM"] = df["HSM"].replace({
    "Pesquisa Complicaτ⌡es Cirurgicas": "Complicações cirurgicas"
})

df["Data de envio"] = pd.to_datetime(df["Data agendamento"], errors="coerce").dt.date

df["Status"] = df["Status"].replace({
    "A Meta decidiu nπo entregar a mensagem": "A Meta decidiu não entregar a mensagem",
    "N·mero Θ parte de um experimento": "Número é parte de um experimento",
    "Usußrio decidiu nπo receber MKT messages": "MKT messages",
    "Mensagem nπo pode ser entregue": "Mensagem não pode ser entregue"
})

df["Respondido"] = df["Respondido"].replace({
    "Nπo": "Não"
})

df = df[df["HSM"] != ""] # colocar depois >>>>> complicações cirurgicas
#df = df[df["HSM"] != "Pesquisa_Pos_cir_eletivo"]

# 2) AJUSTE E MANIPULAÇÃO DE DADOS

df.loc[df["Respondido"] == "Sim", "Status"] = "Lida"

df["nome_manipulado"] = df["Contato"].astype(str).str.split("_").str[0]

df[["Conta", "Mensagem", "Categoria", "Template", "Template", "Protocolo", "Status agendamento", "Agente"]] = pd.NA

df.to_excel("status.xlsx", index=False)








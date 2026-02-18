import pandas as pd

df = pd.read_excel("status.xlsx")

# Garante a coluna de resposta para fluxos que nao passam pelo processo 0.0.
if "Resposta" not in df.columns:
    df["Resposta"] = pd.NA
if "RESPOSTA" not in df.columns:
    df["RESPOSTA"] = df["Resposta"]

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

df = df[df["HSM"] != "Complicações cirurgicas"]

df.loc[df["Respondido"] == "Sim", "Status"] = "Lida"

df["nome_manipulado"] = df["Contato"].astype(str).str.split("_").str[0]

df[["Conta", "Mensagem", "Categoria", "Template", "Template", "Protocolo", "Status agendamento", "Agente"]] = pd.NA

df.to_excel("status.xlsx", index=False)

print("\n🎉 Processo concluído com sucesso!")

import pandas as pd

# 1️⃣ Ler o arquivo
df = pd.read_excel("duplicados.xlsx")

# 2️⃣ Criar coluna de status
df["ULTIMO STATUS DE ENVIO"] = ""

# 3️⃣ Palavras-chave de internação
palavras_chave = [
    "INTERNACAO CLINICA",
    "INTERNACAO CIRURGICA",
    "INTERNACAO EM"
]

# 4️⃣ Identificar duplicados por TELEFONE + USUARIO
duplicados = (
    df.groupby(["TELEFONE RELATORIO", "USUARIO"])
      .size()
      .loc[lambda x: x > 1]
      .reset_index()[["TELEFONE RELATORIO", "USUARIO"]]
)

# 5️⃣ Função de decisão
def definir_status(grupo):

    proc_upper = grupo["PROCEDIMENTO"].astype(str).str.upper()

    # 🔹 REGRA DOMINANTE: CESARIANA
    tem_cesariana = proc_upper.str.contains("CESARIANA", na=False)

    if tem_cesariana.any():
        grupo.loc[tem_cesariana, "ULTIMO STATUS DE ENVIO"] = "PERMANECE UNICO"
        grupo.loc[~tem_cesariana, "ULTIMO STATUS DE ENVIO"] = "APAGAR DUPLICADO"
        return grupo

    # 🔹 Regras de internação (se não houver cesariana)
    tem_internacao = proc_upper.apply(
        lambda x: any(p in x for p in palavras_chave)
    )

    total_com_internacao = tem_internacao.sum()
    total_linhas = len(grupo)

    # 🔹 Caso: ninguém tem internação
    if total_com_internacao == 0:
        grupo["ULTIMO STATUS DE ENVIO"] = "APAGAR POR SUPERVISIONAMENTO"
        return grupo

    # 🔹 Caso: todos têm internação
    if total_com_internacao == total_linhas:
        grupo["ULTIMO STATUS DE ENVIO"] = "APAGAR DUPLICADO"
        grupo.iloc[0, grupo.columns.get_loc("ULTIMO STATUS DE ENVIO")] = "PERMANECE UNICO"
        return grupo

    # 🔹 Caso misto
    grupo.loc[tem_internacao, "ULTIMO STATUS DE ENVIO"] = "APAGAR DUPLICADO"
    grupo.loc[~tem_internacao, "ULTIMO STATUS DE ENVIO"] = "PERMANECE UNICO"

    return grupo

# 6️⃣ Aplicar apenas aos duplicados corretos
df = df.merge(
    duplicados.assign(_duplicado=True),
    on=["TELEFONE RELATORIO", "USUARIO"],
    how="left"
)

df.loc[df["_duplicado"] == True] = (
    df[df["_duplicado"] == True]
    .groupby(["TELEFONE RELATORIO", "USUARIO"], group_keys=False)
    .apply(definir_status)
)

# 7️⃣ Limpar coluna auxiliar
df.drop(columns="_duplicado", inplace=True)

# 8️⃣ Salvar resultado
df.to_excel("duplicados_tratados.xlsx", index=False)

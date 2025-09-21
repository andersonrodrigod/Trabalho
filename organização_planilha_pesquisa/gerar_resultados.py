import pandas as pd

# 1️⃣ Carregar o arquivo
df = pd.read_excel("merged_output.xlsx")

# 2️⃣ Variável filtro
responsavel_filtro = "ADRIA CANDIDO"

# 3️⃣ Filtrar apenas os dados desse responsável
df_filtro = df[df["responsavel"] == responsavel_filtro].copy()

# 4️⃣ Ajustes na coluna Atuação_Rede_Propria (6 vira 5)
df_filtro["Atuação_Rede_Propria"] = df_filtro["Atuação_Rede_Propria"].replace(6, 5)

# 5️⃣ Escala_0a10
escala = df_filtro["Escala_0a10"].dropna()
total = escala.count()

# Quantidade de cada nota 0 a 10
contagem_notas = escala.value_counts().sort_index()

# Agrupamentos: 0-6, 7-8, 9-10
agrupamentos = pd.cut(
    escala,
    bins=[-1, 6, 8, 10],
    labels=["0-6", "7-8", "9-10"]
)
contagem_agrup = agrupamentos.value_counts().sort_index()
percentual_agrup = (contagem_agrup / contagem_agrup.sum() * 100).round(2)

# NPS
total_respostas = len(escala)
promotores = (escala >= 9).sum()
detratores = (escala <= 6).sum()
nps = ((promotores - detratores) / total_respostas) * 100

# 6️⃣ Ponto_Focal
ponto = df_filtro["Ponto_Focal"].dropna()
contagem_ponto = ponto.value_counts()
percentual_ponto = (contagem_ponto / contagem_ponto.sum() * 100).round(2)

# 7️⃣ Médias das outras colunas (Ignorando nulos)
colunas_media = ["Avaliação_Relac", "Cumprimento", "Atuação_Rede_Propria", "Dificuldade"]
medias = df_filtro[colunas_media].mean().round(2)

# 8️⃣ Criar arquivo Excel detalhado
with pd.ExcelWriter(f"Resumo_{responsavel_filtro}.xlsx", engine="xlsxwriter") as writer:

    
    # Aba: Detalhes originais filtrados
    df_filtro.to_excel(writer, sheet_name="Dados Filtrados", index=False)
    
    # Aba: Contagem de notas
    df_notas = pd.DataFrame({"Nota": contagem_notas.index, "Quantidade": contagem_notas.values})
    df_notas.loc[len(df_notas)] = ["Total", df_notas["Quantidade"].sum()]

    df_notas.to_excel(writer, sheet_name="Contagem_Notas", index=False)

    
    # Aba: Agrupamentos
    df_agrup = pd.DataFrame({
        "Agrupamento": contagem_agrup.index,
        "Quantidade": contagem_agrup.values,
        "Percentual (%)": percentual_agrup.values
    })
    df_agrup.to_excel(writer, sheet_name="Agrupamentos", index=False)
    
    # Aba: NPS
    df_nps = pd.DataFrame({
        "Promotores": [promotores],
        "Detratores": [detratores],
        "Total Respostas": [total_respostas],
        "NPS (%)": [round(nps, 2)]
    })
    df_nps.to_excel(writer, sheet_name="NPS", index=False)
    
    # Aba: Ponto Focal
    df_ponto = pd.DataFrame({
        "Ponto_Focal": contagem_ponto.index,
        "Quantidade": contagem_ponto.values,
        "Percentual (%)": percentual_ponto.values
    })
    df_ponto.to_excel(writer, sheet_name="Ponto_Focal", index=False)
    
    # Aba: Médias
    df_medias = pd.DataFrame({"Coluna": medias.index, "Média": medias.values})
    df_medias.to_excel(writer, sheet_name="Medias", index=False)


print(f"Arquivo Resumo_{responsavel_filtro}.xlsx gerado com sucesso!")


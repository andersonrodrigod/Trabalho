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
# Remover valores nulos
escala = df_filtro["Escala_0a10"].dropna()
total = escala.count()

# Quantidade de cada nota 0 a 10
contagem_notas = escala.value_counts().sort_index()
print("Quantidade por nota (0-10):\n", contagem_notas, "\n")
print("Total de Notas:\n", total)

# Agrupamentos: 0-6, 7-8, 9-10
agrupamentos = pd.cut(
    escala,
    bins=[-1, 6, 8, 10],
    labels=["0-6", "7-8", "9-10"]
)
contagem_agrup = agrupamentos.value_counts().sort_index()
percentual_agrup = (contagem_agrup / contagem_agrup.sum() * 100).round(2)
print("Contagem por agrupamento:\n", contagem_agrup)
print("Percentual por agrupamento:\n", percentual_agrup, "\n")

# NPS: (Promotores 9-10) - (Detratores 0-6)
total_respostas = len(escala)

promotores = (escala >= 9).sum()
detratores = (escala <= 6).sum()

nps = ((promotores - detratores) / total_respostas) * 100

print(f"NPS: {nps:.2f}%")

# 6️⃣ Ponto_Focal
ponto = df_filtro["Ponto_Focal"].dropna()
contagem_ponto = ponto.value_counts()
percentual_ponto = (contagem_ponto / contagem_ponto.sum() * 100).round(2)
print("Ponto_Focal - Contagem:\n", contagem_ponto)
print("Ponto_Focal - Percentual:\n", percentual_ponto, "\n")

# 7️⃣ Médias das outras colunas (Ignorando nulos)
colunas_media = ["Avaliação_Relac", "Cumprimento", "Atuação_Rede_Propria", "Dificuldade"]
medias = df_filtro[colunas_media].mean().round(2)
print("Médias das colunas:\n", medias)


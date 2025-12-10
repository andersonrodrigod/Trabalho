import pandas as pd

print("📘 Lendo o arquivo nao_lidos.xlsx...")
df_nao_lidos = pd.read_excel("nao_lidos.xlsx")
print("✔ nao_lidos carregado!\n")

print("📗 Lendo o arquivo status.xlsx...")
df_status = pd.read_excel("status.xlsx")
print("✔ status carregado!\n")

print("🔎 Filtrando somente registros com Status = 'Lida'...")

# Aqui o dataframe status se limpa e diz: "Só deixo passar quem é Lida"
df_status_lida = df_status[
    df_status["Status"].astype(str).str.strip() == "Lida"
]

print("✔ Filtro aplicado! Só usuários Lida permanecem.\n")

print("🔗 Fazendo merge apenas com os Status = Lida...")

df_resultado = pd.merge(
    df_nao_lidos,
    df_status_lida,
    left_on="USUARIO",
    right_on="nome_manipulado",
    how="inner"
)

print("✔ Merge realizado apenas com Lida!\n")

print("🧹 Selecionando colunas finais...")

df_final = df_resultado[
    ["USUARIO", "CHAVE", "nome_manipulado", "Contato"]
]

print("✔ Colunas prontas!\n")

print("💾 Salvando arquivo chave_errada_nao_lidos.xlsx...")
df_final.to_excel("chave_errada_nao_lidos.xlsx", index=False)

print("✅ Tudo finalizado com sucesso!")

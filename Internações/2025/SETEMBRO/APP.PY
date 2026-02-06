import pandas as pd

# 1️⃣ Ler o arquivo Excel
df = pd.read_excel("INTERNACOES.xlsx")

# 2️⃣ Converter a coluna de data para datetime
# dayfirst=True garante que 9/1/2025 seja interpretado corretamente como 09/01/2025
df["DT_REFERENCIA_5000"] = pd.to_datetime(
    df["DT_REFERENCIA_5000"],
    dayfirst=True,
    errors="coerce"
)

# (opcional) verificar se existe data inválida
#print(df[df["DT_REFERENCIA_5000"].isna()])

# 3️⃣ Criar colunas auxiliares de mês e ano
df["MES"] = df["DT_REFERENCIA_5000"].dt.month
df["ANO"] = df["DT_REFERENCIA_5000"].dt.year

# 4️⃣ Filtrar cada mês
df_setembro = df[(df["MES"] == 9)]
df_outubro  = df[(df["MES"] == 10)]
df_novembro = df[(df["MES"] == 11)]

# 5️⃣ Remover colunas auxiliares antes de salvar
df_setembro = df_setembro.drop(columns=["MES", "ANO"])
df_outubro  = df_outubro.drop(columns=["MES", "ANO"])
df_novembro = df_novembro.drop(columns=["MES", "ANO"])

# 6️⃣ Salvar os arquivos separados
df_setembro.to_excel("INTERNACOES_SETEMBRO.xlsx", index=False)
df_outubro.to_excel("INTERNACOES_OUTUBRO.xlsx", index=False)
df_novembro.to_excel("INTERNACOES_NOVEMBRO.xlsx", index=False)

print("Arquivos gerados com sucesso!")

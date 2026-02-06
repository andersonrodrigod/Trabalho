import pandas as pd

# 1️⃣ Ler o arquivo de novembro
df = pd.read_excel("OUTUBRO_INTERNAÇOES.xlsx")

# 2️⃣ (Opcional) verificar quantidade de linhas antes
print("Linhas antes:", len(df))

# 3️⃣ Remover duplicadas mantendo o primeiro registro de cada CD_USUARIO
df_sem_duplicadas = df.drop_duplicates(
    subset="CD_USUARIO",
    keep="first"
)

# 4️⃣ (Opcional) verificar quantidade de linhas depois
print("Linhas depois:", len(df_sem_duplicadas))

# 5️⃣ Salvar o novo arquivo
df_sem_duplicadas.to_excel(
    "OUTUBRO_INTERNAÇOES_SEM_DUPLICADAS.xlsx",
    index=False
)

print("Arquivo de outubro sem duplicadas gerado com sucesso!")
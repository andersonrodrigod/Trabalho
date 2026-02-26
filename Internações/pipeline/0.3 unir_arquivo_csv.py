import pandas as pd

# =========================
# 1️⃣ Ler os arquivos
# =========================

df1 = pd.read_csv("eletivo.csv", sep=";", encoding="latin-1")
df2 = pd.read_csv("internacao.csv", sep=";", encoding="latin-1")

print("Eletivo:", df1.shape)
print("Internação:", df2.shape)

# =========================
# 2️⃣ Concatenar (empilhar)
# =========================

df_final = pd.concat([df1, df2], axis=0, ignore_index=True)

print("Final:", df_final.shape)

# =========================
# 3️⃣ Salvar resultado
# =========================

df_final.to_csv("status_resposta.csv", index=False, encoding="latin-1")

print("Arquivo salvo com sucesso!")
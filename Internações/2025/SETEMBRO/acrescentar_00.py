import pandas as pd

# 1️⃣ Leitura correta
df = pd.read_excel(
    "BASE_CONCATENADA_FINAL.xlsx",
)

# 2️⃣ Normaliza coluna
df.columns = df.columns.str.strip().str.upper()
df["COD USUARIO"] = df["COD USUARIO"].astype(str).str.strip()

# 3️⃣ CONTAGEM ANTES
antes_12 = (df["COD USUARIO"].str.len() == 12).sum()
antes_13 = (df["COD USUARIO"].str.len() == 13).sum()

print("ANTES DO AJUSTE")
print(f"Registros com 12 caracteres: {antes_12}")
print(f"Registros com 13 caracteres: {antes_13}")

# 4️⃣ APLICA AS REGRAS
df.loc[df["COD USUARIO"].str.len() == 12, "COD USUARIO"] = (
    "00" + df.loc[df["COD USUARIO"].str.len() == 12, "COD USUARIO"]
)

df.loc[df["COD USUARIO"].str.len() == 13, "COD USUARIO"] = (
    "0" + df.loc[df["COD USUARIO"].str.len() == 13, "COD USUARIO"]
)

# 5️⃣ CONTAGEM DEPOIS
depois_14 = (df["COD USUARIO"].str.len() == 14).sum()

print("\nDEPOIS DO AJUSTE")
print(f"Registros com 14 caracteres: {depois_14}")

# 6️⃣ SALVA
df.to_excel(
    "BASE_CONCATENADA_FINAL_AJUSTADA.xlsx"
)

print("\nArquivo salvo com sucesso.")

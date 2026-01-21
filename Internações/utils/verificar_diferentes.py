import pandas as pd

# Ler arquivo
df = pd.read_excel("duplicados_tratados.xlsx")

# Normalização básica
df["TELEFONE RELATORIO"] = df["TELEFONE RELATORIO"].astype(str).str.strip()
df["USUARIO"] = df["USUARIO"].astype(str).str.strip()

# Contar pares únicos (telefone + usuário)
total_chaves_antes = df[["TELEFONE RELATORIO", "USUARIO"]].drop_duplicates().shape[0]

print("===== CONTAGEM ANTES DA EXCLUSÃO =====")
print(f"Total de (TELEFONE RELATORIO + USUARIO) únicos: {total_chaves_antes}")

# Remover apenas os marcados como APAGAR DUPLICADO
df_limpo = df[df["ULTIMO STATUS DE ENVIO"] != "APAGAR DUPLICADO"].copy()

# Recontar pares únicos
total_chaves_depois = (
    df_limpo[["TELEFONE RELATORIO", "USUARIO"]]
    .drop_duplicates()
    .shape[0]
)

print("\n===== CONTAGEM APÓS EXCLUSÃO =====")
print(f"Total de (TELEFONE RELATORIO + USUARIO) únicos: {total_chaves_depois}")

# Diferença
print("\n===== IMPACTO =====")
print(f"Redução de chaves: {total_chaves_antes - total_chaves_depois}")


import pandas as pd

# Lê a aba BASE da planilha
df = pd.read_excel("Planilha Julho nova.xlsx", sheet_name="BASE", dtype=str)

# Conta quantos registros têm "sem numero" na coluna TELEFONE
sem_numero = df["TELEFONE"].str.strip().str.lower() == "sem numero"
quantidade = sem_numero.sum()

print(f"📌 Total de registros com 'sem numero' na coluna TELEFONE: {quantidade}")

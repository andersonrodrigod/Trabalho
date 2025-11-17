import pandas as pd

# Caminho do arquivo original
arquivo = "Planilha Julho 04.11.xlsx"

# Nome da aba que você quer manter
aba_principal = "BASE"

# 1️⃣ Lendo apenas a aba BASE (Pandas ignora fórmulas e lê o valor final)
df = pd.read_excel(arquivo, sheet_name=aba_principal)

# 2️⃣ Sobrescrevendo o arquivo, mantendo só a aba BASE (com valores)
with pd.ExcelWriter("dados_limpos.xlsx", engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name=aba_principal, index=False)

print("✅ Arquivo 'dados_limpos.xlsx' criado com sucesso (apenas aba BASE, sem fórmulas ou dependências).")

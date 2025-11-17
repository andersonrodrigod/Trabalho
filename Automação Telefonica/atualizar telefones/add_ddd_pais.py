import pandas as pd

arquivo = "complica_minas.xlsx"

# 1. Ler o arquivo Excel
df = pd.read_excel(arquivo)

# 2. Garantir que a coluna "Telefone 1" seja tratada como string
df["Telefone 2"] = df["Telefone 2"].astype(str)

# 3. Adicionar '55' na frente dos números que não começam com '55'
df["Telefone 2"] = df["Telefone 2"].apply(
    lambda x: "55" + x if not x.startswith("55") else x
)

# 4. Salvar o resultado em um novo arquivo
df.to_excel("complica_minas_55.xlsx", index=False)

print("✅ Arquivo salvo com sucesso: total_julho_corrigido.xlsx")

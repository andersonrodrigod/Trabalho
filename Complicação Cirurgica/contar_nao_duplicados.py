import pandas as pd

# Ler arquivo CSV ou Excel (ajuste conforme necessário)
# Para CSV:
# df = pd.read_csv('seu_arquivo.csv')
# Para Excel:
# df = pd.read_excel('seu_arquivo.xlsx', engine='openpyxl')

# Exemplo fictício:
dados = "status_limpo.xlsx"
df = pd.read_excel(dados)

# Contar valores únicos na coluna "Contato"
contagem_unicos = df['Contato'].nunique()

print(f"Quantidade de valores únicos na coluna 'Contato': {contagem_unicos}")
import pandas as pd

# Exemplo: carregando um arquivo Excel com uma aba chamada "BASE"
arquivo = "MES OUTUBRO GERAL.xlsx"
df = pd.read_excel(arquivo, sheet_name="BASE")

# Variável com o valor do filtro
valor_filtro = "CCG"

# Filtrar pela coluna 'BASE' e pegar valores únicos da coluna 'PRESTADOR'
resultado = df.loc[df['BASE'] == valor_filtro, 'PRESTADOR'].drop_duplicates()

# Exibir resultado
print("\n ".join(map(str, resultado.tolist())))

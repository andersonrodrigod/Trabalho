import pandas as pd

# Caminho do arquivo original
arquivo_entrada = "detalhamento/detalhe.xlsx"
arquivo_saida = "detalhamento/detalhe_limpo.xlsx"

# Carregar todas as abas
xls = pd.ExcelFile(arquivo_entrada, engine='openpyxl')
sheet_names = xls.sheet_names

# Função para remover duplicação do nome
def remove_duplicate_name(entry):
    parts = str(entry).split('_')
    if len(parts) > 1 and parts[0] == parts[1]:
        return '_'.join(parts[1:])
    return entry

# Dicionário para armazenar os DataFrames modificados
abas_modificadas = {}

# Processar cada aba
for sheet in sheet_names:
    df = pd.read_excel(xls, sheet_name=sheet, engine='openpyxl')

    # Verifica e aplica a função se a coluna existir
    if 'Nome' in df.columns:
        df['Nome'] = df['Nome'].apply(remove_duplicate_name)
    if 'Contato' in df.columns:
        df['Contato'] = df['Contato'].apply(remove_duplicate_name)

    # Armazena o DataFrame modificado
    abas_modificadas[sheet] = df

# Salvar todas as abas modificadas em um novo arquivo Excel
with pd.ExcelWriter(arquivo_saida, engine='openpyxl') as writer:
    for aba, df_modificado in abas_modificadas.items():
        df_modificado.to_excel(writer, sheet_name=aba, index=False)
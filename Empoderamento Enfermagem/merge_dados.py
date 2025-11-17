import pandas as pd

# Nomes dos arquivos
arquivo_match = 'final_match_3palavras.xlsx'
arquivo_base = 'base dr jovita atualizado.xlsx'

# Ler os arquivos Excel                         
match_df = pd.read_excel(arquivo_match, engine='openpyxl')
base_df = pd.read_excel(arquivo_base, engine='openpyxl')

# Verificar colunas
if 'Nome 1' not in match_df.columns or 'Nome 2' not in match_df.columns:
    raise ValueError("O arquivo final_match_3palavras deve conter as colunas 'Nome 1' e 'Nome 2'.")
if 'Nome 1' not in base_df.columns or 'Nome 2' not in base_df.columns:
    raise ValueError("O arquivo base dr jovita atualizado deve conter as colunas 'Nome 1' e 'Nome'.")

# Criar dicionário Nome 1 -> Nome 2
mapa_nome = dict(zip(match_df['Nome 1'], match_df['Nome 2']))

# Atualizar coluna 'Nome' no base_df
base_df['Nome 2'] = base_df.apply(lambda row: mapa_nome.get(row['Nome 1'], row['Nome 2']), axis=1)

# Salvar resultado
arquivo_saida = 'base_atualizado_com_nome2.xlsx'
base_df.to_excel(arquivo_saida, index=False)

print(f"Junção concluída com sucesso! Arquivo salvo como: {arquivo_saida}")

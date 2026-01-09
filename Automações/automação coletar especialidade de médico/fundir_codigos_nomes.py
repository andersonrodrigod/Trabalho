import pandas as pd

# Carregar o arquivo
df = pd.read_excel('ESPECIALISTA TOTAL.xlsx')  # Ajuste o nome do arquivo

# Criar um dicionário de mapeamento CODIGO -> ESPECIALIDADE
# Remove duplicatas, mantendo a primeira ocorrência
df_unico = df[['CODIGO', 'ESPECIALIDADE']].drop_duplicates(subset='CODIGO', keep='first')
mapeamento = df_unico.set_index('CODIGO')['ESPECIALIDADE'].to_dict()

# Para ESPECIALIDADE 2 -> ESPEC 1
df['ESPEC 1'] = df['ESPECIALIDADE 2'].map(mapeamento).fillna('NÃO ENCONTRADO')

# Para ESPECIALIDADE 3 -> ESPEC 2
df['ESPEC 2'] = df['ESPECIALIDADE 3'].map(mapeamento).fillna('NÃO ENCONTRADO')

# Salvar o resultado
df.to_excel('resultado.xlsx', index=False)

print("Processamento concluído!")
print(f"\nTotal de registros processados: {len(df)}")
print(f"ESPEC 1 encontrados: {(df['ESPEC 1'] != 'NÃO ENCONTRADO').sum()}")
print(f"ESPEC 2 encontrados: {(df['ESPEC 2'] != 'NÃO ENCONTRADO').sum()}")

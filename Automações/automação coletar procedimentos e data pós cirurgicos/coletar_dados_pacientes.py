import pandas as pd

# Ler a planilha na aba BASE
arquivo_entrada = 'NOVEMBRO GERAL.xlsx'  # Substitua pelo caminho do seu arquivo
df = pd.read_excel(arquivo_entrada, sheet_name='BASE')

# Selecionar apenas as colunas desejadas
colunas_selecionadas = ['BASE', 'COD USUARIO', 'DT AUTORIZACAO', 'DT INTERNACAO', 'COD PROCEDIMENTO', 'PROCEDIMENTO', "SENHA"]
df_filtrado = df[colunas_selecionadas]

# Formatar as colunas de data para o formato brasileiro (DD/MM/AAAA)
df_filtrado['DT AUTORIZACAO'] = pd.to_datetime(df_filtrado['DT AUTORIZACAO'], errors='coerce').dt.strftime('%d/%m/%Y')
df_filtrado['DT INTERNACAO'] = pd.to_datetime(df_filtrado['DT INTERNACAO'], errors='coerce').dt.strftime('%d/%m/%Y')

# Adicionar as colunas STATUS BOT e STATUS COLETA vazias
df_filtrado['STATUS BOT'] = ''
df_filtrado['STATUS COLETA'] = ''
df_filtrado['COD PROCEDIMENTO'] = ''
df_filtrado['PROCEDIMENTO'] = ''
df_filtrado['DATA DA REINTERNACAO'] = ''

# Reordenar as colunas para STATUS BOT ser a primeira
df_filtrado = df_filtrado[['STATUS BOT', 'BASE', 'COD USUARIO', 'DT AUTORIZACAO', 'DT INTERNACAO', 'COD PROCEDIMENTO', 'PROCEDIMENTO', 'SENHA', 'COD PROCEDIMENTO', 'PROCEDIMENTO', 'DATA DA REINTERNACAO', 'STATUS COLETA']]

# Criar a nova planilha com os dados filtrados
arquivo_saida = 'NOVEMBRO_AUTOMACAO_INTERNACAO.xlsx'
df_filtrado.to_excel(arquivo_saida, index=False)

print(f"Planilha '{arquivo_saida}' criada com sucesso!")
print(f"Total de registros: {len(df_filtrado)}")

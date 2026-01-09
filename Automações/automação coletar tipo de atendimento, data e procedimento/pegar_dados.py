import pandas as pd

# Ler a planilha na aba BASE
arquivo_entrada = 'OUTUBRO.xlsx'  # Substitua pelo caminho do seu arquivo
df = pd.read_excel(arquivo_entrada, sheet_name='BASE')

# Selecionar apenas as colunas desejadas
colunas_selecionadas = ['BASE', 'COD USUARIO', "USUARIO", "SENHA"]
df_filtrado = df[colunas_selecionadas]

df_filtrado['STATUS BOT'] = ''
df_filtrado['STATUS COLETA'] = ''
df_filtrado['COD PROCEDIMENTO'] = ''
df_filtrado['PROCEDIMENTO'] = ''
df_filtrado['DATA DA REINTERNACAO'] = ''
df_filtrado['TP ATENDIMENTO'] = ''

df_filtrado = df_filtrado[['STATUS BOT', 'BASE', 'COD USUARIO', 'USUARIO','COD PROCEDIMENTO', 'PROCEDIMENTO', 'TP ATENDIMENTO', 'SENHA','STATUS COLETA']]

arquivo_saida = 'OUTUBRO_AUTOMACAO_INTERNACAO.xlsx'
df_filtrado.to_excel(arquivo_saida, index=False)
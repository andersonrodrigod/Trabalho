import pandas as pd

arquivo = "base para automação escuta ativa 1411.xlsx"

# Ler as duas planilhas
planilha1 = pd.read_excel(arquivo, sheet_name="pre")
planilha2 = pd.read_excel(arquivo, sheet_name="pos")

# Normalizar nomes das colunas
planilha1.columns = planilha1.columns.str.strip().str.lower()
planilha2.columns = planilha2.columns.str.strip().str.lower()

# Garantir que as colunas CPF sejam strings
planilha1['cpf'] = planilha1['cpf'].astype(str).str.strip()
planilha2['cpf'] = planilha2['cpf'].astype(str).str.strip()

# Filtrar CPFs válidos na planilha1 (mais de 3 caracteres e não apenas zeros)
planilha1_validos = planilha1[planilha1['cpf'].str.len() > 3]
planilha1_validos = planilha1_validos[planilha1_validos['cpf'].str.replace('0', '').str.strip() != '']

# Criar dicionário CPF -> Nome apenas com CPFs válidos
mapa_nome = dict(zip(planilha1_validos['cpf'], planilha1_validos['nome 1']))

# Atualizar coluna na planilha2
planilha2['nome correspondente'] = planilha2['cpf'].map(mapa_nome).fillna(planilha2['nome correspondente'])

# Salvar resultado
novo_arquivo = "resultado_escuta_ativa.xlsx"
with pd.ExcelWriter(novo_arquivo, engine='openpyxl') as writer:
    planilha1.to_excel(writer, sheet_name="pre", index=False)
    planilha2.to_excel(writer, sheet_name="pos", index=False)


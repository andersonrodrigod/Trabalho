import pandas as pd

# Nome do arquivo Excel de origem
arquivo_excel = "Planilha_Julho.xlsx"

# Carregar todas as abas em um dicionário {nome_aba: DataFrame}
abas = pd.read_excel(arquivo_excel, sheet_name=None)

# Criar um CSV para cada aba
for nome_aba, df in abas.items():
    nome_csv = f"{nome_aba}.csv"
    df.to_csv(nome_csv, index=False, sep=";")  # sep=";" deixa mais compatível com Excel em PT-BR
    print(f"Aba '{nome_aba}' salva como {nome_csv}")

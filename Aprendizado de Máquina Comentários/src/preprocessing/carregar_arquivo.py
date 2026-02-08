import pandas as pd




def carregar_arquivo_excel(arquivo, aba=None):
    if aba is None:
        df = pd.read_excel(arquivo)
    else:
        df = pd.read_excel(arquivo, sheet_name=aba)
    return df
    
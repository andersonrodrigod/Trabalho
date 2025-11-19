import pandas as pd

# --- Caminho do arquivo ---
arquivo_original = "base para automação escuta ativa 1411.xlsx" 
arquivo_merge = "total consolidado.xlsx"

# --- Ler as planilhas ---
df_original = pd.read_excel(arquivo_original, sheet_name="Planilha8")
df_merge = pd.read_excel(arquivo_merge)

# --- Váriaveis referencias ---
coluna_1 = "Nome 1"
coluna_2 = "Nome 2"

# --- Função para verificar correspondência da coluna Nome 1 de ambos arquivos ---
def verificar_correspondencia(df_orginal, df_merge, coluna_1, coluna_2):
    correspondencia = []

    for nome in df_orginal[coluna_1].astype(str):
        nome_limpo = nome.strip().lower()
        valor_extraido = None

        for _, linha in df_merge.iterrows():
            base_limpa = str(linha[coluna_2]).strip().lower()
            if nome_limpo == base_limpa:
                valor_extraido = linha[coluna_1]
                break

        correspondencia.append((nome, valor_extraido))
        
    return correspondencia           
                   

correspondencia = verificar_correspondencia(df_original, df_merge, coluna_1, coluna_2)

df_resultado = pd.DataFrame(correspondencia, columns=[coluna_1, coluna_1])
df_resultado.to_excel("resultado_correspondencia.xlsx", index=False) 

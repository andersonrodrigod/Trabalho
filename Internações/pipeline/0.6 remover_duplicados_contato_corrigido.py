import pandas as pd

ARQUIVO_ENTRADA = "status_chaves_corrigidas.xlsx"
ARQUIVO_SAIDA = "status_chaves_corrigidas_sem_duplicados.xlsx"
COLUNA_CHAVE = "Contato_corrigido"

print(f"Lendo arquivo: {ARQUIVO_ENTRADA}")
df = pd.read_excel(ARQUIVO_ENTRADA)

if COLUNA_CHAVE not in df.columns:
    raise ValueError(f"Coluna '{COLUNA_CHAVE}' nao encontrada no arquivo {ARQUIVO_ENTRADA}.")

linhas_antes = len(df)

df_sem_duplicados = df.drop_duplicates(subset=[COLUNA_CHAVE], keep="first")

linhas_depois = len(df_sem_duplicados)
removidas = linhas_antes - linhas_depois

df_sem_duplicados.to_excel(ARQUIVO_SAIDA, index=False)

print(f"Linhas antes: {linhas_antes}")
print(f"Linhas depois: {linhas_depois}")
print(f"Duplicados removidos: {removidas}")
print(f"Arquivo gerado: {ARQUIVO_SAIDA}")

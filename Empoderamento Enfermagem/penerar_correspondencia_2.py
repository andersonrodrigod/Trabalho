import pandas as pd


# --- Caminho do arquivo ---
arquivo = "final_match_2palavras.xlsx"

# --- Ler a planilha ---
df = pd.read_excel(arquivo)

# --- Palavras a ignorar ---
ignorar = {"de", "da", "do", "dos"}

# --- Função para normalizar e remover palavras irrelevantes ---
def limpar_nome(nome):
    partes = nome.strip().lower().split()
    return [p for p in partes if p not in ignorar]


def ignorar_duas_primeiras_palavras(partes):
    return partes[2:] if len(partes) > 2 else [] 


com_match = []
sem_match = []

# --- Verificar correspondência linha por linha ---
for index, row in df.iterrows():
    nome_col1 = str(row["Coluna 1"])
    nome_col2 = str(row["Coluna 2"])
    
    # Limpar e ignorar as 2 primeiras palavras de cada nome
    col1_limpa = ignorar_duas_primeiras_palavras(limpar_nome(nome_col1))
    col2_limpa = ignorar_duas_primeiras_palavras(limpar_nome(nome_col2))
    
    # Verificar se há palavras em comum (independente da ordem)
    palavras_em_comum = set(col1_limpa) & set(col2_limpa)
    
    if palavras_em_comum:
        com_match.append({
            "Coluna 1": nome_col1,
            "Coluna 2": nome_col2,
            "Palavras Extras Matchadas": ", ".join(palavras_em_comum)
        })
    else:
        sem_match.append({
            "Coluna 1": nome_col1,
            "Coluna 2": nome_col2
        })

df_com_match = pd.DataFrame(com_match)
df_sem_match = pd.DataFrame(sem_match)

# --- Salvar arquivos ---
df_com_match.to_excel("match_2palavras_com_extra.xlsx", index=False)
df_sem_match.to_excel("match_2palavras_sem_extra.xlsx", index=False)

print("✅ Processamento concluído!")
print(f"📄 Com match extra: {len(df_com_match)} registros → match_2palavras_com_extra.xlsx")
print(f"📄 Sem match extra: {len(df_sem_match)} registros → match_2palavras_sem_extra.xlsx")


#print(df["Coluna 2 Limpa"])


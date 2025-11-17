import pandas as pd

# --- Caminho do arquivo ---
arquivo = "base para automação escuta ativa 1411.xlsx"  # substitua pelo seu arquivo

# --- Ler a planilha ---
df = pd.read_excel(arquivo, sheet_name="pos")

# --- Palavras a ignorar ---
ignorar = {"de", "da", "do", "dos"}

# --- Função para normalizar e remover palavras irrelevantes ---
def limpar_nome(nome):
    partes = nome.strip().lower().split()
    return [p for p in partes if p not in ignorar]

# --- Guardar correspondências ---
match_3palavras = []
match_2palavras = []
match_1palavra = []

# --- Verificar correspondência ---
for nome in df["Nome 1"].astype(str):
    nome_limpo = limpar_nome(nome)
    achou = False

    # --- Match 3 primeiras palavras ---
    if len(nome_limpo) >= 3:
        chave = " ".join(nome_limpo[:3])
        for base in df["Nome 2"].astype(str):
            base_limpa = " ".join(limpar_nome(base))
            if base_limpa.startswith(chave):
                match_3palavras.append({"Coluna 1": nome, "Coluna 2": base})
                achou = True
                break

    # --- Match 2 palavras exatas ---
    if not achou and len(nome_limpo) >= 2:
        chave = " ".join(nome_limpo[:2])
        for base in df["Nome 2"].astype(str):
            base_limpa = " ".join(limpar_nome(base))
            if base_limpa.startswith(chave):
                match_2palavras.append({"Coluna 1": nome, "Coluna 2": base})
                achou = True
                break

    # --- Match 1 palavra ---
    if not achou and len(nome_limpo) >= 1:
        chave = nome_limpo[0]
        for base in df["Nome 2"].astype(str):
            base_limpa = limpar_nome(base)
            if chave in base_limpa:
                match_1palavra.append({"Coluna 1": nome, "Coluna 2": base})
                achou = True
                break

# --- Criar DataFrames finais ---
df_3palavras = pd.DataFrame(match_3palavras)
df_2palavras = pd.DataFrame(match_2palavras)
df_1palavra = pd.DataFrame(match_1palavra)

# --- Salvar arquivos Excel finais ---
df_3palavras.to_excel("final_match_3palavras.xlsx", index=False)
df_2palavras.to_excel("final_match_2palavras.xlsx", index=False)
df_1palavra.to_excel("final_match_1palavra.xlsx", index=False)

print("✅ Processamento concluído!")
print(f"📄 Planilha 'final_match_3palavras.xlsx' criada com {len(df_3palavras)} registros.")
print(f"📄 Planilha 'final_match_2palavras.xlsx' criada com {len(df_2palavras)} registros.")
print(f"📄 Planilha 'final_match_1palavra.xlsx' criada com {len(df_1palavra)} registros.")

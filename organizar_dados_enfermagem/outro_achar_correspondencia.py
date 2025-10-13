import pandas as pd

# --- Caminho do arquivo ---
arquivo = "novo.xlsx"  # substitua pelo seu arquivo

# --- Ler a planilha ---
df = pd.read_excel(arquivo)

# --- Palavras a ignorar ---
ignorar = {"de", "da", "do", "dos"}

# --- Função para normalizar e remover palavras irrelevantes ---
def limpar_nome(nome):
    partes = nome.strip().lower().split()
    return [p for p in partes if p not in ignorar]

# --- Guardar correspondências ---
match_3palavras = []
match_2palavras = []

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
                match_3palavras.append({
                    "Nome 1": nome,
                    "Nome 2 Correspondente": base,
                    "Substring Match": chave
                })
                achou = True
                break

    # --- Match 2 palavras exatas ---
    elif len(nome_limpo) == 2:
        chave = " ".join(nome_limpo)
        for base in df["Nome 2"].astype(str):
            base_limpa = " ".join(limpar_nome(base))
            if base_limpa.startswith(chave):
                match_2palavras.append({
                    "Nome 1": nome,
                    "Nome 2 Correspondente": base,
                    "Substring Match": chave
                })
                achou = True
                break

# --- Criar DataFrames ---
df_3palavras = pd.DataFrame(match_3palavras)
df_2palavras = pd.DataFrame(match_2palavras)

# --- Salvar arquivos Excel ---
df_3palavras.to_excel("match_3palavras_limpo.xlsx", index=False)
df_2palavras.to_excel("match_2palavras_limpo.xlsx", index=False)

# --- Salvar arquivos texto ---
with open("match_3palavras_limpo.txt", "w", encoding="utf-8") as f:
    for r in match_3palavras:
        f.write(f"{r['Nome 1']} | {r['Nome 2 Correspondente']} | {r['Substring Match']}\n")

with open("match_2palavras_limpo.txt", "w", encoding="utf-8") as f:
    for r in match_2palavras:
        f.write(f"{r['Nome 1']} | {r['Nome 2 Correspondente']} | {r['Substring Match']}\n")

# --- Mensagem final ---
print("✅ Processamento concluído com remoção de 'de', 'da', 'do', 'dos'.")
print(f"📄 Match 3 palavras: {len(df_3palavras)} registros (Excel + TXT)")
print(f"📄 Match 2 palavras: {len(df_2palavras)} registros (Excel + TXT)")

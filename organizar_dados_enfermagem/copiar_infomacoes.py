import pandas as pd

# --- Arquivos ---
arquivo_base = "Base Colaboradores Enfermagem_04.08.2025 final.xlsx"
arquivo_match_3 = "final_match_3palavras.xlsx"
arquivo_match_2 = "final_match_2palavras.xlsx"
saida = "Base_Atualizada_Completa.xlsx"

# --- Ler a aba Base do arquivo principal ---
df_base = pd.read_excel(arquivo_base, sheet_name="Base", header=1)  # header=1 porque a linha 2 é o cabeçalho

# --- Ler os arquivos de correspondência ---
df_match_3 = pd.read_excel(arquivo_match_3)
df_match_2 = pd.read_excel(arquivo_match_2)

# --- Normalizar colunas para busca ---
colaborador_base = df_base["Colaborador"].astype(str).str.strip().str.lower()

# Normalizar colunas dos arquivos de correspondência
df_match_3["Coluna 2_norm"] = df_match_3["Coluna 2"].astype(str).str.strip().str.lower()
df_match_2["Coluna 2_norm"] = df_match_2["Coluna 2"].astype(str).str.strip().str.lower()

# --- Criar coluna para armazenar correspondência ---
df_base["nome_correspondente"] = ""

# --- Função para atualizar correspondência ---
def atualizar_correspondencia(df_base, colaborador_base, df_match):
    for i, colaborador in enumerate(colaborador_base):
        # só atualiza se ainda não tiver correspondência
        if df_base.loc[i, "nome_correspondente"] == "":
            cond = df_match["Coluna 2_norm"] == colaborador
            if cond.any():
                df_base.loc[i, "nome_correspondente"] = df_match.loc[cond.idxmax(), "Coluna 1"]

# --- Atualizar primeiro com match de 3 palavras ---
atualizar_correspondencia(df_base, colaborador_base, df_match_3)

# --- Atualizar depois com match de 2 palavras ---
atualizar_correspondencia(df_base, colaborador_base, df_match_2)

# --- Salvar arquivo atualizado ---
with pd.ExcelWriter(saida, engine="openpyxl") as writer:
    df_base.to_excel(writer, sheet_name="Base", index=False)

print(f"✅ Atualização completa concluída! Planilha salva como '{saida}'")

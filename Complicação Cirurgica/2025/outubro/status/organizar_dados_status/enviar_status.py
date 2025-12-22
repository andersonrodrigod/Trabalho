import pandas as pd
import numpy as np

print("📘 Lendo a planilha novos_contatos.xlsx ...")
abas = pd.read_excel("novos_contatos.xlsx", sheet_name=None)
df_novos = abas["novos_contatos"]
print("   ✔ Aba novos_contatos carregada!\n")

print("📗 Lendo a planilha status.xlsx ...")
df_status = pd.read_excel("status.xlsx")
print("   ✔ Planilha tratada carregada!\n")

# Normalizar strings
df_novos["Nome"] = df_novos["Nome"].astype(str).str.strip()
df_status["nome_manipulado"] = df_status["nome_manipulado"].astype(str).str.strip()

# ------------------------------------------------------------
# 🔥 PARTE NOVA: Processar o ULTIMO STATUS ANTES do merge
# ------------------------------------------------------------
status_colunas = {
    "Lida": "Lida",
    "Entregue": "Entregue",
    "Enviada": "Enviada",
    "A Meta decidiu não entregar a mensagem": "Nao_Entregue_Meta",
    "Mensagem não pode ser entregue": "Mensagem_Nao_Entregue",
    "Número é parte de um experimento": "Experimento",
    "MKT messages": "Opt_Out"
}

# garantir que todas as colunas existem e são numéricas
for coluna in status_colunas.values():
    if coluna not in df_novos.columns:
        df_novos[coluna] = np.nan
    

# ------------------------------------------------------------
# 🔥 NOVO: manter apenas a ÚLTIMA informação por Contato
# ------------------------------------------------------------
df_status_last = df_status.sort_values(by=df_status.columns.tolist()).groupby("Contato").last().reset_index()

print("✔ Mantida somente a ÚLTIMA linha encontrada por Contato.\n")

# Merge
print("🔍 Procurando correspondências entre Nome e nome_manipulado...")
df_merge = df_novos.merge(
    df_status_last[["nome_manipulado", "Status", "Telefone"]],
    left_on="Nome",
    right_on="nome_manipulado",
    how="left"
)

# Criar coluna final
df_merge["ULTIMO STATUS DE ENVIO"] = df_merge["Status"]
df_merge["Telefone Enviado"] = df_merge["Telefone"]
df_merge["Chave Status"] = df_merge["Contato"]


total_encontrados = df_merge["ULTIMO STATUS DE ENVIO"].notna().sum()

print(f"✔ Total de nomes encontrados no status.xlsx: {total_encontrados}\n")

# Somar status apenas para quem realmente teve atualização nova
for status, coluna in status_colunas.items():
    
    # condição: só atualizar LINHAS que receberam status novo no merge
    cond = (df_merge["ULTIMO STATUS DE ENVIO"] == status) & (df_merge["Status"].notna())

    # se a coluna estava vazia, vira 0
    df_merge.loc[cond & df_merge[coluna].isna(), coluna] = 0

    # se já existia valor antes, soma +1
    df_merge.loc[cond & df_merge[coluna].notna(), coluna] += 1


# Remover temporários
df_merge = df_merge.drop(columns=["nome_manipulado", "Status", "Telefone"], errors="ignore")



# ------------------------------------------------------------
# 🔥 SUBSTITUIR A ABA MODIFICADA E SALVAR TODAS AS ABAS
# ------------------------------------------------------------

abas["novos_contatos"] = df_merge

print("💾 Salvando novos_contatos_atualizado.xlsx com TODAS as abas ...")
with pd.ExcelWriter("novos_contatos_atualizados.xlsx", engine='openpyxl') as writer:
    for nome_aba, df in abas.items():
        df.to_excel(writer, sheet_name=nome_aba, index=False)

print("🎉 Arquivo final criado com sucesso!")
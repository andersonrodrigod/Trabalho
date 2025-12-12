import pandas as pd
import numpy as np
from funcao_trazer_para_usuarios import retornar_registros_para_usuarios

print("📘 Lendo a planilha novos_contatos.xlsx ...")
abas = pd.read_excel("novos_contatos.xlsx", sheet_name=None)
abas = retornar_registros_para_usuarios(abas)
df_novos = abas["usuarios"]
print("   ✔ Aba usuarios carregada!\n")

print("📗 Lendo a planilha status.xlsx ...")
df_status = pd.read_excel("status.xlsx")
print("   ✔ Planilha tratada carregada!\n")

# Normalizar strings
df_novos["USUARIO"] = df_novos["USUARIO"].astype(str).str.strip()
df_status["nome_manipulado"] = df_status["nome_manipulado"].astype(str).str.strip()

# ------------------------------------------------------------
# 🔥 PARTE NOVA: Processar o ULTIMO STATUS ANTES do merge
# ------------------------------------------------------------
status_colunas = {
    "Lida": "LIDA",
    "Entregue": "ENTREGUE",
    "Enviada": "ENVIADA",
    "A Meta decidiu não entregar a mensagem": "NAO_ENTREGUE_META",
    "Mensagem não pode ser entregue": "MENSAGEM_NAO_ENTREGUE",
    "Número é parte de um experimento": "EXPERIMENTO",
    "MKT messages": "OPT_OUT"
}

# garantir que todas as colunas existem e são numéricas
for coluna in status_colunas.values():
    if coluna not in df_novos.columns:
        df_novos[coluna] = np.nan

# garantir também as colunas QT para cada status
for coluna in status_colunas.values():
    qt_col = "QT " + coluna
    if qt_col not in df_novos.columns:
        df_novos[qt_col] = np.nan

# ------------------------------------------------------------
# 🔥 NOVO: manter apenas a ÚLTIMA informação por Contato
# ------------------------------------------------------------
df_status_last = df_status.sort_values(by=df_status.columns.tolist()).groupby("Contato").last().reset_index()

print("✔ Mantida somente a ÚLTIMA linha encontrada por Contato.\n")

# Merge
print("🔍 Procurando correspondências entre Nome e nome_manipulado...")
df_merge = df_novos.merge(
    df_status_last[["nome_manipulado", "Status", "Telefone", "Contato"]],
    left_on="USUARIO",
    right_on="nome_manipulado",
    how="left"
)

# Criar coluna final
df_merge["ULTIMO STATUS DE ENVIO"] = df_merge["Status"]
df_merge["TELEFONE ENVIADO"] = df_merge["Telefone"]
df_merge["CHAVE STATUS"] = df_merge["Contato"]

total_encontrados = df_merge["ULTIMO STATUS DE ENVIO"].notna().sum()
print(f"✔ Total de nomes encontrados no status_f_tratado: {total_encontrados}\n")

# Somar status apenas para quem realmente teve atualização nova
for status, coluna in status_colunas.items():
    
    # condição: só atualizar LINHAS que receberam status novo no merge
    cond = (df_merge["ULTIMO STATUS DE ENVIO"] == status) & (df_merge["Status"].notna())

    # se a coluna estava vazia, vira 0
    df_merge.loc[cond & df_merge[coluna].isna(), coluna] = 0

    # se já existia valor antes, soma +1
    df_merge.loc[cond & df_merge[coluna].notna(), coluna] += 1

    # Preparar QT coluna (se estiver vazia, vira 0)
    qt_col = "QT " + coluna
    df_merge.loc[cond & df_merge[qt_col].isna(), qt_col] = 0

    # Soma na QT coluna
    df_merge.loc[cond, qt_col] += 1

# ------------------------------------------------------------
# 🔍 VERIFICAÇÕES FINAIS: CHAVE E TELEFONE
# ------------------------------------------------------------

# 1) Verificação da CHAVE
df_merge["STATUS CHAVE"] = np.where(
    df_merge["CHAVE STATUS"] == df_merge["CHAVE RELATORIO"],
    "OK",
    "ERRO"
)

# 2) Verificação dos telefones
telefones_lista = ["TELEFONE RELATORIO", "TELEFONE 1", "TELEFONE 2", "TELEFONE 3", "TELEFONE 4", "TELEFONE 5"]

df_merge["STATUS TELEFONE"] = df_merge.apply(
    lambda row: "OK" if row["TELEFONE ENVIADO"] in [row[col] for col in telefones_lista] else "ERRO",
    axis=1
)

# Remover temporários
df_merge = df_merge.drop(columns=["nome_manipulado", "Status", "Contato", "Telefone"], errors="ignore")


# ------------------------------------------------------------
# 🔥 SUBSTITUIR A ABA MODIFICADA E SALVAR TODAS AS ABAS
# ------------------------------------------------------------

abas["usuarios"] = df_merge

print("💾 Salvando novos_contatos_atualizado.xlsx com TODAS as abas ...")
with pd.ExcelWriter("novos_contatos_atualizados.xlsx", engine='openpyxl') as writer:
    for nome_aba, df in abas.items():
        df.to_excel(writer, sheet_name=nome_aba, index=False)

print("🎉 Arquivo final criado com sucesso!")

import pandas as pd
import numpy as np

print("📘 Lendo a planilha novos_contatos.xlsx ...")
abas = pd.read_excel("novos_contatos.xlsx", sheet_name=None)
df_novos = abas["usuarios"]
print("   ✔ Aba usuarios carregada!\n")

print("📗 Lendo a planilha status.xlsx ...")
df_status = pd.read_excel("status.xlsx")
print("   ✔ Planilha status carregada!\n")

# Normalizar strings
df_novos["USUARIO"] = df_novos["USUARIO"].astype(str).str.strip()
df_status["nome_manipulado"] = df_status["nome_manipulado"].astype(str).str.strip()
df_status["Status"] = df_status["Status"].astype(str).str.strip()

# ------------------------------------------------------------
# 🔥 STATUS → COLUNAS DO RELATÓRIO
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

# Criar colunas vazias no df_novos caso não existam
for nova_coluna in status_colunas.values():
    if nova_coluna not in df_novos.columns:
        df_novos[nova_coluna] = 0


# ------------------------------------------------------------
# 🔥 PARTE NOVA — CONTAR TODOS OS STATUS
# ------------------------------------------------------------
print("🔢 Contando todos os status por Contato...")

# Contagem completa por Contato
contagem = (
    df_status.groupby(["Contato", "Status"])
    .size()
    .reset_index(name="qtd")
)

# Pivot: cada status vira uma coluna
tabela_status = contagem.pivot_table(
    index="Contato",
    columns="Status",
    values="qtd",
    fill_value=0
)

# Renomear colunas conforme dicionário
tabela_status = tabela_status.rename(columns=status_colunas)

# Garantir que todas as colunas existam
for col in status_colunas.values():
    if col not in tabela_status.columns:
        tabela_status[col] = 0

tabela_status = tabela_status.reset_index()

print("✔ Contagem acumulada concluída!\n")


# ------------------------------------------------------------
# 🔥 ENCONTRAR O ÚLTIMO STATUS REAL
# ------------------------------------------------------------
print("⏳ Descobrindo o último status real por contato...")

df_status_sorted = df_status.sort_values(by=["Contato", "Data do envio"], ascending=True)

ultimo_status = df_status_sorted.groupby("Contato").last().reset_index()

ultimo_status = ultimo_status[["Contato", "Status", "Telefone"]]
ultimo_status = ultimo_status.rename(columns={
    "Status": "ULTIMO STATUS DE ENVIO",
    "Telefone": "TELEFONE ENVIADO"
})

print("✔ Último status obtido!\n")


# ------------------------------------------------------------
# 🔥 MERGE FINAL — UNIR CONTAGENS + ÚLTIMO STATUS
# ------------------------------------------------------------
print("🔍 Realizando o merge final com df_novos...")

df_merge = df_novos.merge(
    tabela_status,
    left_on="CHAVE RELATORIO",
    right_on="Contato",
    how="left"
)

df_merge = df_merge.merge(
    ultimo_status,
    left_on="CHAVE RELATORIO",
    right_on="Contato",
    how="left",
    suffixes=("", "_ULT")
)

# Remover a coluna Contato duplicada
df_merge = df_merge.drop(columns=["Contato", "Contato_ULT"], errors="ignore")


# ------------------------------------------------------------
# 🔎 CHAVE STATUS & STATUS TELEFONE
# ------------------------------------------------------------

df_merge["CHAVE STATUS"] = df_merge["CHAVE RELATORIO"]

df_merge["STATUS CHAVE"] = np.where(
    df_merge["CHAVE STATUS"] == df_merge["CHAVE RELATORIO"],
    "OK",
    "ERRO"
)

lista_telefones = ["TELEFONE RELATORIO", "TELEFONE 1", "TELEFONE 2", "TELEFONE 3", "TELEFONE 4", "TELEFONE 5"]

df_merge["STATUS TELEFONE"] = df_merge.apply(
    lambda row: "OK" if row["TELEFONE ENVIADO"] in [row[col] for col in lista_telefones] else "ERRO",
    axis=1
)

print("✔ Validações concluídas!\n")


# ------------------------------------------------------------
# 🔥 SALVAR ARQUIVO FINAL
# ------------------------------------------------------------

abas["usuarios"] = df_merge

print("💾 Salvando novos_contatos_atualizados.xlsx ...")

with pd.ExcelWriter("novos_contatos_atualizados.xlsx", engine='openpyxl') as writer:
    for nome_aba, df in abas.items():
        df.to_excel(writer, sheet_name=nome_aba, index=False)

print("🎉 Arquivo final criado com sucesso!")

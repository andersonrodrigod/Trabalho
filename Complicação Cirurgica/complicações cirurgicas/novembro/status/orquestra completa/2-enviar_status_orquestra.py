import pandas as pd
import numpy as np
from controle_usuarios import retornar_registros_para_usuarios

# ==========================================================
# 1) LEITURA DOS ARQUIVOS
# ==========================================================
print("📘 Lendo a planilha novos_contatos.xlsx ...")
abas = pd.read_excel("novos_contatos.xlsx", sheet_name=None)
abas = retornar_registros_para_usuarios(abas)
df_novos = abas["usuarios"].copy()
print(f"   ✔ Aba usuarios carregada: {len(df_novos)} registros\n")

print("📗 Lendo a planilha status.xlsx ...")
df_status = pd.read_excel("status.xlsx")
print(f"   ✔ Planilha status carregada: {len(df_status)} registros\n")

# ==========================================================
# 2) NORMALIZAÇÃO
# ==========================================================
df_novos["USUARIO"] = df_novos["USUARIO"].astype(str).str.strip()
df_status["nome_manipulado"] = df_status["nome_manipulado"].astype(str).str.strip()

# ==========================================================
# 3) MAPEAMENTO DE STATUS
# ==========================================================
status_colunas = {
    "Lida": "LIDA",
    "Entregue": "ENTREGUE",
    "Enviada": "ENVIADA",
    "A Meta decidiu não entregar a mensagem": "NAO_ENTREGUE_META",
    "Mensagem não pode ser entregue": "MENSAGEM_NAO_ENTREGUE",
    "Número é parte de um experimento": "EXPERIMENTO",
    "MKT messages": "OPT_OUT"
}

# garantir colunas numéricas
for col in status_colunas.values():
    df_novos[col] = 0
    df_novos["QT " + col] = 0

# ==========================================================
# 4) HISTÓRICO COMPLETO (CONTAGEM REAL)
# ==========================================================
print("📊 Criando histórico expandido...")

df_hist = df_novos[["USUARIO"]].merge(
    df_status[["nome_manipulado", "Status"]],
    left_on="USUARIO",
    right_on="nome_manipulado",
    how="left"
)

print("🔍 Exemplo do histórico expandido:")
print(df_hist.head(10))
print("Total linhas histórico:", len(df_hist), "\n")

# ----------------------------------------------------------
# CONTAR STATUS POR USUARIO
# ----------------------------------------------------------
print("🧮 Contando status por usuário...")

df_hist["CONTADOR"] = 1

df_contagem = (
    df_hist
    .pivot_table(
        index="USUARIO",
        columns="Status",
        values="CONTADOR",
        aggfunc="sum",
        fill_value=0
    )
    .reset_index()
)

print("📊 Exemplo da contagem por usuário:")
print(df_contagem.head(), "\n")

# ----------------------------------------------------------
# APLICAR CONTAGEM NO DF PRINCIPAL
# ----------------------------------------------------------
print("🔁 Aplicando contagens no dataframe principal...")

for status, coluna in status_colunas.items():
    if status in df_contagem.columns:
        df_novos[coluna] = (
            df_novos["USUARIO"]
            .map(df_contagem.set_index("USUARIO")[status])
            .fillna(0)
            .astype(int)
        )
        df_novos["QT " + coluna] = df_novos[coluna]

print("📊 Verificação após aplicar contagens:")
print(df_novos[list(status_colunas.values())].head(), "\n")

# ==========================================================
# 5) ÚLTIMO STATUS (APENAS 3 CAMPOS)
# ==========================================================
print("🕒 Processando último status por contato...")

df_status_last = (
    df_status
    .sort_values("Data do envio")   # CONFIRME O NOME DA COLUNA
    .groupby("Contato", as_index=False)
    .last()
)

df_last = df_novos.merge(
    df_status_last[["nome_manipulado", "Status", "Telefone", "Contato", "Respondido"]],
    left_on="USUARIO",
    right_on="nome_manipulado",
    how="left"
)

df_novos["ULTIMO STATUS DE ENVIO"] = df_last["Status"]
df_novos["TELEFONE ENVIADO"] = df_last["Telefone"]
df_novos["CHAVE STATUS"] = df_last["Contato"]
df_novos["RESPONDIDO"] = df_last["Respondido"]

print("📌 Exemplo de último status aplicado:")
print(
    df_novos[
        ["USUARIO", "ULTIMO STATUS DE ENVIO", "TELEFONE ENVIADO", "CHAVE STATUS"]
    ].head(),
    "\n"
)

# ==========================================================
# 6) VERIFICAÇÕES
# ==========================================================
df_novos["STATUS CHAVE"] = np.where(
    df_novos["CHAVE STATUS"] == df_novos["CHAVE RELATORIO"],
    "OK",
    "ERRO"
)

telefones = [
    "TELEFONE RELATORIO", "TELEFONE 1", "TELEFONE 2",
    "TELEFONE 3", "TELEFONE 4", "TELEFONE 5"
]

df_novos["STATUS TELEFONE"] = df_novos.apply(
    lambda row: "OK" if row["TELEFONE ENVIADO"] in [row[t] for t in telefones] else "ERRO",
    axis=1
)

# ==========================================================
# 6.1) LIMPAR ZEROS (APRESENTAÇÃO)
# ==========================================================
print("🧹 Convertendo zeros em NaN para colunas de contagem...")

colunas_contagem = []
for col in status_colunas.values():
    colunas_contagem.append(col)
    colunas_contagem.append("QT " + col)

df_novos[colunas_contagem] = (
    df_novos[colunas_contagem]
    .replace(0, np.nan)
)

print("✔ Zeros convertidos para NaN.")


# ==========================================================
# 7) LIMPEZA
# ==========================================================
df_novos = df_novos.drop(
    columns=["nome_manipulado", "Status", "Contato", "Telefone", "Respondido"],
    errors="ignore"
)

# ==========================================================
# 8) SALVAR ARQUIVO FINAL
# ==========================================================
abas["usuarios"] = df_novos

print("💾 Salvando novos_contatos_atualizados.xlsx ...")
with pd.ExcelWriter("novos_contatos_atualizados.xlsx", engine="openpyxl") as writer:
    for nome_aba, df_aba in abas.items():
        df_aba.to_excel(writer, sheet_name=nome_aba, index=False)

print("🎉 Arquivo final criado com sucesso!")

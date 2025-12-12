import pandas as pd

print("📘 Lendo o arquivo MES OUTUBRO GERAL.xlsx...")
df = pd.read_excel("MES OUTUBRO GERAL.xlsx", sheet_name="status")

print("🔎 Filtrando apenas registros com Status = Lida...")
df = df[df["Status"].astype(str).str.strip() == "Lida"]

print("📝 Selecionando a coluna Contato...")
df_nomes = df[["Contato"]].copy()

print("✂️ Manipulando os nomes (pegando só o conteúdo antes do primeiro '_')...")

df_nomes["nome_manipulado"] = (
    df_nomes["Contato"]
    .fillna("")
    .astype(str)
    .str.split("_")
    .str[0]
    .str.strip()
)

print("💾 Salvando nova planilha...")
df_nomes.to_excel("Nomes_tratados_status.xlsx", index=False)

print("🎉 Concluído! Arquivo gerado: Nomes_tratados_status.xlsx")

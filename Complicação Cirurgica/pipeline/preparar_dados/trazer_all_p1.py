import pandas as pd

print("📘 Lendo o arquivo MES OUTUBRO GERAL.xlsx...")
df = pd.read_excel("MES OUTUBRO GERAL.xlsx", sheet_name="comen p4")

print("📝 Selecionando a coluna Nome...")
df_nomes = df[["Nome"]].copy()

print("✂️ Manipulando os nomes (pegando só o conteúdo antes do primeiro '_')...")

# Trata valores vazios e converte tudo pra string para evitar erro
df_nomes["nome_manipulado"] = (
    df_nomes["Nome"]
    .fillna("")
    .astype(str)
    .str.split("_")
    .str[0]
    .str.strip()
)

print("💾 Salvando nova planilha com Nome e nome_manipulado...")
df_nomes.to_excel("Nomes_tratados_comen_p4.xlsx", index=False)

print("🎉 Concluído! Arquivo gerado: Nomes_tratados_comen_p4.xlsx")
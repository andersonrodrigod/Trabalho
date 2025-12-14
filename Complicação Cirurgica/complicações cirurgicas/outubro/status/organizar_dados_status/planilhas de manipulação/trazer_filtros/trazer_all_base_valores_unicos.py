import pandas as pd

print("📘 Lendo o arquivo MES OUTUBRO GERAL.xlsx...")
df = pd.read_excel("MES OUTUBRO GERAL.xlsx", sheet_name="BASE")

print("🔎 Pegando valores únicos da coluna USUARIO...")

# Remove vazios e pega somente valores únicos
usuarios_unicos = (
    df["USUARIO"]
    .dropna()
    .astype(str)
    .str.strip()
    .unique()
)

# Converte para DataFrame
df_unicos = pd.DataFrame(usuarios_unicos, columns=["USUARIO"])

print(f"✅ Total de usuários únicos encontrados: {len(df_unicos)}")

print("💾 Salvando planilha com usuários únicos...")
df_unicos.to_excel("usuarios_unicos_BASE.xlsx", index=False)

print("🎉 Concluído! Arquivo gerado: usuarios_unicos_BASE.xlsx")

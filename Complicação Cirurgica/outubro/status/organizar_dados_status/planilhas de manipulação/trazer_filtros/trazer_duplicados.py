import pandas as pd

print("📘 Lendo o arquivo MES OUTUBRO GERAL.xlsx...")
df = pd.read_excel("MES OUTUBRO GERAL.xlsx", sheet_name="BASE")

print("🔎 Buscando valores duplicados da coluna USUARIO...")

# Limpa os dados
col = (
    df["USUARIO"]
    .dropna()
    .astype(str)
    .str.strip()
)

# Marca todos que aparecem mais de uma vez
duplicados = col[col.duplicated(keep=False)]

# Converte para DataFrame
df_duplicados = pd.DataFrame(duplicados, columns=["USUARIO"])

print(f"✅ Total de registros duplicados encontrados: {len(df_duplicados)}")

print("💾 Salvando planilha com duplicados...")
df_duplicados.to_excel("usuarios_duplicados_BASE.xlsx", index=False)

print("🎉 Concluído! Arquivo gerado: usuarios_duplicados_BASE.xlsx")

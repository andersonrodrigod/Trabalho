import pandas as pd

print("📄 Carregando as planilhas...")

# Carrega os arquivos
df_disparo = pd.read_excel("complica_outubro_sp_55.xlsx")
df_geral = pd.read_excel("MES OUTUBRO GERAL.xlsx")

print("🔄 Convertendo CODIGO para string...")
df_disparo["Codigo"] = df_disparo["Codigo"].astype(str).str.strip()
df_geral["COD USUARIO"] = df_geral["COD USUARIO"].astype(str).str.strip()

print("🔗 Procurando DT INTERNACAO da planilha geral usando o Código...")

# Merge usando o CÓDIGO como chave
df_merge = df_disparo.merge(
    df_geral[["COD USUARIO", "DT INTERNACAO"]],
    left_on="Codigo",
    right_on="COD USUARIO",
    how="left"
)

print("📝 Criando coluna DT INTERNACAO final...")

# Se não achar data, coloca 'NÃO ENCONTRADO'
df_merge["DT INTERNACAO"] = df_merge["DT INTERNACAO"].fillna("NÃO ENCONTRADO")

# Remove coluna COD USUARIO duplicada
df_merge = df_merge.drop(columns=["COD USUARIO"])

# Salvar resultado final
df_merge.to_excel("complica_outubro_sp_55_atualizado.xlsx", index=False)

print("💾 Arquivo salvo como 'complica_outubro_sp_55_atualizado.xlsx'!")
print("✔ Processo concluído!")

import pandas as pd

print("📘 Lendo o arquivo principal: codigos_verificar.xlsx ...")
df_verificar = pd.read_excel("codigos_verificar.xlsx")

print("📗 Lendo o arquivo de parâmetros: codigos_parametros.xlsx ...")
df_parametros = pd.read_excel("codigos_parametros.xlsx")

# Garantir que as colunas existem
# (se o nome tiver diferente, ajuste aqui)
# print(df_verificar.columns)
# print(df_parametros.columns)

print("🧼 Padronizando os códigos como texto (evita problema de tipo)...")
df_verificar["codigo"] = df_verificar["codigo"].astype(str).str.strip()
df_parametros["codigo"] = df_parametros["codigo"].astype(str).str.strip()

print("🔍 Criando dicionário codigo → especialista...")
dic_especialistas = dict(zip(df_parametros["codigo"], df_parametros["especialista"]))

print("🧠 Buscando especialista para cada código do arquivo principal...")
df_verificar["especialista"] = df_verificar["codigo"].map(dic_especialistas)

print("✏️ Preenchendo os códigos não encontrados...")
df_verificar["especialista"] = df_verificar["especialista"].fillna("Não encontrado")

print("📦 Montando resultado final (codigo, procedimento, especialista)...")
df_resultado = df_verificar[["codigo", "procedimento", "especialista"]]

print("💾 Salvando em resultado_codigos_especialistas.xlsx ...")
df_resultado.to_excel("resultado_codigos_especialistas.xlsx", index=False)

print("✅ Pronto! Arquivo gerado: resultado_codigos_especialistas.xlsx")

import pandas as pd

print("📘 Lendo arquivo trazer_chave.xlsx...")
df_trazer = pd.read_excel("trazer_chave.xlsx")

print("📗 Lendo arquivo MES OUTUBRO GERAL.xlsx (aba BASE)...")
df_geral = pd.read_excel("MES OUTUBRO GERAL.xlsx", sheet_name="BASE")

print("\n🔍 Iniciando a busca das CHAVES correspondente aos Nomes...")

# Vamos criar um dicionário: USUARIO → CHAVE
print("🔧 Criando mapa de USUARIO -> CHAVE...")
mapa_chave = df_geral.set_index("USUARIO")["CHAVE"].to_dict()

# Agora, aplicar para cada linha do arquivo trazer_chave
print("📝 Procurando chave correspondente para cada 'Nome 1'...")
df_trazer["chave"] = df_trazer["Nome 1"].map(mapa_chave)

print("\n✅ Processo finalizado!")
print("➡️ Nova coluna 'TELEFONE' criada com sucesso.")

# Salvar resultado
df_trazer.to_excel("trazer_chave_RESULTADO.xlsx", index=False)
print("💾 Arquivo salvo como 'trazer_chave_RESULTADO.xlsx'")

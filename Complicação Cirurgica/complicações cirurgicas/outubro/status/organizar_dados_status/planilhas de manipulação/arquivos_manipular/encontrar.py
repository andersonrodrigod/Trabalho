import pandas as pd

print("📘 Lendo os arquivos...")

df_nomes = pd.read_excel("Nomes_tratados_p1.xlsx")
df_resultado = pd.read_excel("Resultado_nome_chave.xlsx")

print("🧹 Limpando os dados usados na busca...")

# Normalizando textos para comparação
df_nomes["busca"] = df_nomes["nome_manipulado"].astype(str).str.strip()
df_resultado["busca"] = df_resultado["nome_manipulado"].astype(str).str.strip()

print("🔗 Criando mapeamento nome → CHAVE...")

# Cria um dicionário: nome_manipulado -> CHAVE
mapa_chave = pd.Series(
    df_resultado["CHAVE"].values,
    index=df_resultado["busca"]
).to_dict()

print("⚙️ Gerando a nova coluna CHAVE_CERTA...")

def definir_chave(linha):
    nome = linha["busca"]
    if nome in mapa_chave:
        return mapa_chave[nome]
    else:
        return linha["Nome"]

df_nomes["CHAVE_CERTA"] = df_nomes.apply(definir_chave, axis=1)

print("💾 Salvando novo arquivo...")

df_nomes.to_excel("Nomes_tratados_com_CHAVE_CERTA.xlsx", index=False)

print("🎉 Concluído! Arquivo gerado: Nomes_tratados_com_CHAVE_CERTA.xlsx")

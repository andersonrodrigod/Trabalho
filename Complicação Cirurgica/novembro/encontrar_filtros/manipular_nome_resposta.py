import pandas as pd

print("📘 Lendo o arquivo resposta_tratada.xlsx (todas as abas)...")
abas = pd.read_excel("resposta_tratada.xlsx", sheet_name=None)

print("📗 Lendo o arquivo nao_lidos.xlsx ...")
df_nao_lidos = pd.read_excel("nao_lidos.xlsx")

print("🧠 Limpando a coluna CHAVE...")
lista_chaves = (
    df_nao_lidos["CHAVE"]
    .astype(str)
    .str.strip()
)

novas_abas = {}

# Variáveis pra controle dos não encontrados
nomes_p1_filtrados = pd.Series(dtype=str)

for nome_aba, df in abas.items():
    print(f"\n🔄 Processando a aba: {nome_aba}")

    if "Nome" in df.columns:
        print("   ✔ Coluna 'Nome' encontrada")

        # Limpando a coluna Nome
        df["Nome_limpo"] = (
            df["Nome"]
            .astype(str)
            .str.strip()
        )

        antes = len(df)

        # Mantendo só quem existe em CHAVE
        df_filtrado = df[df["Nome_limpo"].isin(lista_chaves)].copy()

        depois = len(df_filtrado)

        print(f"   📊 Linhas antes: {antes}")
        print(f"   ✅ Linhas depois: {depois}")
        print(f"   ❌ Removidas: {antes - depois}")

        # Se for a aba p1, guardar os nomes filtrados
        if nome_aba.lower() == "p1":
            nomes_p1_filtrados = df_filtrado["Nome"].astype(str).str.strip()

        # Removendo coluna auxiliar
        df_filtrado.drop(columns=["Nome_limpo"], inplace=True)

        novas_abas[nome_aba] = df_filtrado
    else:
        print("   ⚠️ Coluna 'Nome' não existe nesta aba")
        novas_abas[nome_aba] = df


print("\n💾 Salvando arquivo como status_filtrado.xlsx ...")

with pd.ExcelWriter("status_filtrado.xlsx") as writer:
    for nome_aba, df in novas_abas.items():
        df.to_excel(writer, sheet_name=nome_aba, index=False)

# 👇 NOVA PARTE – agora o print dos que NÃO foram encontrados na p1
print("\n🔎 Verificando quem do nao_lidos NÃO foi encontrado na aba p1...")

nao_encontrados = lista_chaves[~lista_chaves.isin(nomes_p1_filtrados)]

print("\n🚨 NÃO ENCONTRADOS:")
for valor in nao_encontrados:
    print(f"   👉 {valor}")

print("\n📊 TOTAL NÃO ENCONTRADOS:", len(nao_encontrados))

print("\n✅ Processo finalizado com sucesso!")

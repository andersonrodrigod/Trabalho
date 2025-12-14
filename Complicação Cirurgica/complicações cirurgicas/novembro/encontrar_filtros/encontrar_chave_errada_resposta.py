import pandas as pd

print("📘 Lendo resposta_tratada.xlsx (todas as abas)...")
abas = pd.read_excel("resposta_tratada.xlsx", sheet_name=None)

print("📗 Lendo nao_lidos.xlsx ...")
df_nao_lidos = pd.read_excel("nao_lidos.xlsx")

# Limpando a coluna USUARIO
print("🧼 Limpando a coluna USUARIO...")
lista_usuarios = (
    df_nao_lidos["USUARIO"]
    .astype(str)
    .str.strip()
)

novas_abas = {}

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

        # Mantendo só quem existe em nao_lidos
        antes = len(df)
        df_filtrado = df[df["Nome_limpo"].isin(lista_usuarios)].copy()
        depois = len(df_filtrado)

        print(f"   🧹 Linhas antes: {antes}")
        print(f"   ✅ Linhas depois: {depois}")
        print(f"   ❌ Removidas: {antes - depois}")

        # Remover coluna auxiliar
        df_filtrado.drop(columns=["Nome_limpo"], inplace=True)

        novas_abas[nome_aba] = df_filtrado
    else:
        print("   ⚠️ Coluna 'Nome' NÃO encontrada — aba mantida sem alterações")
        novas_abas[nome_aba] = df


print("\n💾 Salvando o novo arquivo como resposta_filtrada.xlsx ...")

with pd.ExcelWriter("resposta_filtrada.xlsx") as writer:
    for nome_aba, df in novas_abas.items():
        df.to_excel(writer, sheet_name=nome_aba, index=False)

print("\n✅ Processo finalizado com sucesso!")

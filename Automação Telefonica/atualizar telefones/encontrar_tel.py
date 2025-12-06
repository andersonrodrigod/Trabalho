import pandas as pd

print("📘 Lendo ref.xlsx...")
df_ref = pd.read_excel("ref.xlsx")

print("📗 Lendo TOTAL_55.xlsx...")
df_total = pd.read_excel("TOTAL_55.xlsx")

print("🔍 Construindo mapa {Codigo: Telefone 2}...")
mapa_telefone = dict(zip(df_total["Codigo"], df_total["Telefone 2"]))

print("🔄 Atualizando coluna 'Telefone' em df_ref quando o código existir em TOTAL_55...")
for i, codigo in enumerate(df_ref["Codigo"]):
    print(f"→ Linha {i} — Código: {codigo} — Valor atual Telefone: {df_ref.at[i,'Telefone']}")
    if codigo in mapa_telefone:
        novo_tel = mapa_telefone[codigo]
        df_ref.at[i, "Telefone"] = novo_tel
        print(f"   ✔ Substituído por Telefone 2: {novo_tel}")
    else:
        print("   ✖ Código não encontrado em TOTAL_55 — mantém o valor atual.")

print("💾 Salvando resultado em ref_atualizado.xlsx...")
df_ref.to_excel("ref_atualizado.xlsx", index=False)

print("✅ Pronto — arquivo salvo como ref_atualizado.xlsx")

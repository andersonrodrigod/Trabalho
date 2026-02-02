import pandas as pd

# Ler o arquivo
df = pd.read_excel("duplicados_tratados.xlsx")

# Garantir texto limpo
df["USUARIO"] = df["USUARIO"].astype(str).str.strip()
df["TELEFONE RELATORIO"] = df["TELEFONE RELATORIO"].astype(str).str.strip()

# Telefones duplicados
telefones_duplicados = (
    df["TELEFONE RELATORIO"]
    .value_counts()
    .loc[lambda x: x > 1]
    .index
)

# Filtrar apenas duplicados
df_dup = df[df["TELEFONE RELATORIO"].isin(telefones_duplicados)]

# Agrupar e verificar usuários diferentes
problemas = []

for telefone, grupo in df_dup.groupby("TELEFONE RELATORIO"):
    usuarios_unicos = grupo["USUARIO"].unique()

    if len(usuarios_unicos) > 1:
        problemas.append({
            "TELEFONE": telefone,
            "USUARIOS": list(usuarios_unicos),
            "QTD_USUARIOS": len(usuarios_unicos)
        })

# 🔍 PRINTS DE VERIFICAÇÃO
print("===== VERIFICAÇÃO DE SEGURANÇA =====")
print(f"Total de telefones duplicados analisados: {df_dup['TELEFONE RELATORIO'].nunique()}")
print(f"Telefones com USUÁRIOS DIFERENTES: {len(problemas)}")
print("")

# Listar detalhes
for item in problemas:
    print(f"📞 TELEFONE: {item['TELEFONE']}")
    print(f"👤 USUÁRIOS ({item['QTD_USUARIOS']}):")
    for u in item["USUARIOS"]:
        print(f"   - {u}")
    print("-" * 40)

# Alerta final
if len(problemas) > 20:
    print("⚠️ ALERTA: Mais de 20 casos encontrados. RECOMENDADO remodelar o arquivo.")
else:
    print("✅ Quantidade controlável. Dá pra tratar manualmente com segurança.")

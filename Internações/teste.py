import pandas as pd

# ===============================
# 1️⃣ DataFrame com estado atual
# ===============================
df_estado_atual = pd.DataFrame({
    "Contato": ["A", "B", "C"],
    "Status": ["LIDA", "ENVIADA", "ENTREGUE"]
})

print("\n📌 df_estado_atual (tabela de referência):")
print(df_estado_atual)

# ===============================
# 2️⃣ Transformar Contato em index
# ===============================
map_chave = df_estado_atual.set_index("Contato")

print("\n🗺️ map_chave (Contato vira index):")
print(map_chave)

print("\n🔑 Índice do map_chave:")
print(map_chave.index.tolist())

# ===============================
# 3️⃣ DataFrame de novos usuários
# ===============================
df_novos = pd.DataFrame({
    "CHAVE RELATORIO": ["A", "B", "D"],
    "ULTIMO STATUS DE ENVIO": [None, None, None]
})

print("\n📄 df_novos (antes do map):")
print(df_novos)

# ===============================
# 4️⃣ Criar máscara
# ===============================
mask_chave = df_novos["CHAVE RELATORIO"].isin(map_chave.index)

print("\n🎭 mask_chave (quem existe no map_chave?):")
print(mask_chave.tolist())

# ===============================
# 5️⃣ A LINHA QUE CONFUNDE
# ===============================
valores_para_mapear = df_novos.loc[mask_chave, "CHAVE RELATORIO"]

print("\n🔎 Valores usados no map (CHAVE RELATORIO):")
print(valores_para_mapear.tolist())

status_mapeado = valores_para_mapear.map(map_chave["Status"])

print("\n🎯 Resultado do map (Status encontrado):")
print(status_mapeado.tolist())

# ===============================
# 6️⃣ Escrita no df_novos
# ===============================
df_novos.loc[mask_chave, "ULTIMO STATUS DE ENVIO"] = status_mapeado

print("\n✅ df_novos FINAL:")
print(df_novos)

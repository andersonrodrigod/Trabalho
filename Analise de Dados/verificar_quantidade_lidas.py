import pandas as pd

print("🔄 Carregando arquivos...")

# 1) Ler os arquivos
df_complica = pd.read_excel("complica_outubro_hap.xlsx")
df_base = pd.read_excel("MES OUTUBRO GERAL.xlsx", sheet_name="BASE")

print("✔ Arquivos carregados!")

# 2) Pegar a coluna Codigo do complica e transformar em string
codigos = df_complica["Codigo"].dropna().astype(str)

# Transformar COD USUARIO da BASE em string também
df_base["COD USUARIO"] = df_base["COD USUARIO"].astype(str)

# 3) Filtrar apenas linhas na BASE cujo COD USUARIO aparece no complica
base_filtrada = df_base[df_base["COD USUARIO"].isin(codigos)]

print(f"🔍 Registros encontrados na BASE para esses códigos: {len(base_filtrada)}")

# 4) Contar quantos estão com STATUS = 'Lida'
total_lida = (base_filtrada["STATUS"] == "Lida").sum()

# 5) Contar quantos têm algum valor em p1
total_p1 = base_filtrada["P1"].notna().sum()

# 6) Contar quantos têm STATUS = 'Lida' E p1 preenchido
total_lida_e_p1 = base_filtrada[
    (base_filtrada["STATUS"] == "Lida") & (base_filtrada["P1"].notna())
].shape[0]

print("\n📊 RESULTADOS:")
print(f"👉 Total com STATUS = 'Lida': {total_lida}")
print(f"👉 Total com valor na coluna p1: {total_p1}")
print(f"👉 Total com STATUS = 'Lida' e p1 preenchido: {total_lida_e_p1}")


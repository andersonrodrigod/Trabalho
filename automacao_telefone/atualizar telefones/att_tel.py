import pandas as pd

# Lê apenas a aba BASE da planilha original
df_base = pd.read_excel("Planilha Julho 14.10 atualizada 1.xlsx", sheet_name="BASE", dtype=str)

# Lê os novos telefones
new_tel = pd.read_excel("total_julho_adicionar.xlsx", dtype=str)
new_tel = new_tel[["Codigo", "Telefone 2"]].dropna()
new_tel["Telefone 2"] = new_tel["Telefone 2"].apply(lambda x: "55" + str(x).strip() if pd.notnull(x) else x)

# Cria um dicionário para busca rápida
tel_dict = new_tel.drop_duplicates(subset="Codigo").set_index("Codigo")["Telefone 2"].to_dict()

# Atualiza os telefones diretamente
df_base = df_base.copy()
df_base["TELEFONE_ANTIGO"] = df_base["TELEFONE"]
df_base["TELEFONE"] = df_base.apply(
    lambda row: tel_dict.get(row["COD USUARIO"], row["TELEFONE"]),
    axis=1
)

# Salva apenas a aba BASE atualizada
with pd.ExcelWriter("Planilha Julho nova.xlsx", engine="openpyxl") as writer:
    df_base.to_excel(writer, sheet_name="BASE", index=False)

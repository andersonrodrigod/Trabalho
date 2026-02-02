import pandas as pd

# 1. Ler os arquivos
df_excel = pd.read_excel("BASE DEZEMBRO INTERNACAO MAIN.xlsx")
df_csv = pd.read_csv("telefone_procedimentos_dezembro.csv")

# 2. Converter colunas de usuário para string
df_excel["COD USUARIO"] = df_excel["COD USUARIO"].astype(str).str.strip()
df_csv["CD_USUARIO"] = df_csv["CD_USUARIO"].astype(str).str.strip()

# 3. Lista de telefones
telefones = ["TELEFONE_1", "TELEFONE_2", "TELEFONE_3", "TELEFONE_4", "TELEFONE_5"]

# 4. Tratar telefones do CSV
for col in telefones:
    df_csv[col] = (
        df_csv[col]
        .fillna("")              # remove NaN real
        .astype(str)
        .str.strip()
        .replace("nan", "")      # remove 'nan' em string
    )

# 5. Criar colunas no Excel (já vazias)
for col in telefones:
    df_excel[col] = ""

# 6. Criar dicionário de busca (1 usuário = 1 conjunto de telefones)
dict_telefones = (
    df_csv
    .drop_duplicates(subset=["CD_USUARIO"])
    .set_index("CD_USUARIO")[telefones]
    .to_dict(orient="index")
)

# 7. Percorrer o Excel linha a linha
for idx, cod_usuario in df_excel["COD USUARIO"].items():
    if cod_usuario in dict_telefones:
        for tel_col in telefones:
            telefone = dict_telefones[cod_usuario][tel_col]

            # Só preenche se tiver valor
            if telefone != "":
                df_excel.at[idx, tel_col] = "55" + telefone
            else:
                df_excel.at[idx, tel_col] = ""

# 8. Salvar arquivo final
df_excel.to_excel(
    "BASE DEZEMBRO INTERNACAO MAIN_COM_TELEFONES.xlsx",
    index=False
)

print("Processo finalizado com sucesso, sem NaN e com prefixo 55.")

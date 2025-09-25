import pandas as pd


def ajustar_numero_telefone(telefone):

    if telefone.startswith("55"):
        telefone = telefone[2:]
    if len(telefone) != 11 or telefone[2] != "9":
        return "NÚMERO ERRADO"
    else:
        return telefone

def verificar_existencia_numero(telefone, df):
    df = pd.read_excel(df)

    for i, row in df.iterrows():
        codigo = row["Codigo"]
        telefone1 = row["Telefone 1"]
        telefone2 = row["Telefone 2"]
        telefone3 = row["Telefone 3"]
        telefone4 = row["Telefone 4"]

        if telefone not in [telefone1, telefone2, telefone3, telefone4]:
            colunas_para_verificar = ["Telefone 2", "Telefone 3", "Telefone 4"]

            for col in colunas_para_verificar:
                if pd.isna(row[col]) or row[col] == "":
                    df.at[i, col] = str(telefone)

                print(f"Código {row['Codigo']}: número adicionado em {col}")
                df.to_excel("dados.xlsx", index=False)
                break
        else:
            print(f"Código {row['Codigo']}: número já existe na linha")

        print(f"Código: {codigo} | Tel1: {telefone1} | Tel2: {telefone2} | Tel3: {telefone3}")




df = "dados.xlsx"
telefone = "31987150823"
verificar_existencia_numero(telefone, df)




ajuste = ajustar_numero_telefone(telefone)

if ajuste == "NÚMERO ERRADO":
    # nova automação
    print(ajuste)


import pandas as pd
from load_data import carregar_arquivo_excel

arquivo = "data/raw/Planilha Agosto.xlsx"

coluna_1 = [ "ELOGIO OU QUEIXA", 'GRUPO', 'MOTIVO',
       'comentário p1']

coluna_2 = ['ELOGIO OU QUEIXA.1', 'GRUPO.1', 'MOTIVO.1',
       'comentário p2']

coluna_3 = ['ELOGIO OU QUEIXA.2', 'GRUPO.2', 'MOTIVO.2',
       'comentário p3']

coluna_4 = ['ELOGIO OU QUEIXA.3', 'GRUPO.3', 'MOTIVO.3',
       'comentário p4']

coluna_5 = ['ELOGIO OU QUEIXA.4', 'GRUPO.4', 'MOTIVO.4',
       'comentario p5',]

coluna_6 = ['ELOGIO OU QUEIXA.5', 'GRUPO.5', 'MOTIVO.5',
       'comentario p6']

df = carregar_arquivo_excel(arquivo=arquivo, aba="BASE")


def pre_processamento(df, colunas):
    # Passo 1 – Selecionar só as colunas
    df = df[colunas].copy()

    # Passo 2 – Padronizar nomes (fica mais fácil de trabalhar)
    df.columns = (
        df.columns
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("á", "a")
        .str.replace("ã", "a")
    )

    # Passo 3 – Remover linhas totalmente vazias
    df = df.dropna(how="all")

    # Passo 4 – Encontrar automaticamente a coluna grupo e comentário
    col_grupo = [c for c in df.columns if "grupo" in c][0]
    col_comentario = [c for c in df.columns if "coment" in c][0]

    # Passo 5 – Remover linhas onde esse comentário está vazio
    df[col_comentario] = df[col_comentario].astype(str)

    # Passo 6 – Remover linhas onde esse comentário está vazio
    df[col_grupo] = df[col_grupo].replace("", pd.NA)

    # Remover linhas com NA no comentário
    df = df.dropna(subset=[col_grupo])
    # Passo 7 – Remover comentários com menos de 10 caracteres
    df = df[df[col_comentario].str.len() >= 5]
    print(df)



    df.to_csv("data/labeled/coluna_1_agosto_total.csv", index=False)


pre_processamento(df, coluna_1)












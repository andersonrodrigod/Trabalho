import pandas as pd


def contar_status(df):
    return {
        "Lidas": df[df["Status"] == "Lida"].shape[0],
        "Não quis": df[df["Status"] == "Não quis"].shape[0],
        "Óbito": df[df["Status"] == "Óbito"].shape[0],
        "Sem resultado": df[df["Status"].isna()].shape[0]
    }

def contar_status_resposta(df):
    return {
        "p1": df[(df["Status"] == "Lida") & (df["p1"].notna())].shape[0],
        "p2": df[(df["Status"] == "Lida") & (df["p2"].notna())].shape[0],
        "p3": df[(df["Status"] == "Lida") & (df["p3"].notna())].shape[0],
        "p4": df[(df["Status"] == "Lida") & (df["p4"].notna())].shape[0],
        "p5": df[(df["Status"] == "Lida") & (df["p5"].notna())].shape[0],
        "p6": df[(df["Status"] == "Lida") & (df["p6"].notna())].shape[0],
    }

def contar_elogio_queixas_geral(df):
    tabela = df.groupby(["GRUPO-1", "MOTIVO-1", "ELOGIO OU QUEIXA-1"]).size().unstack(fill_value=0)
    return tabela

"""def contar_elogio(df):
    df_elogio = df[df["ELOGIO OU QUEIXA-1"] == "ELOGIO"]
    tabela = df_elogio.groupby(["GRUPO-1", "MOTIVO-1"]).size().unstack(fill_value=0)
    return tabela"""

def contar_elogio(df):
    tabelas = []

    for i in range(1, 7):  # GRUPO-1 até GRUPO-6
        grupo_col = f"GRUPO-{i}"
        motivo_col = f"MOTIVO-{i}"
        tipo_col = f"ELOGIO OU QUEIXA-{i}"

        if grupo_col in df.columns and motivo_col in df.columns and tipo_col in df.columns:
            df_elogio = df[df[tipo_col] == "ELOGIO"]
            tabela = df_elogio.groupby([grupo_col, motivo_col]).size().reset_index(name="Quantidade")
            tabela.columns = ["Grupo", "Motivo", "Quantidade"]
            tabelas.append(tabela)

    # Junta todas as tabelas em uma só
    tabela_final = pd.concat(tabelas, ignore_index=True)

    # Agrupa novamente para somar os elogios por grupo e motivo
    tabela_resumo = tabela_final.groupby(["Grupo", "Motivo"]).sum().unstack(fill_value=0)

    return tabela_resumo
"""
def contar_queixas(df):
    df_elogio = df[df["ELOGIO OU QUEIXA-1"] == "QUEIXA"]
    tabela = df_elogio.groupby(["GRUPO-1", "MOTIVO-1"]).size().unstack(fill_value=0)
    return tabela"""
    
def contar_queixas(df):
    tabelas = []

    for i in range(1, 7):  # GRUPO-1 até GRUPO-6
        grupo_col = f"GRUPO-{i}"
        motivo_col = f"MOTIVO-{i}"
        tipo_col = f"ELOGIO OU QUEIXA-{i}"

        if grupo_col in df.columns and motivo_col in df.columns and tipo_col in df.columns:
            df_elogio = df[df[tipo_col] == "QUEIXA"]
            tabela = df_elogio.groupby([grupo_col, motivo_col]).size().reset_index(name="Quantidade")
            tabela.columns = ["Grupo", "Motivo", "Quantidade"]
            tabelas.append(tabela)

    # Junta todas as tabelas em uma só
    tabela_final = pd.concat(tabelas, ignore_index=True)

    # Agrupa novamente para somar os elogios por grupo e motivo
    tabela_resumo = tabela_final.groupby(["Grupo", "Motivo"]).sum().unstack(fill_value=0)

    return tabela_resumo



def contar_respostas(df):
    perguntas = ["p1", "p2", "p3", "p4", "p5", "p6"]
    resultado = {}

    for pergunta in perguntas:
        resultado[pergunta] = {
            str(nota): df[df[pergunta] == nota].shape[0]
            for nota in range(1, 6)
        }

    return resultado

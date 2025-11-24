import pandas as pd
import unicodedata



coluna_1 = ["ELOGIO OU QUEIXA", "GRUPO", "MOTIVO", "p1", "comentário p1"]

caminho_arquivo = "data/labeled/coluna_1.csv"

def remover_acentos(texto):
    if isinstance(texto, str):
        return "".join(
            c for c in unicodedata.normalize("NFD", texto)
            if unicodedata.category(c) !="Mn"
        )
    return texto

def limpar_texto(texto):
    


def pre_processamento():
    print("Iniciando o pré-processamento da coluna 1...")

    # 1 — LER ARQUIVO
    df = pd.read_csv(caminho_arquivo, sep=",", encoding="utf-8")
    df = df["comentario_p1"].apply(remover_acentos)
    print(df.head(50))





pre_processamento()
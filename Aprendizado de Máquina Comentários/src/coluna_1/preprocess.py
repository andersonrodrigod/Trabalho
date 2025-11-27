import pandas as pd
import unicodedata
import re



caminho_arquivo = "data/labeled/coluna_1/coluna_1_grupo.csv"
caminho_vai = "data/processed/coluna_1_grupo.csv"

def remover_acentos(texto):
    if isinstance(texto, str):
        return "".join(
            c for c in unicodedata.normalize("NFD", texto)
            if unicodedata.category(c) !="Mn"
        )
    return texto

def limpar_texto(texto):
    if not isinstance(texto,str):
        return ""

    texto = texto.lower()
    texto = remover_acentos(texto)
    texto = texto.replace("\n", " ")
    texto = re.sub(r"[^a-z0-9\s.,!?]", " ", texto)
    texto = " ".join(texto.split())

    return texto

def pre_processamento(caminho):
    print("Iniciando o pré-processamento da coluna 1...")

    
    df = pd.read_csv(caminho_arquivo, sep=",")

    df = df.dropna()

    df["comentario_p1"] = df["comentario_p1"].apply(limpar_texto)

    #df = df[df["grupo"].isin(["ELOGIO", "QUEIXA"])]


    df.to_csv(caminho, index=False)

    





pre_processamento(caminho_vai)
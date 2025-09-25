import pandas as pd
import pyautogui as py

def ajustar_numero_telefone(telefone):
    telefone = telefone.strip()

    if telefone.startswith("55"):
        telefone = telefone[2:]
    
    # valida número (11 dígitos e começa com 9)
    if len(telefone) != 11 or telefone[2] != "9":
        return None  # retorna None em vez de string
    return telefone


def is_numero_telefone(telefone):
    if telefone is None:
        return "INVALIDO"
    return "NOVO"  # pode ser tratado depois como "ENCERRA O LOOP"



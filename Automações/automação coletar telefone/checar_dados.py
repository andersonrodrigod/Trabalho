import pandas as pd
import pyautogui as py


def ajustar_numero_telefone(telefone):
    telefone = telefone.strip()

    # Remove o código do país, se presente
    if telefone.startswith("55"):
        telefone = telefone[2:]

    # Corrige celular sem o 9 (ex: 10 dígitos, começa com 6, 7, 8 ou 9)
    if len(telefone) == 10 and telefone[2] in ["6", "7", "8", "9"]:
        telefone = telefone[:2] + "9" + telefone[2:]

    # Validação para celular compatível com WhatsApp
    if len(telefone) == 11 and telefone[2] == "9":
        return telefone

    # Se não for celular, retorna None
    return None


def is_numero_telefone(telefone):
    if telefone is None:
        return "INVALIDO"
    return "NOVO"  # pode ser tratado depois como "ENCERRA O LOOP"

"""def ajustar_numero_telefone(telefone):
    telefone = str(telefone).strip()
    if telefone.endswith(".0"):
        telefone = telefone[:-2]
    return telefone
"""





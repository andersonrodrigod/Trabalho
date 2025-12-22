import pandas as pd
import pyautogui as py
import pyperclip
import time


def copy_vazio():
    pyperclip.copy("")

def automar_function(df):

    for idx, valor in df["SOLICITANTE"].head(1).items():

        medico = str(valor).strip()





        especialidade_1 = "CARDIOLOGIA"
        especialidade_2 = "OFTALMOLOGIA"

        if especialidade_1:
            df.at[idx, "ESPECIALIDADE 1"] = especialidade_1
        if especialidade_2:
            df.at[idx, "ESPECIALIDADE 2"] = especialidade_2

        print(f"Iniciando automação para o médico: {medico}")

        df.to_excel("medicos_unicos_atualizado.xlsx", index=False)


df = pd.read_excel("medicos_unicos.xlsx")

automar_function(df)
import pandas as pd
import pyautogui as py
import pyperclip
import time


def copy_vazio():
    pyperclip.copy("")

df = pd.read_excel("medicos_unicos_ccg.xlsx")

colunas_texto = [
    "STATUS ESPECIALISTA",
    "STATUS ESPECIALIDADE",
    "ESPECIALIDADE 1",
    "ESPECIALIDADE 2"
]

for col in colunas_texto:
    if col not in df.columns:
        df[col] = pd.NA
    df[col] = df[col].astype("string")

mask_nao_processado = (
    df["STATUS ESPECIALISTA"].isna() |
    (df["STATUS ESPECIALISTA"].str.strip() == "") |
    (df["STATUS ESPECIALISTA"].str.lower() == "nan")
)

# 

def automar_function(df):

    time.sleep(1)

    for idx, row in df[mask_nao_processado].head(5).iterrows():
        valor = str(row["SOLICITANTE"]).strip()

        copy_vazio()
        medico = str(valor).strip()

        pyperclip.copy(medico)
        time.sleep(0.5)
        py.hotkey("ctrl", "v")
        py.press('f8')
        time.sleep(3)
        copy_vazio()
        py.hotkey("ctrl", "c")

        if pyperclip.paste() == "":
            py.press("enter", presses=2, interval=0.4)
            df.at[idx, "STATUS ESPECIALISTA"] = "MÉDICO NÃO ENCONTRADO"
            df.at[idx, "ESPECIALIDADE 1"] = ""
            df.at[idx, "ESPECIALIDADE 2"] = ""
            df.at[idx, "STATUS ESPECIALIDADE"] = ""
            continue
        copy_vazio()

        py.press("pagedown")
        time.sleep(1)
        py.hotkey("ctrl", "c")

        if pyperclip.paste() == "":
            py.press("pageup")
            time.sleep(1)
            py.press("f7")
            time.sleep(1)
            py.press("enter")
            time.sleep(1)
            py.press("enter", presses=2, interval=0.4)
            df.at[idx, "STATUS ESPECIALISTA"] = "SEM IDENTIFICAÇÃO DE ESPECIALISTA"
            df.at[idx, "ESPECIALIDADE 1"] = ""
            df.at[idx, "ESPECIALIDADE 2"] = ""
            df.at[idx, "STATUS ESPECIALIDADE"] = "0 ESPECIALIDADE"
            continue
        
        especialista_1 = pyperclip.paste()
        df.at[idx, "ESPECIALIDADE 1"] = especialista_1
        time.sleep(0.5)

        copy_vazio()

        py.press("down")
        time.sleep(1)
        py.hotkey("ctrl", "c")

        if pyperclip.paste() == "" or especialista_1 == pyperclip.paste():
            copy_vazio()
            df.at[idx, "ESPECIALIDADE 2"] = ""
            df.at[idx, "STATUS ESPECIALIDADE"] = "1 ESPECIALIDADE"
            df.at[idx, "STATUS ESPECIALISTA"] = "ESPECIALISTA CONCLUIDO"
            py.press("pagedown", presses=2, interval=0.4)
            py.hotkey("ctrl", "c")
            time.sleep(0.2)
            especialista_3 = pyperclip.paste()
            df.at[idx, "ESPECIALIDADE 3"] = especialista_3
            py.press("pageup", presses=3, interval=0.4)
            time.sleep(1)
            py.press("f7")
            time.sleep(1)
            py.press("enter")
            time.sleep(1)
            py.press("enter", presses=2, interval=0.4)
            continue

        especialista_2 = pyperclip.paste()
        df.at[idx, "ESPECIALIDADE 2"] = especialista_2
        df.at[idx, "STATUS ESPECIALIDADE"] = "2 ESPECIALIDADES"
        df.at[idx, "STATUS ESPECIALISTA"] = "ESPECIALISTA CONCLUIDO"

        py.press("up")
        py.press("pagedown", presses=2, interval=0.4)
        py.hotkey("ctrl", "c")
        time.sleep(0.2)
        especialista_3 = pyperclip.paste()
        df.at[idx, "ESPECIALIDADE 3"] = especialista_3
        py.press("pageup", presses=3, interval=0.4)
        time.sleep(1)
        py.press("f7")
        time.sleep(1)
        py.press("enter")
        time.sleep(1)
        py.press("enter", presses=2, interval=0.4)  
        

        
        df.to_excel("medicos_unicos_ccg.xlsx", index=False)
        
    df.to_excel("medicos_unicos_ccg.xlsx", index=False)



automar_function(df)
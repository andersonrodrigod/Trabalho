import pandas as pd
import pyautogui as py
import pyperclip
import time
import os

dados = []

def copy_vazio():
    pyperclip.copy("")

time.sleep(2)  # tempo pra posicionar o cursor

for i in range(5):
    copy_vazio()
    py.hotkey("ctrl", "c")
    time.sleep(0.5)
    numero_copiado = pyperclip.paste()

    py.press("tab")

    copy_vazio()
    py.hotkey("ctrl", "c")
    time.sleep(0.5)
    texto_copiado = pyperclip.paste()

    py.hotkey("shift", "tab")
    py.press("down")

    dados.append([numero_copiado, texto_copiado])
    print(f"Linha {i} capturada")

# cria DataFrame novo
df_novo = pd.DataFrame(dados, columns=["CODIGO", "ESPECIALIDADE"])

arquivo = "codigo_especialidade.xlsx"

# se já existir, concatena
if os.path.exists(arquivo):
    df_antigo = pd.read_excel(arquivo)
    df_final = pd.concat([df_antigo, df_novo], ignore_index=True)
else:
    df_final = df_novo

df_final.to_excel(arquivo, index=False)

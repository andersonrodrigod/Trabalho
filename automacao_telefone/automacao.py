import pandas as pd
import pyperclip
import time
import pyautogui as py


def copy_vazio():
    pyperclip.copy("")

def automacao_codigo_inicio(codigo):
    pyperclip.copy(codigo)
    time.sleep(0.5)
    py.hotkey("ctrl", "v")
    time.sleep(0.5)
    py.press("f8")
    time.sleep(0.5)

    copy_vazio()

    py.press("enter")
    time.sleep(0.5)
    py.press("enter")
    time.sleep(0.5)


def automacao_codigo_next():
    py.click(54,120)
    time.sleep(0.5)
    py.press("f7")
    time.sleep(0.5)


def pegar_telefone():
    time.sleep(0.5)
    py.hotkey("ctrl", "c")
    time.sleep(0.5)
    telefone = pyperclip.paste()
    #print(telefone)
    print(telefone)
    time.sleep(0.5)
    #print(repr(telefone))
    return telefone

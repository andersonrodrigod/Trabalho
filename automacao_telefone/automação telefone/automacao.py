import pandas as pd
import pyperclip
import time
import pyautogui as py
import re


def copy_vazio():
    pyperclip.copy("")

def automacao_codigo_inicio(codigo):
    pyperclip.copy(codigo)
    print(codigo)
    time.sleep(0.5)
    py.hotkey("ctrl", "v")
    time.sleep(0.5)
    py.press("f8")
    time.sleep(0.5)

    verificar_cor_vermelho_puro(121, 159)

    copy_vazio()

    py.press("enter")
    py.press("enter")
    py.press("enter")
    time.sleep(0.5)
    py.press("enter")
    time.sleep(0.5)


def verificar_cor_vermelho_puro(x, y):
    time.sleep(0.5)

    for x_atual in range(x, x + 61):
        r, g, b = py.pixel(x_atual, y)
        print(f"Pixel em ({x_atual},{y}): RGB = ({r}, {g}, {b})")

        if (r, g, b) == (255, 0, 0):
            print("Cor vermelha pura detectada.")
            py.press("esc")
            return  # Interrompe a função após detectar vermelho

    print("Nenhuma cor vermelha pura encontrada.")


def automacao_codigo_next():
    py.click(54,120)
    time.sleep(0.5)
    py.press("f7")
    time.sleep(0.5)

    py.click(880,121)
    py.press("up")
    time.sleep(0.5)
    py.press("enter")
    time.sleep(0.5)

    py.click(54,120)
    time.sleep(0.5)


def automacao_codigo_next_sem_dado():
    py.click(54,120)
    time.sleep(0.5)
    py.press("f7")
    time.sleep(0.5)


def pegar_telefone():
    time.sleep(0.5)
    py.hotkey("ctrl", "c")
    time.sleep(0.5)
    telefone = pyperclip.paste()
    telefone_limpo = re.sub(r'\s+', '', telefone)  # remove espaços, tabs, quebras de linha

    print(f"Telefone copiado: {repr(telefone)}")

    if not telefone_limpo or telefone_limpo in ["\u200b", "\ufeff"]:
        print("⚠️ Nenhum telefone válido encontrado. Encerrando tentativa.")
        return None  # sinaliza que não encontrou nada útil

    return telefone

def aplicar_filtro():
    py.click(79, 545)
    py.press("f7")
    py.press("l")
    py.press("enter")
    py.press("f8")
    time.sleep(0.5)



def verificar_cor_pixel(x, y):
    py.click(x, y)
    time.sleep(0.5)
    padroes_verde = [
        (142, 150, 57),
        (182, 172, 0),
        (0, 128, 0),
        (0, 150, 102),
        (57, 127, 0),
        (142, 150, 0),
        (57, 127, 57)
    ]

    for x_atual in range(x, x + 61):  
        r, g, b = py.pixel(x_atual, y)
        print(f"Pixel em ({x},{y}): RGB = ({r}, {g}, {b})")

        if (r, g, b) == (0, 0, 0):
            print("Cor preta detectada.")
            return "PRETO"

        elif (r, g, b) in padroes_verde:
            print("Cor verde detectada.")
            return "VERDE"

        else:
            print("Cor não reconhecida, continuando varredura...")

    print("Nenhuma cor válida encontrada.")
    return False

import pyautogui as py
import time


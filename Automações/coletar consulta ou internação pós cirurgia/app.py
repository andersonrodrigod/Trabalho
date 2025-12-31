import pandas as pd
import pyautogui as py
import pyperclip
import time

codigo = "0DCB9000126012" 
data = "%11/2025"
internacao = "I"

time.sleep(3)

pyperclip.copy(codigo)

py.hotkey("ctrl", "v")

py.click(643, 422)

py.write(internacao)
time.sleep(1)

py.click(405, 380)

pyperclip.copy(data)

time.sleep(1)

py.hotkey("ctrl", "v")

py.press("f8")

time.sleep(1)

py.click(405, 380)

time.sleep(0.5)

py.press("down")






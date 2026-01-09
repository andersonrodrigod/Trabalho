import pandas as pd
import time
import pyautogui as py
import pyperclip


def copy_vazio():
    pyperclip.copy("")


def automar_function(df):

    time.sleep(2)
    df["STATUS BOT"] = df["STATUS BOT"].fillna("").astype(str).str.strip()

    for idx, row in df[df["STATUS BOT"] == ""].head(5).iterrows():
        tempo_inicio = time.time() 
        copy_vazio()
        senha = str(row["SENHA"]).strip()

        time.sleep(0.5)
        pyperclip.copy(senha)
        py.hotkey("ctrl", "v")
        time.sleep(0.5)
        py.press("f8")

        copy_vazio()
        time.sleep(0.5)

        # verificação pra saber se apareceu a senha depois de carregado
        py.hotkey("ctrl", "c")
        time.sleep(0.3)
        senha_copiada = pyperclip.paste().strip()
        if senha_copiada == "":
            df.at[idx, "STATUS COLETA"] = "SENHA INVÁLIDA"
            df.at[idx, "STATUS BOT"] = "VERIFICADO"
            py.press("f7")
            continue
        
        copy_vazio()

        py.click(233, 161)
        time.sleep(0.5)
        py.hotkey("ctrl", "c")
        tp_atendimento = pyperclip.paste().strip()

        copy_vazio()

        py.click(401, 380)
        time.sleep(0.5)
        py.hotkey("ctrl", "c")
        dt_internacao = pyperclip.paste().strip()

        copy_vazio()

        py.click(122, 243)
        time.sleep(0.5)
        py.hotkey("ctrl", "c")
        cod_procedimento = pyperclip.paste().strip()     

        copy_vazio()

        py.click(244, 244)
        time.sleep(0.5)
        py.hotkey("ctrl", "c")
        procedimento = pyperclip.paste().strip()   

        copy_vazio()


        df.at[idx, "TP ATENDIMENTO"] = tp_atendimento
        df.at[idx, "DT INTERNACAO"] = dt_internacao
        df.at[idx, "COD PROCEDIMENTO"] = cod_procedimento
        df.at[idx, "PROCEDIMENTO"] = procedimento
        df.at[idx, "STATUS BOT"] = "CONCLUÍDO"

        py.click(122, 163)
        time.sleep(0.5)
        py.press("f7")
        tempo_decorrido = time.time() - tempo_inicio
        print(f"⏱️ Tempo de processamento: {tempo_decorrido:.2f} segundos")

        df.to_excel('OUTUBRO_AUTOMACAO_INTERNACAO.xlsx', index=False)




df = pd.read_excel('OUTUBRO_AUTOMACAO_INTERNACAO.xlsx')

automar_function(df)

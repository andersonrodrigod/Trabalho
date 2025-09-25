import pandas as pd
import pyperclip
import time
import pyautogui as py
from automacao import pegar_telefone, automacao_codigo_inicio, automacao_codigo_next
from checar_dados import ajustar_numero_telefone, is_numero_telefone

def copy_vazio():
    pyperclip.copy("")

def coordenadas_telefone():
    return [
        (114, 544),  # Telefone 1
        (108, 561),  # Telefone 2
        (105, 580),  # Telefone 3
    ]

def automar_fuction(df):
    df = pd.read_excel(df)

    colunas_telefone = ["Telefone 1", "Telefone 2", "Telefone 3", "Telefone 4"]
    df[colunas_telefone] = df[colunas_telefone].fillna("").astype(str).apply(lambda col: col.str.strip())
    df["Etiqueta"] = df["Etiqueta"].fillna("").astype(str).str.strip()

    for i, row in df.iterrows():
        codigo = row["Codigo"]
        automacao_codigo_inicio(codigo)

        consecutivos_invalidos = 0
        repeticoes_telefone = 0

        for j in range(3):
            x, y = coordenadas_telefone()[j]
            copy_vazio()
            py.click(x, y)
            telefone = pegar_telefone()
            telefone = ajustar_numero_telefone(telefone)
            #print(telefone)

            resultado = is_numero_telefone(telefone)

            telefones_existentes = [row[col] for col in colunas_telefone]

            if resultado == "NOVO" and telefone not in telefones_existentes:
                print("Número diferente, levando para o Excel.")
                for col in ["Telefone 2", "Telefone 3", "Telefone 4"]:
                    if row[col] == "":
                        df.at[i, col] = telefone
                        print(f"Código {codigo}: número adicionado em {col}")
                        df.at[i, "Etiqueta"] = "NOVO CONTATO"
                        break
            elif telefone in telefones_existentes:
                repeticoes_telefone += 1
                print(f"Número igual ({repeticoes_telefone}x), tentando novamente...")
                if repeticoes_telefone >= 4:
                    df.at[i, "Etiqueta"] = "MESMO CONTATO"
                    print("Número repetido 4 vezes. Encerrando.")
                    break
            else:
                print("Número inválido")
                consecutivos_invalidos += 1
                if consecutivos_invalidos >= 2:
                    print("Dois números inválidos consecutivos. Encerrando.")
                    df.at[i, "Etiqueta"] = "SEM CONTATO"
                    break
            
        telefones_atualizados = [df.at[i, c] for c in colunas_telefone]
        print(f"Código: {codigo} | Tel1: {telefones_atualizados[0]} | Tel2: {telefones_atualizados[1]} | Tel3: {telefones_atualizados[2]}")

        # Salvar checkpoint a cada 10 linhas
        if i % 10 == 0:
            df.to_excel("dados.xlsx", index=False)
            print(f"Checkpoint salvo na linha {i}")

        automacao_codigo_next()







import pandas as pd
import pyperclip
import time
import pyautogui as py
from automacao import pegar_telefone, automacao_codigo_next, automacao_codigo_next_sem_dado, aplicar_filtro, verificar_cor_pixel, automacao_nome_inicio, automacao_nome_next
from checar_dados import ajustar_numero_telefone, is_numero_telefone




def copy_vazio():
    pyperclip.copy("")

def coordenadas_telefone():
    return [
        (79, 545),  # Telefone 1
        (79, 561),  # Telefone 2
        (79, 580),  # Telefone 3
    ]


def telefone_valido(telefone):
    return telefone is not None and telefone.strip() != ""

def automar_fuction(df):
    
    df = pd.read_excel(df, dtype=str)

    time.sleep(2)

    colunas_telefone = ["Telefone 1", "Telefone 2", "Telefone 3", "Telefone 4"]
    df[colunas_telefone] = df[colunas_telefone].fillna("").astype(str).apply(lambda col: col.str.strip())
    df["Status"] = df["Status"].fillna("").astype(str).str.strip()
    

    
    for i, row in df[df["Status"] == ""].iterrows():
        codigo = str(row["Codigo"]).strip()
        nome = str(row["Nome"]).strip()
        idade = str(row["IDADE T"]).strip()
        automacao_nome_inicio(nome)
        #print(codigo)
        copy_vazio()
        telefone_adicionado = False
        consecutivos_invalidos = 0
        repeticoes_telefone = 0
        filtro_aplicado = True

        time.sleep(0.7)
        py.hotkey("ctrl", "c")
        time.sleep(0.5)
        conteudo_copy = pyperclip.paste().strip()

        if not conteudo_copy:
            #print(f"Código {codigo}: sem conteúdo no Ctrl+C. Pulando para próxima linha.")
            df.at[i, "Status"] = "BASE INCORRETA"
            #print(f"Código {codigo}: sem conteúdo no Ctrl+C. Pulando para próxima linha.")
            automacao_codigo_next_sem_dado() 
            continue 
        
        py.click(792,119)
        time.sleep(0.7)
        py.hotkey("ctrl", "c")
        idade_copy = pyperclip.paste().strip()
        print(idade_copy)
        print(type(idade_copy))
        time.sleep(0.5)

        if idade_copy != idade:
            df.at[i, "Status"] = "IDADE DIFERENTE"
            automacao_codigo_next_sem_dado()
            continue 


        numero_preto = None
        for j in range(6):
            if j == 0 and filtro_aplicado:
                aplicar_filtro()

            if j > 2:
                py.click(361, 581)
                time.sleep(0.5)
                x, y = coordenadas_telefone()[2] 
            else:
                x, y = coordenadas_telefone()[j]
                    
            copy_vazio()
            py.click(x, y)
            time.sleep(0.5)
            telefone = pegar_telefone()

            if telefone is None:
                print("Telefone vazio ou inválido. Pulando para próxima tentativa.")
                consecutivos_invalidos += 1
                filtro_aplicado = False
                break 

            telefone = ajustar_numero_telefone(telefone)
            resultado = is_numero_telefone(telefone)
            telefones_existentes = [ajustar_numero_telefone(row[col].strip()) for col in colunas_telefone if row[col].strip()]

            cor = verificar_cor_pixel(x, y)


            if cor == "PRETO" and resultado == "NOVO" and telefone not in telefones_existentes:
                numero_preto = telefone 
                print("Número preto armazenado.")

            elif cor == "VERDE" and resultado == "NOVO" and telefone not in telefones_existentes:
                telefone_final = telefone
                print("Número diferente, levando para o Excel.")
                for col in ["Telefone 2", "Telefone 3", "Telefone 4"]:
                    if row[col] == "":
                        df.at[i, col] = telefone
                        print(f"Código {codigo}: número adicionado em {col}")
                        df.at[i, "Status"] = "NOVO CONTATO"
                        telefone_adicionado = True
                        break
                if telefone_adicionado:
                    break

            elif telefone in telefones_existentes:
                repeticoes_telefone += 1
                print(f"Número igual ({repeticoes_telefone}x), tentando novamente...")

                if repeticoes_telefone >= 4:
                    filtro_aplicado = False
                    print("Número repetido 4 vezes. Encerrando.")
                    break

            elif telefone is None:
                print("Número inválido")
                consecutivos_invalidos += 1

                if consecutivos_invalidos >= 1:
                    print("Dois números inválidos consecutivos. Encerrando.")
                    py.press("f4") 
                    filtro_aplicado = False
                    break

        py.press("f4")           
        if not telefone_adicionado and not filtro_aplicado:
            print("cheguei")
            py.press("f8")
            numero_verde_segundo_loop = None
            numero_preto_segundo_loop = None
            repeticoes_telefone = 0
            for j in range(8):
                if j > 2:
                    py.click(361, 581)
                    time.sleep(0.5)
                    x, y = coordenadas_telefone()[2]
                else:
                    x, y = coordenadas_telefone()[j]

                copy_vazio()
                py.click(x, y)
                time.sleep(0.5)
                telefone = pegar_telefone()

                if telefone is None:
                    if j == 1:
                        print("segundo loop")
                        py.press("esc")
                        if df.at[i, "Status"] not in ["NOVO CONTATO", "MESMO CONTATO"]:
                            df.at[i, "Status"] = "SEM CONTATO"
                        break
                    continue     
                telefone = ajustar_numero_telefone(telefone)
                resultado = is_numero_telefone(telefone)
                telefones_existentes = [ajustar_numero_telefone(row[col].strip()) for col in colunas_telefone if row[col].strip()]
                cor = verificar_cor_pixel(x, y)
                print(telefone)

                if resultado == "NOVO" and telefone not in telefones_existentes:
                    if cor == "VERDE":
                        numero_verde_segundo_loop = telefone
                        telefone_final = numero_verde_segundo_loop
                        print("Número verde armazenado.")
                        break        
                    elif cor == "PRETO" and not numero_preto_segundo_loop:
                        numero_preto_segundo_loop = telefone
                        print("Número preto armazenado.")

                elif telefone in telefones_existentes:
                    repeticoes_telefone += 1
                    print(f"Número igual ({repeticoes_telefone}x), tentando novamente...")
                    if df.at[i, "Status"] != "NOVO CONTATO":
                        df.at[i, "Status"] = "MESMO CONTATO"
                    if repeticoes_telefone >= 4:
                        print("Número repetido 4 vezes. Encerrando.")
                        break

                elif telefone is None:
                    print("Número inválido")
                    consecutivos_invalidos += 1
                    if consecutivos_invalidos >= 2:
                        print("Dois números inválidos consecutivos. Encerrando.")
                        if df.at[i, "Status"] not in ["NOVO CONTATO", "MESMO CONTATO"]:
                            df.at[i, "Status"] = "SEM CONTATO"
                        break 
            
            print("final")
            telefone_final = None
            if numero_verde_segundo_loop:
                telefone_final = numero_verde_segundo_loop
                print("Salvando número verde do segundo loop.")
            elif numero_preto and numero_preto not in telefones_existentes:
                telefone_final = numero_preto
                print("Salvando número preto do primeiro loop.")
            elif numero_preto_segundo_loop and numero_preto_segundo_loop not in telefones_existentes:
                telefone_final = numero_preto_segundo_loop
                print("Salvando número preto do segundo loop.")

            if telefone_final:
                for col in ["Telefone 2", "Telefone 3", "Telefone 4"]:
                    if row[col] == "":
                        df.at[i, col] = telefone_final
                        df.at[i, "Status"] = "NOVO CONTATO"
                        telefone_adicionado = True
                        break
                       

        telefones_atualizados = [df.at[i, c] for c in colunas_telefone]
        #print(f"Código: {codigo} | Tel1: {telefones_atualizados[0]} | Tel2: {telefones_atualizados[1]} | Tel3: {telefones_atualizados[2]}")

        # Salvar checkpoint a cada 1 linhas
        if i % 2 == 0:
            df.to_excel("complica_outubro_hap_base_incorreta_id.xlsx", index=False)
            #print(f"Checkpoint salvo na linha {i}")


        automacao_nome_next()  
        
    
    df.to_excel("complica_outubro_hap_base_incorreta_id.xlsx", index=False)
    #print("Salvamento final concluído.")





dados = "complica_outubro_hap_base_incorreta_id.xlsx"

automar_fuction(dados)



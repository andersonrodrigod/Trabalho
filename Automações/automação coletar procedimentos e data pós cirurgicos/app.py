import pandas as pd
import time
import pyautogui as py
import pyperclip

def formatar_ano(data_str):
    """
    Recebe 'DD/MM/AAAA' e retorna '%MM/AAAA'
    """
    dia, mes, ano = data_str.split("/")
    return f"%{ano}"

def ano_posterior(data_str):
    _, mes, ano = data_str.split("/")
    mes = int(mes)
    ano = int(ano)

    if mes == 12:
        ano += 1
    else:
        mes += 1

    return f"%{ano}"

def copy_vazio():
    pyperclip.copy("")

def automar_function(df):

    time.sleep(2)
    df["STATUS BOT"] = df["STATUS BOT"].fillna("").astype(str).str.strip()

    for idx, row in df[df["STATUS BOT"] == ""].head(5).iterrows():
        
        tempo_inicio = time.time()  # Marca o tempo de início
        copy_vazio()
        internacao = "I"
        codigo = str(row["COD USUARIO"]).strip()
        dt_internacao_str = str(row["DT INTERNACAO"]).strip()
        dt_internacao_dt = pd.to_datetime(dt_internacao_str, format="%d/%m/%Y")
        dt_internacao_atual = formatar_ano(dt_internacao_str)
        dt_internacao_posterior = ano_posterior(dt_internacao_str)
        senha_arquivo = str(row["SENHA"]).strip()

        pyperclip.copy(codigo)
        py.hotkey("ctrl", "v")
        time.sleep(0.5)

        copy_vazio()

        pyperclip.copy(dt_internacao_atual)
        py.click(118, 379)  
        time.sleep(0.5)
        py.hotkey("ctrl", "v")
        time.sleep(0.5)

        py.click(639, 424)
        time.sleep(0.5)
        pyperclip.copy(internacao)
        py.hotkey("ctrl", "v")
        time.sleep(0.5)

        py.press("f8")
        time.sleep(1)

        # Loop para encontrar a senha correta
        senha_encontrada = False
        max_tentativas = 50

        df.at[idx, "STATUS BOT"] = "VERIFICADO"

        for tentativa in range(max_tentativas):
            copy_vazio()
            # Copiar a senha do sistema
            py.hotkey("ctrl", "c")
            time.sleep(0.3)
            senha_sistema = pyperclip.paste().strip()
            
            # Se estiver vazio, pula para o próximo loop
            if not senha_sistema:
                print("  Clipboard vazio, pulando...")
                df.at[idx, "STATUS COLETA"] = "SEM INTERNACAO POS CIRURGICA"
                continue
            
            # Verificar se encontrou a senha
            if senha_sistema == senha_arquivo:
                print(f"✓ Senha encontrada: {senha_sistema}")
                senha_encontrada = True
                
                # Agora verifica os próximos até encontrar um diferente
                while True:
                    copy_vazio()
                    py.press("down")
                    time.sleep(0.3)
                    py.hotkey("ctrl", "c")
                    time.sleep(0.3)
                    senha_proxima = pyperclip.paste().strip()
                    
                    # Se estiver vazio, encerra o loop interno
                    if not senha_proxima:
                        print("  Clipboard vazio, finalizando verificação")
                        df.at[idx, "STATUS COLETA"] = "SEM INTERNACAO POS CIRURGICA"
                        break
                    
                    if senha_proxima != senha_arquivo:
                        copy_vazio()
                        print(f"✓ Encontrado registro diferente. Nova senha: {senha_proxima}")
                        py.click(407, 377)
                        time.sleep(0.5)
                        py.hotkey("ctrl", "c")
                        time.sleep(0.3)
                        dt_internacao_sistema = pyperclip.paste().strip()
                        print(f"  Data de internação do sistema: {dt_internacao_sistema}")
                        
                        # Se a data estiver vazia ou for menor/igual, continua o loop
                        if not dt_internacao_sistema:
                            print("  Data vazia, voltando ao loop...")
                            py.click(130, 161)
                            time.sleep(0.3)
                            continue
                        
                        dt_internacao_sistema = pd.to_datetime(dt_internacao_sistema, format="%d/%m/%Y")

                        if dt_internacao_sistema <= dt_internacao_dt:
                            print(f"  Data {dt_internacao_sistema.strftime('%d/%m/%Y')} <= {dt_internacao_dt.strftime('%d/%m/%Y')}, voltando ao loop...")
                            py.click(130, 161)
                            time.sleep(0.3)
                            continue

                        if dt_internacao_sistema > dt_internacao_dt:
                            copy_vazio()
                            print(f"✓ Data {dt_internacao_sistema.strftime('%d/%m/%Y')} > {dt_internacao_dt.strftime('%d/%m/%Y')}, prosseguindo...")

                            py.click(126, 243)
                            time.sleep(0.5)
                            py.hotkey("ctrl", "c")
                            codigo_procedimento = pyperclip.paste().strip()
                            print(f"  Código do procedimento: {codigo_procedimento}")
                            time.sleep(0.5)

                            py.click(268, 245)
                            time.sleep(0.5)
                            py.hotkey("ctrl", "c")
                            nome_procedimento = pyperclip.paste().strip()
                            print(f"  Nome do procedimento: {nome_procedimento}")
                            time.sleep(0.5)

                            df.at[idx, "COD PROCEDIMENTO"] = codigo_procedimento
                            df.at[idx, "PROCEDIMENTO"] = nome_procedimento
                            df.at[idx, "STATUS COLETA"] = "INTERNACAO POS CIRURGICA"
                            df.at[idx, "DATA DA REINTERNACAO"] = dt_internacao_sistema.strftime('%d/%m/%Y')
                            break
                        break
                    else:
                        print(f"  Ainda é a mesma senha, continuando...")
                break
            else:
                # Senha não encontrada, desce para o próximo
                print(f"  Senha diferente ({senha_sistema}), tentando próximo...")
                py.press("down")
                time.sleep(0.3)
        print("finalizando ")
        py.press("f7")
        time.sleep(0.5)
        py.click(365, 161)
        time.sleep(0.3)


        if not senha_encontrada:
            print(f"✗ Senha não encontrada após {max_tentativas} tentativas")

        tempo_decorrido = time.time() - tempo_inicio
        print(f"Iniciando automação para o código: {codigo}")
        print(f"Data original: {dt_internacao_str}")
        print(f"Internação atual: {dt_internacao_atual}")
        print(f"Internação posterior: {dt_internacao_posterior}")
        print(f"⏱️ Tempo de processamento: {tempo_decorrido:.2f} segundos")
        print("-" * 50)
        
        # Salvar o DataFrame atualizado no arquivo Excel após cada registro processado
        df.to_excel('NOVEMBRO_AUTOMACAO_INTERNACAO.xlsx', index=False)
        print("✓ Arquivo salvo com sucesso!")



# Exemplo de uso (descomente para testar)
df = pd.read_excel('NOVEMBRO_AUTOMACAO_INTERNACAO.xlsx')

automar_function(df)

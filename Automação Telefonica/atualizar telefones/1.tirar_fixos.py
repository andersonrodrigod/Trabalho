import pandas as pd
import re

# 1. Carregar a planilha
df = pd.read_excel("novembro.xlsx")

print("👋 Oi Rodrigo, carreguei a planilha e agora vou olhar cada telefone!")

# 2. Função para validar o telefone
def classificar_telefone(num):
    num_str = str(num)

    # Mantém só os números para analisar
    apenas_num = re.sub(r'\D', '', num_str)

    # Verifica se tem pelo menos 3 dígitos
    if len(apenas_num) < 3:
        return "Fixo"

    # Verifica se o 3º dígito é 9 (ou seja: XX9.....)
    if apenas_num[2] == "9":
        return num  # mantém o telefone original
    else:
        return "Fixo"

# 3. Aplicar a função na coluna TELEFONE
df["TELEFONE"] = df["TELEFONE"].apply(classificar_telefone)

print("✔️ Terminei! Todos os telefones que não tinham 9 depois dos dois primeiros dígitos viraram 'Fixo'.")

# 4. (Opcional) Salvar um novo arquivo
df.to_excel("novembro_tratado.xlsx", index=False)
print("📁 Arquivo salvo como novembro_tratado.xlsx")

import pandas as pd

# 1. Carregar a planilha
print("📄 Carregando a planilha novembro.xlsx...")
df = pd.read_excel("novembro.xlsx")

# 2. Conferir se a coluna existe
if "TELEFONE" not in df.columns:
    raise ValueError("A coluna 'TELEFONE' não existe no arquivo!")

print("🔍 Transformando todos os telefones em string...")
df["TELEFONE"] = df["TELEFONE"].astype(str)

# 3. Função para adicionar 55 caso não comece com 55
def ajustar_telefone(num):
    num = num.strip()           # tira espaços
    print(f"➡️ Telefone recebido: {num}")  # conversa do código com você

    # Se já começa com '55', só retorna
    if num.startswith("55"):
        print("   ✔ Já começa com 55, então não vou mexer.\n")
        return num
    
    # Caso contrário, coloca 55 na frente
    novo = "55" + num
    print(f"   ➕ Não começava com 55. Transformei em: {novo}\n")
    return novo

# 4. Aplicar a função
print("⚙️ Ajustando todos os telefones...")
df["TELEFONE"] = df["TELEFONE"].apply(ajustar_telefone)

# 5. Salvar arquivo final
df.to_excel("novembro_ajustado.xlsx", index=False)
print("💾 Arquivo salvo como 'novembro_ajustado.xlsx'!")

import pandas as pd

print("🔄 Carregando arquivos...")

# 1) Ler arquivos
df_resposta = pd.read_excel("RESPOSTA.xlsx")
df_complica = pd.read_excel("complica_outubro_hap.xlsx")

print("✔ Arquivos carregados!")

# 2) Transformar a coluna Nome em string para evitar erros
nomes_resposta = df_resposta["Nome"].dropna().astype(str)
nomes_complica = df_complica["Nome"].dropna().astype(str)

print("🔍 Verificando nomes iguais...")

# 3) Verificar quais nomes de complica aparecem na RESPOSTA
nomes_iguais = nomes_complica.isin(nomes_resposta)

# 4) Contar o total
total_iguais = nomes_iguais.sum()

print("\n📊 RESULTADO:")
print(f"👉 Total de nomes que aparecem nas duas planilhas: {total_iguais}")

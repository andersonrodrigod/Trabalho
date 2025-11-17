import pandas as pd
from collections import Counter
from itertools import islice
import re

# Nome do arquivo Excel
excel_file = 'dados.xlsx'  # Substitua pelo nome real do arquivo

# Ler a planilha
df = pd.read_excel(excel_file, engine='openpyxl')

# Verificar se a coluna 'palavra' existe
if 'palavra' not in df.columns:
    raise ValueError("A coluna 'palavra' não foi encontrada na planilha.")

# Lista de preposições e palavras comuns para ignorar
stopwords = {"de", "da", "do", "dos", "das", "e", "em", "a", "o", "as", "os", "por", "para", "com", "não foi", "não", "me", "dia", "no", "que", "fez", "tive"}

# Extrair todas as palavras da coluna 'palavra'
texto = ' '.join(df['palavra'].astype(str))

# Normalizar texto: remover pontuação e colocar em minúsculas
texto = re.sub(r'[^\w\s]', '', texto).lower()

# Tokenizar palavras
palavras = [p for p in texto.split() if p not in stopwords]

# Função para gerar n-gramas
def gerar_ngrams(lista, n):
    return zip(*(islice(lista, i, None) for i in range(n)))

# Gerar bigramas e trigramas
bigrams = [' '.join(bg) for bg in gerar_ngrams(palavras, 2)]
trigrams = [' '.join(tg) for tg in gerar_ngrams(palavras, 3)]

# Contar frequências
contagem_bigramas = Counter(bigrams)
contagem_trigramas = Counter(trigrams)

# Top 3 mais frequentes
top3_bigramas = contagem_bigramas.most_common(3)
top3_trigramas = contagem_trigramas.most_common(3)

# Exibir resultados
print("Top 3 Bigramas mais frequentes:")
for bg, freq in top3_bigramas:
    print(f"{bg}: {freq}")

print("\nTop 3 Trigramas mais frequentes:")
for tg, freq in top3_trigramas:
    print(f"{tg}: {freq}")
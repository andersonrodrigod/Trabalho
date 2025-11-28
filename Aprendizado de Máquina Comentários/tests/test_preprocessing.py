import pandas as pd
import re
from collections import Counter

arquivo = "tests/coluna_1_grupo.csv"

df = pd.read_csv(arquivo, sep=",")

# FILTRA SOMENTE O GRUPO RECEPÇÃO

#df = df[df["grupo"] == "RECEPÇAO"]
df_admin = df[df["grupo"] == "ADMINISTRATIVO"]

# Junta todos os comentários em um único texto
texto = " ".join(df_admin["comentario_p1"].astype(str).tolist())

# Remove pontuação (deixa só letras e espaços)
texto =  re.sub(r"[^\w\s]", "", texto)


# Lista de Exclusão
excluir = ['muito', 'estava', 'minha', 'tinha', 'muita', 'cheguei', 'falta', 'manha', 'fazer', 'mesmo', 'fiquei', 'depois', 'quando', 'chegar', 'horario', 'pessoas', 'relata', 'pouco', 'ninguem', 'chegada', 'ainda', 'ficar', 'sendo']

# Separa em palavras
palavras = texto.split()

contagem_filtrada = [p for p in palavras if len(p) > 4 and p not in excluir]

contagem = Counter(contagem_filtrada)

lista_palavra = []
for palavra, cont in contagem.most_common(30):
    lista_palavra.append(palavra)

print(lista_palavra)


lista_recepcao = ['recepcao', 'atendimento', 'demora', 'recepcionista', 'cirurgia', 'hospital', 'paciente', 'internacao', 'tempo', 'horas', 'espera', 'totem', 'atendida', 'esperando', 'entrada', 'demorou', 'informacoes', 'informacao', 'atencao', 'recepcionistas', 'demorado', 'procedimento', 'medico', 'jejum', 'atendentes', 'parto', 'atender', 'atendido', 'aguardando', 'emergencia']








import pandas as pd
import re
from collections import Counter

arquivo = "tests/contem_recepcao.csv"

df = pd.read_csv(arquivo, sep=",")

# FILTRA SOMENTE O GRUPO RECEPÇÃO

#df = df[df["grupo"] == "RECEPÇAO"]
df_admin = df[df["grupo"] == "ADMINISTRATIVO"]

#print(df_admin)

# Junta todos os comentários em um único texto
texto = " ".join(df_admin["comentario_p1"].astype(str).tolist())

# Remove pontuação (deixa só letras e espaços)
texto =  re.sub(r"[^\w\s]", "", texto)


# Lista de Exclusão
excluir = ['muito', 'estava', 'minha', 'tinha', 'muita', 'cheguei', 'falta', 'manha', 'fazer', 'mesmo', 'fiquei', 'depois', 'quando', 'chegar', 'horario', 'pessoas', 'relata', 'pouco', 'ninguem', 'chegada', 'ainda', 'ficar', 'sendo', 'disse', 'hapvida', 'todos', 'porem', 'noite', 'tambem', 'reclama', 'momento', 'estou', 'tenho', 'assim', 'filho', 'outra', 'nenhum', 'havia', 'antes', 'quase', 'feito', 'passei', 'sobre', 'pessimo', 'vezes', 'descaso', 'entao', 'realizar','foram', 'houve', 'desde', 'devido', 'passou', 'conseguir', 'nenhuma', 'poderia', 'apenas', 'durante', 'subir', 'somente', 'passar', 'pessoa', 'problema', 'outro', 'filha', 'porque', 'ficou', 'chegou','deveria', 'sempre', 'disponivel','voces', 'pronto' 'local',]

# Separa em palavras
palavras = texto.split()

contagem_filtrada = [p for p in palavras if len(p) > 4 and p not in excluir]

contagem = Counter(contagem_filtrada)

lista_palavra = []
for palavra, cont in contagem.most_common(50):
    lista_palavra.append(palavra)

print(lista_palavra)


lista_recepcao = ['recepcao', 'atendimento', 'demora', 'recepcionista', 'cirurgia', 'hospital', 'paciente', 'internacao', 'tempo', 'horas', 'espera', 'totem', 'atendida', 'esperando', 'entrada', 'demorou', 'informacoes', 'informacao', 'atencao', 'recepcionistas', 'demorado', 'procedimento', 'medico', 'jejum', 'atendentes', 'parto', 'atender', 'atendido', 'aguardando', 'emergencia', 'atendente', 'equipe', 'ficha', 'profissionais', 'funcionarios', 'aguardar', 'pacientes', 'quarto', 'medica', 'maqueiro', 'chegamos', 'local', 'cadeira', 'volta', 'gente', 'pessoal', 'super', 'marcada', 'frente', 'porteiro']



lista_administrativo = ['hospital', 'cirurgia', 'atendimento', 'demora', 'paciente', 'horas', 'quarto', 'internacao', 'leito', 'medico', 'recepcao', 'plano', 'tempo', 'pacientes', 'parto', 'equipe', 'espera', 'procedimento', 'emergencia', 'medica', 'esperando', 'atendida', 'demorou', 'exames', 'profissionais', 'cirurgico', 'medicacao', 'exame', 'enfermaria', 'aguardando', 'medicos', 'acompanhante', 'internada', 'cadeira', 'entrada', 'consulta', 'convenio', 'jejum', 'apartamento', 'observacao', 'informacoes', 'informacao', 'local', 'atendido', 'centro', 'funcionarios', 'saude', 'internado', 'atender', 'pronto']




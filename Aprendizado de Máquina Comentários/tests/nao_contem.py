import pandas as pd
import re
from collections import Counter

df = pd.read_csv("tests/contem_recepcao.csv", sep=",")

# Filtrar grupo especifico

df_administrativo = df[df["grupo"] == "ADMINISTRATIVO"]
df_recepcao = df[df["grupo"] == "RECEPÇAO"]

palavras_administrativo = " ".join(df_administrativo["comentario_p1"].astype(str).tolist())
palavras_recepcao = " ".join(df_recepcao["comentario_p1"].astype(str).tolist())

texto_administrativo =  re.sub(r"[^\w\s]", "", palavras_administrativo)
texto_recepcao =  re.sub(r"[^\w\s]", "", palavras_recepcao)

palavras_administrativo = texto_administrativo.split()
palavras_recepcao = texto_recepcao.split()

excluir = ['muito', 'estava', 'minha', 'tinha', 'muita', 'cheguei', 'falta', 'manha', 'fazer', 'mesmo', 'fiquei', 'depois', 'quando', 'chegar', 'horario', 'pessoas', 'relata', 'pouco', 'ninguem', 'chegada', 'ainda', 'ficar', 'sendo', 'disse', 'hapvida', 'todos', 'porem', 'noite', 'tambem', 'reclama', 'momento', 'estou', 'tenho', 'assim', 'filho', 'outra', 'nenhum', 'havia', 'antes', 'quase', 'feito', 'passei', 'sobre', 'pessimo', 'vezes', 'descaso', 'entao', 'realizar','foram', 'houve', 'desde', 'devido', 'passou', 'conseguir', 'nenhuma', 'poderia', 'apenas', 'durante', 'subir', 'somente', 'passar', 'pessoa', 'problema', 'outro', 'filha', 'porque', 'ficou', 'chegou','deveria', 'sempre', 'disponivel','voces', 'pronto' 'local']

palavras_administrativo_filtradas = [p for p in palavras_administrativo if len(p) > 4 and p not in excluir]
palavras_recepcao_filtradas = [p for p in palavras_recepcao if len(p) > 4 and p not in excluir]

cont_administrativo = Counter(palavras_administrativo_filtradas)
cont_recepcao = Counter(palavras_recepcao_filtradas)
print(cont_administrativo)

so_no_administrativo = set(cont_administrativo.keys()) - set(cont_recepcao.keys())
so_no_recepcao = set(cont_recepcao.keys()) - set(cont_administrativo.keys())

resultados_so_no_administrativo = {palavra: cont_administrativo[palavra] for palavra in so_no_administrativo}
resultados_so_no_recepcao = {palavra: cont_recepcao[palavra] for palavra in so_no_recepcao}


lista_palavras_so_no_administrativo = []
for palavra, cont in Counter(resultados_so_no_administrativo).most_common(50):
    lista_palavras_so_no_administrativo.append(palavra)

lista_pavras_so_no_recepcao = []
for palavra, cont in Counter(resultados_so_no_recepcao).most_common(50):
    lista_pavras_so_no_recepcao.append(palavra)

#print(lista_palavras_so_no_administrativo)
#print(lista_pavras_so_no_recepcao)

lista_palavras_so_no_administrativo = ['infeccao', 'leite', 'contar', 'feira', 'elogia', 'particular', 'consigo', 'faleceu', 'material', 'leitos', 'pneumonia', 'longe', 'comida', 'tomografia', 'ortopedista', 'biopsia', 'negligencia', 'gracas', 'fisioterapia', 'administracao', 'relatei', 'coracao', 'hospitais', 'julho', 'ouvidoria', 'obstetra', 'inducao', 'protocolo', 'conforto', 'anterior', 'conseguiu', 'visitas', 'anestesia', 'dormir', 'operar', 'dificuldades', 'visivel', 'justica', 'tenha', 'medicacoes', 'pesquisa', 'acomodar', 'triste', 'prestado', 'acionar', 'atraves', 'hospitalar', 'sexta', 'pudesse', 'comecei']

lista_pavras_so_no_recepcao = ['gentil', 'grosseira', 'preferencial', 'simpatica', 'obstetrica', 'olham', 'amigos', 'arrogante', 'vazando', 'orientando', 'preencher', 'terminarem', 'carteirinha', 'cadastrar', 'realizando', 'explicacao', 'indiferentes', 'cordiais', 'rindo', 'senso', 'autoatendimento', 'adultos', 'dirigi', 'lorenzo', 'grosseria', 'profissionalismo', 'retornando', 'leigas', 'devolveram', 'respondidas', 'mangueira', 'recepcoes', 'nariz', 'emcaminha', 'atenta', 'houveram', 'antipatica', 'informei', 'histeroscopia', 'litrotripsia', 'obrigacao', 'desmaiei', 'atente', 'atrasa', 'queridos', 'dedicar', 'escutava', 'rispidos', 'hostis', 'digitar']
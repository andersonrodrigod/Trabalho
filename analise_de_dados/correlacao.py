import pandas as pd

# --- 1️⃣ Ler a planilha ---
arquivo = "dados_a.xlsx"  # substitua pelo seu arquivo
df = pd.read_excel(arquivo)

# --- 2️⃣ Mapear as escalas para números ---
quantidade_map = {
    "Nenhuma - 1": 1,
    "Alguma - 2": 2,
    "Alguma - 3": 3,
    "Muita - 4": 4,
    "Muita - 5": 5
}

concordancia_map = {
    "Discordo totalmente": 1,
    "Discordo parcialmente": 2,
    "Discordo": 3,
    "Nem concordo, nem discordo": 4,
    "Concordo parcialmente": 5,
    "Concordo": 6,
    "Concordo totalmente": 7
}


frequencia_map = {
    "Nunca ou quase nunca": 1,
    "Muito poucas vezes": 2,
    "Poucas vezes": 3,
    "Algumas vezes": 4,
    "Por vezes": 5,
    "Muitas vezes": 6,
    "Sempre ou quase sempre": 7
}

# --- 3️⃣ Colunas que serão transformadas ---
colunas_quantidade = [
    "quanto de oportunidade você tem em seu trabalho: o trabalho desafiador (multiple)",
    "quanto de oportunidade você tem em seu trabalho: oportunidade de obter novas habilidades e conhecimentos (multiple)",
    "quanto de acesso á informação você tem em seu trabalho: sobre a condição atual do seu setor de trabalho (multiple)",
    "quanto de oportunidade você tem em seu trabalho: tarefas que requerem todas as minhas habilidades e conhecimentos (multiple)",
    "quanto de acesso á informação você tem em seu trabalho: sobre os valores da administração do seu setor de trabalho (multiple)",
    "quanto de acesso á informação você tem em seu trabalho: os objetivos da administração do seu setor de trabalho (multiple)",
    "quanto de suporte você tem no seu trabalho: comentário específicos sobre o que você faz bem (multiple)",
    "quanto de suporte você tem em seu trabalho: comentários específicos sobre o que você poderia melhorar (multiple)",
    "quanto de suporte você tem em seu trabalho: dicas úteis ou conselhos para resolução de problemas (multiple)",
    "quanto de acesso a recursos você tem em seu trabalho: tempo disponível para realizar o trabalho burocrático (multiple)",
    "quanto de acesso a recursos você tem em seu trabalho: tempo disponível para cumprir as exigências do trabalho (multiple)",
    "quanto de acesso a recursos você tem em seu trabalho: obtenção de ajuda temporária quando necessário (multiple)",
    "em relação as recompensas por inovação no trabalho são? (multiple)",
    "a flexibilidade em meu trabalho é? (multiple)",
    "a visibilidade das minhas atividades no trabalho dentro da instituição é? (multiple)",
    "há oportunidades para você realizar estas atividades em seu trabalho: participar com médicos no cuidado ao paciente (multiple)",
    "há oportunidades para você realizar estas oportunidades em seu trabalho: ser procurado por seus pares para auxiliar a resolver problemas (multiple)",
    "há oportunidades para você realizar estas atividades em seu trabalho: ser procurado por administradores para auxiliar nos problemas (multiple)",
    "há oportunidades para você realizar estas atividades em seu trabalho: buscar ideias de outros profissionais além de médicos (ex.: fisioterapeutas, terapeutas ocupacionais, nutricionistas) (multiple)",
    "empoderamento global: em geral, o ambiente de trabalho me empodera para realizar meu trabalho de forma eficaz (multiple)",
    "empoderamento global: em geral, considero meu local de trabalho um ambiente de empoderamento (multiple)"

]

colunas_concordancia = [
    "eu estou confiante quanto a minha capacidade de fazer o meu trabalho? (multiple)",
    "o trabalho que eu faço é importante pra mim? (multiple)",
    "eu tenho significativa autonomia para decidir como faço o meu trabalho? (multiple)",
    "o impacto que eu exerço sobre o que acontece no meu setor é relevante? (multiple)",
    "minhas atividades de trabalho são particularmente gratificantes para mim? (multiple)",
    "eu tenho grande controle sobre o que acontece no meu setor? (multiple)",
    "eu posso tomar as minhas próprias decisões de como fazer o meu trabalho? (multiple)",
    "eu tenho considerável oportunidade para fazer meu trabalho com independência e liberdade? (multiple)",
    "eu tenho domínio das habilidades necessárias para o meu trabalho? (multiple)",
    "o trabalho que faço é significativo para mim? (multiple)",
    "eu estou seguro quanto a minha capacidade para realizar minhas atividades de trabalho? (multiple)",
    "eu exerço significativa influência sobre o que acontecer em meu setor? (multiple)"

]

coluna_vezes = [
    "no meu trabalho sinto-me cheio(a) de energia? (multiple)",
    "estou entusiasmado (a) com o meu trabalho? (multiple)",
    "sinto-me feliz quando estou a trabalhar imensamente? (multiple)",
    "sinto-me enérgico(a) e com vigor quando estou a trabalhar? (multiple)",
    "estou imerso no meu trabalho? (multiple)",
    "o meu trabalho inspira-me? (multiple)",
    "quando acordo de manhã, sinto-me bem por ir trabalhar? (multiple)",
    "estou orgulhoso(a) do meu trabalho? (multiple)",
    '"deixo-me levar" quando estou no trabalho? (multiple)'

]

# --- 3️⃣ Transformar valores para números ---
for col in colunas_quantidade:
    df[col] = df[col].map(quantidade_map)

for col in colunas_concordancia:
    df[col] = df[col].map(concordancia_map)

for col in coluna_vezes:
    df[col + "_num"] = df[col].map(frequencia_map)

# --- 4️⃣ Preparar lista com todas as colunas numéricas ---
colunas_todas = colunas_quantidade + colunas_concordancia + [col + "_num" for col in coluna_vezes]

# --- 5️⃣ Filtrar por estado e coletar correlações ---
limite = 0.7
estados = df["qual estado você reside? (input)"].dropna().unique()

# lista para armazenar todas as correlações fortes
todos_resultados = []

for estado in estados:
    df_estado = df[df["qual estado você reside? (input)"] == estado]
    correlacao = df_estado[colunas_todas].corr()
    
    # pegar apenas correlações fortes (>= limite) e < 1.0
    correlacoes_altas = correlacao[(correlacao.abs() >= limite) & (correlacao.abs() < 1.0)]
    correlacoes_altas = correlacoes_altas.dropna(how="all", axis=0).dropna(how="all", axis=1)
    
    if not correlacoes_altas.empty:
        # percorrer linhas e colunas da matriz para criar registros
        for linha in correlacoes_altas.index:
            for coluna in correlacoes_altas.columns:
                valor = correlacoes_altas.loc[linha, coluna]
                if pd.notna(valor):
                    todos_resultados.append({
                        "Estado": estado,
                        "Pergunta 1": linha,
                        "Pergunta 2": coluna,
                        "Correlação": valor
                    })

# --- 6️⃣ Criar DataFrame final e salvar em Excel ---
df_resultados = pd.DataFrame(todos_resultados)

# salva em Excel
df_resultados.to_excel("correlacoes_por_estado.xlsx", index=False)

print("Arquivo 'correlacoes_por_estado.xlsx' criado com sucesso!")
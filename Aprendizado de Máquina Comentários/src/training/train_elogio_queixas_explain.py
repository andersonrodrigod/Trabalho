# Manipulação de dados em DataFrame
import pandas as pd

# Manipulação segura de caminhos de arquivos
from pathlib import Path

# Divide dados em treino e teste
from sklearn.model_selection import train_test_split

# Converte texto em números (TF-IDF)
from sklearn.feature_extraction.text import TfidfVectorizer

# Modelo linear para classificação binária
from sklearn.linear_model import LogisticRegression

# Relatório de métricas do modelo
from sklearn.metrics import classification_report

# Serialização eficiente de objetos Python
import joblib


# Caminho do dataset final já processado
DATASET_PATH = "data/processed/comentarios_processados_full.csv"

# Diretório onde o modelo será salvo
MODEL_DIR = Path("models/elogio_queixa")

# Junta diretório + arquivo (Path usa / como join)
MODEL_PATH = MODEL_DIR / "elogio_queixa.pkl"  # join de caminhos

# Semente fixa para reprodutibilidade
RANDOM_STATE = 42

# Remove comentários muito curtos (ruído)
MIN_TEXTO_LEN = 5


# Carrega o dataset a partir de um CSV
def load_data(path):
    df = pd.read_csv(path)
    return df


# Limpa, valida e normaliza o dataset
def prepare_dataset(df):
    # Evita alterar o DataFrame original
    df = df.copy()

    # Remove linhas sem rótulo ou comentário
    df = df.dropna(subset=["elogio_ou_queixa", "comentario"])

    # Garante texto como string e sem espaços inúteis
    df["comentario"] = df["comentario"].astype(str).str.strip()

    # Mantém apenas comentários com tamanho mínimo
    df = df[df["comentario"].str.len() >= MIN_TEXTO_LEN]

    # Normaliza rótulos para evitar duplicidade semântica
    df["elogio_ou_queixa"] = (
        df["elogio_ou_queixa"]
        .str.upper()
        .str.replace(" ", "_")
    )

    return df


# Separa entrada (texto) e saída (rótulo)
def split_features_labels(df):
    # Texto que o modelo vai ler
    X = df["comentario"]

    # Rótulo correto (elogio ou queixa)
    y = df["elogio_ou_queixa"]

    return X, y


# Treina o modelo e avalia desempenho
def train_model(X, y):

    # Divide dados mantendo proporção das classes
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=y
    )

    # Vetorizador TF-IDF com unigramas e bigramas
    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2)
    )

    # Aprende vocabulário e transforma texto de treino
    X_train_vec = vectorizer.fit_transform(X_train)

    # Apenas transforma texto de teste (sem aprender)
    X_test_vec = vectorizer.transform(X_test)

    # Modelo linear para classificação de texto
    model = LogisticRegression(max_iter=1000)

    # Ajusta pesos com base nos dados de treino
    model.fit(X_train_vec, y_train)

    # Predição do modelo nos dados nunca vistos
    y_pred = model.predict(X_test_vec)

    # Mostra métricas de avaliação do modelo
    print(classification_report(y_test, y_pred))

    return model, vectorizer


# Salva modelo treinado e vetorizador
def save_model(model, vectorizer, path):

    # Cria diretórios caso não existam
    path.parent.mkdir(parents=True, exist_ok=True)

    # Salva modelo + vectorizer juntos
    joblib.dump(                       # serialização
        {"model": model, "vectorizer": vectorizer},
        path
    )


# Orquestra o fluxo completo de treino
def main():
    # Carrega dados do disco
    df = load_data(DATASET_PATH)

    # Prepara e limpa o dataset
    df = prepare_dataset(df)

    # Separa texto e rótulo
    X, y = split_features_labels(df)

    # Treina modelo e vetorizador
    model, vectorizer = train_model(X, y)

    # Persiste o modelo treinado
    save_model(model, vectorizer, MODEL_PATH)


# Executa o pipeline apenas se rodar este arquivo
if __name__ == "__main__":
    main()





"""

📘 Relatório explicativo do pipeline de classificação de comentários
(elogio vs queixa – NLP clássico com ML supervisionado)

Este código implementa um pipeline completo de Machine Learning para classificação de texto, com o objetivo de identificar automaticamente se um comentário escrito por um cliente representa um elogio ou uma queixa.

O pipeline foi construído de forma intencionalmente explícita, priorizando clareza conceitual, controle do fluxo e evitar erros silenciosos, mesmo que isso custe mais linhas de código.

A ideia central não é apenas “treinar um modelo”, mas criar um processo reproduzível, compreensível e confiável.

1️⃣ Visão geral do que o código faz

Em alto nível, o código executa as seguintes etapas:

Carrega um dataset já previamente processado

Limpa e valida os dados textuais e os rótulos

Separa texto (entrada) e rótulo (resposta correta)

Divide os dados em treino e teste

Converte texto em representação numérica (TF-IDF)

Treina um modelo de classificação (Logistic Regression)

Avalia o modelo de forma honesta

Salva o modelo treinado junto com o tradutor de texto

Cada uma dessas etapas existe para evitar um tipo específico de erro conceitual, muitos deles comuns em projetos de ML.

2️⃣ Por que dividir dados em treino e teste

Um dos pontos centrais do código é a separação entre dados de treino e dados de teste.

O modelo é treinado apenas com uma parte dos dados (80%) e avaliado com dados que ele nunca viu (20%).
Isso existe para evitar o problema clássico de overfitting, também chamado informalmente de o modelo “decorar” os dados.

Sem essa divisão, o modelo poderia simplesmente memorizar frases específicas e aparentar ter uma performance excelente — quando, na prática, não teria aprendido padrões gerais, apenas exemplos pontuais.

O uso de stratify=y garante que a proporção entre elogios e queixas seja mantida tanto no treino quanto no teste.
Isso evita avaliações distorcidas em datasets desbalanceados.

3️⃣ Por que texto precisa virar número

Modelos de Machine Learning não entendem linguagem natural.
Eles operam exclusivamente sobre números, vetores e operações matemáticas.

Por isso, o texto dos comentários precisa ser traduzido para uma forma numérica.
Essa tradução é feita pelo TfidfVectorizer.

O TF-IDF transforma cada comentário em um vetor numérico, onde:

cada posição representa uma palavra (ou conjunto de palavras)

o valor representa a importância daquela palavra naquele texto

Essa etapa não classifica nada.
Ela apenas cria uma ponte entre linguagem humana e matemática.

4️⃣ Por que TF-IDF usa 1-gram e 2-gram

O uso de ngram_range=(1, 2) significa que o modelo considera:

palavras isoladas (unigramas)

pares de palavras (bigramas)

Isso é fundamental para capturar contexto.

Por exemplo:

a palavra “demora” isolada já carrega sentido negativo

mas a expressão “demora no atendimento” é ainda mais informativa

Usar 3-gramas (triplas de palavras) foi evitado porque:

os textos são curtos

triplas tendem a aparecer poucas vezes

isso gera ruído e piora a generalização

5️⃣ Por que existe um limite de 5000 features

O parâmetro max_features=5000 define o tamanho máximo do vocabulário que o modelo pode usar.

Mais features:

aumentam a complexidade

aumentam risco de overfitting

consomem mais memória

Menos features:

simplificam o modelo

podem perder nuances importantes

O valor 5000 é um equilíbrio prático, especialmente adequado para:

datasets de texto de tamanho médio

modelos lineares como Logistic Regression

Importante: aumentar esse número não garante melhora de performance.
Muitas vezes, piora.

6️⃣ Por que o teste não “aprende” nada

Um ponto crítico do código é a diferença entre:

fit_transform(X_train)
transform(X_test)


O vetor de treino:

aprende o vocabulário

cria a matriz numérica

O vetor de teste:

usa exatamente o mesmo vocabulário

não aprende palavras novas

Isso evita vazamento de informação, que tornaria a avaliação irreal.
Se o teste ensinasse algo ao modelo, o resultado seria enganoso.

7️⃣ O papel do modelo de classificação

O LogisticRegression é o algoritmo responsável pela decisão final.

Ele não entende texto, apenas os vetores gerados pelo TF-IDF.

Durante o treinamento, o modelo:

ajusta pesos matemáticos

aprende quais palavras puxam para elogio

e quais puxam para queixa

Esses pesos representam tendências estatísticas, não regras fixas.

Esse modelo foi escolhido porque:

é simples

rápido

interpretável

funciona muito bem com dados TF-IDF

Ele serve como baseline sólido, capaz de mostrar se o problema é resolvível.

8️⃣ O significado das métricas de avaliação

O modelo é avaliado com:

Precision: quando o modelo diz “elogio”, ele acerta?

Recall: de todos os elogios reais, quantos ele encontrou?

F1-score: equilíbrio entre os dois

O F1-score é o mais confiável porque:

impede que o modelo “trapaceie”

penaliza modelos desequilibrados

Valores típicos:

acima de 0.75 → bom

entre 0.6 e 0.75 → aceitável

abaixo disso → problema estrutural

Sempre interpretado no contexto do problema.

9️⃣ Por que salvar modelo e vectorizer juntos

O modelo treinado não funciona sozinho.

O fluxo completo sempre é:

texto novo
→ vectorizer
→ vetor numérico
→ modelo
→ previsão


Se o vectorizer não for salvo:

o modelo não consegue interpretar texto novo

o pipeline quebra

Por isso, ambos são serializados juntos usando joblib.

🔟 Por que o código é estruturado em funções

Cada função existe para:

isolar responsabilidade

facilitar testes

permitir reaproveitamento

evitar efeitos colaterais

O main() atua como orquestrador, deixando o fluxo explícito.

O bloco if __name__ == "__main__" garante que:

o pipeline só execute quando o arquivo for rodado diretamente

o código possa ser importado sem treinar o modelo de novo

🧠 Conclusão final

Este código não é apenas um script de Machine Learning.
Ele é a materialização de um raciocínio completo sobre:

generalização vs memorização

simplicidade vs complexidade

clareza vs atalhos perigosos

As dúvidas levantadas ao longo do processo — sobre F1-score, n-grams, vocabulário, vetorização, split e salvamento — não foram periféricas.
Elas tocam o núcleo do Machine Learning aplicado a texto.

Se você voltou aqui no futuro e entendeu este texto, então:

o conhecimento não se perdeu, apenas ficou em repouso.

Este pipeline é uma base sólida.
Tudo que vier depois será evolução, não correção.


"""



























"""
📘 Relatório de leitura —
Interpretação de accuracy, macro avg e weighted avg
(para datasets desbalanceados)

Este relatório existe para resolver uma confusão clássica e recorrente em Machine Learning:
por que números “bons” no relatório nem sempre significam um modelo bom.

Ele deve ser lido com calma, não como estudo ativo, mas como lembrança conceitual.

1️⃣ O problema central: dados desbalanceados

Quando um dataset possui uma classe muito maior que as outras, ocorre o chamado desbalanceamento.

No caso analisado:

A classe QUEIXA representa quase todo o dataset

As classes ELOGIO e ELOGIO_QUEIXA são raras

Isso cria um cenário onde:

“A forma mais fácil de acertar muito é prever sempre a classe maior.”

Esse fato estatístico contamina a leitura das métricas.

2️⃣ O que é accuracy e por que ela engana

Accuracy mede apenas:

quantas previsões o modelo acertou no total

Ela não diferencia classes.

Em datasets balanceados, isso funciona bem.
Em datasets desbalanceados, não.

No seu caso, um modelo que previsse tudo como QUEIXA já teria uma accuracy muito alta, mesmo sendo inútil para elogios.

Portanto:

Accuracy alta não significa modelo inteligente.
Significa apenas que ele acertou o que aparece mais.

3️⃣ O que é macro avg e por que ela importa

Macro average calcula as métricas:

uma vez para cada classe

depois tira a média simples

Cada classe vale exatamente o mesmo, mesmo que:

uma tenha milhares de exemplos

outra tenha apenas dezenas

Isso responde à pergunta:

“Se eu tratar todas as classes como igualmente importantes,
o quão bom é meu modelo?”

No seu caso, o macro F1 é baixo porque:

o modelo vai muito bem em QUEIXA

vai mal em ELOGIO

praticamente ignora ELOGIO_QUEIXA

A macro avg não permite esconder esse fato.

Por isso ela é a métrica mais honesta para avaliar:

equilíbrio

justiça entre classes

falhas estruturais

4️⃣ O que é weighted avg e por que ela pode enganar

Weighted average calcula as métricas por classe,
mas pondera pelo número de exemplos de cada classe.

Ou seja:

classes grandes pesam muito

classes pequenas quase não influenciam

Isso responde à pergunta:

“Se eu me importar mais com o que acontece com mais frequência,
o modelo é bom?”

No seu caso, como QUEIXA domina o dataset:

o weighted avg fica muito alto

mesmo com desempenho ruim nas classes raras

Esse número não é falso, mas é perigoso se interpretado fora de contexto.

5️⃣ Como ler o relatório corretamente (regra prática)

Sempre leia nessa ordem:

Support → para entender o tamanho das classes

Macro avg → para avaliar equilíbrio real

Métricas por classe → para entender onde falha

Weighted avg → apenas se fizer sentido no negócio

Accuracy → por último, com desconfiança

Nunca comece pela accuracy.

6️⃣ O que esses números dizem sobre o seu modelo

Eles dizem que:

O modelo é muito bom em identificar QUEIXAS

Ele é conservador ao identificar ELOGIOS

Ele praticamente ignora ELOGIO_QUEIXA

Isso não é bug

É uma consequência direta da distribuição dos dados

O modelo não está errado.
Ele está otimizando estatisticamente.

7️⃣ O ponto mais importante para guardar

Métricas não são verdades absolutas.
Elas respondem perguntas diferentes.

Accuracy responde: “acertou muito?”

Macro avg responde: “foi justo?”

Weighted avg responde: “foi eficiente no comum?”

Nenhuma delas é “a certa” sozinha.

8️⃣ Por que essa parte cansa tanto

Porque aqui você precisa:

abandonar intuição simples

aceitar que matemática otimiza o que é mais frequente

separar avaliação técnica de decisão estratégica

Esse é o ponto onde Machine Learning deixa de ser código
e vira análise crítica.

O cansaço que você sentiu é sinal de aprendizado real.

🧠 Conclusão final

Se você voltar aqui no futuro e estiver confuso, lembre:

Se o dataset é desbalanceado,
accuracy e weighted avg quase sempre mentem por omissão.

O número que revela o problema é o macro avg,
e o verdadeiro diagnóstico vem do support + métricas por classe.

Leia esse relatório devagar.
Ele não é para decorar — é para reancorar o entendimento.

Quando quiser seguir adiante, o próximo passo não é técnico,
é decidir o que realmente importa classificar.



"""
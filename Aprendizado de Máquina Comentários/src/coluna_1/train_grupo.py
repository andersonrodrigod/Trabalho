import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.calibration import CalibratedClassifierCV

from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV


df = pd.read_csv("data/processed/coluna_1_grupo.csv", sep=",")

df = df[df["grupo"].isin(["RECEPÇAO", "ADMINISTRATIVO"])]

x = df["comentario_p1"]
y = df["grupo"]

vectorizer = TfidfVectorizer(max_features=1000)
x_tfidf = vectorizer.fit_transform(x)

x_train, x_test, y_train, y_test = train_test_split(
    x_tfidf,
    y,
    test_size=0.3,
    random_state=42
)

modelolr = LogisticRegression(
    class_weight="balanced",
    max_iter=1000
)

modelolr.fit(x_train, y_train)

y_predlr = modelolr.predict(x_test)

print(accuracy_score(y_test, y_predlr))
print(confusion_matrix(y_test, y_predlr))  
print(classification_report(y_test, y_predlr))


































"""

X_train_texts, X_test_texts, y_train, y_test = train_test_split(
    x,  # nossos dados numéricos
    y,         # rótulos
    test_size=0.3,  # 30% dos dados vão para teste
    random_state=42,  # garante que a divisão seja sempre igual
    stratify=y # garante que a proporção de rótulos seja mantida
)

vectorize = TfidfVectorizer(max_features=1000)
X_train = vectorize.fit_transform(X_train_texts)
Xtest = vectorize.transform(X_test_texts)



# ------------------- modelo Naive Bayes 2 -------------------

nb = MultinomialNB()
calibrated_nb = CalibratedClassifierCV(nb, cv=5)
calibrated_nb.fit(X_train, y_train)

probs = calibrated_nb.predict_proba(Xtest)
preds = calibrated_nb.predict(Xtest)


palavras_adm = [
    'recepcao', 'hospital', 'atendimento', 'cirurgia',
    'internacao', 'quarto', 'recepcionista', 'equipe',
    'medica', 'atendida', 'plano', 'medico', 'cirurgico', 'aguardando',
    'demora', 'leito', 'parto', 'internamento', 'esperando',
    'procedimento', 'porteiro', 'acompanhante', 'profissionais',
    'entrada', 'medicos'
]

padroes_adm = [
    ("recepcao", "hospital"),
    ("atendimento", "hospital"),
    ("internacao", "hospital"),
    ("recepcionista", "atendimento"),
    ("recepcao", "cirurgia"),
    ("recepcao", "quarto"),
    ("hospital", "hospital"),
    ("profissionais", "cirurgia")
]

def score_adm(texto):
    score = 0

    for p in palavras_adm:
        if p in texto:
            score += 2
    

    for p1, p2 in padroes_adm:
        if p1 in texto and p2 in texto:
            score += 10

    return score

idx_administrativo = list(calibrated_nb.classes_).index("ADMINISTRATIVO")

threshold = 0.90
new_preds = []

for texto, prob, pred in zip(X_test_texts, probs, preds):

    score = score_adm(texto)
    bonus = score * 0.03 # +3% por ponto

    # SOMA direto na prob de ADMINISTRATIVO
    prob[idx_administrativo] = min(1.0, prob[idx_administrativo] + bonus)

    # escolhe a classe com maior probabilidade
    melhor_classe = calibrated_nb.classes_[np.argmax(prob)]

    new_preds.append(melhor_classe)


    if prob.max() < threshold:
        new_preds.append("OUTROS")
    else:
        new_preds.append(pred)


new_preds = np.array(new_preds)

<<<<<<< HEAD
print(threshold)
print(accuracy_score(y_test, new_preds))
print(confusion_matrix(y_test, new_preds))
print(classification_report(y_test, new_preds))
=======

print(threshold)
print(accuracy_score(y_test, new_preds))
print(confusion_matrix(y_test, new_preds))
print(classification_report(y_test, new_preds))
"""
>>>>>>> 18d59986d82724942466cd73a1a4f7aa3e353587

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

vectorize = TfidfVectorizer(max_features=1000)
x_tfidf = vectorize.fit_transform(x)

X_train, Xtest, y_train, y_test = train_test_split(
    x_tfidf,  # nossos dados numéricos
    y,         # rótulos
    test_size=0.3,  # 30% dos dados vão para teste
    random_state=42,  # garante que a divisão seja sempre igual
    stratify=y # garante que a proporção de rótulos seja mantida
)


# ------------------- modelo Naive Bayes 2 -------------------

nb = MultinomialNB()
calibrated_nb = CalibratedClassifierCV(nb, cv=5)
calibrated_nb.fit(X_train, y_train)

probs = calibrated_nb.predict_proba(Xtest)
preds = calibrated_nb.predict(Xtest)

threshold = 0.80
new_preds = []

for prob, pred in zip(probs, preds):
    if prob.max() < threshold:
        new_preds.append("OUTROS")
    else:
        new_preds.append(pred)

new_preds = np.array(new_preds)

print(threshold)
print(accuracy_score(y_test, new_preds))
print(confusion_matrix(y_test, new_preds))
print(classification_report(y_test, new_preds))
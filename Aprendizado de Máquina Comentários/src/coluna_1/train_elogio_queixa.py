import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import SVC 
import numpy as np
import joblib

df = pd.read_csv("data/processed/coluna_1_teste.csv")

x = df["comentario_p1"]
y = df["elogio_ou_queixa"]

vectorizer = TfidfVectorizer(max_features=1000) # considera as 1000 palavras mais importantes
x_tfidf = vectorizer.fit_transform(x) # transforma o texto em números

X_train, X_test, y_train, y_test = train_test_split(
    x_tfidf,    # nossos dados numéricos
    y,          # rótulos
    test_size=0.3, # 30% dos dados vão para teste
    random_state=42 # garante que a divisão seja sempre igual
)



# ------------------- modelo Naive Bayes 2 -------------------

nb = MultinomialNB()
calibrated_nb = CalibratedClassifierCV(nb, cv=5)
calibrated_nb.fit(X_train, y_train)

probs = calibrated_nb.predict_proba(X_test)
preds = calibrated_nb.predict(X_test)

threshold = 0.60
new_preds = []

for prob, pred in zip(probs, preds):
    if prob.max() < threshold:
        new_preds.append("OUTROS")
    else:
        new_preds.append(pred)

new_preds = np.array(new_preds)

print(threshold)
print(confusion_matrix(y_test, new_preds))
print(classification_report(y_test, new_preds))

joblib.dump(calibrated_nb, "models/coluna_1_nb.pkl") # salva o modelo treinado
joblib.dump(vectorizer, "models/coluna_1_vectorizer.pkl") # salva o vetorizer




# ------------------- modelo Naive Bayes -------------------

modelonb = MultinomialNB() # cria o modelo Naive Bayes multinomial

modelonb.fit(X_train, y_train)  # treina o modelo com os dados de treino

y_prednb = modelonb.predict(X_test) # Previsão nos dados de teste


acuracianb = accuracy_score(y_test, y_prednb) # Avalia a acurácia
confusion_matrix_nb = confusion_matrix(y_test, y_prednb) # Matriz de confusão
classification_report_nb = classification_report(y_test, y_prednb) # Relatório de classificação

"""print("Número de classes que o modelo conhece:", modelonb.classes_)
print(acuracianb) # vericar a precisão do modelo

print(confusion_matrix(y_test, y_prednb)) # verificar matriz de confusão

print(classification_report(y_test, y_prednb)) # verificar relatório de classificação"""


"""print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)
print("y_train distribution:\n", y_train.value_counts())
print("y_test distribution:\n", y_test.value_counts())"""


# ---------------------- modelo SVM ----------------------

# SVM com probabilidade calibrada
svm = LinearSVC()
calibrated_svm = CalibratedClassifierCV(svm, cv=5)

calibrated_svm.fit(X_train, y_train)

# Probabilidades
probs = calibrated_svm.predict_proba(X_test)

# Predição normal
preds = calibrated_svm.predict(X_test)

# AQUI você escolhe o threshold
threshold = 0.95   # ajuste conforme quiser

new_preds = []
for prob, pred in zip(probs, preds):
    if prob.max() < threshold:
        new_preds.append("OUTROS")   # modelo não teve certeza
    else:
        new_preds.append(pred)

new_preds = np.array(new_preds)

"""print("Acurácia:", accuracy_score(y_test, new_preds))
print("\nMatriz de confusão:\n", confusion_matrix(y_test, new_preds))
print("\nRelatório de classificação:\n", classification_report(y_test, new_preds))
"""

# ---------------------- modelo de regressão logística ----------------------

# cria o modelo com class_weight balanced
modelolr = LogisticRegression(
    class_weight="balanced", # ajusta o peso das classes para lidar com desbalanceamento
    max_iter=1000 # número máximo de iterações para o otimizador
)

modelolr.fit(X_train, y_train) # treina o modelo com os dados de treino
y_predlr = modelolr.predict(X_test) # faz previsões nos dados de teste

acuracialr = accuracy_score(y_test, y_predlr) # Avalia a acurácia
confusion_matrix_lr = confusion_matrix(y_test, y_predlr) # Matriz de confusão
classification_report_lr = classification_report(y_test, y_predlr) # Relatório de classificação

"""print("\nAcurácia:", accuracy_score(y_test, y_predlr))
print("\nMatriz de confusão:\n", confusion_matrix(y_test, y_predlr))
print("\nRelatório de classificação:\n", classification_report(y_test, y_predlr))


print("\n=== Informações do Modelo ===")
print("Classes que o modelo aprendeu:", modelolr.classes_)
print("Coeficientes (tamanho):", modelolr.coef_.shape)
print("Interceptos:", modelolr.intercept_)"""









import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix


import joblib

DATASET_PATH = "data/processed/comentarios_processados_full.csv"
MODEL_DIR = Path("models/grupo")
MODEL_PATH = MODEL_DIR / "grupo.pkl"

RANDOM_STATE = 42
MIN_TEXTO_LEN = 5

def load_data(path):
    df = pd.read_csv(path)
    return df

def prepare_dataset(df):
    df = df.copy()

    # só linhas com rótulo e comentário e fase que seja de valor p1
    df = df.dropna(subset=["grupo", "comentario", "fase"])
    df = df[df["comentario"].str.len() >= MIN_TEXTO_LEN]
    df = df[df["fase"] == "p1"]

    # normalizar rótulo
    df["grupo"] = (
        df["grupo"]
        .str.upper()
        .str.replace(" ", "_")
    )
    # O valor 'm' e deve ser exlcuido todos, e o valor Hotelaria/Nutrição deve ser normalizado para 'HOTELARIA_NUTRICAO'
    df = df[df["grupo"] != "M"]
    df["grupo"] = df["grupo"].replace("HOTELARIA/NUTRIÇÃO", "HOTELARIA_NUTRICAO")

    return df

def split_features_labels(df):
    X = df["comentario"]
    y = df["grupo"]
    return X, y

def aplicar_regras(texto, predicao_modelo):

    texto_lower = texto.lower()

    # =====================
    # 1️⃣ Se modelo previu TOTEM
    # =====================
    if predicao_modelo == "TOTEM":

        if any(p in texto_lower for p in [
            "ninguém", "auxilio", "orientacao", "ajuda"
        ]):
            return "ADMINISTRATIVO"

    # =====================
    # 2️⃣ Se modelo previu RECEPÇÃO
    # =====================
    if predicao_modelo == "RECEPÇAO":

        if "maqueiro" in texto_lower and "portaria" in texto_lower:
            return "ADMINISTRATIVO"

    # =====================
    # 3️⃣ Se modelo previu PORTEIRO
    # =====================
    if predicao_modelo == "PORTEIRO":

        palavras_admin = [
            "recepcao", "totem", "maqueiro"
        ]

        count = sum(p in texto_lower for p in palavras_admin)

        if count >= 2:
            return "ADMINISTRATIVO"

    return predicao_modelo

def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=RANDOM_STATE,
    )

    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        sublinear_tf=True,
        min_df=2
    )

    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    model = LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
    )
    model.fit(X_train_vec, y_train)

    y_pred = model.predict(X_test_vec)

    y_pred_final = [
        aplicar_regras(texto, pred)
        for texto, pred in zip(X_test, y_pred)
    ]

    print("\n=== Classification Report ===")
    print(classification_report(y_test, y_pred_final))

    print("\n=== Confusion Matrix ===")
    cm = confusion_matrix(y_test, y_pred_final, labels=model.classes_)
    cm_df = pd.DataFrame(cm, index=model.classes_, columns=model.classes_)
    print(cm_df)

    return model, vectorizer

def save_model(model, vectorizer, path):

    path.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(
        {"model": model, "vectorizer": vectorizer},
        path
    )


def main():
    df = load_data(DATASET_PATH)
    df = prepare_dataset(df)

    X, y = split_features_labels(df)
    model, vectorizer = train_model(X, y)

    save_model(model, vectorizer, MODEL_PATH)


if __name__ == "__main__":
    main()
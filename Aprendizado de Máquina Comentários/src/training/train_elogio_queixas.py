import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

import joblib

DATASET_PATH = "data/processed/comentarios_processados_full.csv"
MODEL_DIR = Path("models/elogio_queixa")
MODEL_PATH = MODEL_DIR / "elogio_queixa.pkl"  

RANDOM_STATE = 42
MIN_TEXTO_LEN = 5

def load_data(path):
    df = pd.read_csv(path)
    return df

def prepare_dataset(df):
    df = df.copy()

    # só linhas com rótulo e comentário
    df = df.dropna(subset=["elogio_ou_queixa", "comentario"])

    # garantir texto válido
    df["comentario"] = df["comentario"].astype(str).str.strip()
    df = df[df["comentario"].str.len() >= MIN_TEXTO_LEN]

    # normalizar rótulo
    df["elogio_ou_queixa"] = (
        df["elogio_ou_queixa"]
        .str.upper()
        .str.replace(" ", "_")
    )

    # O valor ELOGIO_QUEIXA na coluna "elogio_queixa" é ambigui, então deve se tornar "QUEIXA"
    df["elogio_ou_queixa"] = df["elogio_ou_queixa"].replace("ELOGIO_QUEIXA", "QUEIXA")

    return df

def split_features_labels(df):
    X = df["comentario"]
    y = df["elogio_ou_queixa"]
    return X, y

def train_model(X, y):

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=y
    )

    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2)
    )

    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_vec, y_train)

    y_pred = model.predict(X_test_vec)
    print(classification_report(y_test, y_pred))

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

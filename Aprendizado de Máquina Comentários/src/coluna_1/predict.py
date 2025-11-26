# predict.py
import joblib
import numpy as np
import pandas as pd
import re
import unicodedata
import sys
from typing import Dict, Any, List

# ---------- CONFIG ----------
MODEL_PATH = "models/coluna_1_nb.pkl"
VECTORIZER_PATH = "models/coluna_1_vectorizer.pkl"
THRESHOLD = 0.90   # mesmo threshold que você validou no treino

# ---------- PREPROCESSAMENTO (mesma lógica usada no treino!) ----------
def normalize_text(text: str) -> str:
    """Limpeza simples: lower, remover acentos, retirar caracteres não alfanuméricos."""
    if not isinstance(text, str):
        return ""
    text = text.strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    # manter letras, números e espaços (remover pontuação ruídos)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# ---------- CARREGA MODELO E VETORIZER ----------
def load_resources(model_path: str = MODEL_PATH, vectorizer_path: str = VECTORIZER_PATH):
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    return model, vectorizer

# ---------- PREDIÇÃO UNITÁRIA ----------
def predict_single(text: str, model, vectorizer, threshold: float = THRESHOLD) -> Dict[str, Any]:
    """Retorna dicionário com label final (ELOGIO/QUEIXA/OUTROS), probabilidade e probs por classe."""
    text_norm = normalize_text(text)
    X = vectorizer.transform([text_norm])
    probs = model.predict_proba(X)[0]           # array de probabilidades na ordem model.classes_
    pred = model.predict(X)[0]                  # predição base
    max_prob = float(probs.max())

    # aplicar regra de threshold (se nenhuma classe tiver prob >= threshold => OUTROS)
    if max_prob < threshold:
        final = "OUTROS"
    else:
        final = pred

    # montar dict com probs por classe
    probs_by_class = {cls: float(p) for cls, p in zip(model.classes_, probs)}

    return {
        "text": text,
        "text_norm": text_norm,
        "pred_base": str(pred),
        "final": final,
        "max_prob": max_prob,
        "probs": probs_by_class
    }

# ---------- PREDIÇÃO EM LOTE (CSV) ----------
def predict_csv(input_csv: str,
                text_col: str = "comentario_p1",
                output_csv: str = "predictions_out.csv",
                model_path: str = MODEL_PATH,
                vectorizer_path: str = VECTORIZER_PATH,
                threshold: float = THRESHOLD) -> None:
    model, vectorizer = load_resources(model_path, vectorizer_path)
    df = pd.read_csv(input_csv)
    results: List[Dict[str, Any]] = []

    for _, row in df.iterrows():
        text = row.get(text_col, "")
        r = predict_single(text, model, vectorizer, threshold)
        results.append(r)

    res_df = pd.DataFrame(results)
    # junta ao original (opcional)
    out = pd.concat([df.reset_index(drop=True), res_df], axis=1)
    out.to_csv(output_csv, index=False)
    print(f"Salvou previsões em: {output_csv}")

# ---------- USO INTERATIVO / TESTE RÁPIDO ----------
if __name__ == "__main__":
    # modo 1: python predict.py "texto livre aqui"
    # modo 2: python predict.py --csv caminho/entrada.csv

    if len(sys.argv) == 2 and sys.argv[1].endswith(".csv"):
        # rodar em lote
        input_csv = sys.argv[1]
        print("Rodando predições em lote para:", input_csv)
        predict_csv(input_csv)
        sys.exit(0)

    if len(sys.argv) >= 2:
        # predição rápida de uma string passada como argumento
        text_input = " ".join(sys.argv[1:])
        model, vectorizer = load_resources()
        out = predict_single(text_input, model, vectorizer)
        print("\nResultado da predição (teste rápido):")
        print(f"Texto original: {out['text']}")
        print(f"Texto normalizado: {out['text_norm']}")
        print(f"Predição base: {out['pred_base']}")
        print(f"Predição final (com threshold={THRESHOLD}): {out['final']}")
        print(f"Máxima prob.: {out['max_prob']:.4f}")
        print("Probabilidades por classe:")
        for k, v in out["probs"].items():
            print(f"  {k}: {v:.4f}")
        sys.exit(0)

    # caso nenhum argumento: exemplo interativo
    print("Uso:")
    print("  python predict.py \"fui muito bem atendido\"")
    print("  python predict.py dados_para_prever.csv")
    print("\nExemplo rápido rodando com frases de teste:")
    model, vectorizer = load_resources()
    exemplos = [
        "Fui muito bem atendido, obrigado!",
        "Demorou muito, péssimo atendimento",
        "Não sei, texto confuso"
    ]
    for ex in exemplos:
        r = predict_single(ex, model, vectorizer)
        print(f"\n'{ex}' -> final: {r['final']} (max_prob={r['max_prob']:.3f})")
        print(" probs:", r["probs"])

import pandas as pd
import joblib
import sys
import numpy as np

# ------------------
# CONFIGURAÇÕES
# ------------------
THRESHOLD = 0.90   # ponto de corte que você escolheu

# ------------------
# CARREGAR MODELO E VETORIZER
# ------------------
model = joblib.load("./coluna_1_nb.pkl")
vectorizer = joblib.load("./coluna_1_vectorizer.pkl")

# ------------------
# RECEBER ARQUIVO COMO ARGUMENTO
# ------------------
if len(sys.argv) < 2:
    print("Uso: python predict_csv.py arquivo_para_prever.csv")
    sys.exit()

arquivo = sys.argv[1]

# ------------------
# LER ARQUIVO
# ------------------
df = pd.read_csv(arquivo)

if "comentario_p1" not in df.columns:
    print("ERRO: a planilha precisa conter a coluna 'comentario_p1'")
    sys.exit()

# ------------------
# PREPROCESSAR TEXTO
# ------------------
X = vectorizer.transform(df["comentario_p1"].astype(str))

# ------------------
# FAZER PREVISÕES
# ------------------
probs = model.predict_proba(X)
preds = model.predict(X)

final_preds = []

for prob, pred in zip(probs, preds):
    if prob.max() < THRESHOLD:
        final_preds.append("OUTROS")
    else:
        final_preds.append(pred)

df["previsao"] = final_preds
df["probabilidade_de_acerto"] = (probs.max(axis=1) * 100).round(2).astype(str) + "%"

# ------------------
# SALVAR RESULTADO
# ------------------
saida = arquivo.replace(".csv", "_previsao.csv")
df.to_csv(saida, index=False, encoding="utf-8-sig")

print(f"Arquivo gerado: {saida}")

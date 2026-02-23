import joblib
import pandas as pd

MODEL_PATH = "models/grupo/grupo.pkl"
DATA_PATH = "data/processed/comentarios_processados_full.csv"

artefato = joblib.load(MODEL_PATH)
model = artefato["model"]
vectorizer = artefato["vectorizer"]

df = pd.read_csv(DATA_PATH)

# =========================
# MESMO PRÉ-PROCESSAMENTO DO TREINO
# =========================

df = df.dropna(subset=["grupo", "comentario", "fase"])

df["comentario"] = df["comentario"].astype(str).str.strip()
df = df[df["comentario"].str.len() >= 5]
df = df[df["fase"] == "p1"]

df["grupo"] = (
    df["grupo"]
    .str.upper()
    .str.replace(" ", "_", regex=False)
)

df = df[df["grupo"] != "M"]
df["grupo"] = df["grupo"].replace(
    "HOTELARIA/NUTRIÇÃO", "HOTELARIA_NUTRICAO"
)

X = df["comentario"]
y_true = df["grupo"]

# =========================
# PREDIÇÃO DO MODELO
# =========================

X_vec = vectorizer.transform(X)
y_pred_modelo = model.predict(X_vec)

# =========================
# APLICAR REGRA
# =========================

def aplicar_regras(texto, predicao_modelo):
    texto_lower = texto.lower()

    palavras_admin = [
        "maqueiro", "porteiro", "portaria",
        "recepcao", "recepcionista",
        "enfermeiro", "enfermeira", "recepção"
    ]

    count = sum(p in texto_lower for p in palavras_admin)

    if count >= 2:
        return "ADMINISTRATIVO"

    if "totem" in texto_lower and any(
        p in texto_lower for p in ["ninguém", "auxilio", "orientacao", "ajuda"]
    ):
        return "ADMINISTRATIVO"

    return predicao_modelo


y_pred_final = [
    aplicar_regras(texto, pred)
    for texto, pred in zip(X, y_pred_modelo)
]

# =========================
# SALVAR RESULTADO CORRETO
# =========================

df["y_true"] = y_true
df["y_pred_modelo"] = y_pred_modelo
df["y_pred_final"] = y_pred_final

# Agora erro é baseado na predição FINAL
df_erros = df[df["y_true"] != df["y_pred_final"]].copy()

df_erros["tipo_erro"] = df_erros["y_true"] + " → " + df_erros["y_pred_final"]

df_erros.to_excel("erros_modelo_grupo.xlsx", index=False)

print("Arquivo de erros salvo com regra aplicada.")
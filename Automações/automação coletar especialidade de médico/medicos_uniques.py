import pandas as pd
import warnings
warnings.filterwarnings("ignore")

df = pd.read_excel("NOVEMBRO GERAL.xlsx", sheet_name="BASE")


df["BASE"] = (
    df["BASE"]
    .astype(str)
    .str.strip()          # remove espaços nas pontas
    .str.replace(r"\s+", " ", regex=True)  # reduz múltiplos espaços internos
)
especialista_ccg = df[df["BASE"] == "NDI MINAS"]

especialista_unique = especialista_ccg[["SOLICITANTE"]].drop_duplicates()

especialista_unique.to_excel("medicos_unicos_ndi_MINAS_d.xlsx", index=False)
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

df = pd.read_excel("NOVEMBRO GERAL.xlsx", sheet_name="BASE")


especialista_unique = df[["SOLICITANTE"]].drop_duplicates()

especialista_unique.to_excel("medicos_unicos.xlsx", index=False)
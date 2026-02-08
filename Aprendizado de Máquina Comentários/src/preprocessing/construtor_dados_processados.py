import pandas as pd
from carregar_arquivo import carregar_arquivo_excel


FASES = {
    "p1": {
        "elogio": "ELOGIO OU QUEIXA",
        "grupo": "GRUPO",
        "motivo": "MOTIVO",
        "comentario": "comentário p1",
    },
    "p2": {
        "elogio": "ELOGIO OU QUEIXA_1",
        "grupo": "GRUPO.1",
        "motivo": "MOTIVO.1",
        "comentario": "comentário p2",
    },
    "p3": {
        "elogio": "ELOGIO OU QUEIXA_2",
        "grupo": "GRUPO.2",
        "motivo": "MOTIVO.2",
        "comentario": "comentário p3",
    },
    "p4": {
        "elogio": "ELOGIO OU QUEIXA_3",
        "grupo": "GRUPO.3",
        "motivo": "MOTIVO.3",
        "comentario": "comentário p4",
    },
    "p5": {
        "elogio": "ELOGIO OU QUEIXA_4",
        "grupo": "GRUPO.4",
        "motivo": "MOTIVO.4",
        "comentario": "comentario p5",
    },
    "p6": {
        "elogio": "ELOGIO OU QUEIXA_5",
        "grupo": "GRUPO.5",
        "motivo": "MOTIVO.5",
        "comentario": "comentario p6",
    },
  
}

def build_processed_dataset(df):

    df = df.copy()
    df.columns = df.columns.str.strip()


    registros = []
    for fase, cols in FASES.items(): 
        df_temp = df[list(cols.values())].copy()

        print(f"Fase {fase} - colunas encontradas:")
        print(df[list(cols.values())].columns)
        print(len(df[list(cols.values())].columns))


        df_temp.columns = [
            "elogio_ou_queixa",
            "grupo",
            "motivo",
            "comentario"
        ]

        df_temp["elogio_ou_queixa"] = (
            df_temp["elogio_ou_queixa"]
            .astype(str)
            .str.strip()
            .str.replace(" / ", "_")
        )

        df_temp["fase"] = fase
        df_temp = df_temp.dropna(subset=["comentario"])
        df_temp["comentario"] = df_temp["comentario"].astype(str).str.strip()

        df_temp = df_temp[df_temp["comentario"].str.len() >= 5]

        registros.append(df_temp)
    
    return pd.concat(registros, ignore_index=True)


arquivo = "data/raw/Planilha Agosto.xlsx"

df_raw = carregar_arquivo_excel(arquivo=arquivo, aba="BASE")
df_processed = build_processed_dataset(df_raw)

df_processed.to_csv(
    "data/processed/comentarios_processados_agosto.csv",
    index=False
)
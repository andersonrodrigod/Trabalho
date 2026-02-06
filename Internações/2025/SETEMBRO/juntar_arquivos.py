import pandas as pd

arquivos = [
    "CCG OUT.CSV",
    "CLINIPAM OUT.CSV",
    "HAPVIDA OUT.CSV",
    "MINASOUT.CSV",
    "SP OUT.CSV"
]

dfs = []

for arquivo in arquivos:
    print(f"Lendo: {arquivo}")

    df = pd.read_csv(
        arquivo,
        sep=";",
        encoding="latin1",   # 👈 CORREÇÃO REAL
        engine="python",
        on_bad_lines="skip"
    )

    # Remove linhas totalmente em branco
    df = df.dropna(how="all")

    dfs.append(df)

df_final = pd.concat(dfs, ignore_index=True)

df_final.to_csv(
    "BASE_CONCATENADA_FINAL.csv",
    index=False,
    encoding="latin1"  # mantém padrão
)

print("Arquivos concatenados com sucesso.")

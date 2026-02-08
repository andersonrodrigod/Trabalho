import pandas as pd

# caminho do arquivo full
arquivo = "data/processed/comentarios_processados_full.csv"

# carregar
df = pd.read_csv(arquivo)

# normalizar elogio_ou_queixa
df["elogio_ou_queixa"] = (
    df["elogio_ou_queixa"]
    .astype(str)
    .str.strip()
    .str.replace(" / ", "_", regex=False)
    .str.replace("/", "_", regex=False)
)

# salvar sobrescrevendo (ou troque o nome se preferir versionar)
df.to_csv(arquivo, index=False)

print("Coluna elogio_ou_queixa normalizada com sucesso.")

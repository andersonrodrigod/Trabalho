import pandas as pd
from pathlib import Path


def merge_processed_datasets(
    input_dir="data/processed",
    output_file="data/processed/comentarios_processados_full.csv"
):
    input_dir = Path(input_dir)

    # pega todos os CSVs, menos o arquivo final (se já existir)
    arquivos = [
        f for f in input_dir.glob("*.csv")
        if f.name != Path(output_file).name
    ]

    if not arquivos:
        raise ValueError("Nenhum arquivo CSV encontrado para concatenação.")

    dataframes = []

    for arquivo in arquivos:
        print(f"Lendo arquivo: {arquivo.name}")
        df = pd.read_csv(arquivo)
        dataframes.append(df)

    df_final = pd.concat(dataframes, ignore_index=True)

    df_final.to_csv(output_file, index=False)
    print(f"\nDataset final salvo em: {output_file}")
    print(f"Total de registros: {len(df_final)}")


if __name__ == "__main__":
    merge_processed_datasets()

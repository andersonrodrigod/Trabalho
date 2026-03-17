import argparse
from pathlib import Path

import pandas as pd


def detectar_coluna_procedimento(df: pd.DataFrame) -> str:
    cols_upper = {c.strip().upper(): c for c in df.columns}
    if "PROCEDIMENTO" in cols_upper:
        return cols_upper["PROCEDIMENTO"]
    raise KeyError("Nao encontrei a coluna PROCEDIMENTO.")


def gerar_tabela_combinacoes(df: pd.DataFrame) -> pd.DataFrame:
    if "CD_USUARIO" not in df.columns:
        raise KeyError("Nao encontrei coluna CD_USUARIO.")

    col_proc = detectar_coluna_procedimento(df)

    base = df[["CD_USUARIO", col_proc]].copy()
    base["CD_USUARIO"] = base["CD_USUARIO"].astype(str).str.strip()
    base[col_proc] = base[col_proc].astype(str).str.strip().str.upper()

    # Considera somente usuarios duplicados
    dup = base[base["CD_USUARIO"].duplicated(keep=False)].copy()

    # Lista ordenada de procedimentos por usuario
    por_usuario = (
        dup.groupby("CD_USUARIO")[col_proc]
        .apply(lambda s: sorted(s.tolist()))
        .reset_index(name="PROCEDIMENTOS")
    )

    # Frequencia de cada combinacao (somente combinacoes unicas)
    comb_freq = (
        por_usuario["PROCEDIMENTOS"]
        .apply(tuple)
        .value_counts()
        .rename_axis("COMBINACAO")
        .reset_index(name="QTD_USUARIOS")
    )

    if comb_freq.empty:
        return pd.DataFrame(columns=["CONTEM_PRIORIDADE", "QTD_USUARIOS"])

    max_cols = comb_freq["COMBINACAO"].apply(len).max()

    linhas = []
    for _, row in comb_freq.iterrows():
        procedimentos = list(row["COMBINACAO"])
        dados = {"CONTEM_PRIORIDADE": "", "QTD_USUARIOS": int(row["QTD_USUARIOS"])}
        for i in range(1, max_cols + 1):
            dados[f"PROC_{i}"] = procedimentos[i - 1] if i <= len(procedimentos) else ""
        linhas.append(dados)

    out = pd.DataFrame(linhas)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Gera combinacoes de procedimentos duplicados em colunas separadas."
    )
    parser.add_argument(
        "--entrada",
        default="REGISTROS_MANTIDOS.xlsx",
        help="Arquivo Excel de entrada (padrao: REGISTROS_MANTIDOS.xlsx)",
    )
    parser.add_argument(
        "--saida",
        default="combinacoes_duplicados_para_priorizacao.xlsx",
        help="Arquivo Excel de saida (padrao: combinacoes_duplicados_para_priorizacao.xlsx)",
    )
    args = parser.parse_args()

    entrada = Path(args.entrada)
    saida = Path(args.saida)

    if not entrada.exists():
        raise FileNotFoundError(f"Arquivo de entrada nao encontrado: {entrada}")

    df = pd.read_excel(entrada)
    tabela = gerar_tabela_combinacoes(df)

    # Uma unica aba, conforme solicitado
    with pd.ExcelWriter(saida, engine="openpyxl") as writer:
        tabela.to_excel(writer, index=False, sheet_name="combinacoes")

    print(f"Arquivo gerado: {saida.name}")
    print(f"Linhas (combinacoes): {len(tabela)}")
    print("Coluna 1: CONTEM_PRIORIDADE")


if __name__ == "__main__":
    main()

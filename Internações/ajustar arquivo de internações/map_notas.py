from pathlib import Path

import pandas as pd

ARQ_NOTAS = "DADOS_5_ESTRELAS.xlsx"
ARQ_BASE = "BASE FEVEREIRO INTERNACAO MAIN MANTIDOS.xlsx"
ARQ_SAIDA = "BASE FEVEREIRO INTERNACAO MAIN.xlsx"

COL_CHAVE_NOTAS = "CDUSUARIO"
COL_CHAVE_BASE = "COD USUARIO"

MAPA_COLUNAS = {
    "P1": "NOTA1",
    "P2": "NOTA2",
    "P3": "NOTA3",
    "P4": "NOTA4",
    "P5": "NOTA5",
}


def normalizar_chave(serie: pd.Series) -> pd.Series:
    s = serie.astype(str).str.strip()
    s = s.replace({"nan": "", "None": "", "<NA>": ""})
    # Remove sufixo .0 quando o Excel traz numeros como float (ex.: 12345.0)
    s = s.str.replace(r"\.0$", "", regex=True)
    return s


def obter_arquivo(path_padrao: str, padrao_glob: str) -> Path:
    p = Path(path_padrao)
    if p.exists():
        return p

    candidatos = sorted(Path(".").glob(padrao_glob))
    if not candidatos:
        raise FileNotFoundError(f"Arquivo nao encontrado: {path_padrao}")
    return candidatos[0]


def validar_colunas(df: pd.DataFrame, obrigatorias: list[str], nome_arquivo: str) -> None:
    faltantes = [c for c in obrigatorias if c not in df.columns]
    if faltantes:
        raise KeyError(f"Colunas ausentes em {nome_arquivo}: {', '.join(faltantes)}")


def main() -> None:
    arq_notas = obter_arquivo(ARQ_NOTAS, "*5_ESTRELAS*.xlsx")
    arq_base = obter_arquivo(ARQ_BASE, "*FEVEREIRO*MAIN*MANTIDOS*.xlsx")

    df_notas = pd.read_excel(arq_notas)
    df_base = pd.read_excel(arq_base)

    validar_colunas(df_notas, [COL_CHAVE_NOTAS, *MAPA_COLUNAS.values()], arq_notas.name)
    validar_colunas(df_base, [COL_CHAVE_BASE], arq_base.name)

    df_notas = df_notas.copy()
    df_base = df_base.copy()

    df_notas["_CHAVE_NORM"] = normalizar_chave(df_notas[COL_CHAVE_NOTAS])
    df_base["_CHAVE_NORM"] = normalizar_chave(df_base[COL_CHAVE_BASE])

    # Regra solicitada: sem deduplicar geral; para chave repetida, usa o primeiro encontrado.
    df_notas_primeiro = (
        df_notas[df_notas["_CHAVE_NORM"] != ""]
        .drop_duplicates(subset=["_CHAVE_NORM"], keep="first")
        .copy()
    )

    chaves_com_nota = set(df_notas_primeiro["_CHAVE_NORM"])
    total_matches = int(df_base["_CHAVE_NORM"].isin(chaves_com_nota).sum())

    for col_base, col_nota in MAPA_COLUNAS.items():
        if col_base not in df_base.columns:
            df_base[col_base] = ""

        mapa_notas = df_notas_primeiro.set_index("_CHAVE_NORM")[col_nota]
        mask_match = df_base["_CHAVE_NORM"].isin(mapa_notas.index)
        df_base.loc[mask_match, col_base] = df_base.loc[mask_match, "_CHAVE_NORM"].map(mapa_notas)

    df_base = df_base.drop(columns=["_CHAVE_NORM"])
    df_base.to_excel(ARQ_SAIDA, index=False)

    print("Arquivo de notas usado:", arq_notas.name)
    print("Arquivo base usado:", arq_base.name)
    print("Registros na base:", len(df_base))
    print("Registros com chave encontrada em notas:", total_matches)
    print("Arquivo gerado:", ARQ_SAIDA)


if __name__ == "__main__":
    main()

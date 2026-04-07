from pathlib import Path

import pandas as pd


ARQUIVO_ENTRADA = Path("complicacao_janeiro.xlsx")
ABA_BASE = "BASE"
COLUNA_PROCEDIMENTO = "PROCEDIMENTO"
COLUNA_PRESTADOR = "PRESTADOR"
COLUNA_ESPECIALISTA = "ESPECIALISTA"
COLUNA_TIPO = "TIPO"
COLUNA_UF = "UF"

ARQUIVO_SAIDA_ESPECIALISTA = Path("PROCEDIMENTO_ESPECIALISTA_UNICOS.xlsx")
ARQUIVO_SAIDA_TIPO = Path("PROCEDIMENTO_TIPO_UNICOS.xlsx")
ARQUIVO_SAIDA_TIPO_NAO_CLASSIFICADO = Path("TIPO_NAO_CLASSIFICADO_VIDEO.xlsx")
ARQUIVO_SAIDA_NOVOS_TIPO_NAO_CLASSIFICADO = Path("NOVOS_TIPO_NAO_CLASSIFICADO_VIDEO.xlsx")
ARQUIVO_SAIDA_PRESTADOR_UF = Path("PRESTADOR_UF_UNICOS.xlsx")


def validar_arquivo_entrada(caminho: Path) -> None:
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo nao encontrado: {caminho}")


def carregar_base(caminho: Path) -> pd.DataFrame:
    return pd.read_excel(
        caminho,
        sheet_name=ABA_BASE,
        dtype={
            COLUNA_PROCEDIMENTO: "string",
            COLUNA_PRESTADOR: "string",
            COLUNA_ESPECIALISTA: "string",
            COLUNA_TIPO: "string",
            COLUNA_UF: "string",
        },
    )


def carregar_existente_ou_vazio(colunas: list[str], arquivo_saida: Path) -> pd.DataFrame:
    if not arquivo_saida.exists():
        return pd.DataFrame(columns=colunas)

    return pd.read_excel(
        arquivo_saida,
        dtype={coluna: "string" for coluna in colunas},
    )[colunas]


def salvar_incremental(df_novo: pd.DataFrame, arquivo_saida: Path) -> pd.DataFrame:
    colunas = list(df_novo.columns)
    df_existente = carregar_existente_ou_vazio(colunas, arquivo_saida).drop_duplicates()

    if df_existente.empty:
        df_total = df_novo.drop_duplicates()
        df_novos = df_total.copy()
    else:
        chaves_existentes = set(map(tuple, df_existente.itertuples(index=False, name=None)))
        mascara_novos = ~df_novo.apply(tuple, axis=1).isin(chaves_existentes)
        df_novos = df_novo.loc[mascara_novos].drop_duplicates()
        df_total = pd.concat([df_existente, df_novos], ignore_index=True).drop_duplicates()

    df_total.to_excel(arquivo_saida, index=False)
    return df_novos


def preparar_unicos_classificados(
    df: pd.DataFrame,
    coluna_principal: str,
    coluna_classificacao: str,
) -> pd.DataFrame:
    return (
        df[[coluna_principal, coluna_classificacao]]
        .dropna(subset=[coluna_principal, coluna_classificacao])
        .drop_duplicates()
    )


def preparar_tipo_nao_classificado(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df[df[COLUNA_TIPO].isna()][[COLUNA_PROCEDIMENTO]]
        .dropna(subset=[COLUNA_PROCEDIMENTO])
        .drop_duplicates()
    )


def main() -> None:
    validar_arquivo_entrada(ARQUIVO_ENTRADA)
    df_base = carregar_base(ARQUIVO_ENTRADA)

    df_especialista = preparar_unicos_classificados(
        df=df_base,
        coluna_principal=COLUNA_PROCEDIMENTO,
        coluna_classificacao=COLUNA_ESPECIALISTA,
    )
    df_tipo = preparar_unicos_classificados(
        df=df_base,
        coluna_principal=COLUNA_PROCEDIMENTO,
        coluna_classificacao=COLUNA_TIPO,
    )
    df_prestador_uf = preparar_unicos_classificados(
        df=df_base,
        coluna_principal=COLUNA_PRESTADOR,
        coluna_classificacao=COLUNA_UF,
    )
    df_tipo_nao_classificado = preparar_tipo_nao_classificado(df_base)

    salvar_incremental(
        df_novo=df_especialista,
        arquivo_saida=ARQUIVO_SAIDA_ESPECIALISTA,
    )
    salvar_incremental(
        df_novo=df_tipo,
        arquivo_saida=ARQUIVO_SAIDA_TIPO,
    )
    salvar_incremental(
        df_novo=df_prestador_uf,
        arquivo_saida=ARQUIVO_SAIDA_PRESTADOR_UF,
    )
    df_novos_tipo_nao_classificado = salvar_incremental(
        df_novo=df_tipo_nao_classificado,
        arquivo_saida=ARQUIVO_SAIDA_TIPO_NAO_CLASSIFICADO,
    )
    df_novos_tipo_nao_classificado.to_excel(
        ARQUIVO_SAIDA_NOVOS_TIPO_NAO_CLASSIFICADO,
        index=False,
    )

    print(f"Arquivo gerado: {ARQUIVO_SAIDA_ESPECIALISTA}")
    print(f"Arquivo gerado: {ARQUIVO_SAIDA_TIPO}")
    print(f"Arquivo gerado: {ARQUIVO_SAIDA_PRESTADOR_UF}")
    print(f"Arquivo gerado: {ARQUIVO_SAIDA_TIPO_NAO_CLASSIFICADO}")
    print(f"Arquivo gerado: {ARQUIVO_SAIDA_NOVOS_TIPO_NAO_CLASSIFICADO}")


if __name__ == "__main__":
    main()

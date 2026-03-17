from pathlib import Path

import pandas as pd


ARQ_MAIN = "FEVEREIRO_INTERNAÇÕES_COM_TELEFONES.xlsx"
ARQ_COMP = "COMPLICACAO FEVEREIRO 17.03.xlsx"
ABA_COMP = "BASE"

OUT_MANTIDOS = "BASE FEVEREIRO INTERNACAO MAIN MANTIDOS.xlsx"
OUT_EXCLUIDOS = "BASE FEVEREIRO INTERNACAO MAIN EXCLUIDOS.xlsx"

COL_SENHA = "SENHA"
COL_COD_USUARIO = "COD USUARIO"


def normalizar_serie(serie: pd.Series) -> pd.Series:
    s = serie.astype(str).str.strip()
    s = s.replace({"nan": "", "None": "", "<NA>": ""})
    # Quando o Excel vem como float (ex.: 12345.0), remove o .0 final.
    s = s.str.replace(r"\.0$", "", regex=True)
    return s


def obter_arquivo_main() -> Path:
    p = Path(ARQ_MAIN)
    if p.exists():
        return p

    candidatos = sorted(Path(".").glob("*FEVEREIRO*TELEFONES*.xlsx"))
    if not candidatos:
        raise FileNotFoundError(f"Arquivo principal nao encontrado: {ARQ_MAIN}")
    return candidatos[0]


def main() -> None:
    arq_main = obter_arquivo_main()

    df_main = pd.read_excel(arq_main)
    df_comp = pd.read_excel(ARQ_COMP, sheet_name=ABA_COMP)

    for col in [COL_SENHA, COL_COD_USUARIO]:
        if col not in df_main.columns:
            raise KeyError(f"Coluna ausente no main: {col}")
        if col not in df_comp.columns:
            raise KeyError(f"Coluna ausente na complicacao: {col}")

    df_main = df_main.copy()
    df_comp = df_comp.copy()

    # Normaliza chaves
    df_main["_SENHA_NORM"] = normalizar_serie(df_main[COL_SENHA])
    df_main["_COD_NORM"] = normalizar_serie(df_main[COL_COD_USUARIO])
    df_comp["_SENHA_NORM"] = normalizar_serie(df_comp[COL_SENHA])
    df_comp["_COD_NORM"] = normalizar_serie(df_comp[COL_COD_USUARIO])

    senhas_comp = set(df_comp["_SENHA_NORM"])
    cods_comp = set(df_comp["_COD_NORM"])
    senhas_comp.discard("")
    cods_comp.discard("")

    # Etapa 1: excluir por SENHA
    mask_excluir_senha = df_main["_SENHA_NORM"].isin(senhas_comp)

    # Etapa 2: no restante, excluir por COD USUARIO
    mask_restante = ~mask_excluir_senha
    mask_excluir_cod = mask_restante & df_main["_COD_NORM"].isin(cods_comp)

    mask_excluir_total = mask_excluir_senha | mask_excluir_cod

    df_excluidos = df_main[mask_excluir_total].copy()
    df_excluidos_senha = df_main[mask_excluir_senha].copy()
    df_excluidos_cod = df_main[mask_excluir_cod].copy()
    df_mantidos = df_main[~mask_excluir_total].copy()

    # Remover colunas auxiliares
    cols_aux = ["_SENHA_NORM", "_COD_NORM"]
    df_excluidos = df_excluidos.drop(columns=cols_aux)
    df_excluidos_senha = df_excluidos_senha.drop(columns=cols_aux)
    df_excluidos_cod = df_excluidos_cod.drop(columns=cols_aux)
    df_mantidos = df_mantidos.drop(columns=cols_aux)

    df_mantidos.to_excel(OUT_MANTIDOS, index=False)
    with pd.ExcelWriter(OUT_EXCLUIDOS, engine="openpyxl") as writer:
        df_excluidos_senha.to_excel(writer, index=False, sheet_name="EXCLUIDOS_SENHA")
        df_excluidos_cod.to_excel(writer, index=False, sheet_name="EXCLUIDOS_COD_USUARIO")
        df_excluidos.to_excel(writer, index=False, sheet_name="EXCLUIDOS_TOTAL")

    print("Arquivo main usado:", arq_main.name)
    print("Mantidos:", len(df_mantidos))
    print("Excluidos:", len(df_excluidos))
    print("Excluidos por SENHA:", int(mask_excluir_senha.sum()))
    print("Excluidos por COD USUARIO:", int(mask_excluir_cod.sum()))
    print("Saida mantidos:", OUT_MANTIDOS)
    print("Saida excluidos:", OUT_EXCLUIDOS)


if __name__ == "__main__":
    main()

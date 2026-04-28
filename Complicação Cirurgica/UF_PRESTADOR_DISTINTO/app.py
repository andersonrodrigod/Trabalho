import os
import pandas as pd

# Config
ARQUIVO_EXCEL = "COMPLICAÇÃO DEZEMBRO.xlsx"
NOME_ABA = "BASE"
ARQUIVO_SAIDA = "prestador_sigla.csv"


def normalizar_texto(valor):
    """Normaliza texto para comparação de chaves."""
    return str(valor).strip().upper()


def montar_base_nova(arquivo_excel, nome_aba):
    """Lê Excel e retorna PRESTADOR único com ESTADO e lista de SIGLA(s)."""
    df = pd.read_excel(arquivo_excel, sheet_name=nome_aba)
    df = df[["PRESTADOR", "ESTADO", "SIGLA"]].dropna(
        subset=["PRESTADOR", "SIGLA"]
    ).copy()
    df["PRESTADOR"] = df["PRESTADOR"].astype(str).str.strip()
    df["ESTADO"] = df["ESTADO"].astype(str).str.strip()
    df["SIGLA"] = df["SIGLA"].astype(str).str.strip()
    df["PRESTADOR_CHAVE"] = df["PRESTADOR"].apply(normalizar_texto)

    return (
        df.groupby("PRESTADOR_CHAVE", as_index=False)
        .agg(
            PRESTADOR=("PRESTADOR", "first"),
            ESTADO=(
                "ESTADO",
                lambda x: " | ".join(sorted({i for i in x if i and i != "nan"})),
            ),
            SIGLA=("SIGLA", lambda x: sorted(set(x))),
        )
    )


def csv_para_lista_siglas(df_csv):
    """Converte CSV legado (SIGLA_1..N) para estrutura com ESTADO e lista SIGLA."""
    if df_csv.empty:
        return pd.DataFrame(
            columns=["PRESTADOR_CHAVE", "PRESTADOR", "ESTADO", "SIGLA"]
        )

    sigla_cols = [c for c in df_csv.columns if c.startswith("SIGLA_")]
    if not sigla_cols and "SIGLA" in df_csv.columns:
        sigla_cols = ["SIGLA"]

    if not sigla_cols:
        df_csv["SIGLA"] = [[] for _ in range(len(df_csv))]
    else:
        df_csv["SIGLA"] = df_csv[sigla_cols].values.tolist()
        df_csv["SIGLA"] = df_csv["SIGLA"].apply(
            lambda itens: sorted(
                {
                    str(i).strip()
                    for i in itens
                    if pd.notna(i) and str(i).strip()
                }
            )
        )

    df_csv["PRESTADOR"] = df_csv["PRESTADOR"].astype(str).str.strip()
    if "ESTADO" not in df_csv.columns:
        df_csv["ESTADO"] = ""
    df_csv["ESTADO"] = df_csv["ESTADO"].fillna("").astype(str).str.strip()
    df_csv["PRESTADOR_CHAVE"] = df_csv["PRESTADOR"].apply(normalizar_texto)
    return df_csv[["PRESTADOR_CHAVE", "PRESTADOR", "ESTADO", "SIGLA"]]


def expandir_siglas(df_base):
    """Expande lista de SIGLA em colunas SIGLA_1..SIGLA_N."""
    df_saida = df_base.copy()
    max_siglas = int(df_saida["SIGLA"].apply(len).max()) if not df_saida.empty else 0

    for i in range(max_siglas):
        df_saida[f"SIGLA_{i + 1}"] = df_saida["SIGLA"].apply(
            lambda lista: lista[i] if i < len(lista) else None
        )

    df_saida = df_saida.drop(columns=["SIGLA", "PRESTADOR_CHAVE"])
    colunas_sigla = [c for c in df_saida.columns if c.startswith("SIGLA_")]
    colunas_ordenadas = ["PRESTADOR", "ESTADO"] + colunas_sigla
    return df_saida[colunas_ordenadas]


def main():
    base_nova = montar_base_nova(ARQUIVO_EXCEL, NOME_ABA)

    if os.path.exists(ARQUIVO_SAIDA):
        df_existente = pd.read_csv(ARQUIVO_SAIDA)
        base_existente = csv_para_lista_siglas(df_existente)

        combinado = pd.concat([base_existente, base_nova], ignore_index=True)
        combinado = (
            combinado.groupby("PRESTADOR_CHAVE", as_index=False)
            .agg(
                PRESTADOR=("PRESTADOR", "first"),
                ESTADO=(
                    "ESTADO",
                    lambda x: " | ".join(sorted({i for i in x if i and i != "nan"})),
                ),
                SIGLA=(
                    "SIGLA",
                    lambda listas: sorted(
                        set(sigla for lista in listas for sigla in lista)
                    ),
                ),
            )
        )
    else:
        combinado = base_nova

    df_final = expandir_siglas(combinado)
    df_final.to_csv(ARQUIVO_SAIDA, index=False, encoding="utf-8-sig")
    print(f"Arquivo atualizado com sucesso: {ARQUIVO_SAIDA}")


if __name__ == "__main__":
    main()

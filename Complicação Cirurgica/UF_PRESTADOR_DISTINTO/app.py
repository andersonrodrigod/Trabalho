import os
import pandas as pd

# Config
ARQUIVO_EXCEL = "COMPLICAÇÃO JANEIRO.xlsx"
NOME_ABA = "BASE"
ARQUIVO_SAIDA = "prestador_sigla.csv"


def normalizar_texto(valor):
    """Normaliza texto para comparação de chaves."""
    return str(valor).strip().upper()


def juntar_valores_unicos(serie):
    """Consolida valores únicos em uma célula, ignorando nulos e vazios."""
    valores = set()
    for item in serie:
        if pd.isna(item):
            continue
        texto = str(item).strip()
        if not texto or texto.lower() == "nan":
            continue
        valores.add(texto)
    return " | ".join(sorted(valores))


def unir_textos(valor_a, valor_b):
    """Une textos de duas fontes sem perder o anterior."""
    itens = []
    for valor in [valor_a, valor_b]:
        if pd.isna(valor):
            continue
        texto = str(valor).strip()
        if not texto:
            continue
        partes = [p.strip() for p in texto.split("|")]
        for parte in partes:
            if parte and parte not in itens:
                itens.append(parte)
    return " | ".join(itens)


def garantir_lista(valor):
    """Garante que o valor seja lista de strings."""
    if isinstance(valor, list):
        return [str(x).strip() for x in valor if pd.notna(x) and str(x).strip()]
    if pd.isna(valor):
        return []
    texto = str(valor).strip()
    return [texto] if texto else []


def montar_base_nova(arquivo_excel, nome_aba):
    """Lê Excel e retorna PRESTADOR único com ESTADO/UF/DISTRITO e lista de SIGLA(s)."""
    df = pd.read_excel(arquivo_excel, sheet_name=nome_aba)
    df = df[["PRESTADOR", "ESTADO", "UF", "DISTRITO", "SIGLA"]].dropna(
        subset=["PRESTADOR", "SIGLA"]
    ).copy()
    df["PRESTADOR"] = df["PRESTADOR"].astype(str).str.strip()
    df["ESTADO"] = df["ESTADO"].astype(str).str.strip()
    df["UF"] = df["UF"].astype(str).str.strip()
    df["DISTRITO"] = df["DISTRITO"].astype(str).str.strip()
    df["SIGLA"] = df["SIGLA"].astype(str).str.strip()
    df["PRESTADOR_CHAVE"] = df["PRESTADOR"].apply(normalizar_texto)

    return (
        df.groupby("PRESTADOR_CHAVE", as_index=False)
        .agg(
            PRESTADOR=("PRESTADOR", "first"),
            ESTADO=("ESTADO", juntar_valores_unicos),
            UF=("UF", juntar_valores_unicos),
            DISTRITO=("DISTRITO", juntar_valores_unicos),
            SIGLA=("SIGLA", lambda x: sorted(set(x))),
        )
    )


def csv_para_lista_siglas(df_csv):
    """Converte CSV legado (SIGLA_1..N) para estrutura com dados e lista SIGLA."""
    if df_csv.empty:
        return pd.DataFrame(
            columns=["PRESTADOR_CHAVE", "PRESTADOR", "ESTADO", "UF", "DISTRITO", "SIGLA"]
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
    if "UF" not in df_csv.columns:
        df_csv["UF"] = ""
    if "DISTRITO" not in df_csv.columns:
        df_csv["DISTRITO"] = ""
    df_csv["ESTADO"] = df_csv["ESTADO"].fillna("").astype(str).str.strip()
    df_csv["UF"] = df_csv["UF"].fillna("").astype(str).str.strip()
    df_csv["DISTRITO"] = df_csv["DISTRITO"].fillna("").astype(str).str.strip()
    df_csv["PRESTADOR_CHAVE"] = df_csv["PRESTADOR"].apply(normalizar_texto)
    return df_csv[["PRESTADOR_CHAVE", "PRESTADOR", "ESTADO", "UF", "DISTRITO", "SIGLA"]]


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
    colunas_ordenadas = ["PRESTADOR", "ESTADO", "UF", "DISTRITO"] + colunas_sigla
    return df_saida[colunas_ordenadas]


def main():
    base_nova = montar_base_nova(ARQUIVO_EXCEL, NOME_ABA)

    if os.path.exists(ARQUIVO_SAIDA):
        df_existente = pd.read_csv(ARQUIVO_SAIDA)
        base_existente = csv_para_lista_siglas(df_existente)
        merged = base_existente.merge(
            base_nova,
            on="PRESTADOR_CHAVE",
            how="outer",
            suffixes=("_old", "_new"),
        )

        combinado = pd.DataFrame()
        combinado["PRESTADOR_CHAVE"] = merged["PRESTADOR_CHAVE"]
        combinado["PRESTADOR"] = (
            merged["PRESTADOR_old"].fillna("").astype(str).str.strip()
        )
        mascara_vazio = combinado["PRESTADOR"].eq("")
        combinado.loc[mascara_vazio, "PRESTADOR"] = (
            merged.loc[mascara_vazio, "PRESTADOR_new"].fillna("").astype(str).str.strip()
        )
        combinado["ESTADO"] = [
            unir_textos(a, b) for a, b in zip(merged["ESTADO_old"], merged["ESTADO_new"])
        ]
        combinado["UF"] = [
            unir_textos(a, b) for a, b in zip(merged["UF_old"], merged["UF_new"])
        ]
        combinado["DISTRITO"] = [
            unir_textos(a, b)
            for a, b in zip(merged["DISTRITO_old"], merged["DISTRITO_new"])
        ]
        combinado["SIGLA"] = [
            sorted(set(garantir_lista(a) + garantir_lista(b)))
            for a, b in zip(merged["SIGLA_old"], merged["SIGLA_new"])
        ]
    else:
        combinado = base_nova

    df_final = expandir_siglas(combinado)
    df_final.to_csv(ARQUIVO_SAIDA, index=False, encoding="utf-8-sig")
    print(f"Arquivo atualizado com sucesso: {ARQUIVO_SAIDA}")


if __name__ == "__main__":
    main()

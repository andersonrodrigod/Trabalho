import pandas as pd
import unicodedata

TIPO_FILTRO = "VIDEO ABDOMINAL"


def _normalizar_texto(valor) -> str:
    if pd.isna(valor):
        return ""
    return str(valor).strip()


def _normalizar_sem_acento(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(ch for ch in texto if not unicodedata.combining(ch)).lower().strip()


def _nome_aba_seguro(nome: str, usados: set[str]) -> str:
    inval = ['\\', '/', '*', '[', ']', ':', '?']
    base = nome
    for ch in inval:
        base = base.replace(ch, "_")
    base = base.strip() or "SEM_UF"
    base = base[:31]

    candidato = base
    idx = 1
    while candidato in usados:
        sufixo = f"_{idx}"
        candidato = f"{base[:31-len(sufixo)]}{sufixo}"
        idx += 1

    usados.add(candidato)
    return candidato


def calcular_indicadores_df(
    df_base: pd.DataFrame,
    coluna_pergunta: str,
    valor_alvo: str,
) -> pd.DataFrame:
    df = df_base.copy()

    if coluna_pergunta not in df.columns:
        raise ValueError(f'A coluna "{coluna_pergunta}" nao foi encontrada na planilha BASE.')
    if "ESPECIALISTA" not in df.columns:
        raise ValueError('A coluna "ESPECIALISTA" nao foi encontrada na planilha BASE.')

    # Normaliza texto para evitar diferencas por espacos e caixa
    df["ESPECIALISTA"] = df["ESPECIALISTA"].map(_normalizar_texto)
    df[coluna_pergunta] = df[coluna_pergunta].map(_normalizar_texto)
    df["ESPECIALISTA"] = df["ESPECIALISTA"].replace("", "SEM_ESPECIALISTA")

    # 1) Total por especialista
    total_cirurgias = df.groupby("ESPECIALISTA", dropna=False).size().rename("TOTAL_CIRURGIAS")

    # 2) Total do valor alvo por especialista (ignora acento: Nao = Não)
    alvo_norm = _normalizar_sem_acento(_normalizar_texto(valor_alvo))
    serie_norm = df[coluna_pergunta].map(_normalizar_sem_acento)
    total_alvo = (
        df[serie_norm == alvo_norm]
        .groupby("ESPECIALISTA", dropna=False)
        .size()
        .rename("TOTAL_SIM")
    )

    resultado = (
        total_cirurgias.to_frame()
        .join(total_alvo, how="left")
        .fillna({"TOTAL_SIM": 0})
        .reset_index()
    )

    resultado["TOTAL_SIM"] = resultado["TOTAL_SIM"].astype(int)

    # 3) Proporcao do valor alvo por especialista
    resultado["PERCENTUAL_SIM"] = (
        resultado["TOTAL_SIM"] / resultado["TOTAL_CIRURGIAS"] * 100
    ).round(1)

    # 4) Representatividade no total geral do valor alvo
    total_geral_alvo = resultado["TOTAL_SIM"].sum()
    if total_geral_alvo == 0:
        resultado["REPRESENTATIVIDADE"] = 0.0
    else:
        resultado["REPRESENTATIVIDADE"] = (
            resultado["TOTAL_SIM"] / total_geral_alvo * 100
        ).round(1)

    # Ordenacao opcional para facilitar leitura
    resultado = resultado.sort_values("TOTAL_CIRURGIAS", ascending=False).reset_index(drop=True)

    # Linha total ao final
    total_cirurgias_geral = int(resultado["TOTAL_CIRURGIAS"].sum())
    total_alvo_geral = int(resultado["TOTAL_SIM"].sum())
    percentual_alvo_geral = (
        round(total_alvo_geral / total_cirurgias_geral * 100, 1)
        if total_cirurgias_geral > 0
        else 0.0
    )

    linha_total = pd.DataFrame(
        [
            {
                "ESPECIALISTA": "TOTAL",
                "TOTAL_CIRURGIAS": total_cirurgias_geral,
                "TOTAL_SIM": total_alvo_geral,
                "PERCENTUAL_SIM": percentual_alvo_geral,
                "REPRESENTATIVIDADE": 100.0 if total_alvo_geral > 0 else 0.0,
            }
        ]
    )

    resultado_final = pd.concat([resultado, linha_total], ignore_index=True)

    return resultado_final[
        [
            "ESPECIALISTA",
            "TOTAL_CIRURGIAS",
            "TOTAL_SIM",
            "PERCENTUAL_SIM",
            "REPRESENTATIVIDADE",
        ]
    ]


def calcular_indicadores(
    arquivo_excel: str,
    aba: str = "BASE",
    coluna_pergunta: str = "P1",
    valor_alvo: str = "Sim",
) -> pd.DataFrame:
    df = pd.read_excel(arquivo_excel, sheet_name=aba)
    return calcular_indicadores_df(df, coluna_pergunta=coluna_pergunta, valor_alvo=valor_alvo)


def _gerar_bloco_pergunta(
    writer,
    df_base: pd.DataFrame,
    usados: set[str],
    prefixo: str,
    coluna_pergunta: str,
    valor_alvo: str,
) -> None:
    nome_geral = _nome_aba_seguro(f"{prefixo}_GERAL", usados)
    tabela_geral = calcular_indicadores_df(
        df_base,
        coluna_pergunta=coluna_pergunta,
        valor_alvo=valor_alvo,
    )
    tabela_geral.to_excel(writer, sheet_name=nome_geral, index=False)

    ordem_ufs = (
        df_base.groupby("UF", dropna=False)
        .size()
        .sort_values(ascending=False)
        .index
        .tolist()
    )
    for uf in ordem_ufs:
        df_uf = df_base[df_base["UF"] == uf]
        tabela_uf = calcular_indicadores_df(
            df_uf,
            coluna_pergunta=coluna_pergunta,
            valor_alvo=valor_alvo,
        )
        nome_aba = _nome_aba_seguro(f"{prefixo}_{uf}", usados)
        tabela_uf.to_excel(writer, sheet_name=nome_aba, index=False)


def gerar_indicadores_por_uf(
    arquivo_excel: str,
    arquivo_saida: str = "indicadores_calculados.xlsx",
    aba_origem: str = "BASE",
) -> None:
    df_base = pd.read_excel(arquivo_excel, sheet_name=aba_origem)

    if "UF" not in df_base.columns:
        raise ValueError('A coluna "UF" nao foi encontrada na planilha BASE.')
    if "TIPO" not in df_base.columns:
        raise ValueError('A coluna "TIPO" nao foi encontrada na planilha BASE.')

    # Filtro fixo solicitado: TIPO = VIDEO ABDOMINAL
    tipo_norm = df_base["TIPO"].map(_normalizar_texto).map(_normalizar_sem_acento)
    filtro_norm = _normalizar_sem_acento(TIPO_FILTRO)
    df_base = df_base[tipo_norm == filtro_norm].copy()

    df_base["UF"] = df_base["UF"].map(_normalizar_texto).replace("", "SEM_UF")

    usados = set()
    with pd.ExcelWriter(arquivo_saida, engine="openpyxl") as writer:
        # Primeiro bloco P1 (valor alvo: Sim)
        _gerar_bloco_pergunta(
            writer,
            df_base,
            usados,
            prefixo="P1",
            coluna_pergunta="P1",
            valor_alvo="Sim",
        )

        # Depois bloco P3 (valor alvo: Não)
        _gerar_bloco_pergunta(
            writer,
            df_base,
            usados,
            prefixo="P3",
            coluna_pergunta="P3",
            valor_alvo="Não",
        )


if __name__ == "__main__":
    arquivo = "COMPLICAÇÃO DEZEMBRO 02.02 BI.xlsx"  # ajuste para o nome do arquivo no diretorio atual
    saida = "indicadores_calculados.xlsx"
    gerar_indicadores_por_uf(arquivo_excel=arquivo, arquivo_saida=saida, aba_origem="BASE")
    print(f"Arquivo gerado com abas de P1 e P3 (filtro TIPO={TIPO_FILTRO}): {saida}")

import pandas as pd

def retornar_registros_para_usuarios(abas):
    """
    Retorna registros de várias abas para 'usuarios',
    seguindo a prioridade:
        1) usuarios_lidos_nao_respondidos
        2) segundo_envio_lidos
        3) Bases (HAP, CCG, CLINIPAN, NDI SP, NDI MINAS)
        4) usuarios_duplicados (só se não existir em usuarios)

    E REMOVE das abas de origem os registros que foram movidos.
    """

    abas_base = ["HAP", "CCG", "CLINIPAN", "NDI MINAS", "NDI SP"]

    df_usuarios = abas["usuarios"].copy()
    df_duplicados = abas["usuarios_duplicados"].copy()

    df_usuarios["USUARIO"] = df_usuarios["USUARIO"].astype(str).str.strip()
    df_duplicados["USUARIO"] = df_duplicados["USUARIO"].astype(str).str.strip()

    # ------------------------------
    # FUNÇÃO AUXILIAR PARA MOVER E REMOVER DA ABA ORIGINAL
    # ------------------------------
    def mover_registros(df_origem, nome_aba_origem, filtro=None, condicao_base=False):
        nonlocal df_usuarios, df_duplicados

        df_local = df_origem.copy()

        # aplicar filtro quando necessário (para as bases)
        if filtro is not None:
            df_local = df_local[filtro].copy()

        # limpar strings
        df_local["USUARIO"] = df_local["USUARIO"].astype(str).str.strip()

        # armazenar CHAVES para remover depois
        chaves_remover = df_local["CHAVE RELATORIO"].tolist()

        for _, row in df_local.iterrows():
            usuario = row["USUARIO"]

            if usuario in df_usuarios["USUARIO"].values:
                df_duplicados = pd.concat([df_duplicados, row.to_frame().T], ignore_index=True)
            else:
                df_usuarios = pd.concat([df_usuarios, row.to_frame().T], ignore_index=True)

        # remover da aba original tudo que foi movido
        abas[nome_aba_origem] = df_origem[
            ~df_origem["CHAVE RELATORIO"].isin(chaves_remover)
        ].copy()

    # ==========================================================
    # 1) usuarios_lidos_nao_respondidos
    # ==========================================================
    mover_registros(
        abas["usuarios_lidos_nao_respondidos"],
        "usuarios_lidos_nao_respondidos"
    )

    # ==========================================================
    # 2) segundo_envio_lidos
    # ==========================================================
    mover_registros(
        abas["segundo_envio_lidos"],
        "segundo_envio_lidos"
    )

    # ==========================================================
    # 3) Bases – com condição STATUS BOT
    # ==========================================================
    for aba in abas_base:

        if aba not in abas:
            continue

        df_base = abas[aba]

        filtro_validos = (
            df_base["STATUS BOT"].notna() & 
            (df_base["STATUS BOT"].astype(str).str.strip() != "") &
            ~df_base["STATUS BOT"].isin(["BASE INCORRETA", "SEM CONTATO"])
        )

        mover_registros(
            df_base,
            aba,
            filtro=filtro_validos
        )

    # ==========================================================
    # 4) duplicados só voltam se não existir outro igual
    # ==========================================================

    df_voltar = df_duplicados[
        ~df_duplicados["COD USUARIO"].isin(df_usuarios["COD USUARIO"])
    ].copy()

    # Mover somente esses
    if not df_voltar.empty:
        usuarios_voltar = df_voltar["COD USUARIO"].tolist()
        df_usuarios = pd.concat([df_usuarios, df_voltar], ignore_index=True)

        # remover de duplicados os que voltaram
        df_duplicados = df_duplicados[
            ~df_duplicados["COD USUARIO"].isin(usuarios_voltar)
        ].copy()

    # ==========================================================
    # atualizar abas finais
    # ==========================================================

    abas["usuarios"] = df_usuarios
    abas["usuarios_duplicados"] = df_duplicados

    print("\n🔄 Finalizado retorno inicial de registros para 'usuarios'")
    print(f"   → Total em usuarios: {len(df_usuarios)}")
    print(f"   → Total em usuarios_duplicados: {len(df_duplicados)}")

    return abas

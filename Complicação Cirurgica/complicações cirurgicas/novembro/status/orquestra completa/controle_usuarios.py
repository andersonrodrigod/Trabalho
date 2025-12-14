import pandas as pd


def ingestao_usuarios(df_base, abas):
    """
    Responsável por inserir novos registros em 'usuarios'
    seguindo regras de segurança:

    - Apenas STATUS vazio / NaN
    - Remove duplicados do próprio lote (COD USUARIO + USUARIO)
    - Não insere se CHAVE já existir
    - Se (COD USUARIO + USUARIO) já existir no histórico → vai para duplicados
    - Nunca sobrescreve dados existentes
    """

    print("\n🚪 Iniciando ingestão de novos registros em 'usuarios'...")

    # --------------------------------------------------
    # Garantir existência das abas
    # --------------------------------------------------
    if "usuarios" not in abas:
        abas["usuarios"] = pd.DataFrame()

    if "usuarios_duplicados" not in abas:
        abas["usuarios_duplicados"] = pd.DataFrame()

    df_usuarios = abas["usuarios"].copy()
    df_duplicados = abas["usuarios_duplicados"].copy()

    # --------------------------------------------------
    # Normalizações defensivas
    # --------------------------------------------------
    for col in ["CHAVE RELATORIO", "COD USUARIO", "USUARIO"]:
        if col in df_usuarios.columns:
            df_usuarios[col] = df_usuarios[col].astype(str).str.strip()

    # Criar chave composta no histórico
    if not df_usuarios.empty:
        df_usuarios["CHAVE_DUP"] = (
            df_usuarios["COD USUARIO"].astype(str) + "|" +
            df_usuarios["USUARIO"].astype(str)
        )
    else:
        df_usuarios["CHAVE_DUP"] = pd.Series(dtype=str)

    # --------------------------------------------------
    # 1) Filtrar registros virgens (STATUS vazio)
    # --------------------------------------------------
    candidatos = df_base[
        df_base["STATUS"].isna() |
        (df_base["STATUS"].astype(str).str.strip() == "")
    ].copy()

    print(f"   → Registros virgens encontrados na BASE: {len(candidatos)}")

    if candidatos.empty:
        print("   ⚠️ Nenhum registro para ingestão.")
        return abas

    # --------------------------------------------------
    # 1.1) REMOVER DUPLICADOS DO PRÓPRIO LOTE
    # --------------------------------------------------
    candidatos["CHAVE_DUP"] = (
        candidatos["COD USUARIO"].astype(str).str.strip() + "|" +
        candidatos["USUARIO"].astype(str).str.strip()
    )

    total_antes = len(candidatos)

    candidatos = candidatos[
        ~candidatos.duplicated(subset=["CHAVE_DUP"], keep=False)
    ].copy()

    total_depois = len(candidatos)

    print(f"   → Duplicados removidos do lote: {total_antes - total_depois}")
    print(f"   → Candidatos únicos após limpeza: {total_depois}")

    # --------------------------------------------------
    # 2) Processar linha a linha
    # --------------------------------------------------
    novos_usuarios = []
    novos_duplicados = []

    for _, row in candidatos.iterrows():

        chave = str(row.get("CHAVE", "")).strip()
        cod_usuario = str(row.get("COD USUARIO", "")).strip()
        usuario = str(row.get("USUARIO", "")).strip()

        # Segurança mínima
        if chave == "" or cod_usuario == "" or usuario == "":
            continue

        chave_dup = f"{cod_usuario}|{usuario}"

        # --- REGRA 1: CHAVE já existe ---
        if not df_usuarios.empty and chave in df_usuarios["CHAVE RELATORIO"].values:
            continue

        # --- REGRA 2: DUPLICADO NO HISTÓRICO ---
        if not df_usuarios.empty and chave_dup in df_usuarios["CHAVE_DUP"].values:
            novos_duplicados.append({
                "BASE": row.get("BASE", ""),
                "COD USUARIO": cod_usuario,
                "USUARIO": usuario,
                "TELEFONE RELATORIO": row.get("TELEFONE", ""),
                "PRESTADOR": row.get("PRESTADOR", ""),
                "PROCEDIMENTO": row.get("PROCEDIMENTO", ""),
                "TP ATENDIMENTO": row.get("TP ATENDIMENTO", ""),
                "DT INTERNACAO": row.get("DT INTERNACAO", ""),
                "ENVIO": row.get("DT ENVIO", ""),
                "CHAVE RELATORIO": chave
            })
            continue

        # --- REGRA 3: ENTRADA LIMPA ---
        novos_usuarios.append({
            "BASE": row.get("BASE", ""),
            "COD USUARIO": cod_usuario,
            "USUARIO": usuario,
            "TELEFONE RELATORIO": row.get("TELEFONE", ""),
            "PRESTADOR": row.get("PRESTADOR", ""),
            "PROCEDIMENTO": row.get("PROCEDIMENTO", ""),
            "TP ATENDIMENTO": row.get("TP ATENDIMENTO", ""),
            "DT INTERNACAO": row.get("DT INTERNACAO", ""),
            "ENVIO": row.get("DT ENVIO", ""),
            "CHAVE RELATORIO": chave
        })

    # --------------------------------------------------
    # 3) Consolidar resultados
    # --------------------------------------------------
    if novos_usuarios:
        df_usuarios = pd.concat(
            [
                df_usuarios.drop(columns=["CHAVE_DUP"], errors="ignore"),
                pd.DataFrame(novos_usuarios)
            ],
            ignore_index=True
        )

    if novos_duplicados:
        df_duplicados = pd.concat(
            [df_duplicados, pd.DataFrame(novos_duplicados)],
            ignore_index=True
        )

    abas["usuarios"] = df_usuarios
    abas["usuarios_duplicados"] = df_duplicados

    print(f"   ✔ Novos inseridos em usuarios: {len(novos_usuarios)}")
    print(f"   ⚠️ Enviados para duplicados: {len(novos_duplicados)}")
    print("🚪 Ingestão finalizada.\n")

    return abas



def detectar_usuarios_defeituosos(df_usuarios, df_resolvidos):
    """
    Detecta usuários defeituosos:
    - Registro em usuarios
    - Que já exista semanticamente em usuarios_resolvidos
      (USUARIO + PRESTADOR + PROCEDIMENTO)
    - Independente da CHAVE RELATORIO
    """

    print("\n🔍 Iniciando verificação de usuarios defeituosos...")

    # Copiar para não alterar os originais
    df_u = df_usuarios.copy()
    df_r = df_resolvidos.copy()

    # -------------------------
    # 1) Normalização defensiva
    # -------------------------
    cols = ["USUARIO", "PRESTADOR", "PROCEDIMENTO"]

    for col in cols:
        df_u[col] = (
            df_u[col]
            .astype(str)
            .str.strip()
            .str.upper()
        )

        df_r[col] = (
            df_r[col]
            .astype(str)
            .str.strip()
            .str.upper()
        )

    # -------------------------
    # 2) Criar chave semântica
    # -------------------------
    df_u["CHAVE_SEMANTICA"] = (
        df_u["USUARIO"] + "|" +
        df_u["PRESTADOR"] + "|" +
        df_u["PROCEDIMENTO"]
    )

    df_r["CHAVE_SEMANTICA"] = (
        df_r["USUARIO"] + "|" +
        df_r["PRESTADOR"] + "|" +
        df_r["PROCEDIMENTO"]
    )

    # -------------------------
    # 3) Verificar existência
    # -------------------------
    chaves_resolvidos = set(df_r["CHAVE_SEMANTICA"])

    mask_defeituosos = df_u["CHAVE_SEMANTICA"].isin(chaves_resolvidos)

    df_defeituosos = df_u[mask_defeituosos].copy()

    # -------------------------
    # 4) Limpeza final
    # -------------------------
    df_defeituosos = df_defeituosos.drop(columns=["CHAVE_SEMANTICA"], errors="ignore")

    print(f"⚠️ Usuarios defeituosos encontrados: {len(df_defeituosos)}")

    if len(df_defeituosos) > 0:
        print("   → Primeiras chaves defeituosas:")
        print(df_defeituosos["CHAVE RELATORIO"].head().to_list())

    return df_defeituosos



def retornar_registros_para_usuarios(abas):
    """
    Retorna registros para 'usuarios' respeitando integridade:

    - CHAVE RELATORIO nunca duplica em usuarios
    - COD USUARIO nunca duplica em usuarios
    - Duplicados vão para usuarios_duplicados e NÃO retornam
    """

    abas_base = ["HAP", "CCG", "CLINIPAN", "NDI MINAS", "NDI SP"]

    df_usuarios = abas["usuarios"].copy()
    df_duplicados = abas["usuarios_duplicados"].copy()

    # Normalização defensiva
    for col in ["CHAVE RELATORIO", "COD USUARIO"]:
        df_usuarios[col] = df_usuarios[col].astype(str).str.strip()
        df_duplicados[col] = df_duplicados[col].astype(str).str.strip()

    # --------------------------------------------------
    # FUNÇÃO AUXILIAR
    # --------------------------------------------------
    def mover_registros(df_origem, nome_aba_origem, filtro=None):
        nonlocal df_usuarios, df_duplicados

        df_local = df_origem.copy()

        if filtro is not None:
            df_local = df_local[filtro].copy()

        chaves_remover = df_local["CHAVE RELATORIO"].astype(str).str.strip().tolist()

        for _, row in df_local.iterrows():
            chave = str(row["CHAVE RELATORIO"]).strip()
            cod_usuario = str(row["COD USUARIO"]).strip()

            # 1️⃣ CHAVE já existe → ignora
            if chave in df_usuarios["CHAVE RELATORIO"].values:
                continue

            # 2️⃣ COD USUARIO já existe → duplicado permanente
            if cod_usuario in df_usuarios["COD USUARIO"].values:
                df_duplicados = pd.concat(
                    [df_duplicados, row.to_frame().T],
                    ignore_index=True
                )
                continue

            # 3️⃣ Entrada limpa
            df_usuarios = pd.concat(
                [df_usuarios, row.to_frame().T],
                ignore_index=True
            )

        # remover da aba de origem tudo que foi processado
        abas[nome_aba_origem] = df_origem[
            ~df_origem["CHAVE RELATORIO"].astype(str).str.strip().isin(chaves_remover)
        ].copy()

    # ==================================================
    # 1) usuarios_lidos_nao_respondidos
    # ==================================================
    mover_registros(
        abas["usuarios_lidos_nao_respondidos"],
        "usuarios_lidos_nao_respondidos"
    )

    # ==================================================
    # 2) segundo_envio_lidos
    # ==================================================
    mover_registros(
        abas["segundo_envio_lidos"],
        "segundo_envio_lidos"
    )

    # ==================================================
    # 3) trocar_contato_lida
    # ==================================================
    if "trocar_contato_lida" in abas:
        mover_registros(
            abas["trocar_contato_lida"],
            "trocar_contato_lida"
        )

    # ==================================================
    # 4) Bases
    # ==================================================
    for aba in abas_base:
        if aba not in abas:
            continue

        df_base = abas[aba]

        filtro_validos = (
            df_base["STATUS BOT"].notna() &
            (df_base["STATUS BOT"].astype(str).str.strip() != "") &
            ~df_base["STATUS BOT"].isin(["BASE INCORRETA", "SEM CONTATO"])
        )

        mover_registros(df_base, aba, filtro=filtro_validos)

    # ==================================================
    # Atualizar abas finais
    # ==================================================
    abas["usuarios"] = df_usuarios
    abas["usuarios_duplicados"] = df_duplicados

    print("\n🔄 Retorno para 'usuarios' finalizado")
    print(f"   → Total em usuarios: {len(df_usuarios)}")
    print(f"   → Total em usuarios_duplicados: {len(df_duplicados)}")

    return abas

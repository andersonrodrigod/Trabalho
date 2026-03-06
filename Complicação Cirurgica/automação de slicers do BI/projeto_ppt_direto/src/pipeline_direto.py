from __future__ import annotations

from pathlib import Path

from core.gerar_slide_matplotlib import gerar_ppt_from_sheet_tables

from .dados_indicadores import montar_tabelas_por_uf


def gerar_ppt_direto(
    arquivo_entrada: str,
    arquivo_saida: str,
    assets_dir: str | None = None,
    aba_origem: str = "BASE",
    tipo_filtro: str | None = None,
    layout_mode: str = "paired",
) -> Path:
    ordered_names, tables_by_sheet = montar_tabelas_por_uf(
        arquivo_excel=arquivo_entrada,
        aba_origem=aba_origem,
        tipo_filtro=tipo_filtro,
    )

    saida = Path(arquivo_saida)
    saida.parent.mkdir(parents=True, exist_ok=True)

    gerar_ppt_from_sheet_tables(
        ordered_names=ordered_names,
        tables_by_sheet=tables_by_sheet,
        arquivo_saida=str(saida),
        assets_dir=assets_dir,
        layout_mode=layout_mode,
    )
    return saida

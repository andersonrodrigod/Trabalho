from __future__ import annotations

from pathlib import Path
from typing import Callable

from core.config import PipelineConfig
from core.criar_tabela_excel import gerar_indicadores_por_uf
from core.formatacao import formatar_tabela
from core.gerar_slide import gerar_ppt


def executar_pipeline(
    config: PipelineConfig,
    assets_dir: Path | None = None,
    progress_callback: Callable[[float, str], None] | None = None,
) -> dict[str, Path]:
    def report(progress: float, message: str) -> None:
        if progress_callback is not None:
            progress_callback(progress, message)

    report(0.05, "Preparando arquivos")
    config.pasta_saida.mkdir(parents=True, exist_ok=True)

    report(0.20, "Etapa 1/3: gerando indicadores")
    gerar_indicadores_por_uf(
        arquivo_excel=str(config.arquivo_entrada),
        arquivo_saida=str(config.indicadores),
        aba_origem=config.aba_origem,
        tipo_filtro=config.tipo_filtro,
    )

    report(0.55, "Etapa 2/3: formatando tabela")
    formatar_tabela(
        arquivo_entrada=str(config.indicadores),
        arquivo_saida=str(config.indicadores_formatados),
    )

    report(0.80, "Etapa 3/3: gerando apresentacao")
    gerar_ppt(
        arquivo_excel=str(config.indicadores_formatados),
        arquivo_saida=str(config.apresentacao),
        assets_dir=str(assets_dir) if assets_dir else None,
        layout_mode=config.layout_mode,
    )
    report(1.00, "Pipeline concluido")

    return {
        "indicadores": config.indicadores,
        "indicadores_formatados": config.indicadores_formatados,
        "apresentacao": config.apresentacao,
    }

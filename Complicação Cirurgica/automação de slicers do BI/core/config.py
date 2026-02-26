from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PipelineConfig:
    nome: str
    arquivo_entrada: Path
    pasta_saida: Path
    tipo_filtro: str | None = None
    aba_origem: str = "BASE"
    layout_mode: str = "paired"

    @property
    def indicadores(self) -> Path:
        return self.pasta_saida / "indicadores_calculados.xlsx"

    @property
    def indicadores_formatados(self) -> Path:
        return self.pasta_saida / "indicadores_calculados_formatado.xlsx"

    @property
    def apresentacao(self) -> Path:
        return self.pasta_saida / "indicadores_apresentacao.pptx"


def default_configs(base_dir: Path) -> dict[str, PipelineConfig]:
    arquivo_entrada = base_dir / "data" / "input" / "COMPLICAÇÃO DEZEMBRO 02.02 BI.xlsx"
    pasta_saida = base_dir / "data" / "output"
    return {
        "totais": PipelineConfig(
            nome="totais",
            arquivo_entrada=arquivo_entrada,
            pasta_saida=pasta_saida / "totais",
            tipo_filtro=None,
            layout_mode="paired",
        ),
        "tipo_video_abdominal": PipelineConfig(
            nome="tipo_video_abdominal",
            arquivo_entrada=arquivo_entrada,
            pasta_saida=pasta_saida / "tipo_video_abdominal",
            tipo_filtro="VIDEO ABDOMINAL",
            layout_mode="grid4",
        ),
    }

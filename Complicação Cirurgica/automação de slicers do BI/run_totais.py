from __future__ import annotations

from pathlib import Path

from core.config import default_configs
from core.pipeline import executar_pipeline


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    configs = default_configs(base_dir)
    config = configs["totais"]
    saidas = executar_pipeline(config, assets_dir=base_dir / "assets")

    print("Pipeline concluido: TOTAIS")
    print(f"Indicadores: {saidas['indicadores']}")
    print(f"Indicadores formatados: {saidas['indicadores_formatados']}")
    print(f"Apresentacao: {saidas['apresentacao']}")


if __name__ == "__main__":
    main()


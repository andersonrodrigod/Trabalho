from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from projeto_ppt_direto.src.pipeline_direto import gerar_ppt_direto


def _descobrir_arquivo_entrada(base_dir: Path) -> Path:
    candidatos = sorted((base_dir / "data" / "input").glob("*.xlsx"))
    if candidatos:
        return candidatos[0]
    candidatos = sorted(base_dir.glob("*.xlsx"))
    if candidatos:
        return candidatos[0]
    raise FileNotFoundError("Nenhum arquivo .xlsx encontrado em data/input ou na raiz do projeto.")


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    default_in = _descobrir_arquivo_entrada(base_dir)
    default_out = base_dir / "data" / "output" / f"direto_{datetime.now().strftime('%Y%m%d_%H%M%S')}" / "indicadores_apresentacao.pptx"

    parser = argparse.ArgumentParser(
        description="Gera PowerPoint direto da base, sem arquivo Excel intermediario."
    )
    parser.add_argument("--entrada", default=str(default_in), help="Arquivo XLSX de entrada.")
    parser.add_argument("--saida", default=str(default_out), help="Arquivo PPTX de saida.")
    parser.add_argument("--aba", default="BASE", help="Nome da aba de origem.")
    parser.add_argument("--tipo", default=None, help='Filtro em TIPO (ex.: "VIDEO ABDOMINAL").')
    parser.add_argument("--layout", default="paired", choices=["paired", "grid4"], help="Layout dos slides.")
    parser.add_argument("--assets", default=str(base_dir / "assets"), help="Pasta com logo.jpg e inicio.jpg.")

    args = parser.parse_args()

    saida = gerar_ppt_direto(
        arquivo_entrada=args.entrada,
        arquivo_saida=args.saida,
        assets_dir=args.assets,
        aba_origem=args.aba,
        tipo_filtro=args.tipo,
        layout_mode=args.layout,
    )
    print(f"Arquivo gerado: {saida}")


if __name__ == "__main__":
    main()

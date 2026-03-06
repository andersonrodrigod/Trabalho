from core.gerar_slide_matplotlib import gerar_ppt


if __name__ == "__main__":
    gerar_ppt(
        arquivo_excel="indicadores_calculados_formatado.xlsx",
        arquivo_saida="indicadores_apresentacao_matplotlib.pptx",
    )
    print("Arquivo gerado: indicadores_apresentacao_matplotlib.pptx")

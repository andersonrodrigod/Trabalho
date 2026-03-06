# Slide Direto

Projeto independente para gerar a apresentacao diretamente da base, sem gerar Excel intermediario.

## Estrutura

- `main.py`: entrada principal.
- `src/`: logica de dados e renderizacao do PPT.
- `assets/`: imagens `logo.jpg` e `inicio.jpg`.
- `data/input/`: arquivo XLSX de entrada.
- `data/output/`: arquivos PPTX gerados.

## Como executar

```powershell
cd slide_direto
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py --entrada "data/input/COMPLICAÇÃO DEZEMBRO 02.02 BI.xlsx"
```

Opcional:

```powershell
python main.py --tipo "VIDEO ABDOMINAL" --layout grid4
```

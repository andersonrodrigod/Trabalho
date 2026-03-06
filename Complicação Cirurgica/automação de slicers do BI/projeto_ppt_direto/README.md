# Projeto PPT Direto

Gera o PowerPoint diretamente da aba `BASE` do arquivo de entrada, sem criar Excel intermediario.

## Estrutura

- `src/dados_indicadores.py`: extracao e agregacao dos dados.
- `src/pipeline_direto.py`: orquestra dados + geracao do PPT.
- `requirements.txt`: dependencias do modulo direto.

## Uso rapido

```powershell
python gerar_power_point.py
```

Com filtros:

```powershell
python gerar_power_point.py --tipo "VIDEO ABDOMINAL" --layout grid4
```

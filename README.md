## Ambiente de Desenvolvimento

- Python 3.12

Instalação:

```bash
pip install -r requirements-dev.txt
```

Como rodar o projeto:

Sempre execute os comandos a partir da raiz do projeto (`C:\projetos\AdaptiveAlgorithmSelector`) para evitar erro de módulo ou arquivo não encontrado.

No PowerShell:

```powershell
cd C:\projetos\AdaptiveAlgorithmSelector
$env:PYTHONPATH = (Get-Location).Path
python .\testes\mainb.py
```

Executar verificações:

```bash
ruff check .
pytest
```

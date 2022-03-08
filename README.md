# Teste ALTAVE

[![Python application](https://github.com/mateuslourenco/processo-altave/actions/workflows/ci.yml/badge.svg)](https://github.com/mateuslourenco/processo-altave/actions/workflows/ci.yml)

## Como rodar o projeto

- Clone esse repositorio
- Instale o pip-tools
- Crie um ambiente virtual
- Instale as dependencias

```
git clone https://github.com/mateuslourenco/processo-altave.git
cd processo-altave
pip install pip-tools
python -m venv .venv
source .venv/bin/activate
pip-sync requirements.txt 
```


## Como testar qualidade do código
```
source .venv/bin/activate
flake8
```

## Como rodar testes automaticos
```
source .venv/bin/activate
pytest
```

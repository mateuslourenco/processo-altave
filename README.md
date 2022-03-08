# Teste ALTAVE

[![Python application](https://github.com/mateuslourenco/processo-altave/actions/workflows/ci.yml/badge.svg)](https://github.com/mateuslourenco/processo-altave/actions/workflows/ci.yml)

Projeto disponivel em [https://teste-altave.herokuapp.com/](https://teste-altave.herokuapp.com/)

## Especificação OpenAPI
https://teste-altave.herokuapp.com/docs

## Como rodar o projeto

- Clone esse repositorio
- Instale o pip-tools
- Crie um ambiente virtual
- Instale as dependencias
- Copie as variaveis de ambiente
- Ative o postgres com docker
- Inicie o projeto

Para rodar o projeto sem postgres, exclua a variavel 'DATABASE_URL' do arquivo .env

```
git clone https://github.com/mateuslourenco/processo-altave.git
cd processo-altave
pip install pip-tools
python -m venv .venv
source .venv/bin/activate
pip-sync requirements.txt dev-requirements.txt
cp contrib/env-sample .env
docker-compose up
uvicorn src.server:app --reload --reload-dir=src
```

### Neste projeto, é necessário autenticar o usuário para poder acessar o endpoint '/'. Caso queria remover a autenticação, refatore o código do arquivo src/server.py

```
@app.get('/')
def home(request: Request):
    return {'horário_requisição': request.state.horario_requisicao}

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

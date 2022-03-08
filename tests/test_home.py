from datetime import datetime
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from src.infra.sqlalchemy.config.database import Base, get_db
from src.server import app


# Criar um novo banco de dados somente para teste
# https://fastapi.tiangolo.com/advanced/testing-database/
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture()
def db_test():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture
def resp_criar_usuario(db_test):

    """
    Fixture que cria um usuario conforme o endpoint '/signup/'
    """

    resp = client.post('/signup/', json={"login": "teste", "senha": "teste"})
    return resp


def test_request_sem_token(db_test):

    """
    Testa se o endpoint '/' necessita de autenticação
    """

    response = client.get('/')
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}


def test_home_com_token_invalido():
    """
    Testa se a endpoint '/' retorna erro 401 e mensagem para token invalido
    """

    resp_home_token_invalido = client.get('/', headers={"Authorization": "Bearer token_invalido"})
    assert resp_home_token_invalido.status_code == 401
    assert resp_home_token_invalido.json() == {'detail': 'Token inválido'}


def test_criar_usuario(resp_criar_usuario):

    """
    Testa se o endpoint '/signup/' cria um usuario
    """

    assert resp_criar_usuario.status_code == 201


def test_criar_usuario_ja_existente(resp_criar_usuario):

    """
    Testa se o endpoint '/signup/' reconhece que já existe um usuario com o login criado e retorna erro 400
    """

    nova_resp = client.post('/signup/', json={"login": "teste", "senha": "teste"})
    assert nova_resp.status_code == 400
    assert nova_resp.json() == {'detail': 'Já existe um usuario com esse login'}


def test_home_com_usuario_logado(resp_criar_usuario):

    """
    Testa se o endpoint '/' exibe o horario de requisição quando existe um usuario autenticado
    """

    assert resp_criar_usuario.status_code == 201

    # Realizar autenticação
    resp_token = client.post('/token', data={"username": "teste", "password": "teste"})
    assert resp_token.status_code == 200

    # Lógica para pegar o access_token ao autenticar
    dados = resp_token.json()
    token = dados['access_token']

    # Teste no endpoint '/' com token válido
    resp_home_token_valido = client.get('/', headers={"Authorization": f"Bearer {token}"})
    horario = datetime.now().strftime('%H:%M:%S')

    assert resp_home_token_valido.status_code == 200
    assert resp_home_token_valido.json() == {'horário_requisição': horario}

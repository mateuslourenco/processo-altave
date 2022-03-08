from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from src.infra.providers import hash_provider, token_provider
from src.infra.sqlalchemy.config.database import get_db
from src.infra.sqlalchemy.repositorios.repositorio_usuario import RepositorioUsuario
from src.schemas import schemas

router = APIRouter()


@router.post('/signup/', status_code=status.HTTP_201_CREATED, response_model=schemas.UsuarioSimples)
def signup(usuario: schemas.Usuario, session: Session = Depends(get_db)):

    """
    Endpoint que cria um usuario. Antes de criar o usuário no banco de dados, é verificado se não existe usuario com
    o mesmo login
    """

    usuario_localizado = RepositorioUsuario(session).obter_usuario(usuario.login)
    if usuario_localizado:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Já existe um usuario com esse login')

    usuario.senha = hash_provider.gerar_hash(usuario.senha)
    usuario_criado = RepositorioUsuario(session).criar_usuario(usuario)
    return usuario_criado


@router.post('/token')
def signin(session: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):

    """
    Endpoint que faz a autenticação do usuario e retorna o token de acesso
    """

    dados_invalidos = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Usuario ou senha incorretos')

    senha = form_data.password
    login = form_data.username

    usuario = RepositorioUsuario(session).obter_usuario(login)
    if not usuario:
        raise dados_invalidos

    senha_valida = hash_provider.verificar_hash(senha, usuario.senha)
    if not senha_valida:
        raise dados_invalidos

    token = token_provider.criar_access_token({'sub': usuario.login})

    return {"access_token": token, "token_type": "bearer"}

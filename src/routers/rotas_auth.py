from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.infra.providers import hash_provider
from src.infra.sqlalchemy.config.database import get_db
from src.infra.sqlalchemy.repositorios.repositorio_usuario import RepositorioUsuario
from src.schemas import schemas

router = APIRouter()


@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=schemas.UsuarioSimples)
def signup(usuario: schemas.Usuario, session: Session = Depends(get_db)):

    usuario_localizado = RepositorioUsuario(session).obter_usuario(usuario.login)
    if usuario_localizado:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Já existe um usuario com esse login')

    usuario.senha = hash_provider.gerar_hash(usuario.senha)
    usuario_criado = RepositorioUsuario(session).criar_usuario(usuario)
    return usuario_criado

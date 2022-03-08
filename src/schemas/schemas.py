from typing import Optional

from pydantic import BaseModel


class Usuario(BaseModel):
    id: Optional[int] = None
    login: str
    senha: str

    class Config:
        orm_mode = True


class UsuarioSimples(BaseModel):
    login: str

    class Config:
        orm_mode = True


class LoginSucesso(BaseModel):
    usuario: UsuarioSimples
    token: str

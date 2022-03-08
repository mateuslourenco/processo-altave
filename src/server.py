from datetime import datetime

from fastapi import FastAPI, Depends
from starlette.requests import Request

from src.infra.sqlalchemy.config.database import criar_db
from src.routers import rotas_auth
from src.routers.utils import obter_usuario_logado

criar_db()

app = FastAPI()


@app.middleware('http')
async def horario_da_requisicao(request: Request, call_next):
    horario = datetime.now().strftime('%H:%M:%S')
    request.state.horario_requisicao = horario
    response = await call_next(request)
    return response

app.include_router(rotas_auth.router)


@app.get('/')
def home(request: Request, token=Depends(obter_usuario_logado)):
    return {'horário_requisição': request.state.horario_requisicao}

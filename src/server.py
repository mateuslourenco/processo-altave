from datetime import datetime

from fastapi import FastAPI
from starlette.requests import Request

from src.infra.sqlalchemy.config.database import criar_db
from src.routers import rotas_auth

criar_db()

app = FastAPI()


@app.middleware('http')
async def horario_da_requisicao(request: Request, call_next):
    horario = datetime.now().strftime('%H:%M:%S')
    request.state.horario_requisicao = horario
    response = await call_next(request)
    return response

app.include_router(rotas_auth.router, prefix='/auth')


@app.get('/')
def home(request: Request):
    return {'horário': request.state.horario_requisicao}

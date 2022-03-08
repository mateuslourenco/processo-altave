from datetime import datetime

from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def home():
    horario = datetime.now().strftime('%H:%M:%S')
    return {'msg': horario}

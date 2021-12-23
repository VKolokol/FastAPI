from fastapi import FastAPI
import uvicorn

from db.base import database
from endpoints import users
from endpoints import auth
from endpoints import jobs


app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router, prefix='/auth')
app.include_router(jobs.router, prefix='/jobs')


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


if __name__ == '__main__':
    uvicorn.run('main:app', port=8001, host='0.0.0.0', reload=True)

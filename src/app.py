import uvicorn
from fastapi import FastAPI

from api.router import router


def create_app() -> FastAPI:
    app = FastAPI(docs_url='/swagger')
    app.include_router(router)
    return  app

if __name__ == '__main__':
    uvicorn.run('app:create_app', factory=True, host='0.0.0.0', port=8000, workers=1)


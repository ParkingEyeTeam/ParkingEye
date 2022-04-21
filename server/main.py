from server.api.upd_api import router

from fastapi import FastAPI

app = FastAPI()

app.include_router(router, tags=['cars_api'])
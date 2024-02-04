import importlib

from app.aerich.base import config
from app.api.public.modules import routers
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise


def _register_routers(app: FastAPI, items: list):
    for item in items:
        router = importlib.import_module(f"{item}").router
        app.include_router(router)


def init_fastapi_application():
    app = FastAPI(
        title='component_name',
        docs_url="/",
    )
    _register_routers(app, routers.items)
    register_tortoise(app, config=config)
    return app


app = init_fastapi_application()

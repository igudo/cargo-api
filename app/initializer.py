import json
import os

from fastapi import FastAPI
from tortoise.contrib.starlette import register_tortoise


def init(app: FastAPI):
    """
    Init routers and etc.
    :return:
    """
    init_routers(app)
    init_db(app)


def init_db(app: FastAPI):
    """
    Init database models.
    :param app:
    :return:
    """
    register_tortoise(
        app,
        config={
            'connections': {
                'default': {
                    'engine': 'tortoise.backends.asyncpg',
                    'credentials': {
                        'host': os.environ['POSTGRES_HOST'],
                        'port': os.environ['POSTGRES_PORT'],
                        'user': os.environ['POSTGRES_USER'],
                        'password': os.environ['POSTGRES_PASSWORD'],
                        'database': os.environ['POSTGRES_DB'],
                    }
                },
            },
            'apps': {
                'models': {
                    'models': ['models'],
                }
            }
        },
        generate_schemas=True
    )


def init_routers(app: FastAPI):
    """
    Initialize routers defined in `app.routers`
    :param app:
    :return:
    """
    from routers import router
    app.include_router(router)

import os
from typing import List
from fastapi import FastAPI
from models import PricePlan_Pydantic, PricePlan
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI(title="Cargo API")
DECLARED_RATE = 1000


@app.get("/priceplans", response_model=List[PricePlan_Pydantic])
async def get_priceplans():
    return await PricePlan_Pydantic.from_queryset(PricePlan.all())
    

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
    generate_schemas=True,
    add_exception_handlers=True,
)

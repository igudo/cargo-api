from fastapi import FastAPI
from initializer import init

app = FastAPI(title="Cargo API")

init(app)

from fastapi import FastAPI
from sqlmodel import SQLModel
from app.routers import auth

from app.database import engine
from app.routers.compras import router as compras_router

app = FastAPI()


@app.on_event("startup")
def criar_banco():
    SQLModel.metadata.create_all(engine)


app.include_router(compras_router)
app.include_router(auth.router)

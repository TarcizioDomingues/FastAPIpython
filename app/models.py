from sqlmodel import SQLModel, Field


class Compra(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    item: str
    preco_unitario: float
    quantidade: int
    embalagem: str | None = None
    valor_total: float = Field(default=0)


class Usuario(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    senha_hash: str

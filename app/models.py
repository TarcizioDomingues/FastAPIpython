from sqlmodel import SQLModel, Field


class CompraBase(SQLModel):
    item: str
    preco_unitario: float
    quantidade: int


class Compra(CompraBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class CompraCreate(CompraBase):
    pass

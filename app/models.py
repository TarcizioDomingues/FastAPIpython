from sqlmodel import SQLModel, Field
from pydantic import Field as PydanticField


class CompraBase(SQLModel):
    item: str = Field(
        min_length=3, description="Nome do produto deve conter ao mínimo 3 caracteres"
    )

    preco_unitario: float = Field(gt=0, description="Preço deve ser maior que zero")

    quantidade: int = Field(gt=0, description="Quantidade deve ser maior que zero")


class Compra(CompraBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    valor_total: float = Field(default=0)


class CompraCreate(CompraBase):
    pass

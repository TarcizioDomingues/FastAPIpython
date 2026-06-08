from sqlmodel import SQLModel, Field


class CompraBase(SQLModel):
    item: str = Field(
        min_length=3, description="Nome do produto deve conter ao mínimo 3 caracteres"
    )
    preco_unitario: float = Field(gt=0, description="Preço deve ser maior que zero")
    quantidade: int = Field(gt=0, description="Quantidade deve ser maior que zero")
    embalagem: str | None = None


class CompraCreate(CompraBase):
    pass


class CompraRead(CompraBase):
    id: int
    valor_total: float

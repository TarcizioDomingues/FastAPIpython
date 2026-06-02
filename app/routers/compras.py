from fastapi import APIRouter
from sqlmodel import Session, select

from app.database import engine
from app.models import Compra, CompraCreate

router = APIRouter()


@router.post("/compras")
def criar_compra(compra: CompraCreate):
    nova_compra = Compra(
        item=compra.item,
        preco_unitario=compra.preco_unitario,
        quantidade=compra.quantidade,
    )

    with Session(engine) as session:
        session.add(nova_compra)
        session.commit()
        session.refresh(nova_compra)
        return nova_compra


@router.get("/compras")
def listar_compras():
    with Session(engine) as session:
        resultado = session.exec(select(Compra)).all()
        return resultado


@router.get("/compras/{id_compra}")
def buscar_compra(id_compra: int):
    with Session(engine) as session:
        compra = session.get(Compra, id_compra)
        return compra


@router.put("/compras/{id_compra}")
def atualizar_compra(id_compra: int, compra_atualizada: Compra):
    with Session(engine) as session:
        compra = session.get(Compra, id_compra)

        if compra is None:
            return {"erro": "Compra não encontrada"}

        compra.item = compra_atualizada.item
        compra.preco_unitario = compra_atualizada.preco_unitario
        compra.quantidade = compra_atualizada.quantidade

        session.add(compra)
        session.commit()
        session.refresh(compra)

        return compra


@router.delete("/compras/{id_compra}")
def deletar_compra(id_compra: int):
    with Session(engine) as session:
        compra = session.get(Compra, id_compra)

        if compra is None:
            return {"erro": "Compra não encontrada"}

        session.delete(compra)
        session.commit()

        return {"mensagem": "Compra deletada com sucesso"}

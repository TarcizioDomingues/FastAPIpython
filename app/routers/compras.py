from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select, func


from app.database import engine
from app.models import Compra, CompraCreate

router = APIRouter()


from fastapi import HTTPException


@router.post("/compras")
def criar_compra(compra: CompraCreate):

    with Session(engine) as session:

        compra_existente = session.exec(
            select(Compra).where(Compra.item == compra.item.upper())
        ).first()

        if compra_existente:
            raise HTTPException(
                status_code=409, detail="Produto já cadastrado no sistema"
            )

        nova_compra = Compra(
            item=compra.item,
            preco_unitario=compra.preco_unitario,
            quantidade=compra.quantidade,
            valor_total=compra.preco_unitario * compra.quantidade,
        )

        session.add(nova_compra)
        session.commit()
        session.refresh(nova_compra)

        return nova_compra


@router.get("/compras")
def listar_compras(item: str | None = None):
    with Session(engine) as session:

        query = select(Compra)

        if item:
            query = query.where(func.lower(Compra.item).contains(item.lower()))

        return session.exec(query).all()


@router.get("/compras/{id_compra}")
def buscar_compra(id_compra: int):
    with Session(engine) as session:
        compra = session.get(Compra, id_compra)

        if compra is None:
            raise HTTPException(status_code=404, detail="Compra não encontrada")

        return {
            "id": compra.id,
            "item": compra.item,
            "quantidade": compra.quantidade,
            "preco_unitario": compra.preco_unitario,
            "valor_total": compra.preco_unitario * compra.quantidade,
        }


@router.put("/compras/{id_compra}")
def atualizar_compra(id_compra: int, compra_atualizada: Compra):
    with Session(engine) as session:
        compra = session.get(Compra, id_compra)

        if compra is None:
            raise HTTPException(
                status_code=404, detail=f"Compra {id_compra} não encontrada"
            )

        compra.item = compra_atualizada.item
        compra.preco_unitario = compra_atualizada.preco_unitario
        compra.quantidade = compra_atualizada.quantidade
        compra.valor_total = (
            compra_atualizada.preco_unitario * compra_atualizada.quantidade
        )

        session.add(compra)
        session.commit()
        session.refresh(compra)

        return compra


@router.delete("/compras/{id_compra}")
def deletar_compra(id_compra: int):
    with Session(engine) as session:
        compra = session.get(Compra, id_compra)

        if compra is None:
            raise HTTPException(
                status_code=404, detail=f"Compra {id_compra} não encontrada"
            )

        session.delete(compra)
        session.commit()

        return {"mensagem": "Compra deletada com sucesso"}

from fastapi import HTTPException, status
from sqlmodel import Session, select
from sqlalchemy import func

from app.models import Compra
from app.schemas import CompraCreate


def criar_compra(session: Session, dados: CompraCreate):
    compra_existente = session.exec(
        select(Compra).where(func.lower(Compra.item) == dados.item.lower())
    ).first()

    if compra_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Produto já cadastrado no sistema",
        )

    nova_compra = Compra(
        item=dados.item.upper(),
        preco_unitario=dados.preco_unitario,
        quantidade=dados.quantidade,
        embalagem=dados.embalagem,
        valor_total=dados.preco_unitario * dados.quantidade,
    )

    session.add(nova_compra)
    session.commit()
    session.refresh(nova_compra)

    return nova_compra


def listar_compras(session: Session, item: str | None = None):
    query = select(Compra)

    if item:
        query = query.where(func.lower(Compra.item).contains(item.lower()))

    compras = session.exec(query).all()

    if not compras:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "erro": "Nenhuma compra encontrada",
                "filtro": item,
            },
        )

    return {
        "total": len(compras),
        "compras": compras,
    }


def buscar_compra(session: Session, id_compra: int):
    compra = session.get(Compra, id_compra)

    if compra is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "erro": "Compra não encontrada",
                "id": id_compra,
            },
        )

    return compra


def atualizar_compra(
    session: Session,
    id_compra: int,
    dados: CompraCreate,
):
    compra = buscar_compra(session, id_compra)

    compra_existente = session.exec(
        select(Compra).where(
            func.lower(Compra.item) == dados.item.lower(),
            Compra.id != id_compra,
        )
    ).first()

    if compra_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "erro": "Produto já cadastrado no sistema",
                "item": dados.item.upper(),
            },
        )

    compra.item = dados.item.upper()
    compra.preco_unitario = dados.preco_unitario
    compra.quantidade = dados.quantidade
    compra.embalagem = dados.embalagem
    compra.valor_total = dados.preco_unitario * dados.quantidade

    session.add(compra)
    session.commit()
    session.refresh(compra)

    return {
        "mensagem": "Compra atualizada com sucesso",
        "compra": compra,
    }


def deletar_compra(session: Session, id_compra: int):
    compra = buscar_compra(session, id_compra)

    session.delete(compra)
    session.commit()

    return {
        "mensagem": "Compra deletada com sucesso",
        "id": id_compra,
    }

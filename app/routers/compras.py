from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session, select, func

from app.database import get_session
from app.models import Compra
from app.schemas import CompraCreate, CompraRead

router = APIRouter()


@router.post("/compras", status_code=status.HTTP_201_CREATED)
def criar_compra(compra: CompraCreate, session: Session = Depends(get_session)):
    compra_existente = session.exec(
        select(Compra).where(func.lower(Compra.item) == compra.item.lower())
    ).first()

    if compra_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "erro": "Produto já cadastrado no sistema",
                "item": compra.item.upper(),
            },
        )

    nova_compra = Compra(
        item=compra.item.upper(),
        preco_unitario=compra.preco_unitario,
        quantidade=compra.quantidade,
        valor_total=compra.preco_unitario * compra.quantidade,
    )

    session.add(nova_compra)
    session.commit()
    session.refresh(nova_compra)

    return {
        "mensagem": "Compra cadastrada com sucesso",
        "compra": nova_compra,
    }


@router.get("/compras")
def listar_compras(item: str | None = None, session: Session = Depends(get_session)):
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


@router.get("/compras/{id_compra}", response_model=CompraRead)
def buscar_compra(id_compra: int, session: Session = Depends(get_session)):
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


@router.put("/compras/{id_compra}")
def atualizar_compra(
    id_compra: int,
    compra_atualizada: CompraCreate,
    session: Session = Depends(get_session),
):
    compra = session.get(Compra, id_compra)

    if compra is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "erro": "Compra não encontrada",
                "id": id_compra,
            },
        )

    compra_existente = session.exec(
        select(Compra).where(
            func.lower(Compra.item) == compra_atualizada.item.lower(),
            Compra.id != id_compra,
        )
    ).first()

    if compra_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "erro": "Produto já cadastrado no sistema",
                "item": compra_atualizada.item.upper(),
            },
        )

    compra.item = compra_atualizada.item.upper()
    compra.preco_unitario = compra_atualizada.preco_unitario
    compra.quantidade = compra_atualizada.quantidade
    compra.valor_total = compra_atualizada.preco_unitario * compra_atualizada.quantidade

    session.add(compra)
    session.commit()
    session.refresh(compra)

    return {
        "mensagem": "Compra atualizada com sucesso",
        "compra": compra,
    }


@router.delete("/compras/{id_compra}")
def deletar_compra(id_compra: int, session: Session = Depends(get_session)):
    compra = session.get(Compra, id_compra)

    if compra is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "erro": "Compra não encontrada",
                "id": id_compra,
            },
        )

    session.delete(compra)
    session.commit()

    return {
        "mensagem": "Compra deletada com sucesso",
        "id": id_compra,
    }

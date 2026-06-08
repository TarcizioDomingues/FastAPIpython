from fastapi import APIRouter, status, Depends
from sqlmodel import Session

from app.database import get_session
from app.schemas import CompraCreate, CompraRead
from app.services import compras_service

router = APIRouter()


@router.post("/compras", status_code=status.HTTP_201_CREATED)
def criar_compra(compra: CompraCreate, session: Session = Depends(get_session)):
    return compras_service.criar_compra(session, compra)


@router.get("/compras")
def listar_compras(item: str | None = None, session: Session = Depends(get_session)):
    return compras_service.listar_compras(session, item)


@router.get("/compras/{id_compra}", response_model=CompraRead)
def buscar_compra(id_compra: int, session: Session = Depends(get_session)):
    return compras_service.buscar_compra(session, id_compra)


@router.put("/compras/{id_compra}")
def atualizar_compra(
    id_compra: int,
    compra_atualizada: CompraCreate,
    session: Session = Depends(get_session),
):
    return compras_service.atualizar_compra(
        session,
        id_compra,
        compra_atualizada,
    )


@router.delete("/compras/{id_compra}")
def deletar_compra(id_compra: int, session: Session = Depends(get_session)):
    return compras_service.deletar_compra(session, id_compra)

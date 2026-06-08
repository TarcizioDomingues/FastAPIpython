from sqlmodel import Session, select
from sqlalchemy import func

from app.models import Compra


def buscar_por_item(session: Session, item: str):
    query = select(Compra).where(func.lower(Compra.item) == item.lower())
    return session.exec(query).first()


def criar(session: Session, compra: Compra):
    session.add(compra)
    session.commit()
    session.refresh(compra)
    return compra

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
from app.schemas import UsuarioCreate, UsuarioRead
from app.services.auth_service import cadastrar_usuario

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UsuarioRead)
def register(usuario: UsuarioCreate, session: Session = Depends(get_session)):
    return cadastrar_usuario(usuario, session)

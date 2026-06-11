from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
from app.schemas import UsuarioCreate, UsuarioRead, UsuarioLogin, Token
from app.services.auth_service import cadastrar_usuario, login_usuario

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UsuarioRead)
def register(usuario: UsuarioCreate, session: Session = Depends(get_session)):
    return cadastrar_usuario(usuario, session)


@router.post("/login", response_model=Token)
def login(usuario_login: UsuarioLogin, session: Session = Depends(get_session)):
    return login_usuario(usuario_login, session)

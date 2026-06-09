from fastapi import HTTPException
from sqlmodel import Session, select

from app.models import Usuario
from app.schemas import UsuarioCreate
from app.security import gerar_hash_senha


def cadastrar_usuario(usuario: UsuarioCreate, session: Session) -> Usuario:
    statement = select(Usuario).where(Usuario.username == usuario.username)
    usuario_existente = session.exec(statement).first()

    if usuario_existente:
        raise HTTPException(status_code=400, detail="Username já cadastrado")

    novo_usuario = Usuario(
        username=usuario.username, senha_hash=gerar_hash_senha(usuario.senha)
    )

    session.add(novo_usuario)
    session.commit()
    session.refresh(novo_usuario)

    return novo_usuario

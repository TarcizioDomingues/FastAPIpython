from fastapi import HTTPException
from sqlmodel import Session, select

from app.models import Usuario
from app.schemas import UsuarioCreate, UsuarioLogin
from app.security import gerar_hash_senha, verificar_senha, criar_access_token


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


def login_usuario(usuario_login: UsuarioLogin, session: Session) -> dict:
    statement = select(Usuario).where(Usuario.username == usuario_login.username)
    usuario = session.exec(statement).first()

    if not usuario:
        raise HTTPException(status_code=401, detail="Username ou senha inválidos")

    senha_valida = verificar_senha(usuario_login.senha, usuario.senha_hash)

    if not senha_valida:
        raise HTTPException(status_code=401, detail="Username ou senha inválidos")

    token = criar_access_token({"sub": usuario.username})

    return {"access_token": token, "token_type": "bearer"}

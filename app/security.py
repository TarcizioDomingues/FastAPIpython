from passlib.context import CryptContext
from jose import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "minha-chave-super-secreta"
ALGORITHM = "HS256"


def criar_access_token(data: dict) -> str:
    return jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

def gerar_hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)


def verificar_senha(senha: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha, senha_hash)

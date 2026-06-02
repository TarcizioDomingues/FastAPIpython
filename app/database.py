from sqlmodel import create_engine

DATABASE_URL = "sqlite:///C:/Users/tarci/OneDrive/Documentos/FastAPI/compras.db"

engine = create_engine(DATABASE_URL, echo=True)

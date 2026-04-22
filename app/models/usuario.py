from sqlalchemy import Column, Integer, String
from app.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(200), unique=True, nullable=False)
    password = Column(String(200), nullable=False)

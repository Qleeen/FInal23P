from sqlalchemy import Column, Integer, String
from .database import Base

class Pelicula(Base):
    __tablename__ = "peliculas"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    genero = Column(String)
    anio = Column(Integer)
    clasificacion = Column(String(1))

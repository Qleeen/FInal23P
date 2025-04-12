from sqlalchemy.orm import Session
from . import models, schemas

def get_peliculas(db: Session):
    return db.query(models.Pelicula).all()

def get_pelicula(db: Session, pelicula_id: int):
    return db.query(models.Pelicula).filter(models.Pelicula.id == pelicula_id).first()

def create_pelicula(db: Session, pelicula: schemas.PeliculaCreate):
    db_pelicula = models.Pelicula(**pelicula.dict())
    db.add(db_pelicula)
    db.commit()
    db.refresh(db_pelicula)
    return db_pelicula

def update_pelicula(db: Session, pelicula_id: int, pelicula: schemas.PeliculaUpdate):
    db_pelicula = get_pelicula(db, pelicula_id)
    if db_pelicula:
        for key, value in pelicula.dict().items():
            setattr(db_pelicula, key, value)
        db.commit()
        db.refresh(db_pelicula)
    return db_pelicula

def delete_pelicula(db: Session, pelicula_id: int):
    db_pelicula = get_pelicula(db, pelicula_id)
    if db_pelicula:
        db.delete(db_pelicula)
        db.commit()
    return db_pelicula

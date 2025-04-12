from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from Peliculas import models, schemas, crud

from .database import engine, SessionLocal, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Películas",
    version="1.0.0",
    description="API para gestión de películas"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/peliculas", response_model=schemas.PeliculaOut)
def crear_pelicula(pelicula: schemas.PeliculaCreate, db: Session = Depends(get_db)):
    return crud.create_pelicula(db, pelicula)

@app.get("/peliculas", response_model=list[schemas.PeliculaOut])
def listar_peliculas(db: Session = Depends(get_db)):
    return crud.get_peliculas(db)

@app.get("/peliculas/{pelicula_id}", response_model=schemas.PeliculaOut)
def obtener_pelicula(pelicula_id: int, db: Session = Depends(get_db)):
    db_pelicula = crud.get_pelicula(db, pelicula_id)
    if not db_pelicula:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    return db_pelicula

@app.put("/peliculas/{pelicula_id}", response_model=schemas.PeliculaOut)
def editar_pelicula(pelicula_id: int, pelicula: schemas.PeliculaUpdate, db: Session = Depends(get_db)):
    return crud.update_pelicula(db, pelicula_id, pelicula)

@app.delete("/peliculas/{pelicula_id}")
def eliminar_pelicula(pelicula_id: int, db: Session = Depends(get_db)):
    result = crud.delete_pelicula(db, pelicula_id)
    if not result:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    return {"ok": True, "mensaje": "Película eliminada"}

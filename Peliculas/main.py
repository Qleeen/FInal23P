from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from Peliculas import models, schemas, crud

from .database import engine, SessionLocal, Base

from fastapi.security import OAuth2PasswordRequestForm
from .auth import create_access_token, get_current_user, fake_users_db
from datetime import timedelta

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
def eliminar_pelicula(
    pelicula_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)  
):
    result = crud.delete_pelicula(db, pelicula_id)
    if not result:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    return {"ok": True, "mensaje": "Película eliminada"}


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=400, detail="Credenciales inválidas")
    
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}

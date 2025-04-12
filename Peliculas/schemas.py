from pydantic import BaseModel, constr, conint

class PeliculaBase(BaseModel):
    titulo: constr(min_length=2)
    genero: constr(min_length=4)
    anio: conint(ge=1800, le=2025)
    clasificacion: constr(min_length=1, max_length=1)

class PeliculaCreate(PeliculaBase):
    pass

class PeliculaUpdate(PeliculaBase):
    pass

class PeliculaOut(PeliculaBase):
    id: int

    class Config:
        orm_mode = True

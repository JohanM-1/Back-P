from pydantic import BaseModel, EmailStr, constr

class User(BaseModel):
    nombres: str | None = None
    correo: EmailStr | None = None
    direccion: str | None = None
    contraseña: str | None = None
    apellido: str | None = None
    fecha_n: str | None = None
    rol: str | None = None
    edad: int | None = None
    imagen: str | None = None
    Descripcion: str | None = None
    imagen_fondo: str | None = None  
    id: int |None =None

class UserLogin(BaseModel):
    identifier: str 
    password: str

class Response(BaseModel):
    status: bool
    message: str
    data: User | None = None
    access_token: str | None = None

class Snake(BaseModel):
    nombre3: str  
    nombreCientifico: str 
    reino: str  
    especie: str  
    clase: str  
    genero: str  
    familia: str  

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Annotated

class UserTokenModelResp(BaseModel):
    id: int
    nombre: str
    rol: str

class Usuario(BaseModel):
    correo: EmailStr = Field(..., description="User's email address")
    direccion: str = Field(..., max_length=45, description="User's address")
    contraseña: str = Field(..., max_length=100, description="User's password (hashed)")
    nombre: str = Field(..., max_length=45, description="User's first name")
    apellido: str = Field(..., max_length=45, description="User's last name")
    fecha_n: str = Field(..., max_length=45, description="User's birth date")
    rol: str = Field(..., max_length=45, description="User's role (e.g., admin, user)")
    edad: int = Field(..., description="User's age")

class Comentario(BaseModel):
    contenido: str = Field(..., max_length=1000, description="Comment content")
    fecha_creacion: str = Field(..., max_length=45, description="Comment's creation date")

    report_id_report: int = Field(..., description="Foreign key to Reporte.idReporte")
    usuario_id_usuario: int = Field(..., description="Foreign key to Usuario.idUsuario")

class Serpiente(BaseModel):
    nombre3: str = Field(..., max_length=45, description="Snake's common name")
    nombreCientifico: str = Field(..., max_length=100, description="Snake's scientific name")
    reino: str = Field(..., max_length=45, description="Animal kingdom")
    especie: str = Field(..., max_length=45, description="Snake species")
    clase: str = Field(..., max_length=45, description="Taxonomic class")
    genero: str = Field(..., max_length=45, description="Snake genus")
    familia: str = Field(..., max_length=45, description="Snake family")
    imagen: str = Field(..., max_length=200, description="Snake image URL")
    venenosa: bool = Field(..., description="Is the snake poisonous? True or False")
    descripcion: str = Field(..., max_length=1000, description="Detailed description of the snake sighting, including location, appearance, and behavior.")

class Georeferencia(BaseModel):
    fecha: str = Field(..., max_length=20, description="Date of georeference")
    zona: str = Field(..., max_length=100, description="Georeferenced area")
    coordenadas: str = Field(..., max_length=200, description="Geographic coordinates")

    serpientes_id_serpientes: int = Field(..., description="Foreign key to Serpiente.idSerpiente")
    usuario_id_usuario: int = Field(..., description="Foreign key to Usuario.idUsuario")

class ReporteModel(BaseModel):
    titulo: str = Field(..., max_length=100, description="Report title")
    descripcion: str = Field(..., max_length=1000, description="Detailed description of the snake sighting, including location, appearance, and behavior.")
    imagen: str = Field(..., max_length=200, description="Report image URL")
    
    serpientes_id_serpientes: Optional[Annotated[int, Field(..., description="Foreign key to Serpiente.idSerpiente")]] = None
    usuario_id_usuario: int = Field(..., description="Foreign key to Usuario.idUsuario")

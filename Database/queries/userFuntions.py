
from typing import Dict, Optional, Union
from fastapi import Body
from pydantic import BaseModel
from Database.models.DataBaseModel import async_session, Usuario
from sqlalchemy import func, select , update
from Database.models.PasswordHash import nuevo_token,crear_hash,verificar_hash
from routers.base_models.user import Response, User 

#Insertar un Nuevo usaurio a la db

#interface para guardar la respuesta en este formato


async def insert_usuario(
    
    nombres: str = Body(...),  # Make all parameters mandatory
    correo: str = Body(...),
    direccion: str = Body(...),
    contraseña: str = Body(...),
    apellido: str = Body(...),
    fecha_n: str = Body(...),
    rol: str = Body(...),
    edad: int = Body(...),
    imagen: int = Body(...),
) -> Dict[str, str]:
    """
    Inserts a new user with the provided information into the 'usuarios' table asynchronously.

    Args:
        nombres (str): The name of the user to insert. (required)
        correo (str): The user's email address. (required)
        direccion (str): The user's address. (required)
        contraseña (str): The user's password. (required)
        apellido (str): The user's last name. (required)
        fecha_n (str): The user's birth date (as a string). (required)
        rol (str): The user's role. (required)
        edad (int): The user's age. (required)

    Returns:
        Dict[str, str]: A dictionary with a success message or an error message.
    """

    try:
        async with async_session() as session:
            async with session.begin():
                # Check for existing user with the same name
                existing_user = await session.execute(
                    select(Usuario).where(Usuario.nombre == nombres)
                )
                existing_user = existing_user.scalar()
                if existing_user:
                    return {"error": f"Usuario ya registrado: {existing_user.nombre}"}

                # Create a new user object
                contraseña_hash = await crear_hash(contraseña)
                usuario = Usuario(
                    nombre=nombres,
                    correo=correo,
                    direccion=direccion,
                    contraseña=contraseña_hash,
                    apellido=apellido,
                    fecha_n=fecha_n,
                    rol=rol,
                    edad=edad,
                    imagen=imagen,
                )
                
                session.add(usuario)
                await session.commit()
                session.refresh(usuario)
        return {"message": f"Usuario: {usuario.nombre} agregado exitosamente y su contraseña {usuario.contraseña}"}

    except Exception as e:
        print({"error": f"Error al insertar usuario: {str(e)}"})
        return {"error": f"Error al insertar usuario: {str(e)}"}


async def all_usuarios():
    """
    Retrieves all user information from the 'usuarios' table asynchronously.

    Returns:
        A list of dictionaries, where each dictionary represents a user row.
        On error, returns an informative error message.
    """

    try:
        async with async_session() as session:
            async with session.begin():
                # Fetch all user data using select()
                query = select(Usuario)
                result = await session.execute(query)
                usuarios = tuple(usuario for usuario in result.scalars())  # Extract Usuario objects
                return usuarios    
            
    except Exception as error:
        # Log the error for debugging purposes
        print(f"Error retrieving user data: {error}")
        return {"error": f"An error occurred: {error}"}  # Informative error message

    finally:
        # No explicit engine disposal is necessary within the function scope
        # as the async context manager handles it automatically.
        pass


async def edit_user_DB(id: int, nombre: str, imagen_url: str, Descripcion : str, imagen_fonodo :str):
    try:
        async with async_session() as session:
            async with session.begin():
                stm = select(Usuario).where(Usuario.idUsuario == id)
                
                result = await session.execute(stm)
                user_obj = result.scalar()  # Utilizamos result.scalar() para obtener un único resultado
                
                if user_obj:
                    stmt = (
                        update(Usuario)
                        .where(Usuario.idUsuario == id)
                        .values(nombre=nombre, imagen=imagen_url , Descripcion=Descripcion, imagen_fonodo=imagen_fonodo)
                    )
                    await session.execute(stmt)
                    await session.commit()  # Asegúrate de confirmar los cambios
                    return "success"
                else:
                    return "id no encontrado"
                
    except Exception as error:
        # Manejo de la excepción
        print(f"Se ha producido un error al realizar la búsqueda: {error}")
        return f"Se ha producido un error al realizar la búsqueda: {error}"


async def check_user_email(identifier: str) -> bool:
    try:  
        async with async_session() as session:
            async with session.begin():

                stm = select(Usuario).where(Usuario.correo == identifier)

                result = await session.execute(stm)
                user_obj = result.scalar()  # Utilizamos result.scalar() para obtener un único resultado
                
                if(user_obj):
                    return  True
                else:
                    return False
                
    except Exception as error:
        # Manejo de la excepción
        print(f"Se ha producido un error al realizar la búsqueda: {error}")
        return None

async def get_user_base(identifier: Union[int, str]) -> Optional[Usuario]:
    try:  
        async with async_session() as session:
            async with session.begin():
                if isinstance(identifier, int):
                    stm = select(Usuario).where(Usuario.idUsuario == identifier)
                elif isinstance(identifier, str):
                    stm = select(Usuario).where(Usuario.nombre == identifier)
                else:
                    raise ValueError("El identificador debe ser un entero o una cadena de caracteres")
                
                result = await session.execute(stm)
                user_obj = result.scalar()  # Utilizamos result.scalar() para obtener un único resultado
                
                if(user_obj):
                    return  user_obj
                else:
                    return None
                
    except Exception as error:
        # Manejo de la excepción
        print(f"Se ha producido un error al realizar la búsqueda: {error}")
        return None


async def Login_Verificacion(correo:str,password:str ) -> Response:

    try:  
        async with async_session() as session:
            async with session.begin():
            
                stm = select(Usuario).where(Usuario.correo == correo)
                result = await session.execute(stm)
                user_now = result.scalar()  

                if user_now:
                    #objeto de clase CryptContext para Hasheo de la contraseña
                    
                    if(await verificar_hash(password, user_now.contraseña)): #verificacion de la contraseña

                        user_date = User (
                            nombres= user_now.nombre,
                            correo=user_now.correo,
                            fecha_n=user_now.fecha_n
                        )
                        
                        token = await nuevo_token(user_now.nombre,user_now.idUsuario,user_now.rol)
                        return Response(status=True,message="Inicio de sesión exitoso",access_token=token,data=user_date)
                        
                    else:
                        return Response(status=False,message="Contraseña incorrecta")
                else:
                    return Response(status=False,message="Correo incorrecto")

    except Exception as error:
        # Manejo de la excepción
        return Response(status=False, message=str(error))



        
async def Login_Verificacion(correo:str,password:str ) -> Response:

    try:  
        async with async_session() as session:
            async with session.begin():
            
                stm = select(Usuario).where(Usuario.correo == correo)
                result = await session.execute(stm)
                user_now = result.scalar()  

                if user_now:
                    #objeto de clase CryptContext para Hasheo de la contraseña
                    
                    if(await verificar_hash(password, user_now.contraseña)): #verificacion de la contraseña

                        user_date = User (
                            nombres= user_now.nombre,
                            correo=user_now.correo,
                            fecha_n=user_now.fecha_n,
                            imagen=user_now.imagen,
                            direccion= user_now.direccion,
                            apellido = user_now.apellido,
                            edad = user_now.edad,
                            Descripcion = user_now.Descripcion,
                            imagen_fonodo = user_now.imagen_fonodo,
                            id = user_now.idUsuario,
                        )
                        
                        token = await nuevo_token(user_now.nombre,user_now.idUsuario,user_now.rol)
                        return Response(status=True,message="Inicio de sesión exitoso",access_token=token,data=user_date)
                        
                    else:
                        return Response(status=False,message="Contraseña incorrecta")
                else:
                    return Response(status=False,message="Correo incorrecto")

    except Exception as error:
        # Manejo de la excepción
        return Response(status=False, message=str(error))
    
async def Login_Verificacion_username(username: str, password: str) -> Response:

    try:
        async with async_session() as session:
            async with session.begin():
                stm = select(Usuario).where(Usuario.nombre == username)
                result = await session.execute(stm)
                user_now = result.scalar()

                if user_now:
                    if await verificar_hash(password, user_now.contraseña):
                        user_date = User (
                            nombres= user_now.nombre,
                            correo=user_now.correo,
                            fecha_n=user_now.fecha_n,
                            imagen=user_now.imagen,
                            direccion= user_now.direccion,
                            apellido = user_now.apellido,
                            edad = user_now.edad,
                            Descripcion = user_now.Descripcion,
                            imagen_fonodo = user_now.imagen_fonodo,
                            id = user_now.idUsuario,
                        )
                        token = await nuevo_token(user_now.nombre, user_now.idUsuario, user_now.rol)
                        return Response(status=True, message="Inicio de sesión exitoso", access_token=token, data=user_date)
                    else:
                        return Response(status=False, message="Contraseña incorrecta")
                else:
                    return Response(status=False, message="Nombre de usuario incorrecto")

    except Exception as error:
        return Response(status=False, message=str(error))

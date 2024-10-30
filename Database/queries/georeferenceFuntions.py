from typing import Dict
from fastapi import Body
from Database.models.DataBaseModel import Georeferencia, async_session, Usuario, Reporte
from sqlalchemy import select
from Database.models.PasswordHash import crear_hash
from routers.base_models.user import Response 



async def insert_georeferencia(
    fecha: str = Body(...),
    zona: str = Body(...),
    coordenadas: str = Body(...),
    serpientes_id_serpientes: int = Body(...),
    usuario_id_usuario: int = Body(...),
) -> Dict[str, str]:
  """
  Inserts a new georeference record with the provided information into the 'georeferencia' table asynchronously.

  Args:
      fecha (str): The date of the georeference. (required)
      zona (str): The zone where the georeference was taken. (required)
      coordenadas (str): The coordinates of the georeference. (required)
      serpientes_id_serpientes (int): The ID of the associated snake record in the 'serpientes' table. (required)
      usuario_id_usuario (int): The ID of the associated user record in the 'usuario' table. (required)

  Returns:
      Dict[str, str]: A dictionary with a success message or an error message.
  """
  
  try:
    async with async_session() as session:
      async with session.begin():
        # Create a new georeference object
        georeferencia = Georeferencia(
            fecha=fecha,
            zona=zona,
            coordenadas=coordenadas,
            serpientes_id_serpientes=serpientes_id_serpientes,
            usuario_id_usuario=usuario_id_usuario,
            desarrollador_id_desarrollador = 1
        )

        session.add(georeferencia)
        await session.commit()
        session.refresh(georeferencia)
        return {
            "message": f"Georeferencia creada exitosamente: ID {georeferencia.idGeoreferencia}"
        }

  except Exception as e:
    print({"error": f"Error al insertar georeferencia: {str(e)}"})
    return {"error": f"Error al insertar georeferencia: {str(e)}"}


async def all_georeferencias():
    """
    Retrieves all georeferencias information from the 'Georeferencia' table asynchronously.

    Returns:
        A list of dictionaries, where each dictionary represents a georeferencias row.
        On error, returns an informative error message.
    """

    try:
        async with async_session() as session:
            async with session.begin():
                # Fetch all user data using select()
                query = select(Georeferencia)
                result = await session.execute(query)
                usuarios = tuple(georeferencias for georeferencias in result.scalars())  # Extract Georeferencia objects
                return usuarios  
            
    except Exception as error:
        # Log the error for debugging purposes
        print(f"Error retrieving user data: {error}")
        return {"error": f"An error occurred: {error}"}  # Informative error message

    finally:
        # No explicit engine disposal is necessary within the function scope
        # as the async context manager handles it automatically.
        pass
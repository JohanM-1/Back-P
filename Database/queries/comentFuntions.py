from typing import Dict
from fastapi import Body
from Database.models.DataBaseModel import  async_session 
from Database.models.DataBaseModel import Comentario as ComentarioDb
from routers.base_models.all_base_model import Comentario as ComentarioModel
from sqlalchemy import select



async def insert_coment(
    formComentario:ComentarioModel
) -> Dict[str, str]:
    """
    Inserts a new developer record with the provided information into a table (assuming the table name is 'desarrollador') asynchronously.

    Args:
        nombre2 (str): The developer's name. (required, max length 20)
        direccion2 (str): The developer's address. (required, max length 45)

    Returns:
        Dict[str, str]: A dictionary with a success message or an error message.
    """

    try:
        async with async_session() as session:
            async with session.begin():
                # Create a new developer object (assuming the table name is 'desarrollador')
                newComent = ComentarioDb(
                    contenido = formComentario.contenido,
                    fecha_creacion = formComentario.fecha_creacion,
                    reporte_id_reporte = formComentario.report_id_report,
                    usuario_id_usuario = formComentario.report_id_report,
                )

                session.add(newComent)
                await session.commit()
                session.refresh(newComent)
                return {
                    "message": f"Desarrollador creado exitosamente: ID {newComent.idComentario}"  # Assuming an id field exists
                }

    except Exception as e:
        print({"error": f"Error al insertar desarrollador: {str(e)}"})
        return {"error": f"Error al insertar desarrollador: {str(e)}"}


async def all_coments_for_reportId(idReport:int):
    """
    Retrieves all developer information from the 'desarrollador' table asynchronously.

    Returns:
        List[Dict[str, str]]: A list of dictionaries, where each dictionary represents a developer row.
        On error, returns an informative error message.
    """

    try:
        async with async_session() as session:
            async with session.begin():
                # Fetch all developer data using select()
                query = select(ComentarioDb)
                result = await session.execute(query)
                ComentarioDb = tuple(ComentarioDb for ComentarioDb in result.scalars())  # Extract Desarrollador objects
                return ComentarioDb

    except Exception as error:
        # Log the error for debugging purposes
        print(f"Error retrieving developer data: {error}")
        return {"error": f"An error occurred: {error}"}  # Informative error message
from __future__ import annotations
from fastapi import APIRouter
from Database.queries.georeferenceFuntions import all_georeferencias,insert_georeferencia
from .base_models.all_base_model import Georeferencia


router = APIRouter()

@router.post("/Georeference/create", tags=["Georeference"])
async def create_Georeference(Georeferencia_data: Georeferencia):
    response = await insert_georeferencia(
        fecha = Georeferencia_data.fecha,
        zona = Georeferencia_data.zona,
        coordenadas = Georeferencia_data.coordenadas,
        serpientes_id_serpientes = Georeferencia_data.serpientes_id_serpientes,
        usuario_id_usuario = Georeferencia_data.usuario_id_usuario
    )
    return response


@router.get("/Georeference/all", tags=["Georeference"])
async def get_all_Georeference():
    response = await all_georeferencias()
    return response
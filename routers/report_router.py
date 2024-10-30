from __future__ import annotations
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from Database.queries.reportsFuntions import (
    get_report_base,
    get_report_base_user_id,
    insert_report,
    all_reportes,
    update_report,
    delete_report,
)
from routers.user_router import get_current_active_user
from .base_models.all_base_model import ReporteModel, UserTokenModelResp


router = APIRouter()

@router.post("/Reporte/create", tags=["Reporte"])
async def create_Report(
    Reporte_data: ReporteModel,
    current_user: Annotated[UserTokenModelResp, Depends(get_current_active_user)]
):
    Reporte_data.usuario_id_usuario = current_user.id
    response = await insert_report(Reporte_data)
    return response

@router.get("/users/me/items/", tags=["Reporte"])
async def read_own_items(current_user: Annotated[UserTokenModelResp, Depends(get_current_active_user)]):
    return (current_user.id)

@router.get("/Reporte/id", tags=["Reporte"])
async def get_report_id(id: int):
    response = await get_report_base(id)
    if response is not None:
        return response
    else:
        raise HTTPException(status_code=404, detail=f"Id no encontrado: {id}")

@router.get("/Reporte/all_me", tags=["Reporte"])
async def get_report_id_user(current_user: Annotated[UserTokenModelResp, Depends(get_current_active_user)]):
    response = await get_report_base_user_id(current_user.id)
    if response is not None:
        return response
    else:
        raise HTTPException(status_code=404, detail=f"Id no encontrado: {current_user.id}")

@router.get("/Reporte/all_id", tags=["Reporte"])
async def get_report_id_user(id: int):
    response = await get_report_base_user_id(id)
    if response is not None:
        return response
    else:
        raise HTTPException(status_code=404, detail=f"Id no encontrado: {id}")

@router.get("/Reporte/all", tags=["Reporte"])
async def all_reports():
    response = await all_reportes()
    return response

class report_part(BaseModel):
    titulo: str = Field(..., max_length=100, description="Report title")
    descripcion: str = Field(..., max_length=1000, description="Detailed description of the snake sighting, including location, appearance, and behavior.")

@router.patch("/Reporte/Actualizar", tags=["Reporte"])
async def update_report_id(id: int, report_part: report_part):
    id_verif = await get_report_id(id)
    if id_verif is not None:
        response = await update_report(
            id,
            titulo=report_part.titulo,
            descripcion=report_part.descripcion
        )
        return response
    else:
        raise HTTPException(status_code=404, detail=f"Id no encontrado: {id}")

@router.delete("/Reporte/Eliminar", tags=["Reporte"])
async def delete_report_id(id: int, current_user: Annotated[UserTokenModelResp, Depends(get_current_active_user)]):
    id_verif = await get_report_id(id)
    if id_verif is not None:
        response = await delete_report(id, current_user.id)
        return response
    else:
        raise HTTPException(status_code=404, detail=f"Id no encontrado: {id}")

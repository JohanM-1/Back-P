from __future__ import annotations
from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field
from Database.queries.snakeFuntions import (
    all_Snakes_poison,
    get_snake_base,
    insert_serpiente,
    all_Snakes,
    delete_snake,
)
from .base_models.all_base_model import Serpiente
from pathlib import Path
import os
import uuid
from typing import List

router = APIRouter()

images_dir = "images"
Path(images_dir).mkdir(parents=True, exist_ok=True)

ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}

@router.post("/upload_image", tags=["Files"])
async def create_upload_file(image: UploadFile):
    uid = uuid.uuid4().hex
    filename = f"{uid}.{image.filename.split('.')[-1]}"

    extension = filename.split(".")[-1].lower() 
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(status_code=415, detail="Unsupported image format")

    image_path = os.path.join(images_dir, filename)
    with open(image_path, "wb") as f:
        f.write(image.file.read())

    image_url = f"{filename}"
    return {"image_url": image_url}

@router.get("/view_image/")
async def view_image(imagen: str):
    image_path = os.path.join(images_dir, imagen)
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")
    
    return FileResponse(image_path)

@router.get("/get_all_images/")
async def get_all_images():
    if not os.path.exists(images_dir):
        raise HTTPException(status_code=404, detail="Images directory not found")

    images = os.listdir(images_dir)
    if not images:
        return JSONResponse(content={"images": []}) 

    images_list = [
        {"name": img, "url": f"/view_image?imagen={img}"}
        for img in images
        if img.split('.')[-1].lower() in ALLOWED_IMAGE_EXTENSIONS
    ]

    return JSONResponse(content={"images": images_list})

@router.get("/snake/id", tags=["Snake"])
async def get_snake_id(id: int):
    response = await get_snake_base(id)
    if response is not None:
        return response
    else:
        raise HTTPException(status_code=404, detail=f"Id no encontrado: {id}")

@router.post("/snake/create", tags=["Snake"])
async def post_snake_create(serpiente: Serpiente):
    response = await insert_serpiente(serpiente)
    return response

@router.delete("/snake/delete", tags=["Snake"])
async def delete_snake_id(id: int):
    id_verif = await get_snake_id(id)
    if id_verif is not None:
        response = await delete_snake(id)
        return response
    else:
        raise HTTPException(status_code=404, detail=f"Id no encontrado: {id}")

@router.get("/Snake/all", tags=["Snake"])
async def get_all_snakes():
    response = await all_Snakes()
    return response

@router.get("/Snakes/poison", tags=["Snake"])
async def get_all_snakes(valid: bool):
    response = await all_Snakes_poison(valid)
    return response

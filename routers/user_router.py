from __future__ import annotations
import json
from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import firebase_admin
from httplib2 import Credentials
from sqlalchemy.orm import sessionmaker
from typing import Annotated, Dict
from Database.models.DataBaseModel import Usuario, engine
from Database.models.PasswordHash import verificar_token
from Database.queries.userFuntions import  Login_Verificacion_username, check_user_email, edit_user_DB, insert_usuario,all_usuarios,Login_Verificacion
from routers.base_models.all_base_model import UserTokenModelResp


from .base_models.user import User,UserLogin,Response



from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from firebase_admin import auth,credentials

cred = credentials.Certificate('./meta-snake-firebase-adminsdk-bu6li-0923f24189.json')
default_app = firebase_admin.initialize_app(cred)
router = APIRouter()


class Token (BaseModel):
    access_token: str
    token_type: str


@router.post("/users/create", tags=["users"])
async def create_user(user_data:User):
    response = await insert_usuario(            
            nombres=user_data.nombres,
            correo=user_data.correo,
            direccion=user_data.direccion,
            contraseña=user_data.contraseña,
            apellido=user_data.apellido,
            fecha_n=user_data.fecha_n,
            rol="usuario",
            edad=user_data.edad,
            imagen=user_data.imagen,
            )
    return response


@router.post("/users/google-auth", tags=["users"])
async def get_user_id(id:str):
    try:
        user = auth.get_user(id)
        print(user.email)
        print(user.photo_url)
        bool = await check_user_email(user.email)
        if( bool == False):
            await insert_usuario(            
            nombres=user.display_name,
            correo=user.email,
            direccion= "",
            contraseña= id,
            apellido="",
            fecha_n= "null",
            rol= "usuario",
            edad= 0,
            imagen= user.photo_url,
            )

            response = await Login_Verificacion(user.email, id)
            return response
        else:
            response = await Login_Verificacion(user.email, id)
            return response
        
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )




@router.get("/users/all", tags=["users"])
async def get_all_users():
    print(default_app.name)
    try:
        user = auth.get_user("yjFmIs1SPCWLcwMm4PEWBsXTu8U2")
        print(user.display_name)
    except:
        print("error")
    response = await all_usuarios()
    return response



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await Login_Verificacion(form_data.username,form_data.password)
    if (user.status == False):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=user.access_token, token_type="bearer")


async def verificar_token_route(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
        
    var = await verificar_token(token)

    if (var is not UserTokenModelResp):
        return var
    else:
        
        raise credentials_exception

async def get_current_active_user(
    current_user: Annotated[User, Depends(verificar_token_route)],
):
    return current_user

@router.get("/users/me/", response_model=UserTokenModelResp,tags=["users"])
async def read_users_me(
    current_user: Annotated[UserTokenModelResp, Depends(get_current_active_user)],
):
    return current_user


class Usuario_Edit(BaseModel):
    
    nombre: str 
    imagenurl: str 
    imagen_fonodo: str | None = None
    Descripcion: str | None = None


@router.post("/usuario/edit", tags=["users"])
async def edit_user_route(
    data: Usuario_Edit,
    current_user: Annotated[UserTokenModelResp, Depends(get_current_active_user)]
    ):
    
    response = await edit_user_DB(
        id=current_user.id,
        nombre= data.nombre,
        imagen_url= data.imagenurl,
        imagen_fonodo= data.imagen_fonodo,
        Descripcion=data.Descripcion,

    )

    return response



@router.post("/users/login", tags=["users"])
async def login_user_route(user_data: UserLogin):
    if "@" in user_data.identifier:
        # Verificación por correo electrónico
        Response = await Login_Verificacion(user_data.identifier, user_data.password)
    else:
        # Verificación por nombre de usuario
        Response = await Login_Verificacion_username(user_data.identifier, user_data.password)

    if Response.status:
        return Response
    else:
        raise HTTPException(status_code=401, detail=Response.message)
    
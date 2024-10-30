from fastapi import FastAPI
import firebase_admin
from routers import user_router,snake_router,georefence_router,report_router,aiGenerate  # Import the router object

from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir acceso desde cualquier origen
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Métodos HTTP permitidos
    allow_headers=["*"],  # Permitir todos los encabezados en las solicitudes
)


# Include the router in the app
app.include_router(user_router.router)
app.include_router(snake_router.router)
app.include_router(georefence_router.router)
app.include_router(report_router.router)
app.include_router(aiGenerate.router)
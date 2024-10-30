import json
import typing
import google.generativeai as genai
import os
from fastapi import  APIRouter, HTTPException, UploadFile
import uuid
from pathlib import Path
from googleapiclient.errors import HttpError
import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

def to_markdown(text : str):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))



router = APIRouter()

# Definimos una carpeta para guardar las imágenes
images_dir = "images"

# Creamos la carpeta si no existe
Path(images_dir).mkdir(parents=True, exist_ok=True)

ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}



@router.post("/snakeidentify",tags=["Files"])
async def create_upload_file(image: UploadFile):
    class ResponseJson(typing.TypedDict):
        title: str
        body: str
        venomous: bool
    
    # Generate a unique identifier (UID) using UUID
    uid = uuid.uuid4().hex

    # Construct the filename using the UID and the original filename extension
    filename = f"{uid}.{image.filename.split('.')[-1]}"

    extension = filename.split(".")[-1].lower()  # Get lowercase extension
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(status_code=415, detail="Unsupported image format")


    # Save the image to the specified location using the UID-based filename
    image_path = os.path.join("images", filename)
    with open(image_path, "wb") as f:
        f.write(image.file.read())

    # Generate the URL to access the uploaded image
    image_url = f"{filename}"
    genai.configure(api_key=os.environ["API_KEY"])


    myfile = genai.upload_file("images/"+image_url)
    print(f"{myfile=}")

    model = genai.GenerativeModel("gemini-1.5-flash")

    class Recipe(typing.TypedDict):
        name: str
        description: str
        venomous: bool
        issnake: bool



    result = model.generate_content(
        ["Analyze the image of a snake by carefully observing its physical characteristics, such as color, pattern, size, head shape, and any other visible details (e.g., eyes, fangs, or scales). Also, take into account the environment or habitat, if visible. Based on this information, identify the possible species of the snake and propose a scientific name that matches the observed characteristics. The response should be in Spanish.", myfile],
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json", response_schema=Recipe
        ),
    )

    
    if os.path.exists("images/"+image_url):
        os.remove("images/"+image_url)
        print("La imagen ha sido eliminada exitosamente.")
    

    formatted_json = json.loads(result.text)
    return (formatted_json) 




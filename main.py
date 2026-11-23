from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI(title="Trivia App")
templates = Jinja2Templates(directory="templates")

preguntas_db = [
    {
        "id": 1,
        "pregunta": "¿Cuál es la capital de Colombia?",
        "opciones": ["Medellín", "Bogotá", "Cali", "Cartagena"],
        "respuesta": 1
    },
    {
        "id": 2,
        "pregunta": "¿En qué año llegó el hombre a la luna?",
        "opciones": ["1965", "1969", "1972", "1959"],
        "respuesta": 1
    }
]

class Respuesta(BaseModel):
    pregunta_id: int
    opcion_elegida: int

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "preguntas": preguntas_db})

@app.get("/preguntas")
def get_preguntas():
    return preguntas_db

@app.post("/verificar")
def verificar_respuesta(datos: Respuesta):
    for p in preguntas_db:
        if p["id"] == datos.pregunta_id:
            es_correcta = p["respuesta"] == datos.opcion_elegida
            return {"correcta": es_correcta}
    return {"error": "Pregunta no encontrada"}

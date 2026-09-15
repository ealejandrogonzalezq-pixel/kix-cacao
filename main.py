from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import json, os

app = FastAPI(title="KIX - Biblioteca Mundial de Cacao")

# Datos base de la biblioteca
VARIEDADES = [
    {"nombre": "Criollo", "origen": "Centroamérica", "sabor": "Fino, frutal", "resistencia": "Baja"},
    {"nombre": "Forastero", "origen": "Amazonas", "sabor": "Fuerte, amargo", "resistencia": "Alta"},
    {"nombre": "Trinitario", "origen": "Trinidad", "sabor": "Equilibrado", "resistencia": "Media"},
    {"nombre": "Nacional", "origen": "Ecuador", "sabor": "Floral", "resistencia": "Media"}
]

ENFERMEDADES = [
    {"nombre": "Moniliasis", "sintoma": "Fruto se pone café y polvoso", "solucion": "Poda sanitaria + caldo bordelés"},
    {"nombre": "Escoba de bruja", "sintoma": "Ramas hinchadas como escoba", "solucion": "Poda y quemar ramas enfermas"},
    {"nombre": "Phytophthora", "sintoma": "Mazorcas negras", "solucion": "Drenaje y fungicida orgánico"}
]

@app.get("/")
def inicio():
    return FileResponse("static/index.html")

@app.get("/api/variedades")
def get_variedades():
    return VARIEDADES

@app.get("/api/enfermedades")
def get_enfermedades():
    return ENFERMEDADES

# Para guardar PDFs y fotos de fincas
os.makedirs("biblioteca", exist_ok=True)

@app.get("/api/biblioteca")
def listar_biblioteca():
    archivos = os.listdir("biblioteca")
    return archivos

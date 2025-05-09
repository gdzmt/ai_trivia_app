import os
import json
import re
from dotenv import load_dotenv
from openai import OpenAI
import anthropic

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def generar_pregunta_y_respuestas(proveedor="openai"):
    return "¿Qué haces en tu tiempo libre?", ["ver televisión", "leer", "salir con amigos", "jugar videojuegos", "hacer ejercicio"]

def validar_respuesta_con_modelo(pregunta, lista_respuestas, respuesta_usuario, proveedor="openai"):
    return False, -1

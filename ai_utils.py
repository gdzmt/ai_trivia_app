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
    prompt = (
        "Genera una sola pregunta estilo '100 personas dijeron' y dame 5 respuestas comunes "
        "para esa pregunta. Responde en formato JSON así:\n"
        "{\n  \"pregunta\": \"...\",\n  \"respuestas\": [\"respuesta1\", \"respuesta2\", ...]\n}"
    )

    if proveedor == "openai":
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.choices[0].message.content
    else:
        response = anthropic_client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.content[0].text

    try:
        data = json.loads(content)
        pregunta = data["pregunta"]
        respuestas = [r.strip().lower() for r in data["respuestas"]]
        return pregunta, respuestas
    except:
        return "¿Qué haces en tu tiempo libre?", ["ver televisión", "leer", "salir con amigos", "jugar videojuegos", "hacer ejercicio"]

def validar_respuesta_con_modelo(pregunta, lista_respuestas, respuesta_usuario, proveedor="openai"):
    prompt = (
        f"Pregunta: {pregunta}\n"
        f"Respuestas consideradas válidas: {', '.join(lista_respuestas)}\n"
        f"¿La respuesta '{respuesta_usuario}' se puede considerar equivalente a alguna de las anteriores? "
        "Considera sinónimos, acentos, puntuación o formas similares de decir lo mismo. "
        "Responde solo con 'sí' o 'no', y si es sí, di el número (1 al 5) de la respuesta equivalente."
    )

    if proveedor == "openai":
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.choices[0].message.content.strip().lower()
    else:
        response = anthropic_client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.content[0].text.strip().lower()

    if "sí" in content:
        match = re.search(r"(\d+)", content)
        if match:
            return True, int(match.group(1))
        return True, -1
    return False, -1

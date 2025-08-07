import os
import sys
import logging
import time
import re
import json
import requests
from requests.exceptions import RequestException
import openai

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# Configura tu API Key de OpenAI desde la variable de entorno
try:
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("La variable de entorno OPENAI_API_KEY no está configurada.")
except ValueError as e:
    logger.error("Error de configuración: %s", e)
    sys.exit(1)


def fetch_html(url: str, timeout: int = 5) -> str:
    """
    Descarga el HTML de la URL usando requests, con manejo de errores y timeout.
    Devuelve el texto HTML o cadena vacía en caso de error.
    """
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        return resp.text
    except RequestException as e:
        logger.error("Error al descargar %s: %s", url, e)
        return ""


def ai_select_fields(news_html: str, url: str) -> dict | None:
    """
    Usa GPT-4o para identificar dinámicamente los campos relevantes en el HTML de una noticia.
    Devuelve un dict con las claves: "title", "kicker", "link", "image_url".
    Si falta alguna clave, se asigna None. Retorna None en caso de error.
    """
    prompt = (
        "Eres un asistente experto en scraping de noticias.\n"
        "Analiza el siguiente fragmento de HTML que contiene UNA noticia.\n"
        "Identifica dinámicamente el Título, Kicker (volanta), Enlace (link a la nota), e Imagen principal.\n"
        "Si algún campo no está presente, usa null.\n"
        "Devolvé SOLO el resultado en JSON con las claves: "
        "\"title\", \"kicker\", \"link\", \"image_url\".\n"
        "No incluyas ningún otro texto en la respuesta.\n\n"
        "Ejemplo de formato de salida:\n"
        "{\n"
        '  "title": "Título de la noticia",\n'
        '  "kicker": "Volanta o subtítulo",\n'
        '  "link": "https://www.ejemplo.com/noticia-completa",\n'
        '  "image_url": "https://www.ejemplo.com/imagen.jpg"\n'
        "}\n\n"
        f"El link original de la nota es: {url}\n\n"
        "HTML:\n"
        "```html\n"
        f"{news_html}\n"
        "```"
    )

    # Intentar hasta 3 reintentos en caso de errores transitorios
    for attempt in range(3):
        try:
            resp = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Eres un asistente experto en análisis de HTML para extracción de datos."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,
                timeout=10
            )
            content = resp.choices[0].message.content.strip()
            # Eliminar posibles bloques de código ```json ... ```
            content = re.sub(r"^```(?:json)?|```$", "", content, flags=re.MULTILINE).strip()
            data = json.loads(content)
            # Asegurar que existan todas las keys
            for key in ("title", "kicker", "link", "image_url"):
                data.setdefault(key, None)
            return data

        except openai.APIError as e:
            logger.warning("APIError en intento %d: %s", attempt + 1, e)
            if attempt < 2:
                time.sleep(2 ** attempt)
                continue
            logger.error("No se pudo completar la petición a la API tras 3 intentos.")
            return None
        except json.JSONDecodeError:
            logger.error("La respuesta de la API no es un JSON válido:\n%s", content)
            return None
        except Exception as e:
            logger.exception("Error inesperado al llamar a la API:")
            return None


if __name__ == "__main__":
    # Ejemplo de uso
    sample_url = "https://ejemplo.com/noticia-ejemplo"
    sample_html = fetch_html(sample_url)
    if not sample_html:
        logger.error("No se pudo obtener el HTML de la URL de ejemplo.")
        sys.exit(1)

    extracted = ai_select_fields(sample_html, sample_url)
    if extracted:
        print(json.dumps(extracted, indent=2, ensure_ascii=False))
    else:
        logger.error("No se logró extraer los datos de la noticia.")

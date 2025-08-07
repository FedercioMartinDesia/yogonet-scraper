import os
import openai
import json
import requests
from requests.exceptions import RequestException

# Configura tu API Key de OpenAI desde la variable de entorno
try:
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("La variable de entorno OPENAI_API_KEY no está configurada.")
except ValueError as e:
    print(f"Error de configuración: {e}")
    exit()

def ai_select_fields(news_html, url):
    """
    Usa GPT-4o para identificar dinámicamente los campos relevantes en el HTML de una noticia.
    Devuelve un dict con las claves: "title", "kicker", "link", "image_url".
    Maneja errores de conexión y de formato JSON.
    """
    prompt = f"""
    Eres un asistente experto en scraping de noticias.
    Analiza el siguiente fragmento de HTML que contiene UNA noticia.
    Identifica dinámicamente el Título, Kicker (volanta), Enlace (link a la nota), e Imagen principal.
    Si algún campo no está presente, usa null.
    Devolvé SOLO el resultado en JSON con las claves: "title", "kicker", "link", "image_url".
    No incluyas ningún otro texto en la respuesta.
    
    Ejemplo de formato de salida:
    {{
      "title": "Título de la noticia",
      "kicker": "Volanta o subtítulo",
      "link": "https://www.ejemplo.com/noticia-completa",
      "image_url": "https://www.ejemplo.com/imagen.jpg"
    }}

    El link original de la nota es: {url}

    HTML:
    ```html
    {news_html}
    ```
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Eres un asistente experto en análisis de HTML para extracción de datos."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0
        )
        
        # Obtener el contenido de la respuesta y eliminar bloques de código si existen
        content = response.choices[0].message.content.strip()
        if content.startswith("```json"):
            content = content.strip("```json").strip()
        
        # Intentar parsear la respuesta como JSON
        result_json = json.loads(content)
        
        return result_json

    except json.JSONDecodeError:
        print("Error: La respuesta de la API no es un JSON válido.")
        return None
    except openai.APIError as e:
        print(f"Error de la API de OpenAI: {e}")
        return None
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return None

# Ejemplo de uso (opcional)
if __name__ == '__main__':
    # Simulación de HTML de una noticia
    sample_html = """
    <html>
    <body>
        <h1>Título de ejemplo de la noticia</h1>
        <p>Este es el kicker, una volanta descriptiva.</p>
        <a href="/noticia-ejemplo">Leer más</a>
        <img src="https://ejemplo.com/imagen.jpg" alt="Imagen principal">
    </body>
    </html>
    """
    sample_url = "https://ejemplo.com/noticia-ejemplo"

    extracted_data = ai_select_fields(sample_html, sample_url)
    if extracted_data:
        print(json.dumps(extracted_data, indent=2))
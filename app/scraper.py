import os
import openai
import re
import json
import requests

openai.api_key = os.environ.get("OPENAI_API_KEY")

def ai_select_fields(news_html, url):
    prompt = f"""
Eres un asistente experto en scraping de noticias.
Analiza el siguiente fragmento de HTML que contiene UNA noticia.
Identifica dinámicamente el Título, Kicker (volanta), Enlace (link a la nota), e Imagen principal.
Devolvé SOLO el resultado en JSON con las claves: "title", "kicker", "link", "image_url".

El link original de la nota es: {url}

HTML:
```html
{news_html}

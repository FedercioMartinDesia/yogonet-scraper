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


















# Codigo viejo
# import requests
# from bs4 import BeautifulSoup
# def scrape_news_data(url):
#     """
#     Extrae los datos principales de la noticia.
#     Args:
#         url (str): URL de la noticia
#     Returns:
#         dict: {
#             "title": str or None,
#             "kicker": str or None,
#             "image": str or None,
#             "link": str
#         }
#     """
#     try:
#         # Descargar el HTML de la página
#         response = requests.get(url)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.text, "html.parser")

#         # Título (h1)
#         h1 = soup.find("h1")
#         title = h1.get_text(strip=True) if h1 else None

#         # Kicker (volanta)
#         kicker_div = soup.find("div", class_="volanta_noticia fuente_roboto_slab")
#         kicker = kicker_div.get_text(strip=True) if kicker_div else None

#         # Imagen principal (src que comienza con "https://imagenesyogonet.b-cdn.net")
#         image = None
#         for img in soup.find_all("img"):
#             src = img.get("src", "")
#             if src.startswith("https://imagenesyogonet.b-cdn.net"):
#                 image = src
#                 break

#         return {
#             "title": title,
#             "kicker": kicker,
#             "image": image,
#             "link": url
#         }

#     except Exception as e:
#         # Si ocurre algún error, devolvemos None en los campos (menos link)
#         print(f"Error al scrapear {url}: {e}")
#         return {
#             "title": None,
#             "kicker": None,
#             "image": None,
#             "link": url
#         }

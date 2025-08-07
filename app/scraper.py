import os
import sys
import logging
import time
import re
import json
import requests
from requests.exceptions import RequestException
import openai
import anthropic                             # pip install anthropic
from bs4 import BeautifulSoup                # pip install beautifulsoup4

# --- Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# --- Config OpenAI ---
try:
    openai.api_key = os.environ["OPENAI_API_KEY"]
except KeyError:
    logger.error("OPENAI_API_KEY no configurada")
    sys.exit(1)

# --- Config Claude ---

claude = None
if "ANTHROPIC_API_KEY" in os.environ:
    claude = anthropic.Client()               
    claude.api_key = os.environ["ANTHROPIC_API_KEY"]
else:
    logger.warning("ANTHROPIC_API_KEY no configurada, salto fallback a Claude")


def fetch_html(url: str, timeout: int = 5) -> str:
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        return resp.text
    except RequestException as e:
        logger.error("Error al descargar %s: %s", url, e)
        return ""

def ai_select_fields_openai(html: str, url: str, model: str = "gpt-3.5-turbo") -> dict | None:
    prompt = (
        "Eres un asistente experto en scraping de noticias.\n"
        "Extrae SOLO un JSON con las claves: title, kicker, link, image_url.\n"
        f"URL: {url}\n"
        "HTML:\n```html\n" + html + "\n```"
    )
    for attempt in range(3):
        try:
            resp = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "Eres un asistente..."}, 
                    {"role": "user",   "content": prompt}
                ],
                temperature=0.0,
                timeout=10
            )
            content = resp.choices[0].message.content.strip()
            content = re.sub(r"^```(?:json)?|```$", "", content, flags=re.MULTILINE).strip()
            data = json.loads(content)
            for key in ("title","kicker","link","image_url"):
                data.setdefault(key, None)
            logger.info("Datos extraídos con OpenAI")
            return data
        except Exception as e:
            logger.warning("OpenAI fallo (intento %d): %s", attempt+1, e)
            time.sleep(2**attempt)
    return None

def ai_select_fields_claude(html: str, url: str, model: str = "claude-2.1") -> dict | None:
    if claude is None:
        return None
    prompt = (
        f"{anthropic.HUMAN_PROMPT}"
        "Eres un asistente experto en scraping de noticias.\n"
        "Devuelve SOLO un JSON con keys: title, kicker, link, image_url.\n"
        f"URL: {url}\n"
        "HTML:\n```html\n" + html + "\n```"
        f"{anthropic.AI_PROMPT}"
    )
    try:
        resp = claude.completions.create(
            model=model,
            prompt=prompt,
            max_tokens_to_sample=512,
            temperature=0.0
        )
        content = resp.completion.strip()
        data = json.loads(content)
        for key in ("title","kicker","link","image_url"):
            data.setdefault(key, None)
        logger.info("Datos extraídos con Claude")
        return data
    except Exception as e:
        logger.warning("Claude fallo: %s", e)
        return None

def fallback_parse(html: str, url: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    title  = soup.find("h1")
    kicker = soup.find("p")
    link   = soup.find("a", href=True)
    img    = soup.find("img", src=True)
    data = {
        "title":  title.get_text(strip=True) if title else None,
        "kicker": kicker.get_text(strip=True) if kicker else None,
        "link":   link["href"] if link else url,
        "image_url": img["src"] if img else None
    }
    logger.info("Datos extraídos con fallback HTML")
    return data

def scrape_news_data(url: str) -> dict:
    html = fetch_html(url)
    if not html:
        logger.error("No se pudo descargar %s", url)
        return fallback_parse("", url)

    # 1. Intento OpenAI
    data = ai_select_fields_openai(html, url)
    if data:
        return data

    # 2. Intento Claude
    data = ai_select_fields_claude(html, url)
    if data:
        return data

    # 3. Fallback
    return fallback_parse(html, url)

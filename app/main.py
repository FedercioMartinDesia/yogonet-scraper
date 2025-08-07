import os
import sys
import logging

# --- Manejo seguro de la key desde env ---
if "GCP_CREDS_JSON" in os.environ:
    creds_path = "/tmp/creds.json"
    with open(creds_path, "w") as f:
        f.write(os.environ["GCP_CREDS_JSON"])
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_path

from scraper import scrape_news_data
from processor import process_news_data
from bq_loader import insert_row_to_bigquery

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

def main():
    # URL a scrapear
    news_url = (
        "https://www.yogonet.com/international/news/2024/06/04/"
        "72489-malta-gaming-authority-inks-mou-with-ontario-regulator-to-strengthen-collaborative-efforts"
    )

    # Extraer datos
    scraped_data = scrape_news_data(news_url)

    if not scraped_data:
        logger.error("❌ No se extrajeron datos. Abortando el pipeline.")
        sys.exit(1)
    logger.info("Datos extraídos: %s", scraped_data)

    # Procesar datos con pandas
    try:
        processed_data = process_news_data(scraped_data)
    except Exception as e:
        logger.exception("❌ Error procesando los datos:")
        sys.exit(1)
    logger.info("Datos procesados: %s", processed_data)

    # Cargar en BigQuery
    try:
        insert_row_to_bigquery(processed_data)
    except Exception as e:
        logger.exception("❌ Error cargando en BigQuery:")
        sys.exit(1)
    logger.info("✅ Datos cargados en BigQuery correctamente.")
    logger.info("Fin del proceso.")

if __name__ == "__main__":
    main()

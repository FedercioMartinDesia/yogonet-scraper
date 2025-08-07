import os

# --- Manejo seguro de la key desde env ---
if "GCP_CREDS_JSON" in os.environ:
    creds_path = "/tmp/creds.json"
    with open(creds_path, "w") as f:
        f.write(os.environ["GCP_CREDS_JSON"])
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_path


from scraper import scrape_news_data
from processor import process_news_data
from bq_loader import insert_row_to_bigquery

def main():
    # URL a scrapear
    news_url = "https://www.yogonet.com/international/news/2024/06/04/72489-malta-gaming-authority-inks-mou-with-ontario-regulator-to-strengthen-collaborative-efforts"
    
    # Extraer datos
    scraped_data = scrape_news_data(news_url)
    print("Datos extraídos:", scraped_data)   # <--- LOG

    # Procesar datos con pandas (la función nueva)
    processed_data = process_news_data(scraped_data)
    print("Datos procesados:", processed_data)  # <--- LOG

    # Cargar (o mock) en BigQuery
    insert_row_to_bigquery(processed_data)
    print("✅ Datos cargados en BigQuery correctamente.")  # <--- LOG

    print("Fin del proceso.")  # <--- LOG

if __name__ == "__main__":
    main()


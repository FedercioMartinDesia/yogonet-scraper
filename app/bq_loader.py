from google.cloud import bigquery
import pandas as pd
import json

def insert_row_to_bigquery(row_data):
    project_id = "scraper-challenge"
    dataset_id = "scraper_data"
    table_id = "yogonet"

    client = bigquery.Client(project=project_id)
    table_ref = f"{project_id}.{dataset_id}.{table_id}"

    df = pd.DataFrame([row_data])

    # Convertir a tipos compatibles
    df["title_word_count"] = df["title_word_count"].astype(int)
    df["title_char_count"] = df["title_char_count"].astype(int)
    df["title_capitalized_words"] = df["title_capitalized_words"].apply(json.dumps)  # o ', '.join(x) si preferis

    job = client.load_table_from_dataframe(df, table_ref)
    job.result()

    print(f"Fila insertada correctamente en {table_ref} con método batch.")

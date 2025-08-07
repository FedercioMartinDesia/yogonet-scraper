import pandas as pd

def process_news_data(news_data):
    """
    Procesa los datos del scraper y agrega:
      - Recuento de palabras en el título
      - Recuento de caracteres en el título
      - Lista de palabras que comienzan con mayúscula en el título

    Args:
        news_data (dict): dict con los campos scrapeados

    Returns:
        dict: dict enriquecido listo para cargar en BQ
    """
    # Convertir dict en DataFrame de una fila
    df = pd.DataFrame([news_data])

    # Recuento de palabras en el título
    df['title_word_count'] = df['title'].str.split().apply(len)

    # Recuento de caracteres en el título
    df['title_char_count'] = df['title'].str.len()

    # Lista de palabras con mayúscula inicial en el título
    # Usamos apply con una lambda para obtener la lista
    df['title_capitalized_words'] = df['title'].apply(
        lambda x: [w for w in x.split() if w.istitle()]
    )

    # Convertimos la fila resultante de vuelta a dict (solo la primera fila)
    enriched = df.iloc[0].to_dict()
    return enriched

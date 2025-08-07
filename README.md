# 📰 Yogonet Scraper – IA + Python + BigQuery + Railway

Este proyecto automatiza el scraping de noticias de Yogonet utilizando un enfoque inteligente basado en IA (OpenAI GPT-4o) para identificar dinámicamente los campos clave de cada nota (**Título, Kicker, Imagen, Link**), procesa la información y la carga en una tabla de Google BigQuery.

- **Deploy de referencia:** Railway (evita problemas de facturación de GCP)
- **Arquitectura desacoplada:** todo corre en Docker, se puede adaptar a Cloud Run.

---

## 📂 Estructura del proyecto

```plaintext
yogonet-scraper/
│
├── app/
│   ├── main.py              # Punto de entrada, orquesta todo
│   ├── scraper.py           # Scraping IA-driven con OpenAI
│   ├── processor.py         # Procesamiento de datos
│   ├── bq_loader.py         # Inserción en BigQuery
│
├── requirements.txt         # Dependencias Python
├── Dockerfile               # Imagen Docker para Railway/Cloud Run
├── README.md                # (Este archivo)

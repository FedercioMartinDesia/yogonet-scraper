📰 Yogonet Scraper – IA + Python + BigQuery + Railway

Este proyecto automatiza el scraping de noticias de Yogonet utilizando un enfoque inteligente basado en IA (OpenAI GPT-4o) para identificar dinámicamente los campos clave de cada nota (Título, Kicker, Imagen, Link), procesa la información y la carga en una tabla de Google BigQuery.

Deploy de referencia: Se realiza en Railway para evitar problemas con la facturación de Google Cloud Platform.
Arquitectura desacoplada: todo corre en Docker, puede adaptarse a Cloud Run fácilmente.

📂 Estructura del proyecto

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


🚀 Cómo ejecutar el scraper

1. Prerrequisitos
Cuenta de Google Cloud con un proyecto y una tabla BigQuery ya creada.

Credenciales de Service Account descargadas en JSON.

Una API key de OpenAI.

Una cuenta en Railway (gratis, sin tarjeta) para desplegar.

2. Configuración de variables

Vas a necesitar 2 variables de entorno (se cargan en Railway > Variables):

GCP_CREDS_JSON: Contenido completo del archivo JSON de credenciales (Service Account de GCP).

OPENAI_API_KEY: Tu API Key de OpenAI (GPT-4o).

3. Deploy automático en Railway
   
Subí este repositorio a GitHub
(Si ya está, salteá este paso).

En Railway:

Click en New Project > Deploy from GitHub Repo

Elegí tu repo.

Railway detecta el Dockerfile y hace build automático.

Agregá variables de entorno:

En Settings > Variables:

Pegá el contenido de tu JSON de credenciales en GCP_CREDS_JSON

Pegá tu clave de OpenAI en OPENAI_API_KEY

Railway hace deploy automático.

El script corre y carga los datos en BigQuery.

Ver logs en el dashboard (opción “View logs”).

4. ¿Cómo correrlo localmente?

Instalá dependencias:
pip install -r requirements.txt

Exportá las variables de entorno en tu terminal:

export GCP_CREDS_JSON="$(cat /ruta/a/credenciales.json)"
export OPENAI_API_KEY="sk-...."

Corré el script principal:

python app/main.py

5. ¿Cómo funcionaría en Cloud Run?

Este mismo Dockerfile y código es 100% compatible con Cloud Run.

Simplemente subí tu imagen a Google Artifact Registry o Docker Hub y desplegá en Cloud Run.

En Cloud Run, configurá las variables de entorno GCP_CREDS_JSON y OPENAI_API_KEY igual que en Railway.




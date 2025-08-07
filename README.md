## 📰 Yogonet Scraper – IA + Python + BigQuery + Railway Español

Este proyecto automatiza el scraping de noticias de Yogonet utilizando un enfoque inteligente basado en IA (OpenAI GPT-4o) para identificar dinámicamente los campos clave de cada nota (**Título, Kicker, Imagen, Link**), procesa la información y la carga en una tabla de Google BigQuery.

- **Deploy de referencia:** Railway (evita problemas de facturación de GCP)
- **Arquitectura desacoplada:** todo corre en Docker, se puede adaptar a Cloud Run.

---
Chat con el que se trabajo:
* https://chatgpt.com/share/6895028e-a9cc-8000-8446-3d7429ac2086
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
```
---

### 🚀 Cómo ejecutar el scraper

#### 1. Prerrequisitos

Para poner en marcha este proyecto, necesitarás lo siguiente:

* Una cuenta de Google Cloud con un proyecto y una tabla de BigQuery ya creada.
* Credenciales de Service Account de Google Cloud en formato JSON.
* Una API Key de OpenAI (GPT-4o).
* Una cuenta en Railway (es gratis, no requiere tarjeta de crédito).

#### 2. Configuración de variables de entorno

Debes configurar dos variables de entorno para que el proyecto funcione:

* **`GCP_CREDS_JSON`**: El contenido completo de tu archivo JSON de credenciales de Google Cloud (Service Account).
* **`OPENAI_API_KEY`**: Tu API Key de OpenAI.
* **`ANTHROPIC_API_KEY`**: Tu API Key de Claude.
  
Estas variables se cargan en la configuración de Railway.

<img width="829" height="228" alt="image" src="https://github.com/user-attachments/assets/cc8041c9-7ae4-440c-b2ae-a582f3c375ea" />
<img width="824" height="234" alt="image" src="https://github.com/user-attachments/assets/64176f47-c706-4bb5-a1d9-592014520749" />
<img width="799" height="213" alt="image" src="https://github.com/user-attachments/assets/661b1e16-e173-4634-8d12-9eab70ba6bd2" />
<img width="466" height="59" alt="image" src="https://github.com/user-attachments/assets/5d4cf209-91e2-494c-96dd-c5843e8ee552" />


#### 3. Despliegue automático en Railway

1.  Sube este repositorio a **GitHub**.
2.  En Railway, haz clic en **New Project** y luego en **Deploy from GitHub Repo**.
3.  Selecciona tu repositorio. Railway detectará el **Dockerfile** y hará el _build_ de forma automática.
4.  Configura las variables de entorno en **Settings > Variables**. Pega el contenido de tu JSON en `GCP_CREDS_JSON` y tu clave de OpenAI en `OPENAI_API_KEY`.
5.  Railway hará el _deploy_ automáticamente. El _script_ se ejecutará y cargará los datos en BigQuery. Puedes verificar el progreso y los resultados en la opción **View logs** del _dashboard_.

#### 4. Ejecución local

Si prefieres ejecutar el _scraper_ en tu máquina local, sigue estos pasos:

1.  Instala las dependencias de Python:
    ```bash
    pip install -r requirements.txt
    ```
2.  Exporta las variables de entorno en tu terminal:
    ```bash
    export GCP_CREDS_JSON="$(cat /ruta/a/credenciales.json)"
    export OPENAI_API_KEY="sk-...."
    ```
3.  Corre el _script_ principal:
    ```bash
    python app/main.py
    ```

#### 5. Despliegue en Cloud Run

Este proyecto es 100% compatible con Google Cloud Run. Simplemente sube la imagen Docker a Google Artifact Registry o Docker Hub y despliégala en Cloud Run. Deberás configurar las variables de entorno `GCP_CREDS_JSON` y `OPENAI_API_KEY` en el servicio de Cloud Run, de la misma manera que lo harías en Railway.

```plaintext
#!/bin/bash
docker build -t gcr.io/tu-proyecto/tu-imagen .
docker push gcr.io/tu-proyecto/tu-imagen
gcloud run deploy tu-servicio --image gcr.io/tu-proyecto/tu-imagen --platform managed --region us-central1
```




---
### ¿Cómo cambiar la URL de la noticia a scrapear?

Por defecto, la URL de la noticia a scrapear está definida en app/main.py en la variable news_url.
Puedes editar ese valor antes de correr el script para probar diferentes noticias de Yogonet.

Si deseas hacer el scraper interactivo, reemplaza la línea:
```
news_url = "https://www.yogonet.com/international/news/....."

```

---

### ⚙️ Dependencias clave

Para instalar, ejecuta: 
```
pip install -r requirements.txt
```

El proyecto se basa en las siguientes librerías de Python:

| Paquete                  | Descripción                                             |
|--------------------------|---------------------------------------------------------|
| `requests`               | Descarga de HTML desde la web.                          |
| `beautifulsoup4`         | Parseo y extracción de datos de HTML.                   |
| `openai`                 | Interacción con GPT-4o para extracción dinámica.        |
| `anthropic`              | Interacción con Claude para fallback cuando GPT no funcione. |
| `pandas`                 | Procesamiento y transformación de datos.                |
| `pyarrow`                | Serialización de DataFrames y compatibilidad con BQ.    |
| `pandas-gbq`             | Carga de DataFrames directamente en BigQuery.           |
| `google-cloud-bigquery`  | Cliente oficial para gestión de tablas en BigQuery.     |

---
### Modelo

El código utiliza el modelo de OpenAI "gpt-4o" y Claude "claude-2.1".

---

### Error 429 "You exceeded your current quota, please check your plan and billing details".

Esto sucede si excediste la cuota de Openai o Claude, debes mejorar el plan.




(___)

## 📰 Yogonet Scraper – IA + Python + BigQuery + Railway English

This project automates Yogonet news scraping using an intelligent AI-based approach (OpenAI GPT-4o) to dynamically identify the key fields of each note
(**Título, Kicker, Imagen, Link**), processes the information and loads it into a Google BigQuery table.

- **Reference deployment:** Railway (evita problemas de facturación de GCP)
- **Decoupled architecture:** everything runs in Docker, it can be adapted to Cloud Run.

---
Chat I worked with (in spanish):
* https://chatgpt.com/share/6895028e-a9cc-8000-8446-3d7429ac2086
---

## 📂 Project structure

```plaintext
yogonet-scraper/
│
├── app/
│   ├── main.py              # Entry point, orchestrate everything
│   ├── scraper.py           # AI-driven scraping with OpenAI
│   ├── processor.py         # Data processing
│   ├── bq_loader.py         # Embed in BigQuery
│
├── requirements.txt         #Python dependencies
├── Dockerfile               # Docker image for Railway/Cloud Run
├── README.md                # (This file)
```
---

### 🚀 How to run the scraper

#### 1. Prerequisites

To start this project, you will need the following:

* A Google Cloud account with a project and a BigQuery table already created.
* Google Cloud Service Account credentials in JSON format.
* An OpenAI API Key (GPT-4o).
* A Railway account (it's free, no credit card required).

#### 2. Configuración de variables de entorno

You must set two environment variables for the project to work:

* **`GCP_CREDS_JSON`**: The full content of your Google Cloud credentials (Service Account) JSON file.
* **`OPENAI_API_KEY`**: Your OpenAI API Key.
* **`ANTHROPIC_API_KEY`**: Your Claude API Key.
  
These variables are loaded in the Railway configuration.

<img width="829" height="228" alt="image" src="https://github.com/user-attachments/assets/cc8041c9-7ae4-440c-b2ae-a582f3c375ea" />
<img width="824" height="234" alt="image" src="https://github.com/user-attachments/assets/64176f47-c706-4bb5-a1d9-592014520749" />
<img width="799" height="213" alt="image" src="https://github.com/user-attachments/assets/661b1e16-e173-4634-8d12-9eab70ba6bd2" />
<img width="466" height="59" alt="image" src="https://github.com/user-attachments/assets/5d4cf209-91e2-494c-96dd-c5843e8ee552" />


#### 3. Automatic deployment on Railway

1. Upload this repository to **GitHub**.
2. In Railway, click **New Project** and then **Deploy from GitHub Repo**.
3. Select your repository. Railway will detect the **Dockerfile** and do the _build_ automatically.
4. Configure the environment variables in **Settings > Variables**. Paste the contents of your JSON into `GCP_CREDS_JSON` and your OpenAI key into `OPENAI_API_KEY`.
5. Railway will do the _deploy_ automatically. The _script_ will run and load the data into BigQuery. You can check the progress and results in the **View logs** option of the _dashboard_.

#### 4. Local execution

If you prefer to run _scraper_ on your local machine, follow these steps:

1. Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2. Export the environment variables in your terminal:
    ```bash
    export GCP_CREDS_JSON="$(cat /path/to/credenciales.json)"
    export OPENAI_API_KEY="sk-...."
    ```
3. Run the main _script_:
    ```bash
    python app/main.py
    ```

#### 5. Deploy to Cloud Run

This project is 100% compatible with Google Cloud Run. Simply upload the Docker image to Google Artifact Registry or Docker Hub and deploy it to Cloud Run. You will need to configure the `GCP_CREDS_JSON` and `OPENAI_API_KEY` environment variables in the Cloud Run service, the same way you would in Railway.

```plaintext
#!/bin/bash
docker build -t gcr.io/tu-proyecto/tu-imagen .
docker push gcr.io/tu-proyecto/tu-imagen
gcloud run deploy tu-servicio --image gcr.io/tu-proyecto/tu-imagen --platform managed --region us-central1
```




---
### How to change the URL of the news to be scraped?

By default, the URL of the news to be scraped is defined in app/main.py in the news_url variable.
You can edit that value before running the script to test different Yogonet news.

If you want to make the scraper interactive, replace the line:
```
news_url = "https://www.yogonet.com/international/news/....."

```

---

### ⚙️ Key dependencies

To install, run:
```
pip install -r requirements.txt
```

The project is based on the following Python libraries:

| Paquete                  | Descripción                                             |
|--------------------------|---------------------------------------------------------|
| `requests`               | HTML download from the web.                          |
| `beautifulsoup4`         | HTML parsing and data extraction.                   |
| `openai`                 | Interaction with GPT-4o for dynamic extraction.        |
| `anthropic`              | Interaction with Claude to fallback when GPT doesn't work. |
| `pandas`                 | Data processing and transformation.                |
| `pyarrow`                | DataFrames serialization and BQ support.    |
| `pandas-gbq`             | Loading DataFrames directly into BigQuery.           |
| `google-cloud-bigquery`  | Official client for BigQuery table management.     |

---
### Model

The code uses the OpenAI "gpt-4o" and Claude "claude-2.1" model.
---

### Error 429 "You exceeded your current quota, please check your plan and billing details".

This happens if you exceeded the Openai or Claude quota, you must upgrade the plan.

---










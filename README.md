<img width="829" height="228" alt="image" src="https://github.com/user-attachments/assets/e0c21a9d-1853-4ebe-b454-7a890dc4ef21" /># 📰 Yogonet Scraper – IA + Python + BigQuery + Railway

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

El proyecto se basa en las siguientes librerías de Python:

* `requests` y `beautifulsoup4`: Para la descarga y el parseo de HTML.
* `openai`: Para la selección dinámica de campos con GPT-4o.
* `pandas`, `pyarrow`, `pandas-gbq`: Para el procesamiento de datos y la carga en BigQuery.
* `google-cloud-bigquery`: Para la conexión y la gestión de BigQuery.





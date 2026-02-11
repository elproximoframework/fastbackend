# FastAPI Railway Example

Este es un ejemplo sencillo de una API con FastAPI lista para ser desplegada en Railway.

## Estructura
- `main.py`: Código principal de la API.
- `requirements.txt`: Dependencias del proyecto.
- `Procfile`: Instrucciones para que Railway sepa cómo ejecutar la aplicación.

## Despliegue en Railway

1. Sube este código a un repositorio de GitHub.
2. Ve a [Railway](https://railway.app/).
3. Haz clic en **New Project** -> **Deploy from GitHub repo**.
4. Selecciona tu repositorio.
5. Railway detectará automáticamente el `Procfile` y desplegará la aplicación.

## Ejecución Local

1. Crea un entorno virtual: `python -m venv venv`
2. Actívalo: `.\venv\Scripts\activate`
3. Instala dependencias: `pip install -r requirements.txt`
4. Ejecuta: `uvicorn main:app --reload`

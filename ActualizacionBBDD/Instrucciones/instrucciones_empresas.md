# Prompt de Instrucciones para Rellenar la Tabla `companies`

Tu objetivo es generar los datos necesarios para insertar registros en la tabla `companies` de la base de datos PostgreSQL, tanto en el entorno **local** como en el **remoto (Railway)**.

El proceso comienza con una **lista de nombres de empresas** que yo te proporcionaré. Para cada empresa de la lista, deberás realizar una búsqueda profunda para completar todos los campos del esquema.

## 0. Conexiones de Base de Datos

Deberás ejecutar las inserciones en ambas bases de datos:

*   **Local:** `postgresql://space_user:space_password@localhost:5433/space_db`
*   **Remoto (Railway):** `postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway`

## 1. Referencia del Esquema de la Tabla `companies`

La tabla tiene los siguientes campos (basados en el modelo SQLAlchemy):

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | Integer | Clave primaria (autoincremental). |
| `name` | String | Nombre oficial de la empresa (ej: `SpaceX`). |
| `type` | String | Tipo de entidad (`startup`, `agency`, `contractor`, `university`, `ground_segment`, `investors`, `logistics`, `other`). |
| `country` | String | Código ISO del país (ej: `us`, `es`). |
| `countryName` | String | Nombre completo del país (ej: `EEUU`, `España`). |
| `city` | String | Ciudad de la sede principal. |
| `coordinates` | JSON | Objeto con latitud y longitud: `{"lat": 28.5, "lng": -80.6}`. |
| `employees` | Integer | Número aproximado de empleados. |
| `website` | String | URL oficial del sitio web. |
| `description` | String | Descripción detallada en español. |
| `description_en` | String | Descripción detallada en inglés. |
| `founded` | Integer | Año de fundación (ej: `2002`). |
| `ceo` | String | Nombre del actual CEO. |
| `sector` | String | Sector principal (ver lista abajo). |
| `tags` | JSON | Lista de etiquetas (ej: `["Reusable", "Mars", "Starlink"]`). |
| `socialLinks` | JSON | Enlaces sociales: `{"twitter": "...", "linkedin": "...", "youtube": "..."}`. |
| `keyPrograms` | JSON | Programas principales (ej: `["Starship", "Falcon 9"]`). |
| `fundingStage` | String | Fase de financiación (ej: `Public`, `Series D`). |
| `totalFunding` | String | Financiación total (ej: `$2B`). |
| `stockTicker` | String | Ticker de bolsa si aplica (ej: `PLTR`, `RKLB`). |
| `show` | Boolean | `True` por defecto. Determina si se muestra en el frontend. |

### Valores Permitidos para `sector`:
- `launchers`, `satellites`, `ground_segment`, `propulsion`, `space_tourism`, `defense`, `research`, `software`, `manufacturing`.

## 2. Instrucciones de Generación y Logos

### Identidad y Localización:
1.  **Nombre:** Debe ser el nombre comercial común.
2.  **Coordenadas:** Busca las coordenadas reales de la sede principal si es posible.
3.  **Descripción:** Proporciona un texto rico y profesional tanto en español como en inglés.

### Manejo de Logos (IMPORTANTE):
*   **Convención de Nombres:** El logo de la empresa **NO** se guarda en la base de datos (según el modelo actual). El frontend lo carga dinámicamente usando el nombre de la empresa convertido a "slug".
*   **Proceso de Slug**:
    1.  Convertir a minúsculas.
    2.  Eliminar acentos y caracteres especiales.
    3.  Cambiar espacios por guiones (`-`).
    *   Ejemplo: `SpaceX` -> `spacex.png`, `Blue Origin` -> `blue-origin.png`.
*   **Almacenamiento:** Las imágenes resultantes deben guardarse en la carpeta: `D:\YoutubeElProximoFrameworkEnElEspacio\Web\backendfast\company_logos`.
*   **Formato:** Siempre usar `.png`.
*   **Búsqueda y Creación:** 
    1.  Debes buscar en internet el logo oficial de la empresa en alta resolución (fondo transparente preferido).
    2.  Si **NO** encuentras un logo adecuado o la empresa no tiene uno público, deberás **generar uno** utilizando tus capacidades de creación de imágenes (DALL-E, etc.). El logo generado debe ser profesional, minimalista y relacionado con la identidad de la marca o su sector espacial.
    3.  Asegúrate de que el archivo final sea un `.png` con el nombre de slug correcto.

## 3. Formato de Salida

Genera un script de Python que utilice SQLAlchemy para insertar estos registros, o un archivo JSON con la lista de objetos listos para ser procesados.

### Ejemplo de Estructura JSON:
```json
{
  "name": "SpaceX",
  "type": "startup",
  "country": "us",
  "countryName": "EEUU",
  "city": "Hawthorne",
  "coordinates": { "lat": 33.9213, "lng": -118.3267 },
  "employees": 12000,
  "website": "https://www.spacex.com",
  "description": "SpaceX diseña, fabrica y lanza cohetes y naves espaciales avanzadas.",
  "description_en": "SpaceX designs, manufactures and launches advanced rockets and spacecraft.",
  "founded": 2002,
  "ceo": "Elon Musk",
  "sector": "launchers",
  "tags": ["Reusability", "Mars", "Starlink"],
  "socialLinks": {
    "twitter": "https://twitter.com/spacex",
    "linkedin": "https://www.linkedin.com/company/spacex"
  },
  "keyPrograms": ["Starship", "Falcon 9", "Dragon"],
  "fundingStage": "Private",
  "totalFunding": "$9.8B",
  "stockTicker": null,
  "show": true
}
```

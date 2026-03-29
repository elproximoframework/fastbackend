# Prompt de Instrucciones para Rellenar la Tabla `satellites`

Tu objetivo es generar los datos necesarios para insertar registros en la tabla `satellites` de la base de datos PostgreSQL, tanto en el entorno **local** como en el **remoto (Railway)**.

El proceso comienza con una **lista de nombres de satélites** que yo te proporcionaré. Para cada satélite, deberás realizar una investigación técnica para completar todos los campos del esquema.

## 0. Conexiones de Base de Datos

Deberás ejecutar las inserciones en ambas bases de datos:

*   **Local:** `postgresql://space_user:space_password@localhost:5433/space_db`
*   **Remoto (Railway):** `postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway`

## 1. Referencia del Esquema de la Tabla `satellites`

La tabla tiene los siguientes campos (basados en el modelo SQLAlchemy):

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | Integer | Clave primaria (autoincremental). |
| `name` | String | Nombre oficial del satélite (ej: `Starlink-V2`). |
| `noradId` | String | ID de catálogo NORAD (ej: `55268`). |
| `operator_id` | Integer | ID de la empresa operadora (debe existir en la tabla `companies`). |
| `purpose` | String | Propósito del satélite (ej: `Communications`, `Earth Observation`). |
| `launchDate` | Date | Fecha de lanzamiento (YYYY-MM-DD). |
| `orbitType` | String | Tipo de órbita (ej: `LEO`, `GEO`, `MEO`). |
| `altitude` | Float | Altitud de la órbita en km. |
| `inclination` | Float | Inclinación orbital en grados. |
| `description` | String | Descripción detallada en español. |
| `description_en` | String | Descripción detallada en inglés. |
| `image` | String | URL de la imagen: `/api/v1/satellite_images/slug-satelite.png`. |
| `isFeatured`| Boolean | `True` si es un satélite destacado. |
| `funFact` | String | Dato curioso en español. |
| `funFact_en` | String | Dato curioso en inglés. |
| `show` | Boolean | `True` por defecto. Determina si se muestra en el frontend. |

## 2. Instrucciones de Generación e Imágenes

### Datos Técnicos:
1.  **Operador:** Investiga qué empresa opera el satélite. Si no conoces su `id`, búscalo en la tabla `companies` por nombre antes de generar el SQL.
2.  **Parámetros Orbitales:** Busca la altitud e inclinación real del satélite.
3.  **Descripciones:** Proporciona un texto rico y profesional tanto en español como en inglés.

### Manejo de Imágenes (IMPORTANTE):
*   **Generación de URL:** El campo `image` debe seguir siempre este patrón: `/api/v1/satellite_images/[slug-del-satelite].png`.
*   **Proceso de Slug**:
    1.  Convertir el nombre del satélite a minúsculas.
    2.  Eliminar caracteres especiales.
    3.  Cambiar espacios por guiones (`-`).
    *   Ejemplo: `Hubble Space Telescope` -> `hubble-space-telescope.png`.
*   **Almacenamiento Físico:** Las imágenes deben guardarse en la carpeta: `D:\YoutubeElProximoFrameworkEnElEspacio\Web\backendfast\satellite_images`.
*   **Formato:** Siempre usar `.png`.
*   **Búsqueda y Creación:** 
    1.  Busca una imagen real o representación artística de alta calidad del satélite en el espacio.
    2.  Si **NO** encuentras una imagen adecuada, deberás **generar una imagen** del satélite utilizando tus capacidades de creación. La imagen debe ser realista y mostrar el satélite en su entorno orbital.
    3.  Asegúrate de que el archivo final sea un `.png` con el nombre de slug correcto en la carpeta mencionada.

## 3. Formato de Salida

Genera un script de Python que utilice SQLAlchemy para insertar estos registros, asegurándote de manejar correctamente las claves foráneas (`operator_id`).

### Ejemplo de Estructura SQL:
```sql
INSERT INTO satellites (name, noradId, operator_id, purpose, launchDate, orbitType, altitude, inclination, description, description_en, image, isFeatured, funFact, funFact_en, show)
VALUES ('Hubble Space Telescope', '20580', 2, 'Astronomy', '1990-04-24', 'LEO', 540.0, 28.5, 'El telescopio espacial Hubble es un observatorio espacial que orbita la Tierra...', 'The Hubble Space Telescope is a space observatory that orbits Earth...', '/api/v1/satellite_images/hubble-space-telescope.png', true, 'El Hubble ha realizado más de 1.5 millones de observaciones.', 'Hubble has made more than 1.5 million observations.', true);
```

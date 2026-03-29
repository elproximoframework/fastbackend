# Prompt de Instrucciones para Rellenar la Tabla `rockets`

Tu objetivo es generar los datos necesarios para insertar registros en la tabla `rockets` de la base de datos PostgreSQL, tanto en el entorno **local** como en el **remoto (Railway)**.

El proceso comienza con una **lista de nombres de cohetes** que yo te proporcionaré. Para cada cohete, deberás realizar una investigación para completar todos los campos del esquema, asegurándote de que los datos sean técnicos y precisos.

## 0. Conexiones de Base de Datos

Deberás ejecutar las inserciones en ambas bases de datos:

*   **Local:** `postgresql://space_user:space_password@localhost:5433/space_db`
*   **Remoto (Railway):** `postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway`

## 1. Referencia del Esquema de la Tabla `rockets`

La tabla tiene los siguientes campos (basados en el modelo SQLAlchemy):

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | Integer | Clave primaria (autoincremental). |
| `name` | String | Nombre oficial del cohete (ej: `Falcon 9`). |
| `manufacturer_id` | Integer | ID de la empresa fabricante (debe existir en la tabla `companies`). |
| `country` | String | Código ISO del país o "Multinational" (ej: `us`, `eu`). |
| `height` | Float | Altura en metros. |
| `diameter` | Float | Diámetro en metros. |
| `stages` | Integer | Número de etapas. |
| `fuel` | String | Tipo de combustible (ej: `LOX/RP-1`). |
| `leoCapacity` | Float | Capacidad de carga a LEO en kg. |
| `gtoCapacity` | Float | Capacidad de carga a GTO en kg. |
| `firstFlight` | Date | Fecha del primer vuelo (YYYY-MM-DD). |
| `totalLaunches` | Integer | Número total de lanzamientos realizados. |
| `successRate` | Float | Tasa de éxito (0.0 a 100.0). |
| `status` | String | Estado actual (ver lista abajo). |
| `image` | String | URL de la imagen: `/api/v1/rocket_images/nombre-cohete.png`. |
| `description` | String | Descripción técnica en español. |
| `description_en` | String | Descripción técnica en inglés. |
| `costPerLaunch` | Float | Coste estimado por lanzamiento en millones de USD. |
| `reusable` | Boolean | Indica si el cohete es reutilizable. |

### Valores Permitidos para `status`:
- `active`, `development`, `retired`, `cancelled`.

## 2. Instrucciones de Generación e Imágenes

### Datos Técnicos:
1.  **Fabricante:** Investiga cuál es la empresa fabricante. Si no conoces su `id`, búscalo en la tabla `companies` por nombre antes de generar el SQL.
2.  **Dimensiones:** Usa valores numéricos precisos en metros y kilogramos.
3.  **Descripciones:** Proporciona un texto profesional, destacando hitos tecnológicos o misiones famosas.

### Manejo de Imágenes (IMPORTANTE):
*   **Generación de URL:** El campo `image` debe seguir siempre este patrón: `/api/v1/rocket_images/[slug-del-cohete].png`.
*   **Proceso de Slug**:
    1.  Convertir el nombre del cohete a minúsculas.
    2.  Eliminar caracteres especiales.
    3.  Cambiar espacios por guiones (`-`).
    *   Ejemplo: `Falcon 9` -> `falcon-9.png`, `Delta IV Heavy` -> `delta-iv-heavy.png`.
*   **Almacenamiento Físico:** Las imágenes deben guardarse en la carpeta: `D:\YoutubeElProximoFrameworkEnElEspacio\Web\backendfast\rocket_images`.
*   **Formato:** Siempre usar `.png`.
*   **Búsqueda y Creación:** 
    1.  Busca una imagen real del cohete en alta resolución (preferiblemente en lanzamiento o en plataforma, con fondo limpio).
    2.  Si **NO** encuentras una imagen real de calidad, o prefieres una estética unificada, deberás **generar una imagen** del cohete. La imagen generada debe ser realista, mostrando el cohete en detalle, idealmente en un entorno espacial o en la plataforma de lanzamiento.
    3.  Asegúrate de que el archivo final sea un `.png` con el nombre de slug correcto en la carpeta mencionada.

## 3. Formato de Salida

Genera un script de Python que utilice SQLAlchemy para insertar estos registros, asegurándote de manejar correctamente las claves foráneas (`manufacturer_id`).

### Ejemplo de Estructura SQL (para referencia):
```sql
INSERT INTO rockets (name, manufacturer_id, country, height, diameter, stages, fuel, leoCapacity, gtoCapacity, firstFlight, totalLaunches, successRate, status, image, description, description_en, costPerLaunch, reusable)
VALUES ('Falcon 9', 1, 'us', 70.0, 3.7, 2, 'LOX/RP-1', 22800, 8300, '2010-06-04', 300, 99.0, 'active', '/api/v1/rocket_images/falcon-9.png', 'El Falcon 9 es un cohete de dos etapas diseñado y fabricado por SpaceX...', 'Falcon 9 is a two-stage rocket designed and manufactured by SpaceX...', 62.0, true);
```

# Prompt de Instrucciones para Rellenar la Tabla `satellites`

Tu objetivo es generar los datos necesarios para insertar registros en la tabla `satellites` de la base de datos PostgreSQL, tanto en el entorno **local** como en el **remoto (Railway)**.

El proceso comienza con una **lista de nombres de satélites** que yo te proporcionaré. Para cada satélite, deberás realizar una investigación técnica para completar todos los campos del esquema.

## 0. Conexiones de Base de Datos

Deberás ejecutar las inserciones en ambas bases de datos:

* **Local:** `postgresql://space_user:space_password@localhost:5433/space_db`
* **Remoto (Railway):** `postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway`

## 1. Referencia del Esquema de la Tabla `satellites`

La tabla tiene los siguientes campos (basados en el modelo SQLAlchemy):

| Campo              | Tipo    | Descripción                                                             |
| ------------------ | ------- | ------------------------------------------------------------------------ |
| `id`             | Integer | Clave primaria (autoincremental).                                        |
| `name`           | String  | Nombre oficial del satélite (ej:`Starlink-V2`).                       |
| `noradId`        | String  | ID de catálogo NORAD (ej:`55268`).                                    |
| `operator_id`    | Integer | ID de la empresa operadora (debe existir en la tabla `companies`).     |
| `purpose`        | String  | Propósito del satélite (ej:`Communications`, `Earth Observation`). |
| `launchDate`     | Date    | Fecha de lanzamiento (YYYY-MM-DD).                                       |
| `orbitType`      | String  | Tipo de órbita (ej:`LEO`, `GEO`, `MEO`).                          |
| `altitude`       | Float   | Altitud de la órbita en km.                                             |
| `inclination`    | Float   | Inclinación orbital en grados.                                          |
| `description`    | String  | Descripción detallada en español.                                      |
| `description_en` | String  | Descripción detallada en inglés.                                       |
| `image`          | String  | URL de la imagen:`/api/v1/satellite_images/slug-satelite.png`.         |
| `isFeatured`     | Boolean | `True` si es un satélite destacado.                                   |
| `funFact`        | String  | Dato curioso en español.                                                |
| `funFact_en`     | String  | Dato curioso en inglés.                                                 |
| `show`           | Boolean | `True` por defecto. Determina si se muestra en el frontend.            |

## 2. Instrucciones de Generación e Imágenes

### Datos Técnicos:

1. **Operador:** Investiga qué empresa opera el satélite.
   * **Paso Obligatorio:** Antes de generar el SQL, busca el `id` de la empresa utilizando el siguiente script:
     ```bash
     python D:\YoutubeElProximoFrameworkEnElEspacio\Web\backendfast\ActualizacionBBDD\Scripts\get_company_id.py "Nombre de la Empresa"
     ```
   * Utiliza el `ID` devuelto para el campo `operator_id`.
2. **Parámetros Orbitales:** Busca la altitud e inclinación real del satélite.
3. **Descripciones:** Proporciona un texto rico y profesional tanto en español como en inglés.

### Manejo de Imágenes (IMPORTANTE):

* **Generación de URL:** El campo `image` debe seguir siempre este patrón: `[slug-del-satelite].png`.
* **Proceso de Slug**:

  1. Convertir el nombre del satélite a minúsculas.
  2. Eliminar caracteres especiales.
  3. Cambiar espacios por guiones (`-`).

  * Ejemplo: `Hubble Space Telescope` -> `hubble-space-telescope.png`.
* **Almacenamiento Físico:** Las imágenes deben guardarse en la carpeta: D:\YoutubeElProximoFrameworkEnElEspacio\Web\Cloudinary\satellite_images.
* **Formato:** Siempre usar `.png`.
* **Búsqueda y Creación:**

  1. Busca una imagen real o representación artística de alta calidad del satélite en el espacio.
  2. Si **NO** encuentras una imagen adecuada, deberás **generar una imagen** del satélite utilizando tus capacidades de creación. La imagen debe ser realista y mostrar el satélite en su entorno orbital.
  3. **Imagen por Defecto:** Si se te indica explícitamente que **no generes una imagen**, o si por alguna razón técnica no puedes crear una nueva, utiliza la imagen por defecto:
     * Ruta: `D:\YoutubeElProximoFrameworkEnElEspacio\Web\backendfast\satellite_images\default-satellite.png`
     * En el campo `image` del SQL, deberás poner: `/api/v1/satellite_images/default-satellite.png`.
  4. Asegúrate de que el archivo final sea un `.png` con el nombre de slug correcto (o el nombre de la imagen por defecto) en la carpeta mencionada.

## 3. Formato de Salida y Ejecución

Para insertar los datos, utiliza el script robusto que maneja automáticamente las mayúsculas en los nombres de las columnas y sincroniza ambos entornos:

**Script:** `D:\YoutubeElProximoFrameworkEnElEspacio\Web\backendfast\ActualizacionBBDD\Scripts\insert_satellites_from_json.py`

**Comando:**

```bash
python D:\YoutubeElProximoFrameworkEnElEspacio\Web\backendfast\ActualizacionBBDD\Scripts\insert_satellites_from_json.py ruta/a/tu/archivo.json
```

### Ejemplo de Estructura JSON:

```json
ççç{
  "name": "Hubble Space Telescope",
  "noradId": "20580",
  "operator_id": 2,
  "purpose": "Astronomy",
  "launchDate": "1990-04-24",
  "orbitType": "LEO",
  "altitude": 540.0,
  "inclination": 28.5,
  "description": "El telescopio espacial Hubble es un observatorio espacial que orbita la Tierra...",
  "description_en": "The Hubble Space Telescope is a space observatory that orbits Earth...",
  "image": "hubble-space-telescope.png",
  "isFeatured": true,
  "funFact": "El Hubble ha realizado más de 1.5 millones de observaciones.",
  "funFact_en": "Hubble has made more than 1.5 million observations.",
  "show": true
}
```

*Nota: Asegúrate de incluir todos los campos para mantener la consistencia.*

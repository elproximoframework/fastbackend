# Prompt de Instrucciones para Rellenar la Tabla `newsspacex`

Tu objetivo es extraer información de archivos Markdown de noticias específicas de SpaceX y generar los datos necesarios para insertar registros en la tabla `newsspacex` de la base de datos PostgreSQL, tanto en el entorno **local** como en el **remoto (Railway)**.

## 0. Conexiones de Base de Datos

Deberás ejecutar las inserciones en ambas bases de datos:

* **Local:** `postgresql://space_user:space_password@localhost:5433/space_db`
* **Remoto (Railway):** `postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway`

## 1. Referencia del Esquema de la Tabla `newsspacex`

La tabla tiene los mismos campos que la tabla `news`, pero con filtros de categoría y lugar específicos para SpaceX:

| Campo           | Tipo    | Descripción                                                                |
| --------------- | ------- | --------------------------------------------------------------------------- |
| `id`          | Integer | Clave primaria (autoincremental).                                           |
| `title`       | String  | Título en español.                                                        |
| `title_en`    | String  | Título en inglés.                                                         |
| `excerpt`     | String  | Resumen corto en español.                                                  |
| `excerpt_en`  | String  | Resumen corto en inglés.                                                   |
| `category`    | String  | **Filtro SpaceX:** Starship, Starlink, Falcon 9, Falcon Heavy, Otros. |
| `category_en` | String  | Categoría en inglés (Starship, Starlink, Falcon 9, Falcon Heavy, Others). |
| `location`    | String  | **Filtro SpaceX:** Starbase, Florida, Vancouver, Otros.               |
| `location_en` | String  | Ubicación en inglés (Starbase, Florida, Vancouver, Others).               |
| `covered`     | Boolean | `False` por defecto (indica si está en YouTube).                         |
| `date`        | String  | Fecha en formato ISO (YYYY-MM-DD).                                          |
| `image`       | String  | Nombre del archivo de imagen (ej:`nombre.png`). SIN RUTA.                 |
| `slug`        | String  | URL amigable única (ej:`orbital-flight-test-starship`).                  |
| `tags`        | JSON    | Lista de etiquetas en español (ej:`["Starship", "IFT-3"]`).              |
| `tags_en`     | JSON    | Lista de etiquetas en inglés (ej:`["Starship", "SpaceX"]`).              |
| `featured`    | Boolean | `False` por defecto.                                                      |
| `linkyoutube` | String  | Enlace opcional a YouTube.                                                  |
| `rutanoticia` | String  | Ruta completa al archivo (ej:`/api/v1/newsspacex_content/noticia1.md`).   |
| `timestart`   | Integer | Segundo de inicio en el vídeo (opcional).                                  |
| `show`        | Boolean | `True` por defecto.                                                       |

## 2. Instrucciones de Extracción

Para cada noticia de SpaceX, tendrás dos archivos: `archivo.md` (español) y `archivo_en.md` (inglés).

### Procedimiento:

1. **Título:** Extraer del encabezado `# H1`.
2. **Fecha:** Usar el formato `YYYY-MM-DD`. Si el archivo tiene un prefijo numérico (ej: `260328`), convertirlo a `2026-03-28`.
3. **Resumen (Excerpt/Excerpt_en):** Generar un resumen de 2-3 frases (uno para español y otro para inglés).
4. **Slug:** Generar un slug único basado en el título en español.
5. **Categoría y Lugar:**
   * **Categoría:** Si trata de Starship (IFT, prototipos), usar `Starship`. Si es un despliegue de satélites, `Starlink`. Si es un lanzamiento comercial de Falcon, usar `Falcon 9` o `Falcon Heavy`. En otros casos, `Otros`.
   * **Lugar:** Si es en Texas (Boca Chica), usar `Starbase`. Si es en Cabo Cañaveral o Kennedy Space Center, `Florida`. Si es en las instalaciones de Canadá, `Vancouver`. En otros casos, `Otros`.
6. **Featured y YouTube:** Si se proporciona un enlace de YouTube (`linkyoutube`), establecer `featured` en `True`.
7. **Covered:** El campo `covered` debe ser `False` por defecto, a menos que la noticia ya haya sido cubierta en un vídeo del canal.
8. **Imagen:**
   * Generar una imagen representativa y guardarla en `D:\YoutubeElProximoFrameworkEnElEspacio\Web\backendfast\newsspacex_images`.
   * El campo `image` en la BBDD solo contiene el nombre del archivo (ej: `starship_flight.webp`).
9. **Ruta Noticia:** Usar siempre la ruta `/api/v1/newsspacex_content/` seguida del nombre del archivo (ej: `/api/v1/newsspacex_content/260331_starship_update.md`).

## 3. Ejemplo de Estructura JSON:

```json
adelante
```

## 4. Sincronización con la Base de Datos

Para insertar las noticias en las bases de datos (Local y Railway), se ha creado un script de automatización que procesa los archivos JSON de la carpeta `seeders`.

### Comando de Ejecución:

Desde el directorio raíz `backendfast/`:

```powershell
.\venv\Scripts\python.exe ActualizacionBBDD\Scripts\insert_newsspacex_from_json.py ActualizacionBBDD\Scripts\seeders\nombre_de_la_noticia.json
```

El script utiliza el campo `slug` como identificador único para realizar un **upsert** (insertar si no existe o actualizar si ya existe) tanto en el entorno **local** como en el **remoto (Railway)**.

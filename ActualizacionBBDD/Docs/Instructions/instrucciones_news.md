# Prompt de Instrucciones para Rellenar la Tabla `news`

Tu objetivo es extraer información de archivos Markdown de noticias y generar los datos necesarios para insertar registros en la tabla `news` de la base de datos PostgreSQL, tanto en el entorno **local** como en el **remoto (Railway)**.

## 0. Conexiones de Base de Datos

Deberás ejecutar las inserciones en ambas bases de datos:

*   **Local:** `postgresql://space_user:space_password@localhost:5433/space_db`
*   **Remoto (Railway):** `postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway`

## 1. Referencia del Esquema de la Tabla `news`

La tabla tiene los siguientes campos (basados en el modelo SQLAlchemy):

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | Integer | Clave primaria (autoincremental). |
| `title` | String | Título en español. |
| `title_en` | String | Título en inglés. |
| `excerpt` | String | Resumen corto en español. |
| `excerpt_en` | String | Resumen corto en inglés. |
| `category` | String | Categoría (SpaceX, NASA, Agencias, Sector Privado, Ciencia, Tecnología, Militar, Otros). |
| `category_en` | String | Categoría en inglés. |
| `location` | String | Ubicación (EEUU, Europa, China, Resto). |
| `location_en` | String | Ubicación en inglés. |
| `covered` | Boolean | `False` por defecto (indica si está en YouTube). |
| `date` | String | Fecha en formato ISO (YYYY-MM-DD). |
| `image` | String | Nombre del archivo de imagen (ej: `nombre.png`). SIN RUTA. |
| `slug` | String | URL amigable única (ej: `mision-asteroides-esa`). |
| `tags` | JSON | Lista de etiquetas en español (ej: `["Espacio", "Ciencia"]`). |
| `tags_en` | JSON | Lista de etiquetas en inglés (ej: `["Space", "Science"]`). |
| `featured` | Boolean | `False` por defecto. |
| `linkyoutube` | String | Enlace opcional a YouTube. |
| `rutanoticia` | String | Ruta completa al archivo (ej: `/api/v1/news_content/noticia1.md`). |
| `timestart` | Integer | Segundo de inicio en el vídeo (opcional). |
| `show` | Boolean | `True` por defecto. |

## 2. Instrucciones de Extracción

Para cada noticia, tendrás dos archivos: `archivo.md` (español) y `archivo_en.md` (inglés). 

**NOTA IMPORTANTE:** Aunque el frontend puede cargar los archivos `_en.md` dinámicamente, es recomendable persistir el contenido básico en la base de datos para facilitar búsquedas y consistencia.

### Procedimiento:
1.  **Título:** Extraer del encabezado `# H1`.
2.  **Fecha:** Buscar la línea que indica `**Fecha:**` o extraerla del prefijo numérico del nombre del archivo (ej: `260328` -> `2026-03-28`). Convertir a formato `YYYY-MM-DD`.
3.  **Resumen (Excerpt/Excerpt_en):** Generar un resumen de 2-3 frases a partir del primer párrafo del cuerpo (uno para español y otro para inglés).
4.  **Slug:** Generar un slug a partir del título en español (minúsculas, sin acentos, espacios por guiones).
6.  **Categoría y Lugar:** Identificar la entidad principal (SpaceX, NASA, China, etc.) y asignar la categoría y ubicación correspondientes según la tabla del punto 1.
7.  **Featured y YouTube:** Si se proporciona un enlace de YouTube (`linkyoutube`), el campo `featured` debe establecerse automáticamente en `True`.
8.  **Timestart:** Si se proporciona un archivo o lista con los tiempos de inicio por noticia, deberás incluir el valor `timestart` correspondiente para esa noticia.
9.  **Imagen:** 
      *   **Creación de Imágenes:** Por cada noticia, solicita o genera una imagen representativa (formato `.webp` o `.png`) y asegúrate de que se guarde en la carpeta `D:\YoutubeElProximoFrameworkEnElEspacio\Web\backendfast\news_images`. El nombre de la imagen debe coincidir con el valor del campo `image` redactado en el JSON (sin el prefijo `/api/v1/news_images/`).
      *   El campo `image` en la BBDD **SOLO** debe contener el nombre del archivo (ej: `mi_imagen.png`).
      *   Si no hay imagen previa, dejar como `null` o usar una por defecto si se indica.
10. **Etiquetas:** Generar una lista de 3 a 5 palabras clave relevantes para el contenido.
11. **Ruta Noticia:** Usar siempre la ruta completa `/api/v1/news_content/` seguida del nombre del archivo en español (ej: `/api/v1/news_content/260328_informe.md`).
12. **Link Noticia:** Si se proporciona un enlace externo de la noticia original, guárdalo opcionalmente.

## 3. Formato de Salida

Genera un script de Python que utilice SQLAlchemy para insertar estos registros, o un archivo JSON con la lista de objetos listos para ser procesados.

### Ejemplo de Estructura JSON:
```json
{
  "title": "Informe Técnico: Project Sunrise",
  "title_en": "Technical Report: Project Sunrise",
  "excerpt": "Blue Origin presenta Project Sunrise, una constelación de centros de datos orbitales...",
  "excerpt_en": "Blue Origin unveils Project Sunrise, a constellation of orbital data centers...",
  "category": "Sector Privado",
  "category_en": "Private Sector",
  "location": "EEUU",
  "location_en": "USA",
  "date": "2026-03-28",
  "slug": "informe-tecnico-project-sunrise-blue-origin",
  "rutanoticia": "260328_informe_tecnico_blue_origin_sunrise.md",
  "tags": ["Blue Origin", "IA", "Satélites"],
  "tags_en": ["Blue Origin", "AI", "Satellites"]
}
```

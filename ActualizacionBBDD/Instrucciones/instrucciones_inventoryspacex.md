# Prompt de Instrucciones para Rellenar la Tabla `spacex_inventory`

Tu objetivo es investigar versiones específicas de hardware de SpaceX (Starship, Super Heavy, Raptor, etc.) o lanzamientos, y generar los datos necesarios para insertar o actualizar registros en la tabla `spacex_inventory` de la base de datos PostgreSQL, tanto en el entorno **local** como en el **remoto (Railway)**.

## 0. Conexiones de Base de Datos

Deberás ejecutar las operaciones en ambas bases de datos:

*   **Local:** `postgresql://space_user:space_password@localhost:5433/space_db`
*   **Remoto (Railway):** `postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway`

## 1. Referencia del Esquema de la Tabla `spacex_inventory`

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | Integer | Clave primaria. |
| `title` | String | Nombre del objeto (ej: "Starship SN15"). |
| `title_en` | String | Nombre en inglés. |
| `excerpt` | String | Resumen corto técnico en español. |
| `excerpt_en` | String | Resumen corto técnico en inglés. |
| `category` | String | Starship, Super Heavy, Raptor, Test, Lanzamientos. |
| `category_en` | String | Starship, Super Heavy, Raptor, Test, Launchs. |
| `location` | String | Starbase, Florida, McGregor, Otros. |
| `location_en` | String | Starbase, Florida, McGregor, Others. |
| `version` | String | Versión técnica (ej: "V2", "Block 2", "SN15"). |
| `datestartfabrication`| String | Fecha inicio fabricación (opcional). |
| `datesfinishfabrication`| String | Fecha fin fabricación (opcional). |
| `state` | String | desechado, destruido, retirado, en fabricación, en testing, activo, reutilizado. |
| `state_en` | String | scrapped, destroyed, retired, in fabrication, in testing, active, reused. |
| `datelaunch` | String | Fecha de lanzamiento (si aplica). |
| `resultlaunch` | String | Resultado del lanzamiento (ej: "Éxito", "Fallo"). |
| `resultlaunch_en` | String | Outcome (Success, Failure, Partial Success). |
| `date` | String | Fecha de referencia para ordenación (ISO YYYY-MM-DD). |
| `image` | String | Ruta: `/inventory_images/{categoria}/{slug}.png`. |
| `slug` | String | Identificador único (ej: `raptor-v3`). **USAR PARA CHECK DE REPETIDOS.** |
| `rutainformacion` | String | Ruta relativa al MD: `{categoria}/{slug}`. |
| `show` | Boolean | `True` por defecto. |

## 2. Instrucciones de Investigación y Generación

Cuando recibas una lista de ítems, sigue este procedimiento por cada uno:

### A. Investigación Técnica
1.  **Buscar en Internet:** Busca especificaciones reales (Empuje, presión, fechas de hitos, estado actual).
2.  **Detección de Duplicados:** Antes de insertar, verifica si el `slug` ya existe en la base de datos. Si existe, realiza un **UPDATE** con la información más reciente; si no, realiza un **INSERT**.

### B. Generación de Contenido (Markdown)
Generar dos archivos en `D:\YoutubeElProximoFrameworkEnElEspacio\Web\backendfast\inventory_docs\{categoria}/`:
1.  `{slug}.md` (Español): Título H1, secciones de "Especificaciones Técnicas", "Historia" e "Innovaciones".
2.  `{slug}_en.md` (Inglés): Traducción técnica precisa del anterior.

### C. Generación de Imagen
1.  Generar una imagen representativa del hardware usando una herramienta de IA.
2.  Guardarla en `D:\YoutubeElProximoFrameworkEnElEspacio\Web\backendfast\inventory_images\{categoria}/{slug}.png`.

### D. Registro en Base de Datos
1.  Asegúrate de que el campo `rutainformacion` apunte a `{categoria}/{slug}` (sin extensión .md).
2.  El campo `image` debe ser la ruta servida por la API: `/inventory_images/{categoria}/{slug}.png`.

## 3. Ejemplo de Lógica de Inserción (Python/SQLAlchemy)

```python
existing = db.query(SpaceXInventory).filter(SpaceXInventory.slug == data['slug']).first()
if existing:
    # Actualizar campos
    for key, value in data.items():
        setattr(existing, key, value)
else:
    # Crear nuevo registro
    new_item = SpaceXInventory(**data)
    db.add(new_item)
db.commit()
```

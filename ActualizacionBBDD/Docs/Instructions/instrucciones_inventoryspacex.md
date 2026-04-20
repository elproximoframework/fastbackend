# Instrucciones para Rellenar la Tabla `spacex_inventory` (v2)

Tu objetivo es procesar un **informe técnico** proporcionado sobre versiones específicas de hardware de SpaceX (Starship, Super Heavy, Raptor, etc.) o lanzamientos, y generar los datos necesarios para insertar o actualizar registros en la tabla `spacex_inventory` de la base de datos PostgreSQL, tanto en el entorno **local** como en el **remoto (Railway)**.

## 0. Conexiones de Base de Datos

Deberás ejecutar las operaciones en ambas bases de datos usando el script proporcionado:

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
| `serial_number`| String | Serial exacto del hardware (ej: "SN15", "B12", "R3-SN1"). |
| `block` | String | Block generacional: "Block 1", "Block 2", "Block 3". |
| `datestartfabrication`| String | Fecha inicio fabricación (opcional). |
| `datesfinishfabrication`| String | Fecha fin fabricación (opcional). |
| `state` | String | desechado, destruido, retirado, en fabricación, en testing, activo, reutilizado. |
| `state_en` | String | scrapped, destroyed, retired, in fabrication, in testing, active, reused. |
| `datelaunch` | String | Fecha de lanzamiento (si aplica). |
| `resultlaunch` | String | Resultado del lanzamiento (ej: "Éxito", "Fallo"). |
| `resultlaunch_en` | String | Outcome (Success, Failure, Partial Success). |
| `specs` | JSON | **NUEVO** Parámetros técnicos estructurados (ver ejemplos abajo). |
| `flight_data` | JSON | **NUEVO** Datos del vuelo IFT: booster, ship, resultados por etapa. |
| `milestones` | JSON | **NUEVO** Lista de hitos: `[{"date": "YYYY-MM-DD", "event": "...", "event_en": "..."}]`. |
| `date` | String | Fecha de referencia para ordenación (ISO YYYY-MM-DD). |
| `image` | String | Ruta: `/inventory_images/{categoria}/{slug}.png`. |
| `slug` | String | Identificador único (ej: `raptor-v3`). **USAR PARA UPSERT.** |
| `rutainformacion` | String | Ruta relativa al MD: `{categoria}/{slug}`. |
| `show` | Boolean | `True` por defecto. |

## 2. Instrucciones de Procesamiento y Generación

Cuando recibas un **informe técnico**, sigue este procedimiento:

### A. Extracción de Datos
1.  Analiza el informe para extraer todos los campos requeridos en la tabla `spacex_inventory`.
2.  Asegúrate de que el `slug` sea consistente y único.

### B. Generación de Contenido (Markdown)
Generar dos archivos en `D:\YoutubeElProximoFrameworkEnElEspacio\Web\backendfast\inventory_docs\{categoria}/`:
1.  `{slug}.md` (Español): Título H1, secciones de "Especificaciones Técnicas", "Historia" e "Innovaciones".
2.  `{slug}_en.md` (Inglés): Traducción técnica precisa del anterior.

### C. Generación de Imagen
1.  Generar una imagen representativa del hardware usando una herramienta de IA.
2.  Guardarla en `D:\YoutubeElProximoFrameworkEnElEspacio\Web\backendfast\inventory_images\{categoria}/{slug}.png`.

### D. Generación de Archivo JSON para Base de Datos
1.  Crea un archivo JSON (ej: `inventory_update.json`) que contenga un objeto (o lista de objetos) con los campos de la tabla.
2.  Asegúrate de que `rutainformacion` apunte a `{categoria}/{slug}` y `image` a `/inventory_images/{categoria}/{slug}.png`.

### E. Actualización de Base de Datos
1.  Utiliza el script de Python para cargar los datos en las bases de datos Local y Remota.

## 3. Ejecución del Script de Actualización

Para sincronizar los datos, ejecuta el siguiente comando desde la raíz del proyecto o la carpeta de scripts:

```bash
python d:\YoutubeElProximoFrameworkEnElEspacio\Web\backendfast\ActualizacionBBDD\Scripts\insert_inventory_from_json.py camino/al/archivo/inventory_update.json
```

Este script detectará automáticamente si el `slug` ya existe para realizar un **UPDATE** o si debe realizar un **INSERT**.

---

## 4. Ejemplos de JSON por Categoría

### Raptor (motor)
```json
{
  "slug": "raptor-v3",
  "title": "Raptor 3",
  "title_en": "Raptor 3",
  "category": "Raptor",
  "category_en": "Raptor",
  "serial_number": "R3",
  "block": "Block 3",
  "version": "Raptor 3",
  "state": "activo",
  "state_en": "active",
  "location": "McGregor, Texas",
  "location_en": "McGregor, Texas",
  "specs": {
    "thrust_sea_level_tf": 280,
    "isp_vacuum_s": 350,
    "mass_engine_kg": 1525,
    "mass_with_vehicle_kg": 1720,
    "chamber_pressure_bar": 350
  },
  "milestones": [
    { "date": "2024-08-02", "event": "Primer Raptor 3 (SN1) revelado públicamente", "event_en": "First Raptor 3 (SN1) publicly revealed" },
    { "date": "2025-11-01", "event": "Hasta SN68 producidos", "event_en": "Up to SN68 produced" }
  ],
  "date": "2024-08-02",
  "image": "/inventory_images/raptor/raptor-v3.png",
  "rutainformacion": "raptor/raptor-v3",
  "show": true
}
```

### Lanzamiento IFT
```json
{
  "slug": "ift-5",
  "title": "IFT-5",
  "title_en": "IFT-5",
  "category": "Lanzamientos",
  "category_en": "Launches",
  "serial_number": "IFT-5",
  "block": "Block 1",
  "version": "Block 1",
  "state": "retirado",
  "state_en": "retired",
  "location": "Starbase",
  "location_en": "Starbase",
  "datelaunch": "2024-10-13",
  "resultlaunch": "Éxito",
  "resultlaunch_en": "Success",
  "flight_data": {
    "ift_number": 5,
    "booster": "B12",
    "ship": "S30",
    "result_booster": "Primera captura por Mechazilla (OLP-1)",
    "result_booster_en": "First catch by Mechazilla (OLP-1)",
    "result_ship": "Amerizaje controlado (Índico)",
    "result_ship_en": "Controlled splashdown (Indian Ocean)",
    "overall_result": "Éxito",
    "overall_result_en": "Success"
  },
  "date": "2024-10-13",
  "image": "/inventory_images/lanzamientos/ift-5.png",
  "rutainformacion": "lanzamientos/ift-5",
  "show": true
}
```

### Vehículo (Ship / Booster)
```json
{
  "slug": "ship-s39",
  "title": "Ship S39",
  "title_en": "Ship S39",
  "category": "Starship",
  "category_en": "Starship",
  "serial_number": "S39",
  "block": "Block 3",
  "version": "Block 3",
  "state": "en testing",
  "state_en": "in testing",
  "location": "Starbase",
  "location_en": "Starbase",
  "specs": {
    "height_m": 50,
    "diameter_m": 9,
    "engines": 6,
    "engine_type": "Raptor 3 (3 SL + 3 Vac)"
  },
  "date": "2026-01-01",
  "image": "/inventory_images/starship/ship-s39.png",
  "rutainformacion": "starship/ship-s39",
  "show": true
}
```

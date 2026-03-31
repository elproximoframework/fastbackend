# Prompt de Instrucciones para Rellenar la Tabla `companies`

Tu objetivo es generar los datos necesarios para insertar registros en la tabla `companies` de la base de datos PostgreSQL, tanto en el entorno **local** como en el **remoto (Railway)**.

El proceso comienza con una **lista de nombres de empresas** que yo te proporcionaré. Para cada empresa de la lista, deberás realizar una búsqueda profunda para completar todos los campos del esquema.

## 0. Conexiones de Base de Datos

Deberás ejecutar las inserciones en ambas bases de datos:

*   **Local:** `postgresql://space_user:space_password@localhost:5433/space_db`
*   **Remoto (Railway):** `postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway`

## 1. Referencia del Esquema de la Tabla `companies`

> [!IMPORTANT]
> Los nombres de las columnas son **sensibles a mayúsculas/minúsculas (Case-Sensitive)** en la base de datos PostgreSQL. Debes usar exactamente los nombres indicados (incluyendo CamelCase).

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | Integer | Clave primaria (autoincremental). |
| `name` | String | Nombre oficial de la empresa (ej: `SpaceX`). |
| `type` | String | Tipo de entidad (`startup`, `corporate`, `agency`, `academia`, `investor`, `non_profit`, `other`). |
| `country` | String | Código ISO del país (ej: `us`, `es`). |
| `countryName` | String | **(CamelCase)** Nombre completo del país (ej: `EEUU`). |
| `city` | String | Ciudad de la sede principal. |
| `coordinates` | JSON | Objeto con latitud y longitud: `{"lat": 28.5, "lng": -80.6}`. |
| `employees` | Integer | Número aproximado de empleados. |
| `website` | String | URL oficial del sitio web. |
| `description` | String | Descripción detallada en español. |
| `description_en` | String | Descripción detallada en inglés. |
| `founded` | Integer | Año de fundación (ej: `2002`). |
| `ceo` | String | Nombre del actual CEO. |
| `sector` | String | Sector principal (ver lista abajo). |
| `tags` | JSON | Lista de etiquetas: `["Reusable", "Mars"]`. |
| `socialLinks` | JSON | **(CamelCase)** Enlaces sociales: `{"twitter": "...", "linkedin": "..."}`. |
| `keyPrograms` | JSON | **(CamelCase)** Programas principales: `["Starship", "Falcon 9"]`. |
| `fundingStage` | String | **(CamelCase)** Fase de financiación (ej: `Public`). |
| `totalFunding` | String | **(CamelCase)** Financiación total (ej: `$2B`). |
| `stockTicker` | String | **(CamelCase)** Ticker de bolsa (ej: `PLTR`). |
| `otrassede` | String | Otras sedes o sucursales. |
| `logo` | String | Nombre del archivo de imagen (ej: `spacex.png`). |
| `featured_espacio` | Boolean | Determina si la empresa aparece en la página "Espacio". |
| `show` | Boolean | True por defecto. |

...

## 3. Formato de Salida y Ejecución

Para insertar los datos, utiliza el script robusto que maneja automáticamente las mayúsculas en los nombres de las columnas:

**Script:** `D:\YoutubeElProximoFrameworkEnElEspacio\Web\backendfast\ActualizacionBBDD\Scripts\insert_companies_from_json.py`

**Comando:**
```bash
python D:\YoutubeElProximoFrameworkEnElEspacio\Web\backendfast\ActualizacionBBDD\Scripts\insert_companies_from_json.py ruta/a/tu/archivo.json
```

> [!TIP]
> El script ahora utiliza `psycopg2.sql` para proteger los identificadores. Esto garantiza que columnas como `countryName` se inserten correctamente sin importar las restricciones de PostgreSQL sobre minúsculas automáticas.

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
  "otrassede": null,
  "logo": "spacex.png",
  "featured_espacio": false,
  "show": true
}
```

*Nota: Asegúrate de incluir todos los campos, incluso si son `null` o listas vacías, para mantener la consistencia.*

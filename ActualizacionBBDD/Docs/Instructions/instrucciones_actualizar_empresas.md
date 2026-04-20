# Guía de Enriquecimiento de Datos de Empresas (BBDD Space)

Este documento describe el flujo de trabajo para completar la información técnica de las empresas registradas en la tabla `companies`. Este proceso debe ser ejecutado por un modelo de IA con acceso a búsqueda en internet y herramientas de base de datos.

## 0. Conexiones de Base de Datos

Las actualizaciones deben aplicarse en ambos entornos:

*   **Local:** `postgresql://space_user:space_password@localhost:5433/space_db`
*   **Remoto (Railway):** `postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway`

## 1. Flujo de Trabajo

### Paso 1: Lectura de Datos Iniciales
Se te proporcionará uno o varios **IDs**. Tu primera tarea es consultar la tabla `companies` para obtener los campos básicos que ya existen (generalmente `name` y `country`).

### Paso 2: Investigación (Deep Search)
Utiliza el nombre de la empresa y su país para realizar una búsqueda exhaustiva en internet. Debes localizar:
*   Sitio web oficial.
*   Descripción detallada de sus actividades (en español e inglés).
*   Año de fundación y CEO actual.
*   Número aproximado de empleados.
*   Sedes adicionales (si existen).
*   Programas espaciales o productos estrella.
*   Fase de financiación y monto (si aplica).
*   Redes sociales (LinkedIn y Twitter/X).

### Paso 3: Normalización de Categorías (Frontend Match)
Para que la interfaz de usuario muestre la empresa correctamente, **DEBES** mapear la información a los siguientes valores predefinidos:

#### Tipos de Empresa (`type`)
`startup`, `corporate`, `agency`, `academia`, `investor`, `non_profit`, `other`.

#### Sectores (`sector`)
`launchers`, `satellites`, `ground_segment`, `propulsion`, `space_tourism`, `defense`, `research`, `software`, `manufacturing`, `satellite_manufacturing`, `satellite_components`, `space_equipment`, `space_tech`, `launch_site`, `student_rocketry`, `earth_observation`, `in_space_logistics`, `ssa`, `satcom`, `incubator`, `innovation_hub`, `space_services`, `space_infrastructure`, `regulatory_body`.

## 2. Referencia Completa del Esquema

| Campo | Tipo | Tratamiento / Descripción |
| :--- | :--- | :--- |
| `id` | Integer | Clave primaria. Se te proporcionará para iniciar el flujo. |
| `name` | String | Nombre oficial. Se obtiene del ID antes de la búsqueda. |
| `slug` | String | Versión amigable para URL (ej: `spacex`). |
| `type` | String | `startup`, `corporate`, `agency`, `academia`, `investor`, `non_profit`, `other`. |
| `country` | String | Código ISO de 2 letras (ej: `us`, `fr`, `es`). |
| `countryName` | String | Nombre completo del país (ej: `Francia`, `España`). |
| `city` | String | Ciudad de la sede principal. |
| `coordinates` | JSON | Objeto: `{"lat": 0.0, "lng": 0.0}`. |
| `employees` | Integer | Número aproximado de empleados. |
| `website` | String | URL oficial (comenzando con `https://`). |
| `description` | String | Descripción técnica detallada en **Español** (2-3 párrafos). |
| `description_en` | String | Descripción técnica detallada en **Inglés**. |
| `founded` | Integer | Año de fundación (ej: `1965`). |
| `ceo` | String | Nombre completo del CEO actual. |
| `sector` | String | Sector principal (ver lista de sectores arriba). |
| `tags` | JSON | Lista de etiquetas de búsqueda: `["Satellite", "IoT"]`. |
| `socialLinks` | JSON | Objeto: `{"twitter": "...", "linkedin": "..."}`. |
| `keyPrograms` | JSON | Lista de programas/productos: `["Falcon 9", "Starlink"]`. |
| `fundingStage` | String | Fase de financiación (p. ej., `Series B`, `Public`). |
| `totalFunding` | String | Monto total recaudado (p. ej., `$150M`). |
| `stockTicker` | String | Ticker de bolsa si aplica (p. ej., `PLTR`). Si no, `null`. |
| `otrassede` | String | Texto con otras ubicaciones o centros de la empresa. |
| `logo` | String | Nombre del archivo: `nombre_empresa.png` (minúsculas, sin espacios). |
| `featured_espacio` | Boolean | `false` por defecto, a menos que se indique lo contrario. |
| `show` | Boolean | `true` por defecto para que sea visible en la aplicación. |

## 3. Ejecución de la Actualización

Una vez recolectada la información, utiliza el script de actualización del proyecto para sincronizar los cambios de forma segura (el script realiza un `UPSERT` basado en el nombre):

**Comando:**
```bash
python d:\YoutubeElProximoFrameworkEnElEspacio\Web\backendfast\ActualizacionBBDD\Scripts\insert_companies_from_json.py datos_empresa.json
```

---
> [!IMPORTANT]
> No inventes datos. Si un campo como `totalFunding` no es público, déjalo como `null`. Prioriza la calidad de las descripciones técnicas.

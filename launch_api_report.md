# Informe: Capacidades de la API Launch Library 2 (v2.3.0)

Este informe detalla las funcionalidades y endpoints disponibles en la versión **2.3.0** (la más reciente y recomendada) de la API de **The Space Devs (Launch Library 2)**.

## 📌 Información General
- **Base URL:** `https://ll.thespacedevs.com/2.3.0/`
- **Formato:** JSON
- **Estado:** Versión actual recomendada para producción.
- **Límite de Peticiones (Gratis):** Aproximadamente 15 peticiones por hora.

---

## 🚀 Endpoints de Lanzamientos (`/launches/`)

> [!IMPORTANT]
> A partir de la v2.3.0, el endpoint principal es en plural: `/launches/`. El antiguo `/launch/` (singular) devolverá un error 404 en esta versión.

### 1. Próximos Lanzamientos (`/launches/upcoming/`)
- **Uso:** Obtener lanzamientos futuros.
- **Ejemplo:** `https://ll.thespacedevs.com/2.3.0/launches/upcoming/`

### 2. Lanzamientos Pasados (`/launches/previous/`)
- **Uso:** Historial de misiones completadas.
- **Ejemplo:** `https://ll.thespacedevs.com/2.3.0/launches/previous/`

---

## 🔄 Cambios Clave en la v2.3.0 (vs v2.2.0)

| Característica | Cambio en v2.3.0 |
|----------------|------------------|
| **Endpoint** | `/launch/` (singular) ➔ `/launches/` (plural). |
| **Renombramiento** | `vidURLs` ahora es `vid_urls`. |
| **Renombramiento** | `infoURLs` ahora es `info_urls`. |
| **Eliminación** | Se ha eliminado el campo `holdreason`. |
| **Eliminación** | Se ha eliminado `launch_library_url`. |
| **Filtros** | Los filtros `lsp__ids` y `lsp__id` se han unificado en `lsp__id`. |
| **Cuerpos Celestes** | Nuevo objeto `celestial_body` en localizaciones para soportar misiones en la Luna, Marte, etc. |

---

## 🔍 Parámetros de Filtrado

| Parámetro | Descripción |
|-----------|-------------|
| `search` | Búsqueda global (nombre, cohete, agencia). |
| `limit` / `offset` | Control de paginación. |
| `mode` | `list`, `normal`, o `detailed`. (Usa `detailed` para ver `vid_urls`). |
| `lsp__id` | Filtrar por ID de la agencia (acepta múltiples separados por coma). |
| `net__gte` / `net__lte` | Filtrado por rango de fechas (ISO 8601). |

---

## 💡 Próximos Pasos Sugeridos

1. **Dashboard de Lanzamientos:** Implementar una vista en el frontend que consuma `/launches/upcoming/`.
2. **Soporte Multicuerpo Celular:** Preparar la base de datos para lanzamientos que no sean desde la Tierra (gracias al nuevo objeto `celestial_body`).
3. **Caché Responsable:** Implementar una capa de caché en el backend para no exceder el límite de 15 peticiones/hora.
4. **Integración de Video:** Utilizar el nuevo campo `vid_urls` para incrustar streamings de YouTube directamente en la web.

---
*Informe actualizado para la v2.3.0 (Plural) - Proyecto "El Próximo Framework en el Espacio".*

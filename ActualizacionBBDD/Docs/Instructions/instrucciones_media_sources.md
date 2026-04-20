# Prompt de Instrucciones para Rellenar la Tabla `media_sources`

Tu objetivo es generar los datos necesarios para insertar registros en la tabla `media_sources` de la base de datos PostgreSQL, tanto en el entorno **local** como en el **remoto (Railway)**.

El proceso comienza con un **nombre o una lista de nombres de medios** que yo te proporcionaré. Para cada medio, **deberás buscar activamente la información en internet** antes de rellenar ningún campo.

> [!CAUTION]
> **BÚSQUEDA WEB OBLIGATORIA — SIN EXCEPCIONES.**
> Antes de generar el JSON de cualquier medio, **debes realizar una búsqueda en internet** para verificar y obtener los datos reales: URL del sitio web, handle de YouTube, perfil de Twitter, etc.
> **Está terminantemente prohibido inventar o suponer URLs, handles o datos del medio basándote únicamente en tu memoria de entrenamiento.** Los datos desactualizados o inventados rompen los enlaces en la web y dañan la credibilidad del directorio.
> Si después de buscar no encuentras un dato concreto con certeza, usa `null`.
> **No hay excepciones a esta regla, ni siquiera para medios muy conocidos.**

## 0. Conexiones de Base de Datos

Deberás ejecutar las inserciones en ambas bases de datos:

* **Local:** `postgresql://space_user:space_password@localhost:5433/space_db`
* **Remoto (Railway):** `postgresql://postgres:zjRYAsATFmvPlnQOZruilNIwwEBZcmyU@crossover.proxy.rlwy.net:29288/railway`

---

## 1. Referencia del Esquema de la Tabla `media_sources`

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | Integer | Clave primaria (autoincremental). No incluir en el JSON. |
| `slug` | String | URL-friendly único (ej: `nasaspaceflight-nsf`). Minúsculas, sin acentos, espacios por guiones. |
| `category` | String | Tipo de medio. Ver valores permitidos abajo. |
| `subcategory` | String | Subtipo dentro de la categoría. Ver valores permitidos abajo. |
| `language` | String | Idioma principal: `'es'`, `'en'`, `'fr'`, `'de'`, `'multi'`. |
| `country` | String | Código ISO del país (ej: `'us'`, `'es'`, `'eu'`). Usar `'int'` para Internacional. |
| `country_name` | String | Nombre legible del país (ej: `'EEUU'`, `'España'`, `'Internacional'`). |
| `name` | String | Nombre completo del medio (ej: `'NASASpaceflight (NSF)'`). |
| `description` | Text | Descripción en **español** (2-4 frases). Qué es, qué cubre, por qué es relevante. |
| `description_en` | Text | Descripción en **inglés** (2-4 frases). |
| `tagline` | String | Frase corta en español que define el medio (máx. 10 palabras). |
| `tagline_en` | String | Frase corta en inglés (máx. 10 palabras). |
| `rating` | Integer | Valoración editorial de 1 a 5. Ver criterios abajo. |
| `recommended` | Boolean | `true` si es uno de los medios más recomendados del sector. |
| `difficulty` | String | Nivel del contenido: `'general'`, `'intermedio'`, `'avanzado'`, `'experto'`. |
| `website` | String | URL completa del sitio web principal (ej: `'https://www.spacenews.com'`). Null si no aplica. |
| `youtube_url` | String | URL del canal de YouTube, o del vídeo/tráiler si es documental. Null si no aplica. |
| `youtube_handle` | String | Handle del canal sin la @ (ej: `'NASASpaceflight'`). Null si no aplica. |
| `twitter_url` | String | URL del perfil en X/Twitter. Null si no aplica. |
| `instagram_url` | String | URL del perfil en Instagram. Null si no aplica. |
| `linkedin_url` | String | URL del perfil en LinkedIn. Null si no aplica. |
| `spotify_url` | String | URL del podcast en Spotify (solo para category `'podcast'`). Null si no aplica. |
| `apple_podcasts_url` | String | URL del podcast en Apple Podcasts. Null si no aplica. |
| `rss_feed_url` | String | URL del feed RSS del medio. Null si no aplica. |
| `newsletter_url` | String | URL de la página de suscripción a la newsletter. Null si no aplica. |
| `content_format` | JSON | Lista de formatos disponibles. Ver valores permitidos abajo. |
| `topics` | JSON | Lista de temas que cubre el medio. Ver valores permitidos abajo. |
| `is_free` | Boolean | `true` si el acceso principal es gratuito. |
| `paywall` | Boolean | `true` si tiene paywall o suscripción de pago para contenido completo. |
| `featured` | Boolean | `false` por defecto. Poner `true` solo si se indica explícitamente. |
| `show` | Boolean | `true` por defecto. |

---

## 2. Valores Permitidos por Campo

### `category` (obligatorio)
| Valor | Descripción |
|---|---|
| `'portal'` | Portal web de noticias |
| `'youtube'` | Canal de YouTube |
| `'revista'` | Revista especializada |
| `'podcast'` | Podcast de audio |
| `'newsletter'` | Boletín de suscripción por correo |
| `'agency'` | Agencia gubernamental oficial |
| `'social'` | Cuenta en redes sociales (X/Twitter, etc.) |
| `'blog'` | Blog tecnico o de divulgacion independiente |
| `'documental'` | Documental, película o serie |

### `subcategory` (opcional pero recomendado)
| Valor | Usar cuando... |
|---|---|
| `'divulgacion'` | Contenido para público general / educativo |
| `'industria'` | Foco en negocios, inversión y sector B2B |
| `'tecnico'` | Contenido de ingeniería, análisis técnico profundo |
| `'amateur'` | Creador independiente / aficionado |
| `'institucional'` | Canales oficiales de agencias o instituciones |
| `'pelicula'` | Película de ficción o documental cinematográfico |
| `'serie'` | Serie de televisión o streaming |
| `'documental_corto'` | Documental breve o episódico |

### `difficulty`
| Valor | Descripción |
|---|---|
| `'general'` | Apto para cualquier público sin conocimientos previos |
| `'intermedio'` | Requiere interés en el sector pero no formación técnica |
| `'avanzado'` | Para entusiastas con buenas bases técnicas |
| `'experto'` | Para profesionales e ingenieros del sector |

### `content_format` (JSON array)
Valores posibles para incluir en la lista:
`"video"`, `"articulo"`, `"live"`, `"analisis"`, `"entrevista"`, `"audio"`, `"newsletter"`, `"imagen"`, `"pelicula"`, `"serie"`, `"documental"`

### `topics` (JSON array)
Usar entre 3 y 6 temas de los siguientes (o similares si no aparecen aquí):
`"Starship"`, `"SpaceX"`, `"NASA"`, `"ESA"`, `"Lanzamientos"`, `"Astrofísica"`, `"Astronomía"`, `"Industria Espacial"`, `"Política Espacial"`, `"New Space"`, `"Cohetes"`, `"Satélites"`, `"Exploración Lunar"`, `"Marte"`, `"Historia Espacial"`, `"ISS"`, `"Defensa"`, `"Divulgación Científica"`, `"Ingeniería"`, `"Misiones"`, `"Telescopios"`, `"Exoplanetas"`, `"Cosmología"`

### `rating` — Criterios Editoriales
| Puntuación | Criterio |
|---|---|
| `5` | Referencia absoluta del sector. Imprescindible. |
| `4` | Muy recomendable. Alta calidad y relevancia. |
| `3` | Buena fuente, valor añadido claro. |
| `2` | Interesante pero complementario. |
| `1` | Nicho muy específico o calidad irregular. |

---

## 3. Instrucciones de Generación

Para cada nombre de medio que te proporcione, sigue este procedimiento **en orden estricto**:

1. **🔍 BÚSQUEDA WEB — Paso obligatorio y previo a todo lo demás.**
   Antes de escribir una sola línea de JSON, **busca en internet el medio**. Debes verificar:
   - URL oficial del sitio web (accede y confirma que existe).
   - URL exacta del canal de YouTube (búscalo en YouTube directamente).
   - Handle de YouTube (el `@handle` real, no el que crees recordar).
   - Perfil oficial en X/Twitter.
   - Perfil en Spotify o Apple Podcasts si es un podcast.
   - Si es un documental/película, búscalo en IMDb y verifica la URL de Netflix/Amazon/Apple.
   Usa los resultados reales de la búsqueda. **No uses tu memoria de entrenamiento como fuente primaria para los URLs.**

2. **Slug:** Generar a partir del nombre (minúsculas, sin acentos, espacios → guiones). Añadir sufijo descriptivo si hay ambigüedad (ej: `scott-manley-youtube`).
3. **Category y Subcategory:** Infiere a qué tipo pertenece. Si es un canal de YouTube, `category = 'youtube'`. Si es una web, `category = 'portal'`. Si es documental, `category = 'documental'` y elige la subcategory correcta.
4. **Language y Country:** Basándote en los resultados de la búsqueda. Si tiene contenido en varios idiomas, usar `'multi'`. Para canales/medios sin sede fija, usar `country = 'int'` y `country_name = 'Internacional'`.
5. **Description (es/en):** Redacta 2-4 frases: explica qué es el medio, qué tipo de contenido ofrece y para quién es relevante.
6. **Tagline:** Una frase muy corta y memorable que capture la esencia del medio.
7. **Rating:** Aplica los criterios editoriales de la sección 2.
8. **Recommended:** Poner `true` solo si es ampliamente reconocido como referencia clave en el sector.
9. **Difficulty:** Evalúa el nivel técnico habitual del contenido.
10. **Links:** Rellena **solo con URLs verificadas en la búsqueda del paso 1**. Si un link no apareció en los resultados de búsqueda o no pudiste confirmar que existe, usa `null`. **Nunca construyas una URL a partir de suposiciones** (ej: no asumas que `@NombreCanal` es el handle real sin haberlo buscado).
11. **Content Format:** Elige los formatos que realmente ofrece el medio.
12. **Topics:** Selecciona entre 3 y 6 temas relevantes del listado permitido.
13. **is_free / paywall:** Verifica el modelo de acceso real del medio en la búsqueda.

> [!WARNING]
> **No inventes URLs — busca siempre primero.** Si después de buscar en internet no puedes confirmar una URL (website, youtube, twitter, etc.), usa `null`. Un campo vacío es mejor que un enlace roto o incorrecto.

> [!IMPORTANT]
> El `slug` debe ser **único**. Si te proporciono un medio que ya intuyes podría estar en la BBDD, avísame antes de insertar para evitar conflictos.

---

## 4. Formato de Salida

Genera un archivo JSON con la lista de objetos. Guárdalo en la carpeta:
`D:\YoutubeElProximoFrameworkEnElEspacio\Web\backendfast\ActualizacionBBDD\Scripts\`

Con el nombre `media_sources_[descripcion].json` (ej: `media_sources_youtubers_es.json`).

### Ejemplo de estructura JSON completa:

```json
[
  {
    "slug": "nasaspaceflight-nsf",
    "category": "youtube",
    "subcategory": "tecnico",
    "language": "en",
    "country": "us",
    "country_name": "EEUU",
    "name": "NASASpaceflight (NSF)",
    "description": "NASASpaceflight es el canal de referencia para el seguimiento técnico y en directo de todos los vehículos de lanzamiento orbitales. Cubre Starship, SLS, Falcon 9 y cualquier cohete significativo con análisis fotográfico diario y foros de ingeniería. Es el canal más técnico y riguroso del sector en YouTube.",
    "description_en": "NASASpaceflight is the go-to channel for technical and live tracking of all orbital launch vehicles. It covers Starship, SLS, Falcon 9, and any significant rocket with daily photographic analysis and engineering forums. It is the most technical and rigorous channel in its field on YouTube.",
    "tagline": "El seguimiento orbital más técnico de YouTube",
    "tagline_en": "The most technical orbital tracking on YouTube",
    "rating": 5,
    "recommended": true,
    "difficulty": "avanzado",
    "website": "https://www.nasaspaceflight.com",
    "youtube_url": "https://www.youtube.com/@NASASpaceflight",
    "youtube_handle": "NASASpaceflight",
    "twitter_url": "https://twitter.com/NASASpaceflight",
    "instagram_url": null,
    "linkedin_url": null,
    "spotify_url": null,
    "apple_podcasts_url": null,
    "rss_feed_url": null,
    "newsletter_url": null,
    "content_format": ["video", "live", "analisis"],
    "topics": ["Starship", "SpaceX", "NASA", "Lanzamientos", "Cohetes", "Ingeniería"],
    "is_free": true,
    "paywall": false,
    "featured": false,
    "show": true
  },
  {
    "slug": "everyday-astronaut",
    "category": "youtube",
    "subcategory": "divulgacion",
    "language": "en",
    "country": "us",
    "country_name": "EEUU",
    "name": "Everyday Astronaut",
    "description": "Everyday Astronaut es el canal de Tim Dodd, conocido por sus explicaciones visuales y detalladas sobre ingeniería de cohetes, propulsión y programas espaciales. Famoso por sus guías de Starship y sus entrevistas con Elon Musk y otros líderes de la industria. Perfecto para quienes quieren entender 'cómo funciona' sin perder el rigor técnico.",
    "description_en": "Everyday Astronaut is Tim Dodd's channel, known for its visual and detailed explanations of rocket engineering, propulsion and space programs. Famous for Starship guides and interviews with Elon Musk and other industry leaders. Perfect for those who want to understand 'how it works' without losing technical rigor.",
    "tagline": "Ingeniería de cohetes explicada para todos",
    "tagline_en": "Rocket engineering explained for everyone",
    "rating": 5,
    "recommended": true,
    "difficulty": "intermedio",
    "website": "https://everydayastronaut.com",
    "youtube_url": "https://www.youtube.com/@EverydayAstronaut",
    "youtube_handle": "EverydayAstronaut",
    "twitter_url": "https://twitter.com/Erdayastronaut",
    "instagram_url": null,
    "linkedin_url": null,
    "spotify_url": null,
    "apple_podcasts_url": null,
    "rss_feed_url": null,
    "newsletter_url": null,
    "content_format": ["video", "entrevista", "analisis"],
    "topics": ["Starship", "SpaceX", "Cohetes", "Ingeniería", "Lanzamientos"],
    "is_free": true,
    "paywall": false,
    "featured": false,
    "show": true
  },
  {
    "slug": "return-to-space-netflix",
    "category": "documental",
    "subcategory": "documental",
    "language": "multi",
    "country": "us",
    "country_name": "EEUU",
    "name": "Return to Space",
    "description": "Documental de Netflix dirigido por Elizabeth Chai Vasarhelyi y Jimmy Chin que sigue la misión Crew Dragon Demo-2 de SpaceX, la primera misión tripulada de una empresa privada a la ISS. Ofrece acceso sin precedentes a los astronautas Bob Behnken y Doug Hurley, y al proceso de desarrollo de Crew Dragon.",
    "description_en": "Netflix documentary directed by Elizabeth Chai Vasarhelyi and Jimmy Chin following SpaceX's Crew Dragon Demo-2 mission, the first crewed mission by a private company to the ISS. It offers unprecedented access to astronauts Bob Behnken and Doug Hurley, and the Crew Dragon development process.",
    "tagline": "El regreso de EEUU al espacio con SpaceX",
    "tagline_en": "America's return to space with SpaceX",
    "rating": 5,
    "recommended": true,
    "difficulty": "general",
    "website": "https://www.netflix.com/title/81466146",
    "youtube_url": "https://www.youtube.com/watch?v=0nBTL8OtBSc",
    "youtube_handle": null,
    "twitter_url": null,
    "instagram_url": null,
    "linkedin_url": null,
    "spotify_url": null,
    "apple_podcasts_url": null,
    "rss_feed_url": null,
    "newsletter_url": null,
    "content_format": ["documental"],
    "topics": ["SpaceX", "NASA", "ISS", "Historia Espacial", "Misiones"],
    "is_free": false,
    "paywall": true,
    "featured": false,
    "show": true
  }
]
```

---

## 5. Ejecución del Script de Inserción

Una vez generado el JSON, ejecuta el script de inserción:

**Script:** `D:\YoutubeElProximoFrameworkEnElEspacio\Web\backendfast\ActualizacionBBDD\Scripts\insert_media_sources_from_json.py`

**Comando:**

```bash
python D:\YoutubeElProximoFrameworkEnElEspacio\Web\backendfast\ActualizacionBBDD\Scripts\insert_media_sources_from_json.py ruta\al\archivo.json
```

El script realiza un **upsert** usando el `slug` como identificador único:
- Si el slug **ya existe** → actualiza todos los campos.
- Si el slug **no existe** → inserta un nuevo registro.

> [!TIP]
> Puedes pasar tanto un único objeto `{}` como un array `[{}, {}, ...]`. El script lo maneja automáticamente.

---

## 6. Casos Especiales

### Canales de YouTube en Español con web propia
Si el canal tiene también un sitio web (ej: Everyday Astronaut → everydayastronaut.com), rellena tanto `youtube_url` como `website`. El `category` sigue siendo `'youtube'` si ese es su medio principal.

### Podcasts disponibles en YouTube y Spotify
Rellena todos los links disponibles. El `category` debe ser `'podcast'` aunque también tengan vídeos en YouTube.

### Documentales, Películas y Series
- `website` → enlace a la plataforma oficial o ficha en IMDb.
- `youtube_url` → enlace al tráiler oficial si está disponible en YouTube.
- `is_free` → `false` si está en plataforma de pago. `true` si está disponible en YouTube completo.
- `paywall` → `true` si está en Netflix/Apple/Amazon/etc.

### Agencias Oficiales con múltiples canales
Para NASA, ESA, etc., crear **una entrada por medio relevante** (canal YouTube principal, canal en español si lo tienen, web oficial) con slugs diferenciados: `nasa-youtube`, `nasa-web`, `esa-youtube`, `esa-youtube-es`.

# Informe Técnico: Project Sunrise — Blue Origin y los Centros de Datos Orbitales
**Fecha:** Marzo 2026 | **Clasificación:** Divulgación técnica | **Fuentes:** FCC Filing, SpaceNews, GeekWire, Data Centre Magazine

---

## 1. Contexto: la IA como catalizador del espacio

La explosión de la demanda de computación para inteligencia artificial está saturando la infraestructura terrestre: centros de datos que consumen gigavatios de electricidad, necesitan millones de litros de agua para refrigeración y compiten por suelo urbanizable. En este contexto, varias empresas han empezado a plantear el espacio como **una nueva capa de infraestructura de cómputo**.

El 19 de marzo de 2026, Blue Origin presentó ante la **Comisión Federal de Comunicaciones de EE.UU. (FCC)** una solicitud de autorización para desplegar su propuesta: el **Project Sunrise**, una constelación de hasta 51.600 satélites diseñados específicamente para funcionar como centros de datos en órbita.

---

## 2. Arquitectura de la constelación

### Parámetros orbitales

| Parámetro | Valor |
|---|---|
| Número de satélites | Hasta **51.600** |
| Tipo de órbita | Circular, heliosíncrona (SSO) |
| Altitud | 500 – 1.800 km |
| Inclinación | 97° – 104° |
| Satélites por plano orbital | 300 – 1.000 |
| Separación entre planos | 5 – 10 km en altitud |

La elección de la **órbita heliosíncrona** es deliberada: los satélites permanecen iluminados por el sol casi de forma continua (órbita crepuscular alba-ocaso), maximizando la generación de energía solar y eliminando la variabilidad energética de otras órbitas.

### Comunicaciones entre satélites

- **Enlace primario:** Vínculos ópticos inter-satelitales (*Optical Inter-Satellite Links*, OISL), es decir, láseres de alta velocidad entre satélites, sin uso de espectro de radiofrecuencia para el tráfico principal.
- **Enlace con tierra:** A través de la constelación **TeraWave** de Blue Origin (5.408 satélites, anunciada en enero de 2026), que actúa como red de backhaul mesh hacia las estaciones terrestres.
- **Bandas RF:** Solo para telemetría, seguimiento y control (TT&C), usando banda Ka.
- **Variantes de antena:** Al menos tres variantes por satélite para cubrir diferentes requisitos de cobertura.

---

## 3. Project Sunrise vs. TeraWave: dos capas distintas

Una distinción crítica del ecosistema de Blue Origin:

| Constelación | Función | Nº de satélites | Anuncio |
|---|---|---|---|
| **TeraWave** | Red de conectividad (backbone de comunicaciones) | 5.408 | Enero 2026 |
| **Project Sunrise** | Infraestructura de cómputo en órbita (centros de datos) | 51.600 | Marzo 2026 |

TeraWave es la **autopista de datos**; Project Sunrise es la **granja de servidores** que circula sobre ella. Ambas se complementan y son necesarias para el funcionamiento del sistema completo.

---

## 4. Justificación técnico-económica presentada ante la FCC

Blue Origin argumenta en su solicitud de 14 páginas cuatro ventajas estructurales de los centros de datos orbitales frente a los terrestres:

1. **Energía solar continua** — Eliminación de la dependencia de la red eléctrica terrestre y sus costes de infraestructura.
2. **Sin coste de suelo ni desplazamiento** — El espacio no impone restricciones de uso del territorio ni competencia con otros usos.
3. **Menor presión sobre recursos hídricos** — Los centros de datos terrestres consumen enormes volúmenes de agua para refrigeración. En el vacío, la gestión térmica se realiza por radiación pasiva.
4. **Coste marginal de cómputo inferior** — La combinación de los tres factores anteriores debería reducir el coste por operación de cómputo a escala.

> La compañía afirma que Project Sunrise *"introducirá una nueva capa de cómputo que opera independientemente de las restricciones terrestres"*, funcionando como **complemento** —no sustituto— de la infraestructura en tierra.

---

## 5. Vehículo de lanzamiento: New Glenn

Blue Origin planea desplegar la constelación con su propio cohete pesado **New Glenn**, del que ya ha completado dos vuelos exitosos a fecha de este informe. Esto le otorga una ventaja competitiva clave: no depende de terceros para el lanzamiento, a diferencia de Amazon Leo (Kuiper), que tiene cientos de satélites listos pero sin capacidad de lanzamiento suficiente. Blue Origin será además el proveedor de lanzamiento de 27 misiones de Amazon Leo, lo que genera un potencial conflicto de intereses señalado por analistas del sector.

---

## 6. Panorama competitivo

El mercado de centros de datos orbitales está atrayendo a múltiples actores simultáneamente:

| Empresa | Propuesta | Nº de satélites |
|---|---|---|
| **SpaceX / xAI** | Constelación de datos orbitales | Hasta **1.000.000** |
| **Blue Origin** (Project Sunrise) | Centros de datos en órbita | 51.600 |
| **Starcloud** (Y Combinator + Nvidia) | Datos orbitales con GPUs H100 | 88.000 |
| **Google / Planet Labs** | Project Suncatcher (2 demos) | En fase de prueba |
| **China** (ADA Space + Zhejiang Lab) | Three-Body Computing Constellation | 2.800 (fase 1) |

**SpaceX** ya respondió públicamente calificando los planes de Blue Origin de *"profundamente desproporcionados"*; Blue Origin, a su vez, acusó a SpaceX de carecer de detalles técnicos reales y de poder tardar *"siglos"* en completar su constelación. La **FCC** tendrá que arbitrar entre propuestas que, en conjunto, sumarían más de un millón de satélites nuevos en órbita baja.

El CEO de OpenAI, **Sam Altman**, se ha posicionado escépticamente, calificando los centros de datos orbitales de *"ridículos"* a corto plazo, citando los retos de refrigeración, resistencia a la radiación de los chips y costes de fabricación a escala.

---

## 7. Solicitudes de exención regulatoria

Blue Origin ha pedido a la FCC **exenciones específicas** respecto a los requisitos estándar de despliegue de constelaciones:

- **Exención del plazo de 6 años** para tener el 50% de los satélites en órbita tras la aprobación.
- **Exención del plazo de 9 años** para el despliegue completo.
- Argumento: los satélites están diseñados para minimizar interferencias y cumplir voluntariamente con las directrices de mitigación de basura espacial, incluyendo **desorbitación en menos de 5 años** al final de su vida útil.

---

**Fuentes principales:**
- FCC Filing Blue Origin — Project Sunrise (19 mar. 2026): [fcc.gov](https://fcc.gov)
- SpaceNews (20 mar. 2026): [spacenews.com](https://spacenews.com/blue-origin-joins-the-orbital-data-center-race/)
- GeekWire (21 mar. 2026): [geekwire.com](https://www.geekwire.com/2026/blue-origin-data-center-space-race-project-sunrise/)
- Data Centre Magazine (23 mar. 2026): [datacentremagazine.com](https://datacentremagazine.com/news/project-sunrise-blue-origin-data-centre-space-race)
- New Space Economy (20 mar. 2026): [newspaceeconomy.ca](https://newspaceeconomy.ca/2026/03/20/blue-origin-project-sunrise-the-race-to-build-data-centers-in-orbit/)

# Informe Técnico: Cumbre "Ignition" — NASA reescribe la arquitectura de exploración humana
**Fecha:** 24 marzo 2026 | **Clasificación:** Divulgación técnica | **Fuentes:** NASA.gov, SpaceFlightNow, NASASpaceFlight, SpaceNews, Science/AAAS, ANS

---

## 1. Contexto: el evento Ignition del 24 de marzo de 2026

El administrador de la NASA **Jared Isaacman** convocó el 24 de marzo de 2026, en la sede Mary W. Jackson de la NASA en Washington D.C., el evento denominado **"Ignition"**: una jornada completa de reuniones con contratistas, socios internacionales y medios, en la que la agencia presentó la mayor reestructuración de su programa de exploración humana desde la cancelación del Constellation en 2010.

La presentación se produjo ocho días antes del lanzamiento previsto de **Artemis II** (1 de abril de 2026), con un doble propósito: dar coherencia estratégica al calendario inmediato y trazar una hoja de ruta creíble hacia la **presencia humana permanente en la Luna antes de 2030**.

> *"Esta vez, el objetivo no son banderas y huellas. Esta vez, el objetivo es quedarse."*
> — **Jared Isaacman**, administrador de la NASA, 24 de marzo de 2026

---

## 2. Decisión estratégica: cancelación efectiva del Lunar Gateway

La primera y más impactante decisión anunciada fue la **pausa indefinida del Lunar Gateway** en su forma actual. La estación debía operar en una órbita de halo casi rectilínea (NRHO) a unos 70.000 km de la Luna, sirviendo como punto de encuentro entre las naves Orion y los módulos de aterrizaje comerciales.

### Razones técnicas de la cancelación

| Problema | Impacto |
|---|---|
| Órbita NRHO → penalización de delta-v de ~900 m/s por descenso | Los landers necesitaban enormes reservas de propelente solo para llegar a la superficie |
| Retrasos en el módulo HALO (Northrop Grumman) | Entregado a la NASA en abril de 2025, pero sin fecha de lanzamiento viable |
| Módulo 1-Hab de JAXA | Aún en desarrollo, atrasado |
| Coste de Gateway | Estimado en más de $8.000 M para la configuración inicial, sin retorno científico directo |

El módulo **PPE** (Power and Propulsion Element, construido por Lanteris Space Systems) y el módulo HALO no se desechan: ambos serán **reutilizados** directamente como hardware para la misión SR-1 Freedom y la infraestructura de la base lunar, respectivamente. El Canadarm3 (CSA) podría pasar a formar parte de la logística de superficie.

Carlos García-Galán, hasta entonces Deputy Manager del programa Gateway, fue nombrado **Program Executive de la Moon Base**.

---

## 3. Nuevo calendario Artemis

La reescritura del calendario Artemis es la más profunda desde el inicio del programa:

| Misión | Fecha | Perfil |
|---|---|---|
| **Artemis II** | **1 abril 2026** | Vuelo tripulado circumlunar (trayectoria de retorno libre). Tripulación: Reid Wiseman, Victor Glover, Christina Koch, Jeremy Hansen. 10 días. Sin alunizaje |
| **Artemis III** | **2027** | Rediseñada como misión de prueba en LEO estilo Apolo 9. Acoplamiento Orion + landers comerciales (Starship HLS / Blue Moon) en órbita terrestre baja. Prueba de trajes Axiom y nuevo escudo térmico Orion |
| **Artemis IV** | **2028** | Primer alunizaje tripulado (Polo Sur lunar). Arquitectura de trayectorias cercanas a la Luna; ventanas de aborto reducidas a horas |
| **Artemis V** | **Finales 2028** | Segundo alunizaje; inicio de cadencia semestral. SLS estandarizado con etapa Centaur V de ULA (elimina la etapa EUS y la torre de lanzamiento móvil nº 2) |
| **Artemis VI+** | **2029 en adelante** | Cadencia mínima de 2 alunizajes/año con al menos dos proveedores de landers comerciales |

> **Nota editorial:** Dado el historial de retrasos del sector, múltiples analistas independientes anticipan que el primer alunizaje real (Artemis IV) se producirá entre 2029 y 2031.

---

## 4. Moon Base — Plan de despliegue en tres fases

### Presupuesto y escala

- **Inversión total:** $20.000 millones en 7 años (2026–2032)
  - Fase 1: ~$10.000 M
  - Fases 2 y 3: ~$10.000 M (con reconocimiento de posibles escaladas)
- **Cadencia de misiones robóticas (Fase 1):** hasta 30 alunizajes CLPS en 2027–2028
- **Capacidad de ancho de banda lunar–Tierra:** mínimo 500 Mbit/s (via dos constelaciones de satélites de comunicaciones lunares)
- **Ubicación:** Polo Sur lunar, en los alrededores del cráter Shackleton

---

### Fase 1 (2026–2028): Build, Test, Learn

Transición de misiones aisladas a un **modelo modular y repetible** con alta cadencia:

- Hasta **30 alunizajes robóticos** a través del programa **CLPS 2.0** (contrato de 10 años y 15 de ejecución, capped en $6.000 M)
- Despliegue de constelaciones de satélites para banda ancha e Internet lunar
- **Drones Moonfall (Lunar Hoppers):** herederos del Ingenuity, sin atmósfera, dan saltos propulsivos de hasta 50 km para prospección en cráteres en sombra permanente
- **LTV (Lunar Terrain Vehicle):** rovers no presurizados. Tres contratistas en competición: **Astrolab, Intuitive Machines y Lunar Outpost**. CLPS CX-2 Task Order los llevará al Polo Sur
- **VIPER rover** (lanzamiento 2027, a bordo del lander de Blue Origin): búsqueda de hielo subsuperficial
- Unidades de calentamiento por radioisótopos (RHU) para supervivencia durante las noches lunares de >120 horas

---

### Fase 2 (2029–2032): Establish Early Infrastructure

- Landers CLPS uprated a **5 toneladas de carga útil** por misión; 60 t de cargo total
- **Torres solares** de >10 kW y **reactores nucleares de fisión** a pequeña escala
- Estaciones de recarga inalámbrica para vehículos
- Torres de comunicaciones de superficie con línea de visión directa de 10 km
- **Rover presurizado de JAXA** — 15 t, hábitat móvil para 2 astronautas durante semanas, vida útil 10 años — joya internacional de la fase
- Rovers con tambores dobles para aplanar regolito (carreteras lunares)
- Misiones tripuladas **cada 6 meses** con al menos 2 proveedores de landers

---

### Fase 3 (2033+): Enable Long-Duration Human Presence

- **Hábitats de gran volumen** (incluyendo el MPH de la Agencia Espacial Italiana, ASI, reutilizado del programa Gateway)
- **ISRU industrial:** extracción de agua, O₂, H₂ del regolito lunar para soporte vital y propelente
- Impresoras 3D para construcción con regolito lunar
- **Vehículo Utilitario Lunar (LUV) de la CSA** (Canadá) para movilidad logística
- Capacidad de **retorno de carga a la Tierra** de forma rutinaria
- Red de GPS lunar y constellaciones de observación y relay

---

## 5. Misión Skyfall / SR-1 Freedom — Propulsión Nuclear a Marte

En paralelo a la base lunar, Ignition anunció la primera nave interplanetaria de propulsión nuclear eléctrica de la historia:

### Space Reactor-1 (SR-1) Freedom — Especificaciones técnicas

| Parámetro | Valor |
|---|---|
| Tipo de propulsión | **Nuclear Eléctrica (NEP)** — reactor de fisión genera electricidad para propulsores iónicos de xenón |
| Potencia del reactor | **~20 kWe** (kilovatios eléctricos) |
| Combustible nuclear | Uranio de alta concentración bajo enriquecido (**HALEU**) |
| Bus propulsivo | PPE de Gateway (Lanteris Space Systems) — **ya construido y verificado** |
| Lanzamiento objetivo | **Diciembre 2028** (ventana de transferencia a Marte) |
| Vehículo de lanzamiento | SpaceX Falcon Heavy (contrato previo del PPE para 39A) |
| Masa total estimada | ~5.000 kg + carga útil (margen disponible: ~11.800 kg en Falcon Heavy) |
| Activación del reactor | Dentro de las **48 horas** tras el lanzamiento |
| Duración del viaje a Marte | **~1 año** |
| Gestión tras Marte | Abierta: posible inserción en órbita marciana o flyby hacia otro destino |

> NEP vs. NTP: La SR-1 Freedom usa propulsión nuclear **eléctrica** (el reactor genera electricidad para un propulsor iónico), NO propulsión nuclear **térmica** (que usa el reactor para calentar directamente el propelente). El Isp del sistema iónico es de 3.000–10.000 s frente a los ~450 s del propelente químico, lo que multiplica la eficiencia de masa.

### Carga útil: misión Skyfall

- **3 helicópteros de clase Ingenuity** (AeroVironment + JPL), despliegue en pleno descenso atmosférico sin necesidad de grúa de cielo (*sky crane*)
- Cada helicóptero aterriza de forma autónoma y lleva:
  - Cámaras de alta resolución para mapeo de terreno
  - **Radar de penetración terrestre** para mapear hielo subsuperficial (localización, profundidad, volumen)
  - Sensores para caracterizar pendientes y riesgos para futuros landers tripulados de escala humana
- Cronograma de desarrollo: inicio de diseño detallado en **junio 2026**; hardware listo para integración en **enero 2028**; vehículo completo en pad en **octubre 2028**

---

## 6. Contexto político y financiero

El plan Ignition se enmarca explícitamente en el cumplimiento de la **Executive Order "Ensuring American Space Superiority"** firmada por el presidente Trump en diciembre de 2025. La financiación no requiere incremento del presupuesto de la NASA: Isaacman defiende que los $20.000 M se obtienen cancelando el Gateway, eliminando la torre de lanzamiento móvil nº 2 del SLS y la etapa EUS, y recortando burocracia interna.

La capacidad del Congreso para apropiarlo formalmente —versus reasignar fondos existentes— es la principal incertidumbre financiera a corto plazo.

---

## 7. Críticas y riesgos técnicos identificados

| Riesgo | Fuente |
|---|---|
| Plazo 2028 para SR-1 Freedom considerado no realista por la comunidad científica | Katie Mack (Perimeter Institute), Chase Million (Million Concepts) |
| Arquitectura Artemis aún "incoherente" en detalles de interoperabilidad landers | Mars Society (comunicado 25 mar. 2026) |
| Financiación sin incremento presupuestario no verificada públicamente | SpaceFlightNow, CBS News |
| Retrasos históricos en landers comerciales (SpaceX Starship HLS, Blue Moon) | Antecedentes del sector |

---

**Fuentes principales:**
- NASA.gov — Comunicado oficial Ignition (24 mar. 2026): [nasa.gov/news-release/nasa-unveils-initiatives](https://www.nasa.gov/news-release/nasa-unveils-initiatives-to-achieve-americas-national-space-policy/)
- NASA.gov — Página Ignition con RFIs y RFPs: [nasa.gov/ignition](https://www.nasa.gov/ignition/)
- SpaceFlightNow (25 mar. 2026): [spaceflightnow.com](https://spaceflightnow.com/2026/03/25/nasa-outlines-ambitious-20-billion-plan-for-moon-base/)
- NASASpaceFlight — Moon Base y Gateway (25 mar. 2026): [nasaspaceflight.com](https://www.nasaspaceflight.com/2026/03/nasa-moon-base-pivots-gateway/)
- NASASpaceFlight — SR-1 Freedom (24 mar. 2026): [nasaspaceflight.com](https://www.nasaspaceflight.com/2026/03/nasa-sr1-freedom-mars-2028/)
- SpaceNews — SR-1 Freedom NEP (24 mar. 2026): [spacenews.com](https://spacenews.com/nasa-to-test-nuclear-electric-propulsion-with-2028-mission-to-mars/)
- Science / AAAS (24 mar. 2026): [science.org](https://www.science.org/content/article/nasa-plans-send-nuclear-powered-spacecraft-mars-2028)
- ANS Nuclear Newswire (25 mar. 2026): [ans.org](https://www.ans.org/news/article-7879/nasa-announces-plan-for-space-nuclear-propulsion-by-2028/)

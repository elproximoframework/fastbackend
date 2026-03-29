# Informe Técnico: TransAstra — Minería de Asteroides con Bolsas Inflables (Capture Bag)
**Fecha:** Marzo 2026 | **Clasificación:** Divulgación técnica | **Fuentes:** NASA CCRPP, ISS National Lab, SpaceNews, CNN, Gizmodo

---

## 1. Contexto: por qué minar asteroides

Los asteroides de tipo-C y tipo-S cercanos a la Tierra (NEAs, *Near-Earth Asteroids*) contienen agua, metales y materiales de blindaje frente a la radiación en concentraciones imposibles de igualar por el transporte desde la Tierra. Trasladar una tonelada de material desde la superficie terrestre a órbita baja cuesta entre 1.000 y 2.000 $/kg incluso con los lanzadores más baratos actuales. En cambio, un asteroide en órbita solar muy similar a la de la Tierra puede alcanzarse con un **delta-v menor que el necesario para llegar a la Luna**.

TransAstra, startup aeroespacial con sede en Los Ángeles fundada en 2015 por el ingeniero y exprofesor del Caltech **Joel Sercel**, ha desarrollado una cadena tecnológica completa para abordar este problema estructurando el reto en cuatro etapas: **detectar, capturar, mover y procesar**.

---

## 2. Etapa 1: Detección — Red de telescopios Sutter

Antes de capturar un asteroide, hay que encontrar el candidato adecuado. TransAstra opera su propia red de telescopios de prospección denominada **Sutter** (en referencia a Sutter's Mill, donde se descubrió el oro en California en 1848):

- **Ubicaciones actuales:** Arizona, California y Australia (cuarta ubicación planificada en España)
- **Objetivo:** Identificar asteroides de la familia *Arjuna* (órbitas casi circulares muy similares a la de la Tierra), de entre 5 y 20 metros de diámetro
- **Catálogo esperado:** El observatorio **Vera C. Rubin** en Chile permitirá descubrir ~260 nuevos objetos de hasta 20 metros en los próximos años
- **Criterio de selección:** Asteroides en órbitas de baja energía relativa (*Slowly Drifting Objects*, SDO), alcanzables con maniobras de delta-v mínimo

---

## 3. Etapa 2: Captura — Sistema Capture Bag

### Descripción del sistema

El **Capture Bag** es una bolsa inflable modular diseñada para envolver objetos de cualquier forma, tamaño y estado de rotación (incluyendo objetos en tumbling, el mayor reto tecnológico del sector). A diferencia de los brazos robóticos o los arpones, el sistema no requiere que el objetivo tenga geometría regular ni superficies de agarre definidas.

### Materiales y construcción

| Componente | Material |
|---|---|
| Estructura exterior | Kevlar y aluminio (aplicaciones aeroespaciales estándar) |
| Sellado | Diseño hermético certificado para vacío |
| Mecanismo de cierre | Cinching activo (cierre y apertura reversibles múltiples veces) |
| Sistema de despliegue | Hinchado autónomo desde vehículo portador |

### Escalado de tallas

| Talla | Diámetro | Capacidad máxima | Estado |
|---|---|---|---|
| Prototipo terrestre | ~30 cm | Validación en cámara de vacío | ✅ Completado |
| Pequeña (ISS) | **1 metro** | Demostración en microgravedad | ✅ Completado (oct. 2025) |
| Grande (JPL) | **10 metros** | Asteroides de ~100 t / debris orbital masivo | 🔄 En desarrollo (2026) |
| Operacional final | **32 pies (9,75 m)** | Objetivo asteroide misión New Moon | 🎯 Previsto 2027–2028 |

La bolsa de 10 metros es suficientemente grande para contener un asteroide de **10.000 toneladas**, equivalente en volumen a un edificio pequeño.

---

## 4. Demostración en la ISS — 2 de octubre de 2025

TransAstra completó una demostración exitosa de la tecnología Capture Bag en la ISS el 2 de octubre de 2025. Los detalles operacionales de la prueba fueron los siguientes:

- **Ubicación del test:** Esclusa Bishop (*Bishop Airlock*) del módulo comercial de Voyager Space, exterior de la ISS
- **Condiciones:** Vacío y microgravedad reales (no simulados en tierra)
- **Protocolo:** Los astronautas desplegaron y recogieron la bolsa de 1 metro múltiples veces, validando los ciclos de apertura y cierre en condiciones operacionales
- **Resultado:** Éxito completo. El CEO Sercel describió el hito como el primer funcionamiento en el espacio de su tecnología inflable, sentando las bases para la remediación de basura orbital y la captura de asteroides.
- **Tiempo de desarrollo hardware-a-vuelo:** 7 meses desde diseño hasta entrega del hardware de vuelo

---

## 5. Etapa 3: Traslado — Motor Omnivore de Propulsión Solar Térmica

Una vez capturado, el asteroide debe ser llevado a una órbita estable próxima al sistema Tierra-Luna. Para ello, TransAstra desarrolla el propulsor **Omnivore**:

- **Principio de funcionamiento:** Propulsión solar térmica (*Solar Thermal Propulsion*, STP); concentra la luz solar mediante espejos para calentar y expulsar propelente (agua), generando empuje de alta eficiencia
- **Ventaja clave:** El agua puede extraerse directamente del propio asteroide capturado (si es tipo-C), creando un ciclo de propelente auto-sostenido
- **Impulso específico estimado:** 800–1.000 s (frente a ~450 s de los motores químicos convencionales)
- **Aplicación secundaria:** Generación de energía eléctrica en órbita para las operaciones de procesado

---

## 6. Etapa 4: Procesado — Misión New Moon

La misión operativa objetivo de TransAstra se denomina **New Moon**:

- **Objetivo:** Capturar un asteroide de ~100 toneladas métricas de la familia Arjuna
- **Órbita destino:** Órbita estable en el sistema Tierra-Luna (punto de Lagrange L4 o L5, o DRO)
- **Recursos a extraer:** Agua (fraccionable en H₂ y O₂ para propelente), metales ferrosos, elementos de tierras raras y material de blindaje inerte
- **Coste estimado:** Pocos cientos de millones de dólares (según estimación del CEO)
- **Visión a largo plazo:** Acumular cientos de asteroides durante los años 2030 para constituir un millón de toneladas de material en órbita; transformarlos en bases robóticas de investigación y procesado industrial

---

## 7. Financiación y hoja de ruta

| Fuente | Importe |
|---|---|
| Capital riesgo privado (VC) | ~12 M$ acumulados |
| Contratos y subvenciones NASA / Space Force | ~15 M$ acumulados |
| Contrato NASA CCRPP (bol. 10 m) | 2,5 M$ (sep. 2025) |
| Inversión privada asociada (matching) | 2,5 M$ (sep. 2025) |
| **Total financiación acumulada** | **~32 M$** |

| Hito | Fecha | Estado |
|---|---|---|
| Test en vacío (tierra) | 2023–2024 | ✅ Completado |
| Test en ISS (bolsa 1 m) | 2 oct. 2025 | ✅ Completado |
| Test en JPL High Bay (bolsa 10 m) | 2026 | 🔄 En curso |
| Primera misión real de captura asteroidal | **2028** | 🎯 Objetivo |
| Escala industrial (decenas de asteroides) | 2030+ | 📋 Planificado |

---

## 8. Doble uso: basura espacial

El Capture Bag no es exclusivamente una herramienta minera. El sistema está diseñado para capturar objetos de distintas formas y tamaños, incluidos los que rotan de forma incontrolada, el mayor desafío técnico de la retirada de basura orbital. Trasladar debris a una instalación de reprocesado en órbita, en lugar de desorbitar directamente, costaría seis veces menos, consumiría un 80% menos de propelente y despejaría una órbita dada un 40% más rápido. El mercado combinado de limpieza de debris y minería asteroidal se estima en más de **1.000 M$/año para 2030**.

---

**Fuentes principales:**
- ISS National Lab (2 oct. 2025): [issnationallab.org](https://issnationallab.org/press-releases/bagging-space-junk-transastras-inflatable-tech-takes-aim-at-orbital-debris/)
- NASA CCRPP / Newswire (23 sep. 2025): [newswire.com](https://www.newswire.com/news/transastra-demonstrates-asteroid-capture-and-orbital-debris-cleanup-22651131)
- Gizmodo (mar. 2026): [gizmodo.com](https://gizmodo.com/nasa-backed-startup-to-try-ingenious-asteroid-mining-idea-just-bag-it-2000735650)
- CNN Science (nov. 2025): [cnn.com](https://www.cnn.com/science/asteroid-capture-transastra-giant-bag-spc)
- ZME Science (mar. 2026): [zmescience.com](https://www.zmescience.com/science/bagging-asteroids-mining/)

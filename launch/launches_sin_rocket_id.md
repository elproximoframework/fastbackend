# Lanzamientos sin `rocket_id`

Consulta ejecutada el **2026-04-20** sobre la tabla `launches`.  
Total de registros sin `rocket_id`: **67**

---

## Lista de nombres (ordenados alfabéticamente)

| # | Nombre | Repeticiones |
|---|--------|-------------|
| 1 | Angara 1.2 | 1 |
| 2 | Ariane 64 | 3 |
| 3 | Ariane 64 Block 2 | 1 |
| 4 | Atlas V 551 | 2 |
| 5 | Ceres-1S | 1 |
| 6 | Ceres-2 | 1 |
| 7 | Electron | 8 |
| 8 | Falcon Heavy | 1 |
| 9 | Firefly Alpha | 1 |
| 10 | HASTE | 2 |
| 11 | KAIROS | 1 |
| 12 | Kinetica 1 | 1 |
| 13 | Kinetica 2 | 1 |
| 14 | Kuaizhou 11 | 1 |
| 15 | Long March 12 | 1 |
| 16 | Long March 2C | 2 |
| 17 | Long March 2C/YZ-1S | 1 |
| 18 | Long March 2D | 3 |
| 19 | Long March 2F/G | 1 |
| 20 | Long March 3B/E | 1 |
| 21 | Long March 6A | 3 |
| 22 | Long March 7A | 1 |
| 23 | Long March 8 | 1 |
| 24 | Long March 8A | 2 |
| 25 | Minotaur IV | 1 |
| 26 | New Glenn | 1 |
| 27 | New Shepard | 1 |
| 28 | Pegasus XL | 1 |
| 29 | Proton-M/Blok DM-03 | 1 |
| 30 | PSLV-DL | 1 |
| 31 | SLS Block 1 | 1 |
| 32 | Smart Dragon 3 | 3 |
| 33 | South Korean ADD Solid-Fuel SLV | 1 |
| 34 | Soyuz 2.1a | 4 |
| 35 | Soyuz 2.1a/Fregat-M | 2 |
| 36 | Soyuz 2.1b | 2 |
| 37 | Soyuz 2.1b/Fregat-M | 1 |
| 38 | Soyuz-5 | 1 |
| 39 | Spectrum | 1 |
| 40 | Starship | 1 |
| 41 | Tianlong-3 | 1 |
| 42 | Vega-C | 1 |
| 43 | Vikram-I | 1 |
| 44 | Vulcan VC4S | 1 |
| 45 | Zhuque-2E | 1 |

---

## Nombres únicos (45 cohetes distintos)

```
Angara 1.2
Ariane 64
Ariane 64 Block 2
Atlas V 551
Ceres-1S
Ceres-2
Electron
Falcon Heavy
Firefly Alpha
HASTE
KAIROS
Kinetica 1
Kinetica 2
Kuaizhou 11
Long March 12
Long March 2C
Long March 2C/YZ-1S
Long March 2D
Long March 2F/G
Long March 3B/E
Long March 6A
Long March 7A
Long March 8
Long March 8A
Minotaur IV
New Glenn
New Shepard
Pegasus XL
Proton-M/Blok DM-03
PSLV-DL
SLS Block 1
Smart Dragon 3
South Korean ADD Solid-Fuel SLV
Soyuz 2.1a
Soyuz 2.1a/Fregat-M
Soyuz 2.1b
Soyuz 2.1b/Fregat-M
Soyuz-5
Spectrum
Starship
Tianlong-3
Vega-C
Vikram-I
Vulcan VC4S
Zhuque-2E
```

---

> **Siguiente paso sugerido:** Crear o asociar los rockets correspondientes en la tabla `rockets`
> y luego ejecutar un `UPDATE launches SET rocket_id = ... WHERE name = '...'` para vincularlos.

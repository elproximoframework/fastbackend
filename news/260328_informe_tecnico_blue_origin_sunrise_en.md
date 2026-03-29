# Technical Report: Project Sunrise — Blue Origin and Orbital Data Centers
**Date:** March 2026 | **Classification:** Technical disclosure | **Sources:** FCC Filing, SpaceNews, GeekWire, Data Centre Magazine

---

## 1. Context: AI as a Space Catalyst

The explosion in peak demand for artificial intelligence computing is saturating terrestrial infrastructure: data centers that consume gigawatts of electricity, require millions of liters of water for cooling, and compete for developable land. In this context, several companies have begun to propose space as **a new layer of computing infrastructure**.

On March 19, 2026, Blue Origin submitted an authorization request to the **U.S. Federal Communications Commission (FCC)** to deploy its proposal: **Project Sunrise**, a constellation of up to 51,600 satellites specifically designed to operate as orbiting data centers.

---

## 2. Constellation Architecture

### Orbital Parameters

| Parameter | Value |
|---|---|
| Number of satellites | Up to **51,600** |
| Orbit Type | Circular, Sun-Synchronous (SSO) |
| Altitude | 500 – 1,800 km |
| Inclination | 97° – 104° |
| Satellites per orbital plane | 300 – 1,000 |
| Separation between planes | 5 – 10 km in altitude |

The choice of **Sun-Synchronous Orbit** is deliberate: the satellites remain illuminated by the sun almost continuously (dawn-dusk twilight orbit), maximizing solar power generation and eliminating the energy variability of other orbits.

### Inter-satellite Communications

- **Primary Link:** Optical Inter-Satellite Links (OISL), i.e., high-speed lasers between satellites, without using radio frequency spectrum for main traffic.
- **Ground Link:** Through Blue Origin's **TeraWave** constellation (5,408 satellites, announced in January 2026), which acts as a mesh backhaul network to ground stations.
- **RF Bands:** Only for telemetry, tracking, and control (TT&C), using Ka-band.
- **Antenna Variants:** At least three variants per satellite to cover different coverage requirements.

---

## 3. Project Sunrise vs. TeraWave: Two Distinct Layers

A critical distinction of the Blue Origin ecosystem:

| Constellation | Function | No. of Satellites | Announcement |
|---|---|---|---|
| **TeraWave** | Connectivity network (communications backbone) | 5,408 | January 2026 |
| **Project Sunrise** | Orbital computing infrastructure (data centers) | 51,600 | March 2026 |

TeraWave is the **data highway**; Project Sunrise is the **server farm** that travels over it. Both complement each other and are necessary for the operation of the complete system.

---

## 4. Technical-Economic Justification Presented to the FCC

Blue Origin argues in its 14-page application four structural advantages of orbital data centers compared to terrestrial ones:

1. **Continuous Solar Power** — Elimination of dependence on the terrestrial power grid and its infrastructure costs.
2. **No Land or Displacement Cost** — Space does not impose land-use restrictions or competition with other uses.
3. **Less Pressure on Water Resources** — Terrestrial data centers consume enormous volumes of water for cooling. In a vacuum, thermal management is performed by passive radiation.
4. **Lower Marginal Computing Cost** — The combination of the three factors above should reduce the cost per computing operation at scale.

> The company states that Project Sunrise *"will introduce a new computing layer that operates independently of terrestrial constraints,"* functioning as a **complement** —not a substitute— for ground-based infrastructure.

---

## 5. Launch Vehicle: New Glenn

Blue Origin plans to deploy the constellation with its own heavy rocket **New Glenn**, which has already completed two successful flights as of the date of this report. This gives it a key competitive advantage: it does not depend on third parties for the launch, unlike Amazon Leo (Kuiper), which has hundreds of satellites ready but lacks sufficient launch capacity. Blue Origin will also be the launch provider for 27 Amazon Leo missions, which generates a potential conflict of interest noted by industry analysts.

---

## 6. Competitive Landscape

The orbital data center market is attracting multiple actors simultaneously:

| Company | Proposal | No. of Satellites |
|---|---|---|
| **SpaceX / xAI** | Orbital Data Constellation | Up to **1,000,000** |
| **Blue Origin** (Project Sunrise) | Data Centers in Orbit | 51,600 |
| **Starcloud** (Y Combinator + Nvidia) | Orbital Data with H100 GPUs | 88,000 |
| **Google / Planet Labs** | Project Suncatcher (2 demos) | In testing phase |
| **China** (ADA Space + Zhejiang Lab) | Three-Body Computing Constellation | 2,800 (Phase 1) |

**SpaceX** has already responded publicly, calling Blue Origin's plans *"deeply disproportionate"*; Blue Origin, in turn, accused SpaceX of lacking real technical details and potentially taking *"centuries"* to complete its constellation. The **FCC** will have to arbitrate between proposals that, collectively, would add more than a million new satellites in low Earth orbit.

OpenAI CEO **Sam Altman** has positioned himself skeptically, calling orbital data centers *"ridiculous"* in the short term, citing challenges in cooling, chip radiation resistance, and manufacturing costs at scale.

---

## 7. Regulatory Waiver Requests

Blue Origin has asked the FCC for **specific waivers** regarding standard constellation deployment requirements:

- **Exemption from the 6-year deadline** to have 50% of the satellites in orbit after approval.
- **Exemption from the 9-year deadline** for full deployment.
- **Argument:** the satellites are designed to minimize interference and voluntarily comply with space debris mitigation guidelines, including **deorbiting in less than 5 years** at the end of their useful life.

---

**Main Sources:**
- FCC Filing Blue Origin — Project Sunrise (Mar. 19, 2026): [fcc.gov](https://fcc.gov)
- SpaceNews (Mar. 20, 2026): [spacenews.com](https://spacenews.com/blue-origin-joins-the-orbital-data-center-race/)
- GeekWire (Mar. 21, 2026): [geekwire.com](https://www.geekwire.com/2026/blue-origin-data-center-space-race-project-sunrise/)
- Data Centre Magazine (Mar. 23, 2026): [datacentremagazine.com](https://datacentremagazine.com/news/project-sunrise-blue-origin-data-centre-space-race)
- New Space Economy (Mar. 20, 2026): [newspaceeconomy.ca](https://newspaceeconomy.ca/2026/03/20/blue-origin-project-sunrise-the-race-to-build-data-centers-in-orbit/)

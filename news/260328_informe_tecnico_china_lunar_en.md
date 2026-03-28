# Technical Report: China's Crewed Lunar Program (Project 921)
**Date:** March 2026 | **Classification:** Technical disclosure | **Sources:** CMSA, SpaceNews, NASASpaceFlight

---

## 1. Context and Objective

China is steadily advancing its crewed lunar exploration program under the code name **Project 921**, managed by the China Manned Space Agency (CMSA). The stated goal is to achieve the **first Chinese crewed lunar landing before 2030**, in what represents the most direct competition with NASA's Artemis program.

---

## 2. Launch Vehicle: Long March 10 (CZ-10)

The **CZ-10** is the super-heavy rocket specifically designed for crewed lunar missions. Its main technical characteristics are:

- **Configuration:** Three cores in parallel (similar to Falcon Heavy), powered by YF-100K engines
- **Payload Capacity:** 70 t to Low Earth Orbit (LEO) and 27 t on a translunar injection (TLI) trajectory
- **Combined Thrust (First Stage):** ~382 t of thrust, verified in a static fire test in June 2025
- **Completed Tests:** Static fire of the first stage test article and low-altitude validation flight
- **First Operational Mission:** Planned for 2027, carrying the first Lanyue demonstration lander

Each crewed lunar mission will require **two CZ-10 launches**: one for the Mengzhou spacecraft and another for the Lanyue lunar lander, with docking in lunar orbit.

---

## 3. Crewed Spacecraft: Mengzhou (梦舟, "Dream Vessel")

The **Mengzhou** is the successor to the Shenzhou for deep space missions:

- **Launch Mass:** ~26,000 kg (including service module)
- **Escape System:** Active escape tower (instead of an integrated system), which preserves the overall aerodynamics and reduces the structural load of the service module
- **Completed Abort Tests:**
  - *Zero-height abort test* (pad abort): passed in June 2025 at Jiuquan
  - *Max-Q abort test* (maximum dynamic pressure abort): successfully completed on February 11, 2026; the crew module correctly separated from the test CZ-10A rocket, which performed a controlled landing profile and splashed down near the recovery ship
- **First Uncrewed Flight:** Planned for 2028

In case of emergency after translunar injection, the spacecraft has the capacity for an autonomous return on a free-return trajectory around the Moon. In lunar orbit, the four main engines (or just two, depending on the severity of the failure) can execute a Earth return maneuver within 2 to 5 days.

---

## 4. Lunar Landing Module: Lanyue (揽月, "Embracing the Moon")

**Lanyue** is the vehicle that will take the taikonauts from lunar orbit to the surface:

- **Design:** Two modules — propulsion module (descent) and lunar module (ascent)
- **Descent Propulsion:** YF-58-1 engine, MMH/NTO propellants; performs at least three burns to reach the surface
- **Ascent Propulsion:** Four YF-36 engines with ~6,000 kg of propellant stored in a common dome tank
- **Total Combined Impulse:** 5,100 m/s
- **Communications:** High-speed 100 Mbit/s channel (upload/download) and 2 kbit/64 kbit low-speed channel, with 6 ms latency
- **Internal Network:** Time-Triggered Ethernet (TTE) with redundant optical cabling
- **Completed Tests:** Liftoff and landing test of the prototype; static fire tests at Wenchang launch pad 301 (August-September 2025)

---

## 5. Current Status and Roadmap

| Milestone | Status |
|---|---|
| CZ-10 Static Fire (short article) | ✅ Completed (2025) |
| Mengzhou Pad Abort | ✅ Completed (Jun 2025) |
| Lanyue Liftoff/Landing Test | ✅ Completed (2025) |
| Mengzhou Max-Q Abort | ✅ Completed (Feb 2026) |
| CZ-10 Low-Altitude Flight Validation | ✅ Completed (2026) |
| First Operational CZ-10 Flight | 🔄 Expected 2027 |
| First Uncrewed Mengzhou Flight | 🔄 Expected 2028 |
| Crewed Lunar Landing | 🎯 2030 Goal |

---

## 6. Strategic Considerations

China has completed all critical qualification tests for the three major flight systems in less than 18 months, following a remarkably punctual schedule. The two-launch architecture with lunar orbit docking mirrors the Apollo strategy, though with entirely new and proprietary hardware. The temporal parallel with the Artemis program makes the 2029-2030 window the point of greatest competitive tension between both space powers.

---

**Main Sources:**
- CMSA / Xinhua (Feb 27, 2026): [en.people.cn](https://en.people.cn/n3/2026/0228/c90000-20429547.html)
- SpaceNews (Oct 30, 2025): [spacenews.com](https://spacenews.com/china-targets-2026-for-first-long-march-10-launch-new-lunar-crew-spacecraft-flight/)
- NASASpaceFlight (Feb 5, 2026): [nasaspaceflight.com](https://www.nasaspaceflight.com/2026/02/china-roundup-020526/)
- China-in-Space (Mar 2026): [china-in-space.com](https://www.china-in-space.com/p/mengzhou-abort-plans-lanyue-lander)

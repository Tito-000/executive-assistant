# Fase 1 — Embudos por Producto

**Descripción:** Crear y lanzar embudos de venta individuales para cada producto Immunotec en RD.
**Estado:** Activo
**Fechas:** 2 feb – 2 abr 2026

---

## Estado general por producto

| Producto | Progreso | TPA | MKR | WWP | Landing | Meta Ads | Creativos |
|---|---|---|---|---|---|---|---|
| **Immunocal** | 65% | ✅ PDF | ✅ PDF | ✅ PDF | ❌ | ✅ PDF | ✅ |
| **Platinum** | 80% | ✅ MD | ✅ MD | ✅ MD | ✅ MD | ✅ MD | ❌ |
| **Magistral** | 20% | ❌ | ✅ MD | ❌ | ❌ | ❌ | ❌ |
| **Multi+ Resveratrol** | 85% | ✅ MD | ✅ MD | ✅ MD | ✅ MD | ✅ MD | ❌ |

**Leyenda:** ✅ Completo · ❌ Falta · MD = Markdown editable · PDF = solo lectura

---

## Productos

- [`productos/immunocla/`](productos/immunocla/README.md) — Immunocal · Avatar: adultos 35–65, sistema inmune
- [`productos/platinum/`](productos/platinum/README.md) — Platinum · Avatar: personas con dolor crónico, RD$7,995
- [`productos/magistral/`](productos/magistral/README.md) — Magistral · Avatar: hombres 40–70, próstata · **⚠️ BLOQUEADO**
- [`productos/multi-resveratrol/`](productos/multi-resveratrol/README.md) — Multi+ Resveratrol · Avatar: mujeres 35–55

---

## ⚠️ DECLARATORIO — Magistral bloqueado

Magistral solo tiene el Market Research. Faltan TPA, WWP, Landing Page y Meta Ads.

**Pregunta para Martin:**
> ¿Hay un PDF o fuente con la investigación para completar Magistral? ¿O arrancamos desde cero con el market research existente?

---

## Próximos pasos recomendados

1. **Platinum** — generar creativos visuales para Meta (embudo más listo para lanzar)
2. **Multi+ Resveratrol** — generar creativos + conseguir testimonios reales con foto
3. **Immunocal** — convertir PDFs a markdown + escribir copy de landing page
4. **Magistral** — resolver el declaratorio, luego construir TPA → WWP → Landing → Ads

---

## Estructura estándar por producto

```
producto/
├── README.md
├── top-player-analysis/   tpa-[competidor].md
├── market-research/       market-research-[producto].md
├── WWP/                   wwp-[producto].md
├── landing-page/          landing-page-copy.md
├── meta-ads/              meta-ads-[N]-ads.md
├── creativos-para-test/
└── recursos/
    └── imagenes-producto/
```

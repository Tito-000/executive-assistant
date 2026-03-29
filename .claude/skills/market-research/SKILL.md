# Skill: /market-research

**Invocación:** `/market-research [nombre del proyecto o cliente]`

Este skill ejecuta una investigación de mercado profunda (MKR) para un proyecto o cliente. No se trata de llenar un template con suposiciones — se investiga en fuentes reales (foros, reviews, YouTube, Trustpilot, income disclosures, artículos, estadísticas de la industria) y se responde cada pregunta del MKR con citas textuales, datos verificables y lenguaje real del mercado.

---

## PASO 0 — Verificar si ya existe el MKR

Busca si ya existe un archivo MKR para este proyecto:
- `projects/clientes/[nombre]/market-research/MKR-*.md`
- `projects/[nombre]/**/MKR-*.md`

Si ya existe, léelo y pregunta: "Ya hay un MKR para este proyecto. ¿Quieres que lo actualice con investigación nueva o que empiece desde cero?"

Si no existe, crea la estructura:
```
projects/clientes/[nombre]/market-research/
└── MKR-[nombre].md
```

---

## PASO 1 — Entrevista de clarificación

Antes de investigar, necesitas entender el proyecto. Haz estas preguntas (adapta según lo que ya sepas del contexto):

1. **¿Quién es el cliente/proyecto?** — Nombre, qué hace, qué vende, en qué mercado opera.
2. **¿Cuál es el objetivo principal?** — ¿Atraer prospectos de negocio? ¿Vender producto? ¿Construir audiencia? ¿Generar leads?
3. **¿Quién es la audiencia target?** — Perfil general, si tiene uno definido. Si no, que describa quién le compra hoy.
4. **¿Qué tiene de especial/diferente?** — Su ventaja competitiva, su historia, sus credenciales.
5. **¿Qué objeciones escucha más?** — Las frases textuales que los prospectos le dicen cuando no quieren.

Si ya tienes contexto del proyecto (README, conversaciones previas), usa lo que sabes y solo pregunta lo que falta. No repitas preguntas cuya respuesta ya conoces.

---

## PASO 2 — Investigación web profunda

Esta es la fase más importante. NO se llena el template con suposiciones — se investiga en fuentes reales.

### 2A — Identificar los ejes de búsqueda

Basándote en las respuestas del PASO 1, define 4-6 ejes de búsqueda:

1. **La empresa/marca específica** — reviews, quejas, opiniones, income disclosures, comparaciones de precio
2. **La industria/nicho** — estadísticas, tendencias, sentimiento del mercado, tamaño del mercado
3. **Los detractores/críticos** — foros antiMLM, reviews negativas, YouTube "why I quit", artículos críticos
4. **Los defensores/exitosos** — testimonios reales, casos de éxito, estrategias que funcionan
5. **La audiencia target** — dónde se juntan, qué contenido consumen, qué lenguaje usan
6. **La estrategia de contenido que funciona** — qué hacen los top players, qué convierte, qué tendencias hay

### 2B — Ejecutar las búsquedas

Usa WebSearch y WebFetch agresivamente. Mínimo 15-20 búsquedas diferentes. Incluye:

**Búsquedas obligatorias:**
- `[empresa] review scam opinions [año actual]`
- `[empresa] opiniones experiencia foro español`
- `[industria/nicho] statistics [año actual]`
- `[industria/nicho] "why I quit" OR "left" OR "my experience" honest`
- `[industria/nicho] what actually works success strategy [año actual]`
- `[empresa] Trustpilot reviews`
- `[empresa] income disclosure statement [año actual]`
- `[audiencia target] frustrations problems Reddit forum`
- `[audiencia target] "I wish" OR "I hate" OR "I want" [nicho]`
- `YouTube [industria] honest review comments`

**Fuentes a priorizar:**
- Trustpilot, Glassdoor, Indeed (reviews reales)
- Reddit (buscar via Google con las keywords, no acceso directo)
- YouTube (buscar videos referentes y extraer patrones de comentarios)
- BuzzFeed, HuffPost, Medium (historias personales recopiladas)
- Foros especializados de la industria
- Income disclosure statements oficiales
- FTC, DSA, WFDSA (estadísticas)
- Blogs de análisis de la industria (BehindMLM, Truth in Advertising, etc.)

**Para cada fuente que encuentres:**
- Usa WebFetch para extraer el contenido real
- Anota citas textuales con atribución
- Extrae datos numéricos con fuente
- Captura el lenguaje EXACTO que usan las personas reales

### 2C — Organizar lo encontrado

Antes de escribir el MKR, organiza la investigación en estas categorías:
- **Citas textuales negativas** (quejas, frustraciones, objeciones reales)
- **Citas textuales positivas** (testimonios, defensas, lenguaje aspiracional)
- **Datos duros** (estadísticas, income disclosures, tamaño de mercado)
- **Tendencias** (qué está funcionando, qué está muriendo, hacia dónde va)
- **Insights estratégicos** (oportunidades, vulnerabilidades, diferenciadores)

---

## PASO 3 — Escribir el MKR

Usa el template de `templates/MKR-market-research.md` como estructura base, pero cada sección debe estar enriquecida con la investigación real. El estándar de calidad es:

### Reglas para cada sección:

**Audiencia Objetivo:**
- Cada campo demográfico debe tener un dato de la industria que lo respalde
- Ej: "74% de los participantes en direct selling son mujeres" junto al split de género

**Estado Doloroso Actual:**
- Cada pregunta debe tener 3-5 respuestas basadas en la entrevista directa
- Cada pregunta debe tener 2-3 insights adicionales de la investigación web con citas textuales reales
- Incluir el "por qué" detrás de cada dolor, respaldado con datos o historias documentadas
- El Lenguaje Negativo del Cliente debe tener DOS secciones: (1) de entrevista directa y (2) de investigación web con citas textuales reales de foros/reviews/YouTube

**Estado de Ensueño Deseado:**
- Misma estructura dual: entrevista directa + investigación
- El Lenguaje Positivo debe incluir frases de personas reales que defienden el modelo

**Valores, Creencias y Afiliaciones Tribales:**
- Las creencias deben incluir las que la investigación descubrió que la audiencia tiene (ej: "las 7 mentiras MLM" que ya identifican)
- Las tribus deben incluir comunidades online reales con datos (ej: r/antiMLM 700K+ miembros)
- Las tendencias deben incluir datos de mercado verificables

**Objeciones:**
- Cada objeción necesita:
  - **La frase textual** (como la dicen)
  - **Por qué lo dicen** (con datos reales que respalden la objeción)
  - **Cómo se neutraliza** (estrategia específica, no genérica)
- Buscar 2-3 objeciones NUEVAS que salgan de la investigación web (que el cliente no mencionó pero que la audiencia sí expresa online)

**Avatar:**
- Cada avatar necesita:
  - Nombre, edad, ubicación, ocupación, ingreso, estado civil
  - Su historia completa (párrafo narrativo)
  - Su experiencia previa con el nicho/industria
  - Lo que lo convencería (lista específica de 4-5 puntos)
  - Lo que lo haría huir al instante (lista de red flags)
  - Su lenguaje interno (cita textual de lo que piensa pero no dice)

### Secciones adicionales obligatorias (después de Avatar):

**Investigación de Mercado — Fuentes Externas:**
- Tabla de datos duros de la empresa/industria (con fuente)
- Tabla de datos de la industria global (con fuente)
- Sentimiento del mercado online (citas de detractores y defensores)
- Lo que la audiencia ya sabe (y que la mayoría ignora)
- Tendencia de la estrategia que funciona (con playbook accionable)
- Vulnerabilidades reales del negocio/empresa + cómo neutralizarlas
- Datos del negocio específico (plan de compensación, estructura, etc. si aplica)

**Resumen Estratégico de la Investigación:**
- 5-7 confirmaciones de lo que la investigación valida
- 3-5 reglas de oro derivadas de la investigación (específicas al proyecto, no genéricas)

**Fuentes Consultadas:**
- Organizadas por categoría (empresa específica, industria general, estadísticas, estrategia)
- Con links funcionales
- Incluir comunidades/YouTubers/influencers referentes del mercado

---

## PASO 4 — Validación final

Antes de entregar, verifica:

- [ ] ¿Cada sección tiene datos de la investigación web, no solo suposiciones?
- [ ] ¿Hay citas textuales reales de personas reales (no inventadas)?
- [ ] ¿Los datos numéricos tienen fuente?
- [ ] ¿Las objeciones tienen "por qué lo dicen" con datos y "cómo se neutraliza" con estrategia?
- [ ] ¿Los avatares tienen historia completa, lo que los convence y lo que los ahuyenta?
- [ ] ¿El resumen estratégico es específico al proyecto (no genérico)?
- [ ] ¿Se incluyeron 2+ objeciones nuevas descubiertas en la investigación?
- [ ] ¿Las fuentes están citadas y organizadas?

---

## Notas

- **Tiempo esperado:** 15-30 minutos. La mayor parte es investigación web.
- **Output:** Se guarda en `projects/clientes/[nombre]/market-research/MKR-[nombre].md` o la ruta del proyecto activo.
- **Idioma:** Español por defecto. Citas en inglés se mantienen en inglés con traducción si es necesario.
- **No inventar data.** Si no encuentras datos para una sección, escríbelo: "No se encontraron datos verificables para esta sección — requiere entrevista directa."
- **El Google Test:** Asume que la audiencia target va a buscar "[empresa] + scam" antes de confiar. El contenido del MKR debe anticipar lo que van a encontrar.

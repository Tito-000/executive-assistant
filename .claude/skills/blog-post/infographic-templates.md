# Infographic HTML Templates

Copy-paste these templates into blog post articles. Replace bracketed `[values]` with real content.

## 1. Table (Myth vs Reality, Antes vs Después)

```html
<div class="post-infographic">
  <h3 class="post-infographic-title">[Título de la tabla]</h3>
  <div class="post-infographic-table">
    <div class="post-infographic-row post-infographic-header">
      <div>[Columna 1]</div>
      <div>[Columna 2]</div>
    </div>
    <div class="post-infographic-row">
      <div>[Dato 1A]</div>
      <div>[Dato 1B]</div>
    </div>
    <div class="post-infographic-row">
      <div>[Dato 2A]</div>
      <div>[Dato 2B]</div>
    </div>
    <div class="post-infographic-row">
      <div>[Dato 3A]</div>
      <div>[Dato 3B]</div>
    </div>
  </div>
</div>
```

## 2. Flow / Process Diagram (3-5 steps)

```html
<div class="post-infographic">
  <h3 class="post-infographic-title">[Título del proceso]</h3>
  <div class="post-infographic-flow">
    <div class="post-flow-step">
      <span class="post-flow-num">1</span>
      <span class="post-flow-label">[Paso 1]</span>
    </div>
    <div class="post-flow-arrow">→</div>
    <div class="post-flow-step">
      <span class="post-flow-num">2</span>
      <span class="post-flow-label">[Paso 2]</span>
    </div>
    <div class="post-flow-arrow">→</div>
    <div class="post-flow-step">
      <span class="post-flow-num">3</span>
      <span class="post-flow-label">[Paso 3]</span>
    </div>
    <div class="post-flow-arrow">→</div>
    <div class="post-flow-step">
      <span class="post-flow-num">4</span>
      <span class="post-flow-label">[Paso 4]</span>
    </div>
  </div>
</div>
```

## 3. Checklist

```html
<div class="post-infographic">
  <h3 class="post-infographic-title">[Título del checklist]</h3>
  <div class="post-infographic-checklist">
    <div class="post-check-item">
      <span class="post-check-icon">✓</span>
      <span>[Item 1]</span>
    </div>
    <div class="post-check-item">
      <span class="post-check-icon">✓</span>
      <span>[Item 2]</span>
    </div>
    <div class="post-check-item">
      <span class="post-check-icon">✓</span>
      <span>[Item 3]</span>
    </div>
    <div class="post-check-item">
      <span class="post-check-icon">✓</span>
      <span>[Item 4]</span>
    </div>
    <div class="post-check-item">
      <span class="post-check-icon">✓</span>
      <span>[Item 5]</span>
    </div>
  </div>
</div>
```

## 4. Stats (big numbers)

```html
<div class="post-infographic post-infographic--stats">
  <div class="post-info-stat">
    <span class="post-info-stat-num">[82%]</span>
    <span class="post-info-stat-label">[de dominicanos usan internet]</span>
  </div>
  <div class="post-info-stat">
    <span class="post-info-stat-num">[7M]</span>
    <span class="post-info-stat-label">[usuarios de Facebook en RD]</span>
  </div>
  <div class="post-info-stat">
    <span class="post-info-stat-num">[78%]</span>
    <span class="post-info-stat-label">[activos en WhatsApp]</span>
  </div>
</div>
```

## 5. Hub Diagram (central concept + surrounding elements)

```html
<div class="post-infographic">
  <h3 class="post-infographic-title">[Título]</h3>
  <div style="display:flex;flex-direction:column;align-items:center;gap:16px;">
    <div style="display:flex;gap:16px;justify-content:center;flex-wrap:wrap;">
      <div class="post-flow-step"><span class="post-flow-label">[Elemento 1]</span></div>
      <div class="post-flow-step"><span class="post-flow-label">[Elemento 2]</span></div>
    </div>
    <div class="post-flow-step" style="border-color:#713DFF;padding:24px 32px;">
      <span class="post-flow-num" style="font-size:16px;">[Concepto Central]</span>
    </div>
    <div style="display:flex;gap:16px;justify-content:center;flex-wrap:wrap;">
      <div class="post-flow-step"><span class="post-flow-label">[Elemento 3]</span></div>
      <div class="post-flow-step"><span class="post-flow-label">[Elemento 4]</span></div>
    </div>
  </div>
</div>
```

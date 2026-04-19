# Literatura — Unidad 01: Esencia de la Optimización

## Fuente principal
**Peralta, R. C. & Kalwij, I. M. (2012).** *Groundwater Optimization Handbook: Flow, Contaminant Transport, and Conjunctive Management.* CRC Press. **Capítulo 1, pp. 3–29.**

---

## Conceptos clave extraídos

### 1. Modelos de simulación (S) vs. modelos S-O
- Los modelos S predicen cabeza hidráulica y transporte de contaminantes.
- Un modelo **S-O** acopla un simulador predictivo con un algoritmo de optimización matemática para calcular la **mejor estrategia** para un problema definido por el usuario.
- Ejemplos de modelos S-O: AQMAN, GWM, MGO, MODMAN, MODOFC, SOMOS.

### 2. Ecuaciones de flujo fundamentales

**Acuífero confinado (3D):**
```
∂/∂x(Kx ∂h/∂x) + ∂/∂y(Ky ∂h/∂y) + ∂/∂z(Kz ∂h/∂z) - qs = Ss ∂h/∂t
```

**Acuífero libre (no lineal en h):**
```
∂/∂x(Kx(h-ELEVb) ∂h/∂x) + Q = Ss ∂h/∂t
```

**Transporte de contaminantes:**
```
∂(θ·Conc)/∂t = ∂/∂x(Dxy ∂Conc/∂y) - ∂/∂x(θ vx Conc) + Qs·Concs + RT
```

### 3. Necesidad de la optimización (Sección 1.2)
- Complejidad física del sistema subterráneo: heterogeneidad, anisotropía, incertidumbre en parámetros.
- Rango de velocidades de flujo subterráneo: m/año a m/día.
- Conductividad hidráulica varía ~13 órdenes de magnitud entre materiales geológicos.
- La optimización es esencial para desarrollar estrategias de bombeo costo-efectivas.

### 4. Metas del enfoque S-O (Sección 1.1)
1. Promover el manejo sustentable de aguas subterráneas.
2. Acelerar la adopción del análisis de sistemas y optimización matemática.
3. Fomentar el uso de métodos estocásticos.

### 5. Perspectiva de sistemas (Sección 1.4)
- El enfoque sistémico ayuda a los gestores a obtener apoyo de las partes interesadas.
- S-O complementa (no reemplaza) las habilidades de hidrogeología.
- Pasos típicos en una aplicación S-O:
  1. Identificar objetivos de manejo.
  2. Formular el problema de optimización.
  3. Seleccionar el optimizador adecuado.
  4. Resolver y verificar la estrategia óptima.
  5. Implementar y monitorear.

---

## Páginas de referencia directa (Peralta 2012)
| Tema | Página |
|------|--------|
| Ecuación de flujo 3D (Ec. 1.1) | 3–4 |
| Acuífero confinado vs. libre (Fig. 1.1) | 4 |
| Conductividad hidráulica de materiales (Tabla 1.1, Fig. 1.10) | 17–18 |
| Necesidad de optimización (Sec. 1.2) | 11–21 |
| Enfoque sistémico (Fig. 1.12) | 22–25 |

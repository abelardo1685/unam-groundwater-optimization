# Unidad 01 — Esencia de la Optimización en el Manejo de Aguas Subterráneas

**Horas:** 4 teoría + 4 práctica  
**Referencia principal:** Peralta & Kalwij (2012), Capítulo 1

---

## Objetivos de aprendizaje

Al finalizar esta unidad el estudiante será capaz de:
1. Explicar por qué la optimización es necesaria en el manejo de aguas subterráneas.
2. Distinguir entre un modelo de simulación (S) y un modelo simulación-optimización (S-O).
3. Identificar las ecuaciones de flujo gobernantes y su relación con la linealidad del sistema.
4. Describir el enfoque de análisis de sistemas aplicado a la gestión del agua subterránea.

---

## 1. Introducción

La modelación de simulación de aguas subterráneas ha sido aceptada desde los años 1970s. Los modelos S predicen cabeza hidráulica y transporte de contaminantes. Sin embargo, la simulación por sí sola **no identifica la mejor estrategia** — eso requiere optimización.

Un modelo **S-O** acopla:
- **Simulador (S):** predice el estado del sistema (cabezas, concentraciones).
- **Optimizador (O):** busca la estrategia que minimiza/maximiza el objetivo dado las restricciones del sistema.

---

## 2. La Necesidad y los Beneficios de la Optimización

### ¿Por qué optimizar?
- Los sistemas de aguas subterráneas son **complejos e inciertos**:
  - Heterogeneidad espacial de parámetros (K varía ~13 órdenes de magnitud).
  - Acoplamiento no lineal entre flujo y transporte.
  - Interacción río–acuífero difícil de predecir.
- El ensayo y error manual de estrategias de bombeo es **ineficiente y subóptimo**.
- La optimización garantiza la **mejor estrategia matemáticamente posible** dentro de las restricciones definidas.

### Beneficios demostrados
- Reducción de costos de extracción y remediación.
- Satisfacción simultánea de múltiples restricciones (calidad, cantidad, gradientes).
- Soporte cuantitativo para la toma de decisiones ante partes interesadas.

---

## 3. Consideraciones Generales al Usar Optimización

- La optimización **no reemplaza** el juicio hidrogeológico — lo complementa.
- La calidad del resultado depende de la calidad del modelo de simulación subyacente.
- Es necesario definir claramente:
  - **Función objetivo** (¿qué se minimiza o maximiza?).
  - **Variables de decisión** (¿qué controla el gestor?).
  - **Restricciones** (¿qué límites debe respetar la solución?).
- La linealidad del sistema determina qué tipo de optimizador es adecuado.

---

## 4. Herramientas, Perspectiva y Análisis de Sistemas

### Enfoque sistémico
El análisis de sistemas integra:
1. Modelo conceptual del acuífero.
2. Modelo numérico de simulación (ej. MODFLOW).
3. Formulación matemática del problema de optimización.
4. Algoritmo de optimización (ej. Simplex, algoritmos evolutivos).

### Pasos típicos en una aplicación S-O (Fig. 1.12, Peralta)
1. Definir objetivos de manejo.
2. Recopilar datos y construir modelo S.
3. Calibrar el modelo S.
4. Formular el problema de optimización.
5. Seleccionar y aplicar el optimizador.
6. Verificar e implementar la estrategia óptima.

---

## 5. Resumen de Conceptos Clave

| Concepto | Definición breve |
|----------|-----------------|
| Modelo S | Predice estado del sistema (cabeza, concentración) |
| Modelo S-O | S + optimizador matemático → estrategia óptima |
| Función objetivo | Criterio a minimizar/maximizar |
| Variable de decisión | Lo que el gestor puede controlar (ej. caudales de bombeo) |
| Restricción | Límite físico, legal o de calidad que debe cumplirse |
| Óptimo local vs. global | Relevante en sistemas no lineales |

---

## Referencias
- Peralta, R. C. & Kalwij, I. M. (2012). *Groundwater Optimization Handbook.* CRC Press. Cap. 1.
- Anderson, M. P., Woessner, W. W., & Hunt, R. J. (2015). *Applied Groundwater Modeling.* Academic Press.

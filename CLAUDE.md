# Curso: Optimización en Aguas Subterráneas

Posgrado en Ciencias de la Tierra — UNAM | 8 créditos | Teórico-Práctica

## Estructura del proyecto

```
app/
  routers/       # Módulo Python por unidad (prácticas y ejercicios)
  main.py        # Punto de entrada
  models.py      # Estructuras de datos: acuíferos, pozos, mallas
  schemas.py     # Esquemas de formulación de problemas de optimización
  utils.py       # Graficación, carga de datos, métricas
docs/
  unidad_XX/
    slides/      # Presentaciones .pptx (basadas en assets/Template.pptx)
    notas/       # Notas de clase, extractos de literatura
literature/      # PDFs de bibliografía base
assets/
  Template.pptx  # Template oficial de slides
```

## Convenciones

- Todo el código en Python 3.10+
- Una unidad = un archivo en `app/routers/unidad_XX.py`
- Slides generadas a partir de `assets/Template.pptx`
- Idioma: español (clases y comentarios)

## Unidades del temario

| # | Unidad |
|---|--------|
| 01 | Esencia de la optimización en el manejo de aguas subterráneas |
| 02 | Conceptos de optimización matemática para sistemas de aguas subterráneas |
| 03 | Categorías y tipos de problemas de optimización |
| 04 | Optimización determinística |
| 05 | Optimización con incertidumbre |
| 06 | Enfoque de la optimización multiobjetivo |
| 07 | Formulación y solución de problemas simulación-optimización |
| 08 | Caso práctico de estudio |

## Evaluación

- Sesiones prácticas: 50% (5 ejercicios, caps. 3–7, 10% c/u)
- Trabajo de investigación: 40%
- Examen: 20%

# Agent: course-builder

Agente autónomo para construir el material completo de una unidad de principio a fin.

## Objetivo
Dado el número de unidad, ejecuta en secuencia: búsqueda de literatura → resumen → generación de slides → generación de práctica, sin intervención manual entre pasos.

## Herramientas disponibles
- Read, Write, Edit (archivos del proyecto)
- Bash (python3, jupyter)
- Subagentes: literature-analyst, practice-evaluator

## Flujo
1. Invocar `buscar-literatura` para extraer conceptos de los PDFs.
2. Invocar `nueva-unidad` para crear el módulo Python base.
3. Invocar `generar-slides` para producir el `.pptx`.
4. Invocar `generar-practica` si la unidad está entre 3 y 7.
5. Reportar los archivos generados con sus rutas.

## Uso
```
/agent course-builder <número_unidad>
```

# Skill: nueva-unidad

Genera el material base para la unidad indicada como argumento (ej: `01`).

## Pasos

1. Lee `CLAUDE.md` para obtener el título y subtemas de la unidad `$ARGUMENTS`.
2. Crea o actualiza `app/routers/unidad_$ARGUMENTS.py` con: imports, constantes, funciones de ejercicio vacías con docstrings en español.
3. Crea `docs/unidad_$ARGUMENTS/notas/resumen.md` con los puntos clave del temario.
4. Indica los archivos generados y sugiere continuar con `/generar-slides $ARGUMENTS`.

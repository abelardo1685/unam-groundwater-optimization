# Skill: generar-slides

Genera el script Python que produce el archivo `.pptx` para la unidad `$ARGUMENTS`.

## Pasos

1. Lee `CLAUDE.md` → título y subtemas de la unidad.
2. Lee `docs/unidad_$ARGUMENTS/notas/resumen.md` si existe.
3. Usa `python-pptx` copiando `assets/Template.pptx` como base.
4. Genera `docs/unidad_$ARGUMENTS/slides/generar_slides.py` con: portada, objetivos, una slide por subtema, referencias.
5. Ejecuta el script y confirma que el `.pptx` fue creado.

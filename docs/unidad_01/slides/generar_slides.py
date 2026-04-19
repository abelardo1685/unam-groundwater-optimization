"""
Genera la presentación .pptx para la Unidad 01.
Uso: ~/.pyenv/versions/3.11.14/bin/python3 docs/unidad_01/slides/generar_slides.py
"""

from pptx import Presentation
from pptx.util import Pt
from pptx.dml.color import RGBColor
import copy, os

TEMPLATE = "assets/Template.pptx"
OUTPUT = "docs/unidad_01/slides/Unidad_01_Esencia_Optimizacion.pptx"

AZUL = RGBColor(0x1F, 0x49, 0x7D)
GRIS = RGBColor(0x59, 0x59, 0x59)


def nueva_slide(prs, layout_idx):
    return prs.slides.add_slide(prs.slide_layouts[layout_idx])


def set_texto(ph, texto, negrita=False, tamanio=None, color=None):
    tf = ph.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = texto
    run.font.bold = negrita
    if tamanio:
        run.font.size = Pt(tamanio)
    if color:
        run.font.color.rgb = color


def agregar_bullets(ph, items, tamanio=18):
    tf = ph.text_frame
    tf.clear()
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = item
        p.font.size = Pt(tamanio)


def build():
    prs = Presentation(TEMPLATE)

    # --- 1. Portada ---
    s = nueva_slide(prs, 0)   # "Diapositiva de título"
    set_texto(s.placeholders[0],
              "Unidad 01\nEsencia de la Optimización en el\nManejo de Aguas Subterráneas",
              negrita=True, tamanio=28, color=AZUL)
    set_texto(s.placeholders[1],
              "Posgrado en Ciencias de la Tierra — UNAM\n"
              "Optimización en Aguas Subterráneas",
              tamanio=18, color=GRIS)

    # --- 2. Objetivos ---
    s = nueva_slide(prs, 1)   # "Título y objetos"
    set_texto(s.placeholders[0], "Objetivos de Aprendizaje", negrita=True, tamanio=24)
    agregar_bullets(s.placeholders[1], [
        "• Explicar por qué la optimización es necesaria en aguas subterráneas",
        "• Distinguir entre modelo S y modelo S-O",
        "• Identificar las ecuaciones de flujo gobernantes",
        "• Describir el enfoque de análisis de sistemas en gestión del agua",
    ])

    # --- 3. ¿Por qué optimizar? ---
    s = nueva_slide(prs, 1)
    set_texto(s.placeholders[0], "La Necesidad de la Optimización", negrita=True, tamanio=24)
    agregar_bullets(s.placeholders[1], [
        "• Los sistemas subterráneos son complejos e inciertos:",
        "    – K varía ~13 órdenes de magnitud entre materiales",
        "    – Heterogeneidad espacial difícil de caracterizar",
        "    – Interacción río–acuífero no lineal",
        "",
        "• El ensayo y error manual es ineficiente y subóptimo",
        "",
        "• La optimización garantiza la mejor estrategia posible",
        "  dentro de las restricciones físicas, legales y de calidad",
    ])

    # --- 4. Modelo S vs. Modelo S-O ---
    s = nueva_slide(prs, 3)   # "Dos objetos"
    set_texto(s.placeholders[0], "Simulación (S) vs. Simulación-Optimización (S-O)",
              negrita=True, tamanio=22)
    agregar_bullets(s.placeholders[1], [
        "MODELO S",
        "• Predice cabeza hidráulica y",
        "  transporte de contaminantes",
        "• Entrada: estrategia de bombeo",
        "• Salida: estado del sistema",
        "",
        "Herramientas: MODFLOW, MT3D",
    ], tamanio=16)
    agregar_bullets(s.placeholders[2], [
        "MODELO S-O",
        "• Acopla simulador + optimizador",
        "• Calcula la MEJOR estrategia",
        "• Respeta restricciones del sistema",
        "",
        "Herramientas: MODMAN, GWM,",
        "Python (scipy, pyomo, flopy)",
    ], tamanio=16)

    # --- 5. Ecuaciones de flujo ---
    s = nueva_slide(prs, 1)
    set_texto(s.placeholders[0], "Ecuaciones de Flujo Gobernantes", negrita=True, tamanio=24)
    agregar_bullets(s.placeholders[1], [
        "Acuífero confinado (lineal en h):",
        "  ∂/∂x(Kx ∂h/∂x) + ∂/∂y(Ky ∂h/∂y) + ∂/∂z(Kz ∂h/∂z) - qs = Ss ∂h/∂t",
        "",
        "Acuífero libre (NO lineal — T = K·(h-ELEVb)):",
        "  ∂/∂x(K(h-ELEVb) ∂h/∂x) + Q = Ss ∂h/∂t",
        "",
        "⚠ La no linealidad determina qué optimizador es adecuado:",
        "  Lineal → Programación Lineal (LP)",
        "  No lineal → NLP, metaheurísticas",
    ])

    # --- 6. Componentes del problema S-O ---
    s = nueva_slide(prs, 1)
    set_texto(s.placeholders[0], "Componentes de un Problema de Optimización",
              negrita=True, tamanio=24)
    agregar_bullets(s.placeholders[1], [
        "1. FUNCIÓN OBJETIVO  —  ¿Qué se minimiza o maximiza?",
        "   Ej: min Costo_total = Σ costo_i · Q_i",
        "",
        "2. VARIABLES DE DECISIÓN  —  ¿Qué controla el gestor?",
        "   Ej: caudales de bombeo Q_i [m³/día]",
        "",
        "3. RESTRICCIONES  —  ¿Qué límites debe respetar la solución?",
        "   Ej: abatimiento máximo, demanda mínima, calidad del agua",
        "",
        "   min f(x)   sujeto a:   g(x) ≤ b,   h(x) = c,   x ≥ 0",
    ])

    # --- 7. Enfoque sistémico ---
    s = nueva_slide(prs, 1)
    set_texto(s.placeholders[0], "Pasos Típicos en una Aplicación S-O",
              negrita=True, tamanio=24)
    agregar_bullets(s.placeholders[1], [
        "1. Definir objetivos de manejo (stakeholders)",
        "2. Recopilar datos y construir modelo de simulación",
        "3. Calibrar el modelo S (ajuste de parámetros)",
        "4. Formular el problema de optimización",
        "   – Función objetivo, variables, restricciones",
        "5. Seleccionar el optimizador adecuado",
        "6. Resolver y verificar la estrategia óptima",
        "7. Implementar y monitorear",
        "",
        "Referencia: Peralta & Kalwij (2012), Fig. 1.12",
    ])

    # --- 8. Ejemplo Python en clase ---
    s = nueva_slide(prs, 1)
    set_texto(s.placeholders[0], "Sesión Práctica — Estrategia de Bombeo Óptima",
              negrita=True, tamanio=24)
    agregar_bullets(s.placeholders[1], [
        "Problema: 3 pozos, demanda total = 1000 m³/día",
        "",
        "Minimizar:  Costo = 2.5·Q₁ + 1.8·Q₂ + 3.1·Q₃",
        "",
        "Sujeto a:",
        "  Q₁ + Q₂ + Q₃ = 1000  (demanda)",
        "  0.006·Q₁ ≤ 5 m  (abatimiento pozo 1)",
        "  0.004·Q₂ ≤ 5 m  (abatimiento pozo 2)",
        "  0.008·Q₃ ≤ 5 m  (abatimiento pozo 3)",
        "  Q_i ≥ 0",
        "",
        "→ app/routers/unidad_01.py :: optimizar_bombeo_simple()",
    ])

    # --- 9. Resumen y referencias ---
    s = nueva_slide(prs, 1)
    set_texto(s.placeholders[0], "Resumen y Referencias", negrita=True, tamanio=24)
    agregar_bullets(s.placeholders[1], [
        "Conceptos clave de esta unidad:",
        "  ✓ S-O = Simulación + Optimización",
        "  ✓ La complejidad del sistema justifica la optimización",
        "  ✓ Todo problema S-O tiene: objetivo, variables y restricciones",
        "  ✓ La linealidad del sistema define el tipo de optimizador",
        "",
        "Bibliografía:",
        "  Peralta & Kalwij (2012), Cap. 1 — Essence of Optimizing",
        "  Anderson, Woessner & Hunt (2015), Applied GW Modeling",
        "",
        "Próxima unidad: Conceptos de Optimización Matemática",
    ])

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    prs.save(OUTPUT)
    print(f"Presentación guardada: {OUTPUT}")


if __name__ == "__main__":
    build()

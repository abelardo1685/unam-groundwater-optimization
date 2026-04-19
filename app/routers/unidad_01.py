"""
Unidad 01 — Esencia de la Optimización en el Manejo de Aguas Subterráneas

Contenido:
    - Ecuaciones de flujo en acuíferos confinados y libres (versión discreta)
    - Variabilidad de conductividad hidráulica entre materiales geológicos
    - Comparación ensayo-error vs. optimización en estrategia de bombeo simple
    - Componentes de un problema S-O: variable, restricción, objetivo
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog


# ---------------------------------------------------------------------------
# 1. Ecuaciones de flujo — diferencias finitas 1D (acuífero confinado)
# ---------------------------------------------------------------------------

def flujo_confinado_1d(T, S, Q, dx, dt, h_init, n_steps):
    """
    Diferencias finitas explícitas — flujo en acuífero confinado 1D.

    Args:
        T:       Transmisividad [m²/día]
        S:       Almacenamiento [-]
        Q:       Caudales fuente/sumidero por celda [m³/día] (negativo = extracción)
        dx:      Tamaño de celda [m]
        dt:      Paso de tiempo [días]
        h_init:  Cabeza inicial por celda [m]
        n_steps: Número de pasos de tiempo

    Returns:
        h: matriz (n_steps+1, n_celdas) con la evolución de cabezas
    """
    n = len(h_init)
    h = np.zeros((n_steps + 1, n))
    h[0] = h_init.copy()
    alpha = T * dt / (S * dx**2)

    for t in range(n_steps):
        ht = h[t].copy()
        for i in range(1, n - 1):
            h[t + 1, i] = (ht[i]
                           + alpha * (ht[i-1] - 2*ht[i] + ht[i+1])
                           + Q[i] * dt / (S * dx))
        h[t + 1, 0] = h_init[0]
        h[t + 1, -1] = h_init[-1]

    return h


# ---------------------------------------------------------------------------
# 2. Variabilidad de conductividad hidráulica por material geológico
# ---------------------------------------------------------------------------

MATERIALES_K = {
    "Grava gruesa":       1e2,
    "Arena gruesa":       1e1,
    "Arena media":        1e0,
    "Arena fina":         1e-1,
    "Limo":               1e-3,
    "Arcilla":            1e-6,
    "Roca fracturada":    1e-4,
    "Roca no fracturada": 1e-10,
}


def graficar_rango_K(materiales=MATERIALES_K):
    """
    Ilustra la complejidad paramétrica: K varía ~13 órdenes de magnitud.
    Referencia: Peralta (2012) Fig. 1.10 y Tabla 1.1.
    """
    nombres = list(materiales.keys())
    valores = [np.log10(v) for v in materiales.values()]

    fig, ax = plt.subplots(figsize=(8, 5))
    colores = plt.cm.RdYlGn(np.linspace(0.1, 0.9, len(nombres)))
    ax.barh(nombres, valores, color=colores)
    ax.set_xlabel("log₁₀(K)  [m/s]", fontsize=12)
    ax.set_title("Conductividad Hidráulica por Material Geológico\n"
                 "(varía ~13 órdenes de magnitud)", fontsize=13)
    ax.axvline(0, color="gray", lw=0.8, linestyle="--")
    plt.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# 3. Optimización de estrategia de bombeo — Programación Lineal
# ---------------------------------------------------------------------------

def optimizar_bombeo_simple(demanda, costo, abatimiento_max, coef_abatimiento):
    """
    Minimiza el costo total de extracción en N pozos sujeto a:
        sum(Q_i) = demanda              [restricción de igualdad]
        coef_i * Q_i <= abatimiento_max [restricción de abatimiento]
        Q_i >= 0                        [no negatividad]

    Args:
        demanda:          Caudal total requerido [m³/día]
        costo:            Costo unitario por pozo [$/m³]  (array)
        abatimiento_max:  Abatimiento máximo permitido [m]
        coef_abatimiento: Coeficiente influencia abatimiento-caudal por pozo (array)

    Returns:
        dict con caudales óptimos, costo total y estado de la solución
    """
    n = len(costo)
    resultado = linprog(
        c=costo,
        A_ub=np.diag(coef_abatimiento),
        b_ub=np.full(n, abatimiento_max),
        A_eq=np.ones((1, n)),
        b_eq=np.array([demanda]),
        bounds=[(0, None)] * n,
        method="highs",
    )
    return {
        "caudales_m3_dia": resultado.x,
        "costo_total_dia": resultado.fun,
        "exitoso": resultado.success,
        "mensaje": resultado.message,
    }


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 55)
    print("Unidad 01 — Esencia de la Optimización")
    print("=" * 55)

    # Demo 1: rango de K
    fig = graficar_rango_K()
    fig.savefig("docs/unidad_01/notas/rango_K.png", dpi=150)
    print("Figura rango_K.png generada en docs/unidad_01/notas/")

    # Demo 2: estrategia de bombeo óptima con 3 pozos
    res = optimizar_bombeo_simple(
        demanda=1000,
        costo=np.array([2.5, 1.8, 3.1]),
        abatimiento_max=5.0,
        coef_abatimiento=np.array([0.006, 0.004, 0.008]),
    )
    print("\nEstrategia óptima de bombeo:")
    for i, q in enumerate(res["caudales_m3_dia"]):
        print(f"  Pozo {i+1}: {q:.1f} m³/día")
    print(f"Costo mínimo: ${res['costo_total_dia']:.2f}/día")

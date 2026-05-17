"""
config_structs.py
Dataclasses mirroring the ctrl / grid / model / flowpar / RW structs in MATLAB.
"""
from dataclasses import dataclass, field
from typing import Optional, List
import numpy as np


# ── Boundary conditions sub-struct ───────────────────────────────────────────
@dataclass
class CtrlBC:
    well_pts:    np.ndarray = field(default_factory=lambda: np.array([], int))  # global node indices of all wells
    fix_pts_h:   np.ndarray = field(default_factory=lambda: np.array([], int))
    fix_value_h: np.ndarray = field(default_factory=lambda: np.array([], float))
    in_pts_h:    np.ndarray = field(default_factory=lambda: np.array([], int))
    in_el_h:     np.ndarray = field(default_factory=lambda: np.array([], int))
    in_value_h:  np.ndarray = field(default_factory=lambda: np.array([], float))


# ── Time / transient sub-struct ───────────────────────────────────────────────
@dataclass
class CtrlTim:
    tend:       float = 360.0   # total simulation time [days]
    deltQS:     float = 10.0    # quasi-stationary step length [days]
    superpos:   bool  = True    # use superposition for transient flow
    spill:      int   = 0       # 0=continuous source, 1=single spill
    dtvis:      float = 86400.0 # visualization step [s]
    # sinusoidal ranges for each driver
    dhA:   float = 0.0015; dhE:   float = 0.0065
    dirhA: float = 160.0;  dirhE: float = 200.0
    QpA:   float = 0.005;  QpE:   float = 0.05
    qr0A:  float = 50.0;   qr0E:  float = 500.0
    T_amp_a: float = 0.0;  T_amp_e:   float = 100.0
    T_fr_a:  float = 1.0;  T_fr_e:    float = 1.0
    T_phase_a: float = 0.0; T_phase_e: float = 360.0
    # Uncertainty flags (1=active, 0=constant)
    amp_unc_dh:   int = 1;  amp_unc_dirh: int = 1
    amp_unc_qr:   int = 1;  amp_unc_qp:   int = 1
    T_unc_dh:     int = 0;  T_unc_dirh:   int = 0
    T_unc_qr:     int = 0
    phase_unc_dh: int = 1;  phase_unc_dirh: int = 1
    phase_unc_qr: int = 1


# ── Transport sub-struct ──────────────────────────────────────────────────────
@dataclass
class CtrlTrns:
    n:           float = 0.25   # porosity
    al:          float = 3.0    # longitudinal dispersivity [m]
    at:          float = 0.3    # transverse dispersivity [m]
    Dm:          float = 1e-9   # molecular diffusion [m²/s]
    npartic_QS:  int   = 2000   # particles per well per QS step


# ── Geostatistics structural parameters ───────────────────────────────────────
@dataclass
class CtrlStru:
    muA:   float = -5.5;  muE:   float = -7.5
    variA: float = 0.5;   variE: float = 0.7
    intexA: float = 390.; intexE: float = 450.
    inteyA: float = 110.; inteyE: float = 160.
    kapA:   float = 0.4;  kapE:   float = 0.6


# ── Critical / evaluation values ─────────────────────────────────────────────
@dataclass
class CtrlCrit:
    t_crit: float = 180.0   # protection horizon [days]
    vip:    list  = field(default_factory=lambda: [0.1, 0.5, 0.9])


# ── Well injection geometry ───────────────────────────────────────────────────
@dataclass
class CtrlUse:
    circular:   bool  = True   # circular particle injection (True) or rectangular (False)
    longinject: float = 4.0    # injection radius [cell units]


# ── Reference flow parameters (mean state) ────────────────────────────────────
@dataclass
class CtrlPar0:
    dh:   float = 0.005   # hydraulic head gradient (dimensionless, dh/L)
    Qp:   float = 5e-3    # pumping rate [m³/s]
    qr:   float = 2.0     # recharge [mm/yr]
    dirh: float = 0.0     # flow direction [°]


# ── Main control structure ────────────────────────────────────────────────────
@dataclass
class Ctrl:
    # ── dimensionality ─────────────────────────────────────────────────
    Two_D:       bool  = True   # True → 2D, False → 3D
    dispersion:  bool  = True   # Scheidegger dispersion ON
    R4:          bool  = False  # False → Euler (R4=1 → Runge-Kutta, disabled per main)

    # ── grid size ──────────────────────────────────────────────────────
    n_pts_x: int   = 450;  d_pts_x: float = 15.0
    n_pts_y: int   = 450;  d_pts_y: float = 15.0
    n_pts_z: int   = 4;    d_pts_z: float = 15.0

    # ── well positions (fractional: [x%, y%, z%]) ─────────────────────
    inP:     List[float] = field(default_factory=lambda: [0.80, 0.50, 0.70])
    Ex_pump: bool        = True
    Ex_inP:  np.ndarray  = field(default_factory=lambda: np.array([
        [0.80, 0.45], [0.80, 0.55], [0.80, 0.60],
        [0.80, 0.40], [0.80, 0.35]]))

    # ── injection ──────────────────────────────────────────────────────
    use:         CtrlUse  = field(default_factory=CtrlUse)
    west: bool = True; east: bool = True; north: bool = True; south: bool = True
    space_disc: float = 2.0  # CFL space steps per pixel

    # ── simulation control ─────────────────────────────────────────────
    n_reali:      int  = 100
    t_crit:       bool = True   # activate critical time filter
    het:          bool = True   # heterogeneous K field
    het_geo:      bool = False  # geological K field
    use_well:     bool = False  # well in reference scenario
    use_gwn:      bool = False  # recharge in reference scenario
    href0:        bool = False  # compute reference FEM (always False for superpos)
    RWPTtrans:    bool = True
    source_geo:   int  = 1      # 1=point, 2=line, 3=gaussian

    # ── variance / structural ──────────────────────────────────────────
    variance:     float = 1.0
    kap:          float = 0.5
    nbeta:        int   = 1
    lambda_:      List[float] = field(default_factory=lambda: [120.0, 120.0])
    use_var_matern_kappa: bool = True

    # ── sub-structs ────────────────────────────────────────────────────
    bc:   CtrlBC   = field(default_factory=CtrlBC)
    tim:  CtrlTim  = field(default_factory=CtrlTim)
    trns: CtrlTrns = field(default_factory=CtrlTrns)
    stru: CtrlStru = field(default_factory=CtrlStru)
    crit: CtrlCrit = field(default_factory=CtrlCrit)
    par0: CtrlPar0 = field(default_factory=CtrlPar0)

    # ── sinusoidal transient drivers ───────────────────────────────────
    # mean ± amplitude, frequency [cycles/simulation], phase [°]
    dh_mean:   float = 0.005;  dh_ampl:   float = 0.002; dh_freq:   float = 1.0; dh_phase:   float = 0.0
    Qp_mean:   float = 5e-3;   Qp_ampl:   float = 2e-3;  Qp_freq:   float = 0.5; Qp_phase:   float = 45.0
    qr_mean:   float = 2.0;    qr_ampl:   float = 1.0;   qr_freq:   float = 1.0; qr_phase:   float = 90.0
    dirh_mean: float = 0.0;    dirh_ampl: float = 5.0;   dirh_freq: float = 0.5; dirh_phase: float = 180.0

    # TTI: particle-tracking injection interval [days]
    TTI:        float = 1.0

    # computed at runtime
    num_well:   int = 0   # index of current well being processed
    part_iter:  int = 0   # particles per matrix chunk


# ── Grid structure ────────────────────────────────────────────────────────────
@dataclass
class Grid:
    n_pts:      np.ndarray = field(default_factory=lambda: np.array([450, 450]))    # [ny, nx] or [ny,nx,nz]
    n_el:       np.ndarray = field(default_factory=lambda: np.array([450, 450]))    # same as n_pts (elements = nodes in this code)
    d_pts:      np.ndarray = field(default_factory=lambda: np.array([15., 15.]))    # [dy, dx] or [dy,dx,dz]
    domain_len: np.ndarray = field(default_factory=lambda: np.array([6750., 6750.]))
    npts:       int        = 203401
    nd:         int        = 2                                                       # number of dimensions
    x_pts:      list       = field(default_factory=list)                            # coordinate vectors [y_vec, x_vec, z_vec]


# ── Geostatistical model structure ───────────────────────────────────────────
@dataclass
class Model:
    name:       str   = 'matern'
    variance:   float = 1.0
    lambda_:    np.ndarray = field(default_factory=lambda: np.array([120., 120.]))
    kappa:      float = 0.5
    micro:      float = 0.0
    nugget:     float = 0.0
    flag_kit:   int   = 0     # 0=Dietrich&Newsam
    flag_zh:    int   = 0     # 0=standard, 1=low-K connected, 2=high-K connected
    zh_smoother: float = 0.0  # Zinn & Harvey regularization [0, 0.25]
    beta:       float = -4.0  # log(K) mean
    Qbb:        float = 0.0   # variance of uncertain mean
    periodicity: np.ndarray = field(default_factory=lambda: np.array([0, 0]))


# ── Flow parameters structure (per QS step) ───────────────────────────────────
@dataclass
class FlowPar:
    dh:      float = 0.005  # hydraulic gradient [m/m]
    Qp:      float = 5e-3   # pumping rate [m³/s]  — scalar or per-well array
    qr:      float = 2.0    # recharge [mm/yr]
    HeadDir: float = 0.0    # flow direction [°]
    h_vec:   Optional[np.ndarray] = None   # head field (ny+1, nx+1) or flat
    qx:      Optional[np.ndarray] = None   # x-Darcy velocity
    qy:      Optional[np.ndarray] = None   # y-Darcy velocity
    qz:      Optional[np.ndarray] = None   # z-Darcy velocity
    radius:  float = 0.0


# ── Random Walk state ─────────────────────────────────────────────────────────
@dataclass
class RWState:
    NPi:      int   = 0        # particles per injection position
    rem_time: Optional[np.ndarray] = None  # remaining TTI time per particle [s]
    T:        Optional[np.ndarray] = None  # elapsed time per particle [s]
    ddDyy:    Optional[np.ndarray] = None  # ∇D components (Itô correction)
    ddDyx:    Optional[np.ndarray] = None
    ddDxy:    Optional[np.ndarray] = None
    ddDxx:    Optional[np.ndarray] = None
    ddDyz:    Optional[np.ndarray] = None
    ddDxz:    Optional[np.ndarray] = None
    ddDzz:    Optional[np.ndarray] = None
    ddDzx:    Optional[np.ndarray] = None
    ddDzy:    Optional[np.ndarray] = None
    nan:      Optional[np.ndarray] = None

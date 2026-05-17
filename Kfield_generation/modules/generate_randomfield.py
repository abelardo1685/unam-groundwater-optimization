"""
generate_randomfield.py  —  mirrors generate_randomfield.m (Dietrich & Newsam 1993)
Spectral random field generation via circulant embedding FFT.
Supports: Matérn covariance, Gaussian covariance, Zinn & Harvey connected fields.
2D and 3D capable.
"""
import numpy as np
import scipy.special as sp
from .config_structs import Model, Grid


# ── Covariance functions ──────────────────────────────────────────────────────

def _matern_cov(h: np.ndarray, s2: float, lam: float, kap: float) -> np.ndarray:
    """Matérn covariance C(h) = s2 / (2^(κ-1)·Γ(κ)) · (2√κ·h/λ)^κ · K_κ(2√κ·h/λ).
    Argument = 2√κ · h/λ  — matches evaluate_covariance.m: h_eff*sqrt(kappa)*2.
    """
    C = np.full_like(h, s2, dtype=float)
    m = h > 0
    a = 2.0 * np.sqrt(kap) * h[m] / lam   # FIX: was sqrt(2*kap) — wrong by factor sqrt(2)
    C[m] = s2 / (2**(kap-1) * sp.gamma(kap)) * a**kap * sp.kv(kap, a)
    return C


def _gaussian_cov(h: np.ndarray, s2: float, lam: float) -> np.ndarray:
    return s2 * np.exp(-(h/lam)**2)


def _cov_nd(H: np.ndarray, s2: float, kap: float,
            name: str, nugget: float = 0.0) -> np.ndarray:
    """
    Isotropic covariance over λ-normalized separation distance H.
    nugget effect is added at H==0 (matches evaluate_covariance.m).
    """
    if name == 'matern':
        C = _matern_cov(H, s2, 1.0, kap)   # lam=1 because H already λ-scaled
    else:
        C = _gaussian_cov(H, s2, 1.0)

    if nugget != 0.0:
        C[H == 0] += nugget   # nugget at zero separation distance

    return C


# ── Embedding size search ─────────────────────────────────────────────────────

def _embed_size(n: int, d: float, s2: float, lam: float, kap: float,
                name: str, dec: float = 0.01) -> int:
    """Find smallest power-of-2 embedding ≥ n where tail covariance < dec·C(0)."""
    for m in range(n + 1, 8 * n):
        h = np.arange(m) * d
        if name == 'matern':
            c = _matern_cov(h, s2, lam, kap)
        else:
            c = _gaussian_cov(h, s2, lam)
        if abs(c[-1]) < dec * c[0]:
            return int(2**np.ceil(np.log2(m)))
    return int(2**np.ceil(np.log2(4 * n)))


# ── FFT covariance matrix initialization ─────────────────────────────────────

def initialize_FFT_cov(model: Model, grid: Grid) -> np.ndarray:
    """
    Compute |FFT(Q_e)| for the embedded circulant covariance matrix.
    Returns FFTQe with shape (me_y, me_x) for 2D or (me_y, me_x, me_z) for 3D.
    Mirrors initialize_FFT_cov.m + evaluate_separation.m.
    """
    s2     = model.variance
    lam    = model.lambda_      # [lam_y, lam_x] or [lam_y, lam_x, lam_z]
    kap    = model.kappa
    name   = model.name
    nugget = model.nugget
    micro  = model.micro
    n_pts  = grid.n_pts
    d_pts  = grid.d_pts
    nd     = grid.nd

    if nd == 2:
        ny, nx = int(n_pts[0]), int(n_pts[1])
        dy, dx = d_pts[0], d_pts[1]
        me_y = _embed_size(ny, dy, s2, lam[0], kap, name)
        me_x = _embed_size(nx, dx, s2, lam[1], kap, name)

        hy = np.minimum(np.arange(me_y), me_y - np.arange(me_y)) * dy
        hx = np.minimum(np.arange(me_x), me_x - np.arange(me_x)) * dx
        Hx, Hy = np.meshgrid(hx, hy)   # shape (me_y, me_x) — standard 'xy' indexing
        H = np.sqrt((Hy / lam[0])**2 + (Hx / lam[1])**2)

        if micro > 0:
            H = np.sqrt(H**2 + micro**2) - micro   # Kitanidis microscale correction

        Qe = _cov_nd(H, s2, kap, name, nugget)
        FFTQe = np.abs(np.fft.fftn(Qe))

    else:
        ny, nx, nz = int(n_pts[0]), int(n_pts[1]), int(n_pts[2])
        dy, dx, dz = d_pts[0], d_pts[1], d_pts[2]
        me_y = _embed_size(ny, dy, s2, lam[0], kap, name)
        me_x = _embed_size(nx, dx, s2, lam[1], kap, name)
        me_z = _embed_size(nz, dz, s2, lam[2], kap, name)

        hy = np.minimum(np.arange(me_y), me_y - np.arange(me_y)) * dy
        hx = np.minimum(np.arange(me_x), me_x - np.arange(me_x)) * dx
        hz = np.minimum(np.arange(me_z), me_z - np.arange(me_z)) * dz
        # FIX: use (hy, hx, hz) order so H has shape (me_y, me_x, me_z)
        # matching the conventional (y, x, z) axis ordering used throughout
        Hy, Hx, Hz = np.meshgrid(hy, hx, hz, indexing='ij')
        H = np.sqrt((Hy / lam[0])**2 + (Hx / lam[1])**2 + (Hz / lam[2])**2)

        if micro > 0:
            H = np.sqrt(H**2 + micro**2) - micro   # Kitanidis microscale correction

        Qe = _cov_nd(H, s2, kap, name, nugget)
        FFTQe = np.abs(np.fft.fftn(Qe))

    return FFTQe


# ── Main random field generator ───────────────────────────────────────────────

def generate_randomfield(model: Model, grid: Grid,
                         FFTQe: np.ndarray = None,
                         rng: np.random.Generator = None) -> tuple:
    """
    Generate one realization of ln(K) via Dietrich & Newsam spectral method.
    Mirrors generate_randomfield.m (Wolfgang Nowak).

    Returns
    -------
    Y     : ndarray shape (ny, nx) or (ny, nx, nz)  — ln(K) realization
    FFTQe : ndarray — reusable FFT of covariance (pass back in to avoid recomputation)
    """
    if rng is None:
        rng = np.random.default_rng()

    if FFTQe is None:
        FFTQe = initialize_FFT_cov(model, grid)

    gride_shape = FFTQe.shape
    gride_npts  = FFTQe.size
    sqrtQlambda = np.sqrt(np.maximum(FFTQe / gride_npts, 0.0))

    n_pts = grid.n_pts
    nd    = grid.nd

    while True:
        # Dietrich & Newsam: complex Gaussian white noise → IFFT → real part
        eps = (rng.standard_normal(gride_shape) +
               1j * rng.standard_normal(gride_shape))
        Ye  = np.real(np.fft.ifftn(eps * sqrtQlambda)) * gride_npts

        # Zinn & Harvey connected fields
        if model.flag_zh > 0:
            Ye = Ye / np.sqrt(model.variance)   # normalize to unit variance
            zh_s = model.zh_smoother            # regularization [0, 0.25]
            # FIX: proper erfinv formula — was arcsin (completely wrong function)
            # MATLAB: erfinv(2*(1-s)*erf(|Ye|*sqrt(0.5)) - (1-s)) * sqrt(2)
            Ye_abs = np.abs(Ye)
            arg = 2 * (1 - zh_s) * sp.erf(Ye_abs * np.sqrt(0.5)) - (1 - zh_s)
            arg = np.clip(arg, -0.9999, 0.9999)
            Ye_zh = sp.erfinv(arg) * np.sqrt(2)
            if model.flag_zh == 1:   # low-K connected
                Ye = -Ye_zh
            else:                    # high-K connected (flag_zh == 2)
                Ye =  Ye_zh
            Ye = Ye * np.sqrt(model.variance)   # restore desired variance

        # Extract exactly n_pts elements per dimension from embedded field
        # FIX: was [:ny+1, :nx+1, :nz+1] — returned n_pts+1 per dimension
        if nd == 2:
            ny, nx = int(n_pts[0]), int(n_pts[1])
            Y = Ye[:ny, :nx]
        else:
            ny, nx, nz = int(n_pts[0]), int(n_pts[1]), int(n_pts[2])
            Y = Ye[:ny, :nx, :nz]

        # Add mean: Y is already zero-mean with variance ≈ model.variance
        # FIX: was (Y-mean)/std * sqrt(var) + beta — forced exact per-realization
        # normalization, which is statistically wrong. MATLAB only adds the mean.
        Y = Y + model.beta

        if not (np.any(np.isnan(Y)) or np.any(np.isinf(Y))):
            break

    return Y, FFTQe

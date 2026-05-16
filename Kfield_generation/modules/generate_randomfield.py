"""
generate_randomfield.py  —  mirrors generate_randomfield.m (Dietrich & Newsam 1993)
Spectral random field generation via circulant embedding FFT.
Supports: Matérn covariance, Zinn & Harvey connected fields.
2D and 3D capable.
"""
import numpy as np
import scipy.special as sp
from .config_structs import Model, Grid


# ── Covariance functions ──────────────────────────────────────────────────────

def _matern_cov(h: np.ndarray, s2: float, lam: float, kap: float) -> np.ndarray:
    """Matérn covariance C(h) = s2 / (2^(kap-1)*Γ(kap)) * (√2κ h/λ)^κ * Kv(κ, √2κ h/λ)."""
    C = np.full_like(h, s2, dtype=float)
    m = h > 0
    a = np.sqrt(2*kap) * h[m] / lam
    C[m] = s2 / (2**(kap-1) * sp.gamma(kap)) * a**kap * sp.kv(kap, a)
    return C


def _gaussian_cov(h: np.ndarray, s2: float, lam: float) -> np.ndarray:
    return s2 * np.exp(-(h/lam)**2)


def _cov_nd(H: np.ndarray, s2: float, lam_vec: np.ndarray, kap: float,
            name: str) -> np.ndarray:
    """
    Isotropic covariance over nd-dimensional separation H (already combined distance).
    For anisotropic: caller pre-scales each direction by 1/lambda.
    """
    if name == 'matern':
        return _matern_cov(H, s2, 1.0, kap)  # lam=1 because H already scaled
    else:
        return _gaussian_cov(H, s2, 1.0)


# ── Embedding size search ─────────────────────────────────────────────────────

def _embed_size(n: int, d: float, s2: float, lam: float, kap: float,
                name: str, dec: float = 0.01) -> int:
    """Find smallest power-of-2 embedding where tail covariance < dec*C(0)."""
    for m in range(n+1, 8*n):
        h = np.arange(m) * d
        if name == 'matern':
            c = _matern_cov(h, s2, lam, kap)
        else:
            c = _gaussian_cov(h, s2, lam)
        if abs(c[-1]) < dec * c[0]:
            return int(2**np.ceil(np.log2(m)))
    return int(2**np.ceil(np.log2(4*n)))


# ── FFT covariance matrix initialization ─────────────────────────────────────

def initialize_FFT_cov(model: Model, grid: Grid) -> np.ndarray:
    """
    Compute |FFT(Q_e)| for the embedded circulant covariance matrix.
    Returns FFTQe with shape (me_y, me_x) for 2D or (me_y, me_x, me_z) for 3D.
    Mirrors initialize_FFT_cov.m.
    """
    s2    = model.variance
    lam   = model.lambda_          # array [lam_y, lam_x] or [lam_y, lam_x, lam_z]
    kap   = model.kappa
    name  = model.name
    n_pts = grid.n_pts
    d_pts = grid.d_pts
    nd    = grid.nd

    if nd == 2:
        ny, nx = int(n_pts[0]), int(n_pts[1])
        dy, dx = d_pts[0], d_pts[1]
        me_y = _embed_size(ny+1, dy, s2, lam[0], kap, name)
        me_x = _embed_size(nx+1, dx, s2, lam[1], kap, name)

        hy = np.minimum(np.arange(me_y), me_y - np.arange(me_y)) * dy
        hx = np.minimum(np.arange(me_x), me_x - np.arange(me_x)) * dx
        Hx, Hy = np.meshgrid(hx, hy)
        # anisotropic: scale each direction by its own lambda
        H  = np.sqrt((Hy/lam[0])**2 + (Hx/lam[1])**2)
        Qe = _cov_nd(H, s2, lam, kap, name)
        FFTQe = np.abs(np.fft.fftn(Qe))

    else:
        ny, nx, nz = int(n_pts[0]), int(n_pts[1]), int(n_pts[2])
        dy, dx, dz = d_pts[0], d_pts[1], d_pts[2]
        me_y = _embed_size(ny+1, dy, s2, lam[0], kap, name)
        me_x = _embed_size(nx+1, dx, s2, lam[1], kap, name)
        me_z = _embed_size(nz+1, dz, s2, lam[2], kap, name)

        hy = np.minimum(np.arange(me_y), me_y - np.arange(me_y)) * dy
        hx = np.minimum(np.arange(me_x), me_x - np.arange(me_x)) * dx
        hz = np.minimum(np.arange(me_z), me_z - np.arange(me_z)) * dz
        Hx, Hy, Hz = np.meshgrid(hx, hy, hz, indexing='ij')
        H  = np.sqrt((Hy/lam[0])**2 + (Hx/lam[1])**2 + (Hz/lam[2])**2)
        Qe = _cov_nd(H, s2, lam, kap, name)
        FFTQe = np.abs(np.fft.fftn(Qe))

    return FFTQe


# ── Main random field generator ───────────────────────────────────────────────

def generate_randomfield(model: Model, grid: Grid,
                         FFTQe: np.ndarray = None,
                         rng: np.random.Generator = None) -> tuple:
    """
    Generate one realization of ln(K) via Dietrich & Newsam spectral method.
    Mirrors generate_randomfield.m.

    Returns
    -------
    Y     : ndarray shape (ny+1, nx+1) or (ny+1, nx+1, nz+1)  — ln(K) field
    FFTQe : ndarray — reusable FFT of covariance (cached for speed)
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
        # Dietrich & Newsam: complex Gaussian noise → IFFT → real part
        eps = (rng.standard_normal(gride_shape) +
               1j * rng.standard_normal(gride_shape))
        Ye  = np.real(np.fft.ifftn(eps * sqrtQlambda)) * gride_npts

        # Zinn & Harvey connected fields (if requested)
        if model.flag_zh > 0:
            Ye = Ye / np.sqrt(model.variance)
            if model.flag_zh == 1:   # low-K connected
                Ye = -np.arcsin(np.clip(Ye * np.sqrt(0.5), -0.9999, 0.9999)) * np.sqrt(2)
            elif model.flag_zh == 2: # high-K connected
                Ye =  np.arcsin(np.clip(Ye * np.sqrt(0.5), -0.9999, 0.9999)) * np.sqrt(2)
            Ye = Ye * np.sqrt(model.variance)

        # Extract field from embedded domain
        if nd == 2:
            ny, nx = int(n_pts[0]), int(n_pts[1])
            Y = Ye[:ny+1, :nx+1]
        else:
            ny, nx, nz = int(n_pts[0]), int(n_pts[1]), int(n_pts[2])
            Y = Ye[:ny+1, :nx+1, :nz+1]

        # Normalize to zero mean / unit variance, then add desired mean and σ
        std = Y.std()
        if std < 1e-12:
            continue
        Y = (Y - Y.mean()) / std * np.sqrt(model.variance) + model.beta

        if not (np.any(np.isnan(Y)) or np.any(np.isinf(Y))):
            break

    return Y, FFTQe

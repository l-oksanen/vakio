from dataclasses import dataclass

import numpy as np
from scipy.signal import find_peaks as signal_find_peaks
from scipy.signal import savgol_filter


def generate(L, n_magenta=1, n_cyan=1, shifts=None):
    """
    Return colors on the boundary of the sRGB space at lightness L.

    L must be between 0.3 and 0.7.

    The colors are:
    * Green, blue and red peak values
    * Magentas between blue and red
    * Cyans between green and blue

    Returns `3 + n_magenta + n_cyan` colors in total. An optional
    list of shifts of the same length adjusts each color's position:
    a value of 0 leaves the color unchanged, values in (-1, 0) shift
    it toward the left neighbor, and values in (0, 1) shift it toward
    the right neighbor.
    """
    if L < 0.3 or L > 0.7:
        raise ValueError("L must be between 0.3 and 0.7")

    peaks, properties = find_peaks(L)
    if len(peaks) == 3:
        green, blue, red = peaks
    elif len(peaks) == 4:
        green, blue, _, red = peaks
    else:
        raise _PeakDetectionError(
            L, peaks, properties, _PeakDetectionParams()
        )

    colors = [green, blue, red]
    colors += linspace_ch(blue, red, n_magenta + 2)[1:-1]
    colors += linspace_ch(blue, green, n_cyan + 2)[1:-1]
    colors = hue_sorted(colors, green[2])

    if shifts is not None:
        n = len(colors)
        colors_ = []
        for i in range(n):
            s = shifts[i]
            color = (
                colors[np.mod(i - 1, n)]
                if s < 0
                else colors[np.mod(i + 1, n)]
            )
            bias = 1 - 2 * abs(s)
            w, w_ = (1 - bias) / 2, (1 + bias) / 2
            colors_.append(
                avg_ch(color, colors[i], weight1=w, weight2=w_)
            )
        colors = colors_
    return colors


def find_peaks(L, left_h=100, *, _params=None):
    """
    Find the chroma peaks at lightness L.

    The starting point `left_h` determines the order of peaks.
    The default left_h gives the green peak first.

    Internal parameters:
    _params : _PeakDetectionParams, optional
        Intended only for debugging rare numerical edge cases
        where peak detection fails for otherwise valid L values.
        Not part of the public API and may change without notice.
    """
    _params = _params or _PeakDetectionParams()

    hs = np.linspace(left_h, left_h + 360, _params.resolution)
    cs = np.array([max_c(L, h) for h in hs])
    css = savgol_filter(
        cs,
        window_length=_params.window_length,
        polyorder=_params.polyorder,
    )
    peaks, properties = signal_find_peaks(
        css, prominence=_params.prominence
    )
    return (
        list(
            zip(
                [L] * len(cs),
                cs[peaks],
                [np.mod(h, 360) for h in hs[peaks]],
                strict=False,
            )
        ),
        properties,
    )


def hue_sorted(colors, h_start=0):
    """
    Sort colors in hue starting from h_start.
    """
    return sorted(
        colors, key=lambda p: np.mod(p[2] - (h_start - 0.1), 360)
    )


def dist_perceptual(color1, color2, wL=0.4):
    """
    Perceptual distance between two colors.

    Based on the norm defined by `|color|^2 = wL*L^2 + |(a, b)|^2`
    where `color = (L, a, b)` in the Oklab space, and the Euclidean
    norm is used for `(a, b)`.
    """
    l1, c1, h1 = color1
    l2, c2, h2 = color2
    a1, a2 = np.radians(h1), np.radians(h2)
    c1 = c1 / 1000
    c2 = c2 / 1000
    dab2 = c1**2 + c2**2 - 2 * c1 * c2 * np.cos(a1 - a2)
    dL = l1 - l2
    return np.sqrt(wL * dL**2 + dab2)


def dist_in_ch(color1, color2):
    """
    Compute the distance between two colors in chroma-hue subspace.

    Uses the Euclidean distance, taking into account the periodicity.
    When chroma is given per mille, and hue is given in degrees,
    this gives a sensible distance.
    """
    _, c1, h1 = color1
    _, c2, h2 = color2
    dh = diff_hue(h1, h2)
    dc = c1 - c2
    return np.sqrt(dh**2 + dc**2)


def min_dist_in_ch(colors):
    """
    Compute minimal distance (dist_in_ch) between given colors.
    """
    min_dist = np.inf
    for i in range(len(colors)):
        for j in range(i + 1, len(colors)):
            r = dist_in_ch(colors[i], colors[j])
            if r < min_dist:
                min_dist = r
    return min_dist


def diff_hue(h1, h2):
    """
    Compute the difference between hues.
    """
    return np.mod(h1 - h2 + 180, 360) - 180


def linspace_hue(h1, h2, n):
    """
    Return evenly spaced hue values.
    """
    dh = diff_hue(h2, h1)
    r1, dr = np.radians(h1), np.radians(dh)
    drs = np.linspace(0, dr, n)
    return np.degrees(np.arctan2(np.sin(r1 + drs), np.cos(r1 + drs)))


def avg_hue(h1, h2, weight1=1, weight2=1):
    """
    Compute the weighted average of hues.
    """
    a1, a2 = np.radians(h1), np.radians(h2)
    return np.mod(
        np.degrees(
            np.arctan2(
                weight1 * np.sin(a1) + weight2 * np.sin(a2),
                weight1 * np.cos(a1) + weight2 * np.cos(a2),
            ),
        ),
        360,
    )


def linspace_ch(color1, color2, n):
    """
    Return evenly spaced colors in the chroma-hue subspace.

    Lightness is the same for all colors and is that of color1.
    """
    L = color1[0]
    cs = np.linspace(color1[1], color2[1], n)
    hs = linspace_hue(color1[2], color2[2], n)
    return [
        (L, min(c, max_c(L, h)), h)
        for c, h in zip(cs, hs, strict=True)
    ]


def avg_ch(color1, color2, weight1=1, weight2=1):
    """
    Compute the weighted average of colors in the chroma-hue subspace.

    Lightness is that of color1.
    """
    L, c, h = color1
    _, c_, h_ = color2
    return clamp(
        L,
        weight1 * c + weight2 * c_,
        avg_hue(h, h_, weight1=weight1, weight2=weight2),
    )


def clamp(L, c, h):
    """
    Return color with chroma clamped to the sRGB boundary.
    """
    return (L, min(c, max_c(L, h)), np.mod(h, 360))


def max_c(L, h, margin=0):
    """
    Find the maximum chroma in the sRGB space given lightness and hue.
    """

    def f(c):
        return lin_srgb_mask(*oklch_to_lin_srgb(L, c, h)) - 0.5

    return bisect(0, 360, f) - margin


def bisect(a, b, f, tol=1):
    """
    Find a root of function f between points a and b.

    Uses bisection search, stopping when the interval length falls
    below tol.
    """
    if a > b:
        a, b = b, a
    while np.abs(b - a) > tol:
        c = (b + a) / 2
        if np.sign(f(c)) == np.sign(f(a)):
            a = c
        else:
            b = c
    return a


def lin_srgb_mask(r, g, b):
    """
    Return 1 if linear r, g, b is in sRGB space and 0 otherwise.
    """
    return (np.minimum(r, np.minimum(g, b)) > 0) * (
        np.maximum(r, np.maximum(g, b)) < 1
    )


def oklch_to_srgb(L, c, h, use_mask=False):
    """
    Return r, g, b corresponding to L, c, h.

    Chroma c is given per mille, hue h is given in degrees.
    If mask is used, returns black for points outside the sRBG space.
    """
    r, g, b = oklch_to_lin_srgb(L, c, h)
    if use_mask:
        m = lin_srgb_mask(r, g, b)
        r, g, b = m * r, m * g, m * b
    return srgb_to_nonlin(r), srgb_to_nonlin(g), srgb_to_nonlin(b)


def srgb_to_oklch(r, g, b):
    """
    Return L, c, h corresponding to r, g, b.

    Chroma c is given per mille, hue h is given in degrees.
    """
    return lin_srgb_to_oklch(
        srgb_to_lin(r), srgb_to_lin(g), srgb_to_lin(b)
    )


def srgb_to_nonlin(x):
    """
    Return r, g, or b transformed from linear to nonlinear sRGB space.

    Reference:
    https://bottosson.github.io/posts/colorwrong/
    """
    x = np.asarray(x)
    y = np.empty_like(x)
    mask = x >= 0.0031308
    y[mask] = 1.055 * np.power(x[mask], 1.0 / 2.4) - 0.055
    y[~mask] = 12.92 * x[~mask]
    y = np.clip(y, 0, 1)
    return y.item() if y.ndim == 0 else y


def srgb_to_lin(x):
    """
    Return r, g, or b transformed from nonlinear to linear sRGB space.

    Reference:
    https://bottosson.github.io/posts/colorwrong/
    """
    x = np.asarray(x)
    y = np.empty_like(x)
    mask = x >= 0.04045
    y[mask] = np.power((x[mask] + 0.055) / (1 + 0.055), 2.4)
    y[~mask] = x[~mask] / 12.92
    return y.item() if y.ndim == 0 else y


def oklch_to_lin_srgb(L, c, h):
    """
    Return linear r, g, b corresponding to L, c, h.

    Reference:
    https://bottosson.github.io/posts/oklab/
    """
    c = c / 1000
    a = c * np.cos(np.radians(h))
    b = c * np.sin(np.radians(h))

    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b

    l = np.power(l_, 3)
    m = np.power(m_, 3)
    s = np.power(s_, 3)

    r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    b = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s

    return r, g, b


def lin_srgb_to_oklch(r, g, b):
    """
    Return L, c, h corresponding to linear r, g, b.

    Reference:
    https://bottosson.github.io/posts/oklab/
    """

    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b

    l_ = np.cbrt(l)
    m_ = np.cbrt(m)
    s_ = np.cbrt(s)

    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    b = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_

    c = 1000 * np.sqrt(a**2 + b**2)
    h = np.mod(np.degrees(np.atan2(b, a)), 360)

    return L, c, h


@dataclass(frozen=True)
class _PeakDetectionParams:
    prominence: float = 0.2
    resolution: int = 360
    window_length: int = 10
    polyorder: int = 3


class _PeakDetectionError(RuntimeError):
    def __init__(self, L, peaks, properties, params):
        self.L = L
        self.peaks = peaks
        self.properties = properties
        self.config = params
        prominence_ = (
            params.prominence + 0.05
            if len(peaks) > 4
            else max(0.0, params.prominence - 0.05)
        )
        super().__init__(f"""
Peak detection assumptions were violated.

Expected 3 or 4 peaks, found {len(peaks)} peaks. 

Lightness level: {L}
{params}

This indicates that internal parameters for the peak-detection 
algorithm should be changed. It might help to adjust prominence:
peaks, properties = find_peaks(
    L, _params=_PeakDetectionParams(prominence={prominence_:0.2f})
)

Prominences of detected peaks: 
{properties["prominences"]}
""".strip())

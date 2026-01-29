from dataclasses import dataclass

import numpy as np
from scipy.signal import find_peaks as signal_find_peaks
from scipy.signal import savgol_filter


def generate(L, sky_shift=0, ocean_shift=0):
    """
    Return colors on the boundary of the sRGB space at lightness L.

    L must be between 0.3 and 0.7.

    The selected colors are:
    * Green, blue and red peak values
    * Purple at the hue midpoint between blue and red
    * Ocean at the hue midpoint between green and blue
    * Dull blue, equidistant to ocean and blue

    Blue and ocean can be shifted toward green using sky_shift and
    ocean_shift. A value of 1 sets them equal to green.
    """
    if L < 0.3 or L > 0.7:
        raise ValueError("L must be between 0.3 and 0.7")

    peaks, properties = find_peaks(L)
    if len(peaks) == 3:
        green, sky, red = peaks
    elif len(peaks) == 4:
        green, sky, _, red = peaks
    else:
        raise _PeakDetectionError(
            L, peaks, properties, _PeakDetectionParams()
        )

    blue = color_on_bd(
        L, avg_hue(green[2], sky[2], bias=1 - 2 * sky_shift)
    )
    colors = [green, blue, red]

    colors.append(color_on_bd(L, avg_hue(blue[2], red[2])))

    ocean_h = avg_hue(sky[2], green[2], bias=ocean_shift)
    ocean = color_on_bd(L, ocean_h)
    colors.append(ocean)
    r = dist_in_ch(ocean, blue) / 2
    colors.append(move_along_bd(blue, r, avg_hue(ocean_h, blue[2])))

    return hue_sorted(colors, green[2])


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


def color_on_bd(L, h):
    """
    Return the color at sRGB boundary for given lightness and hue.
    """
    return (L, max_c(L, h), np.mod(h, 360))


def move_along_bd(origin, distance, init_h):
    """
    Return color at sRGB boundary at given distance from origin.

    Color is found using the bisection method and init_h is used as
    an initial guess for hue.
    """
    L, _, h = origin
    h_ = bisect(
        h,
        init_h,
        lambda h_: dist_in_ch(color_on_bd(L, h_), origin) - distance,
    )
    return color_on_bd(L, h_)


def hue_sorted(colors, h_start=0):
    """
    Sort colors in hue starting from h_start.
    """
    return sorted(
        colors, key=lambda p: np.mod(p[2] - (h_start - 0.1), 360)
    )


def dist_perceptual(color1, color2, kL=1, kC=1, kH=0.6):
    """
    Perceptual distance between two colors in Oklch space.
    """
    l1, c1, h1 = color1
    l2, c2, h2 = color2
    c1 = c1 / 1000
    c2 = c2 / 1000
    dL = (l1 - l2) / kL
    dC = (c1 - c2) / kC
    dh = np.radians(diff_hue(h1, h2))
    dH = (2 * np.sqrt(c1 * c2) * np.sin(dh / 2)) / kH
    return np.sqrt(dL**2 + dC**2 + dH**2)


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


def avg_hue(h1, h2, bias=0):
    """
    Compute the biased average of hues.

    The bias should be between -1 and 1.
    """
    bias = max(-1, min(1, bias))
    w1, w2 = (1 - bias) / 2, (1 + bias) / 2
    a1, a2 = np.radians(h1), np.radians(h2)
    return np.degrees(
        np.arctan2(
            w1 * np.sin(a1) + w2 * np.sin(a2),
            w1 * np.cos(a1) + w2 * np.cos(a2),
        )
    )


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

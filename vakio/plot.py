import numpy as np
from matplotlib import pyplot as plt

from .alg import min_dist_in_ch, oklch_to_srgb

left_angle = 100


def L_level(L, resolution=1440):
    """
    Plot the sRGB space at a constant lightness level L.
    """
    hs = np.linspace(left_angle, left_angle + 360, resolution)
    cs = np.linspace(0, 360, resolution)
    Hs, Cs = np.meshgrid(hs, cs)
    r, g, b = oklch_to_srgb(L, Cs, Hs, use_mask=True)
    plt.imshow(
        np.flipud(np.dstack((r, g, b))),
        extent=[hs[0], hs[-1], cs[0], cs[-1]],
    )


def point(L, c, h, col_border="gray", size=50, size_border=30):
    """
    Plot a point in the sRGB space.
    """
    h = np.mod(h - left_angle, 360) + left_angle
    plt.scatter(h, c, color=col_border, s=size)
    r, g, b = oklch_to_srgb(L, c, h)
    plt.scatter(h, c, color=[r, g, b], s=size - size_border)


def points(ps):
    """
    Plot points in the sRGB space.
    """
    for p in ps:
        point(*p)


def cirle(p, r):
    """
    Plot circle with center p and radius r in the sRGB space.
    """
    _, c, h = p
    ts = np.linspace(0, 2 * np.pi)
    hs = r * np.cos(ts) + h
    plt.plot(hs, r * np.sin(ts) + c, color="gray", linewidth=0.75)
    if np.min(hs) < left_angle:
        plt.plot(
            hs + 360, r * np.sin(ts) + c, color="gray", linewidth=0.75
        )
    if np.max(hs) > left_angle + 360:
        plt.plot(
            hs - 360, r * np.sin(ts) + c, color="gray", linewidth=0.75
        )


def colors(ps, show_separation=True):
    """
    Plot the colors and their separation in the sRGB space.
    """
    L_level(ps[0][0])
    points(ps)
    if show_separation:
        r = min_dist_in_ch(ps)
        for p in ps:
            cirle(p, r)
    plt.xlim(left_angle, 360 + left_angle)
    plt.ylim(0, 360)
    plt.xticks([180, 360])
    plt.yticks([100, 200, 300])
    plt.xlabel("hue")
    plt.ylabel("chroma")

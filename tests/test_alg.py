import numpy as np

import vakio.alg as alg
import vakio.view as view

hexes = [
    "#fa4549",
    "#e16f24",
    "#bf8700",
    "#2da44e",
    "#339D9B",
    "#218bff",
    "#a475f9",
    "#4d2d00",
]


def test_srgb_to_oklch_to_srgb():
    for h in hexes:
        color = view.to_rgb(h)
        color_ = alg.oklch_to_srgb(*alg.srgb_to_oklch(*color))
        assert abs(color[0] - color_[0]) < 10**-6
        assert abs(color[1] - color_[1]) < 10**-6
        assert abs(color[2] - color_[2]) < 10**-6


def test_generate():
    for L in np.linspace(0.3, 0.7, 100):
        alg.generate(L)

import html
import textwrap

import numpy as np
from IPython.display import HTML, display
from matplotlib import pyplot as plt
from matplotlib.colors import XKCD_COLORS, to_rgb

from .alg import dist_perceptual, srgb_to_oklch
from .metadata import *


def hex_to_oklch(h):
    """
    OKLCH L, c, h value corresponding to sRGB hex value.
    """
    return srgb_to_oklch(*to_rgb(h))


def hex_to_xkcd_name(h):
    """
    Find the name of the closest XKCD color.
    """
    c = hex_to_oklch(h)
    ds = {
        name: dist_perceptual(c, hex_to_oklch(h_))
        for name, h_ in XKCD_COLORS.items()
    }
    name = min(ds, key=ds.get)
    return name[5:]


def hexes(hexes, lift={}, labels=None, colored_labels=True):
    """
    Plot hex color values as a table with one or two rows.

    Key-value pairs in lift cause hexes[key] to be shown at position
    value on the second row.

    If no labels are provided, XKCD color names as used.

    Setting colored_labels to False prints labels in black instead of
    their corresponding color.
    """
    if labels is None:
        labels = [hex_to_xkcd_name(h) for h in hexes]
    two_rows = len(lift) > 0
    if two_rows:
        n_cols = max(len(hexes) - len(lift), max(lift.keys()))
        _, axs = plt.subplots(
            2,
            n_cols,
            figsize=(n_cols, 2),
            gridspec_kw={"hspace": 0.05},
        )
    else:
        _, axs = plt.subplots(1, len(hexes), figsize=(len(hexes), 1))

    shift = 0
    for i in range(len(hexes)):
        rot = -45
        posy = 1.1
        if two_rows:
            if i in lift:
                ax = axs[0, lift[i]]
                shift += 1
                rot = 45
                posy = -0.65
            else:
                ax = axs[1, i - shift]
        elif len(hexes) > 1:
            ax = axs[i]
        else:
            ax = axs
        h = hexes[i]
        c = h if colored_labels else "black"
        ax.imshow(np.dstack(to_rgb(h)))
        ax.text(
            -0.1,
            posy,
            labels[i],
            horizontalalignment="left",
            rotation=rot,
            rotation_mode="anchor",
            color=c,
        )
    if len(hexes) > 1:
        for ax in axs.flat:
            ax.axis("off")
    else:
        axs.axis("off")


def palette(palette):
    """
    Display palette as a HTML table.
    """
    html = "<table>"
    for s, ix in semantic_mapping_colors.items():
        h = palette[ix]
        r, g, b = to_rgb(h)
        name = hex_to_xkcd_name(h)
        L = hex_to_oklch(h)[0]
        html += f"""
<tr style='
    background: #fff; 
    font-family: 
    monospace; color: 
    rgb({255*r}, {255*g}, {255*b}); 
    text-align: left;
'>
<td>■</td>
<td>{s}</td>
<td>{h}</td>
<td>{100*L:.0f}</td>
<td>{name}</td>
<td>{semantics_color[s]}</td>
</tr>"""
    display(HTML(html + "</table>"))


def copyable_preview(text, max_cols=70, max_lines=5, indent=0):
    """
    Display text as HTML with truncation and “copy full text” button.

    The text is truncated to at most `max_lines` lines, and each line
    is truncated to at `most max_cols` characters. An optional
    indentation of `indent` spaces can be applied to each line.
    """
    text = textwrap.indent(text, indent * " ")
    lines = text.splitlines()
    preview_lines = []
    for i, line in enumerate(lines):
        if i >= max_lines:
            preview_lines.append("…")
            break
        if len(line) > max_cols:
            preview_lines.append(html.escape(line[:max_cols]) + "…")
        else:
            preview_lines.append(html.escape(line))
    preview = "<br>".join(preview_lines)
    escaped = html.escape(text)
    display(HTML(f"""
<div style="
    font-family: monospace;
    border: 1px solid #ddd;
    padding: 8px;
    border-radius: 6px;
    background: #fafafa;
    max-width: 100%;
">
<div><pre>{preview}</pre></div>
<button onclick="
    const ta = document.createElement('textarea');
    ta.value = `{escaped}`;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
    this.innerText = 'Copied!';
    setTimeout(() => this.innerText = 'Copy', 1500);
" style="
    margin-top: 6px;
    padding: 4px 10px;
">
Copy
</button>
</div>
    """))


def closest(hexes, palette):
    """
    Display the closest colors in palette as a HTML table.
    """
    html = """
<table style='border-collapse: collapse;'>
<tr style='
    border-bottom: 2px solid #deddda;
'><th style='
    text-align: center;
'>color and its closest match</th><th style='
    text-align: center;
    background: #f6f5f4;
'>dist</th></tr>
"""
    hexes_ = palette[COLORS]
    for h in hexes:
        dists = [
            dist_perceptual(hex_to_oklch(h), hex_to_oklch(h_))
            for h_ in hexes_
        ]
        d, i = min((d, i) for i, d in enumerate(dists))
        html += _hex_to_html(h)
        html += f"""
<td rowspan='2' style='
    text-align: center;
    background: #f6f5f4;
'>{d:.3f}</td></tr>"""
        html += _hex_to_html(hexes_[i], draw_border=True)
        html += "</tr>"
    html += "</table>"
    display(HTML(html))


def _hex_to_html(h, draw_border=False):
    r, g, b = to_rgb(h)
    name = hex_to_xkcd_name(h)
    L = hex_to_oklch(h)[0]
    border_style = (
        "border-bottom: 2px solid #deddda;" if draw_border else ""
    )
    return f"""
<tr style='
    background: #fff; 
    text-align: left;
    {border_style}
'>
<td style='
    font-family: monospace; 
    color: rgb({255*r}, {255*g}, {255*b}); 
'>■ {h} {100*L:.0f} {name}</td>
"""

import html
import textwrap

import numpy as np
from IPython.display import HTML, display
from matplotlib import pyplot as plt
from matplotlib.colors import XKCD_COLORS, to_rgb

from .alg import dist_perceptual, srgb_to_oklch
from .metadata import (
    ANSI,
    RAINBOW,
    TEXT_COLORS,
    ansi_names,
    catppuccin_translation,
    rainbow_names,
    semantic_mapping,
    semantic_mapping_text,
    semantics_text,
)


def hex_to_oklch(h):
    """
    OKLCH L, c, h value corresponding to sRGB hex value.
    """
    return srgb_to_oklch(*to_rgb(h))


def hex_to_xkcd_name(h, white_threshold=(0.97, 3)):
    """
    Find the name of the closest XKCD color.

    If lightness is greater than `white_threshold[0]`, chroma is less
    than `white_threshold[1]`, and the closest name is not 'white' use
    'almost white' instead of the closest name.
    """
    color = hex_to_oklch(h)
    ds = {
        name: dist_perceptual(color, hex_to_oklch(h_))
        for name, h_ in XKCD_COLORS.items()
    }
    name = min(ds, key=ds.get)[5:]
    l, c, h = color
    if (
        l > white_threshold[0]
        and c < white_threshold[1]
        and name != "white"
    ):
        name = "almost white"
    return name


def mosaic_layout(bottom_keys, top_keys=None, pad_left=True):
    """
    Return a centered two-row mosaic layout.

    Intended for use with matplotlib.pyplot.subplot_mosaic.

    If top_keys is omitted, only the bottom row is used.
    Any leftover padding is placed on the left when pad_left is True,
    otherwise on the right.
    """
    spacer = "."
    span = 2

    if top_keys is None:
        return [[k for k in bottom_keys for _ in range(span)]]

    t, b = len(top_keys), len(bottom_keys)
    if t < b:
        flipped = False
    else:
        flipped = True
        t, b = b, t
        bottom_keys, top_keys = top_keys, bottom_keys

    gaps = t - 1
    extra = b * span - t * span

    bottom_row = []
    for k in bottom_keys:
        bottom_row += [k] * span

    top_row = []
    if extra >= gaps and not (t == 2 and extra == 2):
        for k in top_keys:
            top_row += [k] * span
            top_row.append(spacer)
        top_row = top_row[:-1]
        remaining = extra - gaps
    else:
        for k in top_keys:
            top_row += [k] * span
        remaining = extra

    left = remaining // 2
    right = remaining - left
    if pad_left and left < right:
        left, right = right, left
    top_row = [spacer] * left + top_row + [spacer] * right

    if flipped:
        return [bottom_row, top_row]
    else:
        return [top_row, bottom_row]


def hexes(hexes, top_hexes=None, labels=None, colored_labels=True):
    """
    Plot hex color values as a table with one or two rows.

    If no labels are provided, XKCD color names as used.

    Setting colored_labels to False prints labels in black instead of
    their corresponding color.
    """
    scaling = 0.6  # Ratio of size of squares vs size of text
    ws_aspect = 0.9  # Ratio of whitespace between cols vs rows
    padding = 0.15  # Padding of labels

    n = len(hexes)
    keys_bottom = set(range(n))
    if top_hexes is not None:
        keys_top = set(range(n, n + len(top_hexes)))
        hexes = list(hexes) + list(top_hexes)
    else:
        keys_top = None

    if labels is None:
        labels = [hex_to_xkcd_name(h) for h in hexes]

    layout = mosaic_layout(keys_bottom, keys_top)
    nrows = len(layout)
    ncols = len(layout[0])

    fig, axs = plt.subplot_mosaic(layout)
    fig.set_size_inches(
        scaling * ncols, 2 * ws_aspect * scaling * nrows
    )
    for i in range(len(hexes)):
        ax = axs[i]
        h = hexes[i]
        label = labels[i]
        c = h if colored_labels else "black"
        ax.imshow(np.dstack(to_rgb(h)))
        if i in keys_bottom:
            ax.text(
                0.5,
                -padding,
                label,
                color=c,
                transform=ax.transAxes,
                rotation=-45,
                ha="left",
                va="top",
                clip_on=False,
                rotation_mode="anchor",
            )
        else:
            ax.text(
                0.5,
                1 + padding,
                label,
                color=c,
                transform=ax.transAxes,
                rotation=45,
                ha="left",
                va="bottom",
                clip_on=False,
                rotation_mode="anchor",
            )
        ax.axis("off")


def indices(
    palette,
    ixs,
    show_xkcd_names=False,
    colored_labels=False,
    title=None,
):
    sm_inv = {v: k for k, v in semantic_mapping.items()}
    labels = []
    for i in ixs:
        label = sm_inv[i]
        if show_xkcd_names:
            label += " (" + hex_to_xkcd_name(palette[i]) + ")"
        labels.append(label)
    hexes(palette[ixs], labels=labels, colored_labels=colored_labels)
    if title is not None:
        plt.gcf().text(
            0.13, 1.2, title, ha="left", va="top", fontsize=12
        )


def palette(palette, show_ansi_name=True, show_rainbow_name=True):
    """
    Display palette as a HTML table.
    """
    html = "<table>"
    ansi_inv = {v: i for i, v in enumerate(ANSI)}
    rainbow_inv = {v: i for i, v in enumerate(RAINBOW)}
    for key, ix in semantic_mapping_text.items():
        desc = semantics_text[key]
        if key in catppuccin_translation.values():
            desc = "🐱" + desc
        if ix in RAINBOW:
            rix = rainbow_inv[ix]
            if show_rainbow_name:
                desc = f"({rainbow_names[rix]}) " + desc
            desc = f"🌈{rix} " + desc
        if ix in ansi_inv:
            aix = ansi_inv[ix]
            if show_ansi_name:
                desc = f"({ansi_names[aix]}) " + desc
            desc = f"#️⃣{aix} " + desc
        h = palette[ix]
        html += f"""
<tr style='
    background: #fff; 
    font-family: 
    monospace; 
    color: {h};
'>
<td style='text-align: left !important;'>■&nbsp;{key}</td>
<td style='
    text-align: left !important; 
    white-space: pre;
'>{hex_to_str(h)}</td>
<td style='text-align: left !important;'>{desc}</td>
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
    text-align: center !important;
'>color and its closest match</th><th style='
    text-align: center !important;
    background: #f6f5f4;
'>dist</th></tr>
"""
    hexes_ = palette[TEXT_COLORS]
    for h in hexes:
        dists = [
            dist_perceptual(hex_to_oklch(h), hex_to_oklch(h_))
            for h_ in hexes_
        ]
        d, i = min((d, i) for i, d in enumerate(dists))
        html += _hex_to_html(h)
        html += f"""
<td rowspan='2' style='
    text-align: center !important;
    background: #f6f5f4;
'>{d:.3f}</td></tr>"""
        html += _hex_to_html(hexes_[i], draw_border=True)
        html += "</tr>"
    html += "</table>"
    display(HTML(html))


def hex_to_str(h):
    """
    Return hex as string.

    String consists of hex value, lightness, chroma and XKCD name.
    """
    L, chroma, hue = hex_to_oklch(h)
    name = hex_to_xkcd_name(h)
    return f"{h} {100*L:3.0f} {chroma:3.0f} {hue:3.0f}  {name}"


def _hex_to_html(h, draw_border=False):
    border_style = (
        "border-bottom: 2px solid #deddda;" if draw_border else ""
    )
    return f"""
<tr style='
    background: #fff; 
    {border_style}
'>
<td style='
    font-family: monospace; 
    text-align: left !important;
    white-space: pre;
    color: {h};
'>■ {hex_to_str(h)}</td>
"""


def hex(h):
    """
    Render hex as HTML.
    """
    display(HTML("<table>" + _hex_to_html(h) + "</table>"))


def cycle_colors(text, colors):
    """
    Render as HTML where consecutive characters have different colors.

    Cycles through colors given as hex values.
    """
    spans = []
    for i, ch in enumerate(text):
        color = colors[np.mod(i, len(colors))]
        spans.append(f"<span style='color:{color}'>{ch}</span>")
    display(
        HTML(
            "<div style='font-family: monospace;'>"
            + "".join(spans)
            + "</div>"
        )
    )

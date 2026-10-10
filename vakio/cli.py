import argparse
import json
import re

from vakio import (
    create_palette,
    with_ansi_keys,
    with_catppuccin_keys,
    with_rainbow_keys,
    with_semantic_keys,
)

_KEYS_FUNCS = {
    "semantic": with_semantic_keys,
    "ansi": with_ansi_keys,
    "rainbow": with_rainbow_keys,
    "catppuccin": with_catppuccin_keys,
}

_M4PREFIX_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$|^$")


def main(argv: list[str] | None = None) -> int:
    argparser = argparse.ArgumentParser(description="Print palette.")
    argparser.add_argument(
        "--keys",
        action="append",
        choices=_KEYS_FUNCS.keys(),
        help="key sets to include, repeatable.",
    )
    argparser.add_argument(
        "--to",
        choices=["m4", "json"],
        help=(
            "output format (default: m4, unless only "
            "--keys=catppuccin is given)."
        ),
    )
    argparser.add_argument(
        "--m4prefix",
        default="vakio_",
        help="prefix for m4 macros (default: vakio_).",
    )
    args = argparser.parse_args(argv)
    if not _M4PREFIX_RE.match(args.m4prefix):
        argparser.error(
            "--m4prefix must be empty of alphanumeric with '_' "
            "allowed, and must not start with a number."
        )

    if args.keys:
        selected_keys = args.keys
    else:
        selected_keys = ["semantic", "ansi", "rainbow"]

    if args.to is not None:
        out_format = args.to
    else:
        out_format = (
            "json" if selected_keys == ["catppuccin"] else "m4"
        )

    palette = create_palette()
    colormap = {}
    for key in selected_keys:
        colormap |= _KEYS_FUNCS[key](palette)

    if out_format == "json":
        print_json(colormap)
    else:
        print_m4(colormap, args.m4prefix)
    return 0


def print_m4(colormap, prefix):
    out = "m4_divert(-1)\n"
    for k, v in colormap.items():
        out += f"m4_define(`{prefix}{k}', `{v}')\n"
    out += "m4_divert(0)m4_dnl"
    print(out)


def print_json(colormap):
    print(json.dumps(colormap))


if __name__ == "__main__":
    raise SystemExit(main())

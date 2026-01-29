BLACK = 0
DARK_GREYS = list(range(BLACK + 1, BLACK + 4))
GREY = DARK_GREYS[-1]
SUBTLE_GREY = GREY + 1
BRIGHT_GREYS = list(range(SUBTLE_GREY, SUBTLE_GREY + 5))
CRUST = BRIGHT_GREYS[-1] + 1
MANTLE = CRUST + 1
WHITE = MANTLE + 1

DARK_COLORS = list(range(WHITE + 1, WHITE + 6))
BRIGHT_COLORS = list(range(DARK_COLORS[-1] + 1, DARK_COLORS[-1] + 7))
MANUAL_COLORS = list(
    range(BRIGHT_COLORS[-1] + 1, BRIGHT_COLORS[-1] + 3)
)

GREYS = list(range(BLACK, WHITE + 1))
MANUAL_GREYS = [BLACK, CRUST, MANTLE, WHITE]
COLORS = DARK_COLORS + BRIGHT_COLORS + MANUAL_COLORS
SEMANTIC = [BLACK, GREY, SUBTLE_GREY] + COLORS

semantic_mapping_colors = {
    "text": BLACK,
    "params": DARK_COLORS[0],
    "functions": DARK_COLORS[2],
    "operators": BRIGHT_COLORS[2],
    "keywords": DARK_COLORS[3],
    "classes": DARK_COLORS[4],
    "subtle": SUBTLE_GREY,
    "comments": GREY,
    "strings": BRIGHT_COLORS[0],
    "escapes": BRIGHT_COLORS[1],
    "constants": BRIGHT_COLORS[3],
    "errors": BRIGHT_COLORS[5],
    "cursor": MANUAL_COLORS[0],
    "extra": MANUAL_COLORS[1],
    "dark": DARK_COLORS[1],
}

semantic_mapping_greys = {
    "base": WHITE,
    "mantle": MANTLE,
    "crust": CRUST,
    "surface0": BRIGHT_GREYS[4],
    "surface1": BRIGHT_GREYS[3],
    "surface2": BRIGHT_GREYS[2],
    "overlay0": BRIGHT_GREYS[1],
    "subtext0": DARK_GREYS[1],
    "subtext1": DARK_GREYS[0],
}

semantic_mapping = semantic_mapping_colors | semantic_mapping_greys

semantics_color = {
    "text": "Text",
    "functions": (
        "Methods, Functions, Properties, " "Links, URLs, Tags"
    ),
    "classes": (
        "Warnings, Classes, Interfaces, "
        "Annotations, Metadata, "
        "Enums, Types, Attributes"
    ),
    "params": "Parameters",
    "keywords": "Keywords, Followed Links, Active Line Number",
    "constants": "Constants, Numbers, Warnings",
    "operators": "Operators, Enum Variants, On Hover Links",
    "errors": "Errors, Symbols, Atoms, Builtins",
    "subtle": "Subtle, Line Numbers",
    "comments": "Comments, Braces, Delimiters",
    "strings": "Success, Strings",
    "escapes": "Escape Sequences, Regex",
    "cursor": "Cursor",
    "dark": "N/A (LaTeX Math Mode)",
    "extra": "N/A (Rainbow Highlights)",
}

semantics_grey = {
    "base": "Background Pane",
    "mantle": "Secondary Panes",
    "crust": "Secondary Panes",
    "surface0": "Surface Elements",
    "surface1": "Surface Elements",
    "surface2": "Surface Elements",
    "overlay0": "Overlays",
    "subtext0": "Sub-Headlines, Labels",
    "subtext1": "Sub-Headlines, Labels",
}

catppuccin_translation = {
    "mauve": "keywords",
    "green": "strings",
    "red": "errors",
    "pink": "escapes",
    "overlay2": "comments",
    "peach": "constants",
    "blue": "functions",
    "maroon": "params",
    "yellow": "classes",
    "teal": "operators",
    "rosewater": "cursor",
    "overlay1": "subtle",
    "sky": "operators",
    "lavender": "keywords",
    "flamingo": "dark",
    "sapphire": "extra",
    "text": "text",
    "base": "base",
    "mantle": "mantle",
    "crust": "crust",
    "surface0": "surface0",
    "surface1": "surface1",
    "surface2": "surface2",
    "overlay0": "overlay0",
    "subtext0": "subtext0",
    "subtext1": "subtext1",
}

github_base24 = {
    "base00": "#eaeef2",
    "base01": "#d0d7de",
    "base02": "#afb8c1",
    "base03": "#8c959f",
    "base04": "#6e7781",
    "base05": "#424a53",
    "base06": "#32383f",
    "base07": "#1f2328",
    "base08": "#fa4549",
    "base09": "#e16f24",
    "base0A": "#bf8700",
    "base0B": "#2da44e",
    "base0C": "#339D9B",
    "base0D": "#218bff",
    "base0E": "#a475f9",
    "base0F": "#4d2d00",
    "base10": "#1f2328",
    "base11": "#000000",
    "base12": "#ff8182",
    "base13": "#d4a72c",
    "base14": "#4ac26b",
    "base15": "#49BCB7",
    "base16": "#54aeff",
    "base17": "#c297ff",
}

base24_dark_colors = {
    "base08",
    "base09",
    "base0A",
    "base0B",
    "base0C",
    "base0D",
    "base0E",
    "base0F",
}

base24_bright_colors = {
    "base12",
    "base13",
    "base14",
    "base15",
    "base16",
    "base17",
}

base24_grayscale = {
    "base00",
    "base01",
    "base02",
    "base03",
    "base04",
    "base05",
    "base06",
    "base07",
    "base10",
    "base11",
}

BLACK = 0
ALMOST_BLACK = 1
DARK_GREY = 2
BRIGHT_GREY = 3
SUBTLE_GREY = 4
UI_LIGHT_GREYS = list(range(SUBTLE_GREY + 1, SUBTLE_GREY + 5))
CRUST = UI_LIGHT_GREYS[-1] + 1
MANTLE = CRUST + 1
WHITE = MANTLE + 1

DARK_COLORS = list(range(WHITE + 1, WHITE + 6))
BRIGHT_COLORS = list(range(DARK_COLORS[-1] + 1, DARK_COLORS[-1] + 7))
MANUAL_COLORS = list(
    range(BRIGHT_COLORS[-1] + 1, BRIGHT_COLORS[-1] + 4)
)
TEXT_COLORS = DARK_COLORS + BRIGHT_COLORS + MANUAL_COLORS

GREYS = list(range(BLACK, WHITE + 1))
MANUAL_GREYS = [BLACK, CRUST, MANTLE, WHITE]
UI_GREYS = [ALMOST_BLACK] + UI_LIGHT_GREYS + MANUAL_GREYS[1:]
TEXT_GREYS = [BLACK, DARK_GREY, BRIGHT_GREY, SUBTLE_GREY]

TEXT = TEXT_GREYS + TEXT_COLORS


ANSI = [
    BLACK,
    DARK_COLORS[4],
    BRIGHT_COLORS[0],
    MANUAL_COLORS[0],
    DARK_COLORS[2],
    DARK_COLORS[3],
    DARK_COLORS[1],
    SUBTLE_GREY,
    BRIGHT_GREY,
    BRIGHT_COLORS[5],
    MANUAL_COLORS[2],
    MANUAL_COLORS[1],
    BRIGHT_COLORS[2],
    BRIGHT_COLORS[4],
    BRIGHT_COLORS[1],
    WHITE,
]
ansi_names = [
    "Black",
    "Red",
    "Green",
    "Yellow",
    "Blue",
    "Magenta",
    "Cyan",
    "White",
    "Bright Black",
    "Bright Red",
    "Bright Green",
    "Bright Yellow",
    "Bright Blue",
    "Bright Magenta",
    "Bright Cyan",
    "Bright White",
]


RAINBOW = [
    BRIGHT_COLORS[5],
    MANUAL_COLORS[0],
    MANUAL_COLORS[1],
    MANUAL_COLORS[2],
    BRIGHT_COLORS[2],
    BRIGHT_COLORS[3],
]
rainbow_names = [
    "Red",
    "Orange",
    "Yellow",
    "Green",
    "Blue",
    "Violet",
]


semantic_mapping_text = {
    "text": BLACK,
    "labels": DARK_GREY,
    "params": DARK_COLORS[0],
    "functions": DARK_COLORS[2],
    "operators": BRIGHT_COLORS[2],
    "keywords": DARK_COLORS[3],
    "classes": DARK_COLORS[4],
    "subtle": SUBTLE_GREY,
    "comments": BRIGHT_GREY,
    "strings": BRIGHT_COLORS[0],
    "escapes": BRIGHT_COLORS[1],
    "constants": BRIGHT_COLORS[3],
    "cursor": BRIGHT_COLORS[4],
    "errors": BRIGHT_COLORS[5],
    "rainbow1": MANUAL_COLORS[0],
    "rainbow2": MANUAL_COLORS[1],
    "rainbow3": MANUAL_COLORS[2],
    "ansi6": DARK_COLORS[1],
}

semantic_mapping_ui = {
    "base": WHITE,
    "mantle": MANTLE,
    "crust": CRUST,
    "surface0": UI_LIGHT_GREYS[3],
    "surface1": UI_LIGHT_GREYS[2],
    "surface2": UI_LIGHT_GREYS[1],
    "overlay0": UI_LIGHT_GREYS[0],
    "subtext1": ALMOST_BLACK,
}

semantic_mapping = semantic_mapping_text | semantic_mapping_ui


semantics_text = {
    "text": "Text",
    "labels": "Sub-Headlines, Labels",
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
    "rainbow1": "",
    "rainbow2": "",
    "rainbow3": "",
    "ansi6": "",
}

semantics_ui = {
    "base": "Background Pane",
    "mantle": "Secondary Panes",
    "crust": "Secondary Panes",
    "surface0": "Surface Elements",
    "surface1": "Surface Elements",
    "surface2": "Surface Elements",
    "overlay0": "Overlays",
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
    "flamingo": "ansi6",
    "sapphire": "rainbow1",
    "text": "text",
    "base": "base",
    "mantle": "mantle",
    "crust": "crust",
    "surface0": "surface0",
    "surface1": "surface1",
    "surface2": "surface2",
    "overlay0": "overlay0",
    "subtext0": "labels",
    "subtext1": "subtext1",
}

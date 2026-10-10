from . import metadata
from .palette import create_palette

__all__ = [
    "create_palette",
    "metadata",
    "with_semantic_keys",
    "with_catppuccin_keys",
]


def with_semantic_keys(palette):
    """
    Index the palette using semantic keys.
    """
    return {
        k: str(palette[v])
        for k, v in metadata.semantic_mapping.items()
    }


def with_ansi_keys(palette):
    """
    Index the ANSI colors with keys ansiX, where X=0,1,...,15.
    """
    return {
        f"ansi{i}": str(palette[ix])
        for i, ix in enumerate(metadata.ANSI)
    }


def with_rainbow_keys(palette):
    """
    Index the colors of rainbow with keys rainbowX, where X=0,1,...,5.
    """
    return {
        f"rainbow{i}": str(palette[ix])
        for i, ix in enumerate(metadata.RAINBOW)
    }


def with_catppuccin_keys(palette):
    """
    Index the palette using Catppuccin keys.
    """
    return {
        k: str(palette[metadata.semantic_mapping[v]])
        for k, v in metadata.catppuccin_translation.items()
    }

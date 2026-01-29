from .metadata import *
from .palette import create_palette


def with_semantic_keys(palette):
    """
    Index the palette using semantic keys.
    """
    return {k: str(palette[v]) for k, v in semantic_mapping.items()}


def with_catppuccin_keys(palette):
    """
    Index the palette using Catppuccin keys.
    """
    return {
        k: str(palette[semantic_mapping[v]])
        for k, v in catppuccin_translation.items()
    }

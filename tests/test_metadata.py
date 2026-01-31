from vakio import metadata
from vakio.palette import create_palette
from vakio.view import hex_to_oklch


def assert_grey_order(greys):
    def lightness(h):
        return hex_to_oklch(h)[0]

    assert [str(h) for h in greys] == sorted(greys, key=lightness)


def test_grey_order():
    palette = create_palette()
    assert_grey_order(palette[metadata.GREYS])
    assert_grey_order(palette[metadata.UI_LIGHT_GREYS])
    assert_grey_order(palette[metadata.MANUAL_GREYS])
    assert_grey_order(palette[metadata.UI_GREYS])
    assert_grey_order(palette[metadata.TEXT_GREYS])


def test_grey_text_ui_disjoint():
    assert set(metadata.UI_GREYS).isdisjoint(set(metadata.TEXT_GREYS))


def test_grey_text_ui_union():
    assert set(metadata.UI_GREYS) | set(metadata.TEXT_GREYS) == set(
        metadata.GREYS
    )


def test_semantic_mapping_injective():
    inverse = {v: k for k, v in metadata.semantic_mapping.items()}
    assert len(inverse) == len(metadata.semantic_mapping)

from vakio.view import mosaic_layout


def test_mosaic_layout():
    top = [10, 11, 12, 13, 14]
    bottom = [1, 2, 3, 4, 5, 6, 7]
    assert mosaic_layout(bottom, top) == [
        [10, 10, ".", 11, 11, ".", 12, 12, ".", 13, 13, ".", 14, 14],
        [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7],
    ]

    top = [10, 11, 12, 13, 14]
    bottom = [1, 2, 3, 4, 5]
    assert mosaic_layout(bottom, top) == [
        [10, 10, 11, 11, 12, 12, 13, 13, 14, 14],
        [1, 1, 2, 2, 3, 3, 4, 4, 5, 5],
    ]

    top = [10]
    bottom = [1, 2]
    assert mosaic_layout(bottom, top) == [
        [".", 10, 10, "."],
        [1, 1, 2, 2],
    ]

    top = [10]
    bottom = [1, 2, 3]
    assert mosaic_layout(bottom, top) == [
        [".", ".", 10, 10, ".", "."],
        [1, 1, 2, 2, 3, 3],
    ]

    top = [10, 11]
    bottom = [1, 2, 3]
    assert mosaic_layout(bottom, top) == [
        [".", 10, 10, 11, 11, "."],
        [1, 1, 2, 2, 3, 3],
    ]

    top = [10, 11, 12, 13]
    bottom = [1, 2, 3, 4, 5, 6]
    assert mosaic_layout(bottom, top) == [
        [".", 10, 10, ".", 11, 11, ".", 12, 12, ".", 13, 13],
        [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6],
    ]

    top = [10, 11, 12, 13]
    bottom = [1, 2, 3, 4, 5, 6]
    assert mosaic_layout(bottom, top, pad_left=False) == [
        [10, 10, ".", 11, 11, ".", 12, 12, ".", 13, 13, "."],
        [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6],
    ]

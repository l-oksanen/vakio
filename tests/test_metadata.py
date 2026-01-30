from vakio import metadata


def test_semantic_mapping_injective():
    inverse = {v: k for k, v in metadata.semantic_mapping.items()}
    assert len(inverse) == len(metadata.semantic_mapping)

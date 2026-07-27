def test_import():
    import confostate

    assert confostate.__version__


def test_version_string():
    import confostate

    assert isinstance(confostate.__version__, str)
    assert len(confostate.__version__.split(".")) >= 2


def test_load_annotations_export():
    from confostate import load_annotations

    assert callable(load_annotations)

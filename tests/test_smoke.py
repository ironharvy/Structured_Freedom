"""Smoke test to verify the project is importable."""

import importlib


def test_package_importable():
    mod = importlib.import_module("structured_freedom")
    assert mod is not None

"""Pierwsze testy – sprawdzenie, czy pytest działa w projekcie."""
import pytest


def add(a, b):
    return a + b


def test_add_integers():
    assert add(2, 3) == 5


def test_add_floats():
    assert add(0.1, 0.2) == pytest.approx(0.3)

"""Testy czarnoskrzynkowe: validate_password (HS-1 ... HS-4)."""
import pytest

from sut import validate_password


def password_of_length(n):
    """Hasło z liter i cyfr o długości n, np. 5 -> 'a1a1a'."""
    return ("a1" * n)[:n]


def test_example_valid_password():
    assert validate_password("haslo123") is True


@pytest.mark.parametrize("password", [
    pytest.param(None, id="none"),
    pytest.param(12345678, id="int"),
    pytest.param(["haslo123"], id="list"),
])
def test_example_wrong_type(password):
    with pytest.raises(TypeError):
        validate_password(password)


@pytest.mark.parametrize("password", [
    pytest.param("abc12345", id="letters-and-digits"),
    pytest.param(
        "abc123#!",
        id="special-characters",
        marks=pytest.mark.xfail(reason="DEF-04", strict=True),
    ),
    pytest.param(
        "abc 1234",
        id="space",
        marks=pytest.mark.xfail(reason="DEF-04", strict=True),
    ),
    pytest.param("żółć1234", id="polish-letters"),
    pytest.param("Zażółć12345678901234", id="polish-20-characters"),
])
def test_ep_valid(password):
    assert validate_password(password) is True


@pytest.mark.parametrize("password", [
    pytest.param("12345678", id="no-letter"),
    pytest.param("abcdefgh", id="no-digit"),
    pytest.param("a1a1a1a", id="too-short"),
    pytest.param("a1a1a1a1a1a1a1a1a1a1a", id="too-long"),
])
def test_ep_invalid(password):
    assert validate_password(password) is False


@pytest.mark.parametrize("length, expected", [
    pytest.param(7, False, id="below-min"),
    pytest.param(8, True, id="min"),
    pytest.param(20, True, id="max"),
    pytest.param(21, False, id="above-max"),
])
def test_bva_length_2p(length, expected):
    assert validate_password(password_of_length(length)) is expected


@pytest.mark.parametrize("length, expected", [
    pytest.param(6, False, id="below-min-extra"),
    pytest.param(9, True, id="min-inside"),
    pytest.param(19, True, id="max-inside"),
    pytest.param(22, False, id="above-max-extra"),
])
def test_bva_length_3p_extra(length, expected):
    assert validate_password(password_of_length(length)) is expected


@pytest.mark.parametrize("password, expected", [
    pytest.param("a1aaaaaa", True, id="letter-and-digit"),
    pytest.param("abcdefgh", False, id="no-digit"),
    pytest.param("12345678", False, id="no-letter"),
])
def test_each_choice_minimal(password, expected):
    """Each Choice: obecność i brak litery oraz cyfry przy poprawnej długości."""
    assert validate_password(password) is expected

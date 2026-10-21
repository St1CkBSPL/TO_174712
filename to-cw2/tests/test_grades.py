"""Testy czarnoskrzynkowe: grade_from_percent (OC-1 ... OC-4)."""
import pytest

from sut import grade_from_percent


@pytest.mark.parametrize("percent, grade", [
    pytest.param(25, 2.0, id="fail"),
    pytest.param(55, 3.0, id="satisfactory"),
    pytest.param(65, 3.5, id="satisfactory-plus"),
    pytest.param(75, 4.0, id="good"),
    pytest.param(85, 4.5, id="good-plus"),
    pytest.param(95, 5.0, id="very-good"),
])
def test_ep_valid_classes(percent, grade):
    assert grade_from_percent(percent) == grade


@pytest.mark.parametrize("percent", [
    pytest.param(-10, id="negative"),
    pytest.param(110, id="over-100"),
])
def test_ep_out_of_range(percent):
    with pytest.raises(ValueError):
        grade_from_percent(percent)


@pytest.mark.parametrize("percent", [
    pytest.param(
        50.0,
        id="float",
        marks=pytest.mark.xfail(reason="DEF-01", strict=True),
    ),
    pytest.param(
        "50",
        id="string",
        marks=pytest.mark.xfail(reason="DEF-01", strict=True),
    ),
    pytest.param(None, id="none"),
    pytest.param(
        True,
        id="bool",
        marks=pytest.mark.xfail(reason="DEF-01", strict=True),
    ),
])
def test_ep_wrong_type(percent):
    with pytest.raises(TypeError):
        grade_from_percent(percent)


@pytest.mark.parametrize("percent, grade", [
    pytest.param(0, 2.0, id="min"),
    pytest.param(50, 2.0, id="fail-upper"),
    pytest.param(51, 3.0, id="satisfactory-lower"),
    pytest.param(60, 3.0, id="satisfactory-upper"),
    pytest.param(61, 3.5, id="satisfactory-plus-lower"),
    pytest.param(70, 3.5, id="satisfactory-plus-upper"),
    pytest.param(71, 4.0, id="good-lower"),
    pytest.param(80, 4.0, id="good-upper"),
    pytest.param(81, 4.5, id="good-plus-lower"),
    pytest.param(
        90,
        4.5,
        id="good-plus-upper",
        marks=pytest.mark.xfail(reason="DEF-02", strict=True),
    ),
    pytest.param(91, 5.0, id="very-good-lower"),
    pytest.param(100, 5.0, id="max"),
])
def test_bva_2p(percent, grade):
    assert grade_from_percent(percent) == grade


@pytest.mark.parametrize("percent", [
    pytest.param(-1, id="below-min"),
    pytest.param(101, id="above-max"),
])
def test_bva_2p_out_of_domain(percent):
    with pytest.raises(ValueError):
        grade_from_percent(percent)


@pytest.mark.parametrize("percent, grade", [
    pytest.param(1, 2.0, id="min-inside"),
    pytest.param(49, 2.0, id="fail-upper-inside"),
    pytest.param(52, 3.0, id="satisfactory-lower-inside"),
    pytest.param(59, 3.0, id="satisfactory-upper-inside"),
    pytest.param(62, 3.5, id="satisfactory-plus-lower-inside"),
    pytest.param(69, 3.5, id="satisfactory-plus-upper-inside"),
    pytest.param(72, 4.0, id="good-lower-inside"),
    pytest.param(79, 4.0, id="good-upper-inside"),
    pytest.param(82, 4.5, id="good-plus-lower-inside"),
    pytest.param(89, 4.5, id="good-plus-upper-inside"),
    pytest.param(92, 5.0, id="very-good-lower-inside"),
    pytest.param(99, 5.0, id="max-inside"),
])
def test_bva_3p_extra(percent, grade):
    assert grade_from_percent(percent) == grade

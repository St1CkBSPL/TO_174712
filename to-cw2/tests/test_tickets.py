"""Testy czarnoskrzynkowe: ticket_price (BL-1 ... BL-4)."""
import pytest

from sut import ticket_price


@pytest.mark.parametrize("age, price", [
    pytest.param(3, 0.0, id="free"),
    pytest.param(12, 10.0, id="child-discount"),
    pytest.param(40, 20.0, id="normal"),
    pytest.param(70, 10.0, id="senior-discount"),
])
def test_ep_valid_classes(age, price):
    assert ticket_price(age) == price


@pytest.mark.parametrize("age", [
    pytest.param(-10, id="negative"),
    pytest.param(130, id="over-120"),
])
def test_ep_out_of_range(age):
    with pytest.raises(ValueError):
        ticket_price(age)


@pytest.mark.parametrize("age", [
    pytest.param(18.0, id="float"),
    pytest.param("18", id="string"),
    pytest.param(None, id="none"),
    pytest.param(True, id="bool"),
])
def test_ep_wrong_type(age):
    with pytest.raises(TypeError):
        ticket_price(age)


@pytest.mark.parametrize("age, price", [
    pytest.param(0, 0.0, id="min"),
    pytest.param(6, 0.0, id="free-upper"),
    pytest.param(7, 10.0, id="child-lower"),
    pytest.param(18, 10.0, id="child-upper"),
    pytest.param(19, 20.0, id="normal-lower"),
    pytest.param(64, 20.0, id="normal-upper"),
    pytest.param(65, 10.0, id="senior-lower"),
    pytest.param(
        120,
        10.0,
        id="max",
        marks=pytest.mark.xfail(reason="DEF-05", strict=True),
    ),
])
def test_bva_2p(age, price):
    assert ticket_price(age) == price


@pytest.mark.parametrize("age", [
    pytest.param(-1, id="below-min"),
    pytest.param(121, id="above-max"),
])
def test_bva_2p_out_of_domain(age):
    with pytest.raises(ValueError):
        ticket_price(age)


@pytest.mark.parametrize("age, price", [
    pytest.param(1, 0.0, id="min-inside"),
    pytest.param(5, 0.0, id="free-upper-inside"),
    pytest.param(8, 10.0, id="child-lower-inside"),
    pytest.param(17, 10.0, id="child-upper-inside"),
    pytest.param(20, 20.0, id="normal-lower-inside"),
    pytest.param(63, 20.0, id="normal-upper-inside"),
    pytest.param(66, 10.0, id="senior-lower-inside"),
    pytest.param(
        119,
        10.0,
        id="max-inside",
        marks=pytest.mark.xfail(reason="DEF-05", strict=True),
    ),
])
def test_bva_3p_extra(age, price):
    assert ticket_price(age) == price

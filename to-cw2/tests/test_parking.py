"""Testy czarnoskrzynkowe: parking_fee (PK-1 ... PK-5)."""
import pytest

from sut import parking_fee


@pytest.mark.parametrize("minutes, fee", [
    pytest.param(10, 0.0, id="free"),
    pytest.param(30, 5.0, id="one-hour"),
    pytest.param(90, 10.0, id="two-hours"),
    pytest.param(150, 15.0, id="three-hours"),
    pytest.param(600, 20.0, id="daily"),
])
def test_ep_valid_classes(minutes, fee):
    assert parking_fee(minutes) == fee


@pytest.mark.parametrize("minutes", [
    pytest.param(-10, id="negative"),
    pytest.param(1500, id="over-one-day"),
])
def test_ep_out_of_range(minutes):
    with pytest.raises(ValueError):
        parking_fee(minutes)


@pytest.mark.parametrize("minutes", [
    pytest.param(60.0, id="float"),
    pytest.param("60", id="string"),
    pytest.param(None, id="none"),
    pytest.param(True, id="bool"),
])
def test_ep_wrong_type(minutes):
    with pytest.raises(TypeError):
        parking_fee(minutes)


@pytest.mark.parametrize("minutes, fee", [
    pytest.param(0, 0.0, id="min"),
    pytest.param(15, 0.0, id="free-upper"),
    pytest.param(16, 5.0, id="one-hour-lower"),
    pytest.param(60, 5.0, id="one-hour-upper"),
    pytest.param(61, 10.0, id="two-hours-lower"),
    pytest.param(120, 10.0, id="two-hours-upper"),
    pytest.param(121, 15.0, id="three-hours-lower"),
    pytest.param(180, 15.0, id="three-hours-upper"),
    pytest.param(181, 20.0, id="daily-lower"),
    pytest.param(1440, 20.0, id="max"),
])
def test_bva_2p(minutes, fee):
    assert parking_fee(minutes) == fee


@pytest.mark.parametrize("minutes", [
    pytest.param(-1, id="below-min"),
    pytest.param(1441, id="above-max"),
])
def test_bva_2p_out_of_domain(minutes):
    with pytest.raises(ValueError):
        parking_fee(minutes)


@pytest.mark.parametrize("minutes, fee", [
    pytest.param(
        1,
        0.0,
        id="min-inside",
        marks=pytest.mark.xfail(reason="DEF-03", strict=True),
    ),
    pytest.param(14, 0.0, id="free-upper-inside"),
    pytest.param(17, 5.0, id="one-hour-lower-inside"),
    pytest.param(59, 5.0, id="one-hour-upper-inside"),
    pytest.param(62, 10.0, id="two-hours-lower-inside"),
    pytest.param(119, 10.0, id="two-hours-upper-inside"),
    pytest.param(122, 15.0, id="three-hours-lower-inside"),
    pytest.param(179, 15.0, id="three-hours-upper-inside"),
    pytest.param(182, 20.0, id="daily-lower-inside"),
    pytest.param(1439, 20.0, id="max-inside"),
])
def test_bva_3p_extra(minutes, fee):
    assert parking_fee(minutes) == fee

import pytest

from seat_reservation_system.cli import _parse_seat_numbers
from seat_reservation_system.seat_store import SeatStore


def test_reserve_many_with_range():
    store = SeatStore([1, 2, 3, 4, 5])
    store.reserve_many(_parse_seat_numbers("1-3,5"), "Alex")

    assert store.status(1) == (1, "Alex")
    assert store.status(3) == (3, "Alex")
    assert store.status(5) == (5, "Alex")
    assert store.status(4) == (4, None)


def test_reserve_many_keeps_seats_when_one_is_already_reserved():
    store = SeatStore([1, 2, 3])
    store.reserve(2, "Mina")

    with pytest.raises(ValueError, match="already reserved"):
        store.reserve_many([1, 2, 3], "Alex")

    assert store.status(1) == (1, None)
    assert store.status(2) == (2, "Mina")
    assert store.status(3) == (3, None)

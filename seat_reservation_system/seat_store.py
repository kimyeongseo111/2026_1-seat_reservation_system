class SeatStore:
    def __init__(self, seat_ids):
        self._seats = {seat_id: None for seat_id in seat_ids}

    def list_seats(self):
        return self._seats.items()

    def reserve(self, seat_id, name):
        self._require_name(name)
        current = self._get(seat_id)
        if current is not None:
            raise ValueError("Seat is already reserved.")
        self._seats[seat_id] = name
        return seat_id, name

    def cancel(self, seat_id, name=None):
        current = self._get(seat_id)
        if current is None:
            raise ValueError("Seat is not reserved.")
        if name is not None and current != name:
            raise ValueError("Name does not match the reservation.")
        self._seats[seat_id] = None
        return seat_id, None

    def status(self, seat_id):
        return seat_id, self._get(seat_id)

    def stats(self):
        reserved = sum(1 for name in self._seats.values() if name)
        total = len(self._seats)
        return {"total": total, "reserved": reserved, "available": total - reserved}

    def reserve_many(self, seat_numbers, name):
        self._require_name(name)
        seats = self._validate_seat_numbers(seat_numbers)
        # 먼저 모든 좌석이 예약 가능한지 확인한 뒤 한 번에 변경합니다.
        for seat_id in seats:
            if self._seats[seat_id] is not None:
                raise ValueError("Seat is already reserved.")
        for seat_id in seats:
            self._seats[seat_id] = name
        return [(seat_id, name) for seat_id in seats]

    def cancel_many(self, seat_numbers, name=None):
        seats = self._validate_seat_numbers(seat_numbers)
        # 취소도 먼저 전체 조건을 확인해서 일부 좌석만 바뀌지 않게 합니다.
        for seat_id in seats:
            current = self._seats[seat_id]
            if current is None:
                raise ValueError("Seat is not reserved.")
            if name is not None and current != name:
                raise ValueError("Name does not match the reservation.")
        for seat_id in seats:
            self._seats[seat_id] = None
        return [(seat_id, None) for seat_id in seats]

    def _validate_seat_numbers(self, seat_numbers):
        seats = list(seat_numbers)
        if not seats:
            raise ValueError("No seats specified.")
        if len(set(seats)) != len(seats):
            raise ValueError("Duplicate seat numbers are not allowed.")
        for seat_id in seats:
            if seat_id not in self._seats:
                raise ValueError("Seat does not exist.")
        return seats

    def _require_name(self, name):
        if name is None or not name.strip():
            raise ValueError("Reservation name is required.")

    def _get(self, seat_id):
        if seat_id not in self._seats:
            raise ValueError("Seat does not exist.")
        return self._seats[seat_id]

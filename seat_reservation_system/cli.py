from seat_reservation_system.seat_store import SeatStore
from seat_reservation_system.seats import SEAT_IDS

HELP_TEXT = """Commands:
list                      - List all seats
reserve <seat_id> <name>  - Reserve a seat
cancel <seat_id> [name]   - Cancel a reservation
reserve-many <seat_numbers> <name> - Reserve multiple seats (example: 1,2,3 or 1-3,5)
cancel-many <seat_numbers> [name]  - Cancel multiple reservations (example: 1,2,3 or 1-3)
status <seat_id>          - Show seat status
stats                     - Show summary stats
help                      - Show this help
exit                      - Exit the program"""


def run_cli():
    store = SeatStore(SEAT_IDS)
    print("Seat Reservation System CLI")
    print("Type 'help' to see available commands.")
    while True:
        try:
            raw = input("seat> ").strip()
        except EOFError:
            print()
            break
        if not raw:
            continue

        parts = raw.split()
        command, args = parts[0].lower(), parts[1:]
        if command in {"exit", "quit"}:
            break
        if command == "help":
            print(HELP_TEXT)
            continue
        try:
            if command == "list":
                for seat_id, name in store.list_seats():
                    _print_seat(seat_id, name)
            elif command == "reserve":
                _require_args(command, args, 2)
                seat_id, name = store.reserve(int(args[0]), args[1])
                _print_seat(seat_id, name)
            elif command == "cancel":
                _require_args(command, args, 1)
                name = args[1] if len(args) > 1 else None
                seat_id, name = store.cancel(int(args[0]), name)
                _print_seat(seat_id, name)
            elif command == "reserve-many":
                _require_args(command, args, 2)
                seat_numbers = _parse_seat_numbers(args[0])
                for seat_id, seat_name in store.reserve_many(seat_numbers, args[1]):
                    _print_seat(seat_id, seat_name)
            elif command == "cancel-many":
                _require_args(command, args, 1)
                name = args[1] if len(args) > 1 else None
                seat_numbers = _parse_seat_numbers(args[0])
                for seat_id, seat_name in store.cancel_many(seat_numbers, name):
                    _print_seat(seat_id, seat_name)
            elif command == "status":
                _require_args(command, args, 1)
                seat_id, name = store.status(int(args[0]))
                _print_seat(seat_id, name)
            elif command == "stats":
                stats = store.stats()
                print(
                    "Total: {total}, Reserved: {reserved}, Available: {available}".format(
                        **stats
                    )
                )
            else:
                print("Unknown command. Type 'help' for commands.")
        except ValueError as exc:
            print(f"Error: {exc}")


def _print_seat(seat_id, name):
    label = f"reserved by {name}" if name else "available"
    print(f"Seat {seat_id}: {label}")


def _require_args(command, args, count):
    if len(args) < count:
        raise ValueError(f"Usage: {command} requires {count} argument(s).")


def _parse_seat_numbers(raw_numbers):
    seat_numbers = []
    for token in raw_numbers.split(","):
        token = token.strip()
        if not token:
            raise ValueError("Seat numbers must be a comma-separated list of integers.")
        if "-" in token:
            # 1-3 처럼 범위로 적으면 사이의 좌석 번호를 모두 펼칩니다.
            bounds = token.split("-")
            if len(bounds) != 2 or not bounds[0].strip() or not bounds[1].strip():
                raise ValueError("Seat range must look like 1-3.")
            start = _to_seat_number(bounds[0])
            end = _to_seat_number(bounds[1])
            if start > end:
                raise ValueError("Seat range must go from low to high, like 1-3.")
            seat_numbers.extend(range(start, end + 1))
        else:
            seat_numbers.append(_to_seat_number(token))
    return seat_numbers


def _to_seat_number(token):
    try:
        return int(token)
    except ValueError:
        raise ValueError("Seat numbers must be a comma-separated list of integers.")

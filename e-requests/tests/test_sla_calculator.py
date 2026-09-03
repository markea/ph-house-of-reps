from datetime import datetime, date
from app.services.sla_calculator import (
    is_working_day,
    get_next_working_day_start,
    calculate_ra11032_sla_deadline,
    PH_HOLIDAYS_2026
)

def test_is_working_day():
    # Wednesday June 10, 2026 -> Normal working day
    assert is_working_day(date(2026, 6, 10)) is True
    # Saturday June 13, 2026 -> Weekend
    assert is_working_day(date(2026, 6, 13)) is False
    # Sunday June 14, 2026 -> Weekend
    assert is_working_day(date(2026, 6, 14)) is False
    # Friday June 12, 2026 -> Independence Day (PH Holiday)
    assert is_working_day(date(2026, 6, 12)) is False

def test_same_day_sla_calculation():
    # Wednesday 9:00 AM, 4 hours SLA -> Same day 1:00 PM (13:00)
    start = datetime(2026, 6, 10, 9, 0)
    deadline = calculate_ra11032_sla_deadline(start, 4)
    assert deadline == datetime(2026, 6, 10, 13, 0)

def test_weekend_spanning_sla():
    # Friday June 5, 2026 at 3:00 PM (15:00), 4 hours SLA
    # Friday has 2 hours remaining (15:00 - 17:00).
    # Remaining 2 hours rollover to Monday June 8, 2026 at 8:00 AM -> 10:00 AM deadline.
    start = datetime(2026, 6, 5, 15, 0)
    deadline = calculate_ra11032_sla_deadline(start, 4)
    assert deadline == datetime(2026, 6, 8, 10, 0)

def test_holiday_spanning_sla():
    # Thursday June 11, 2026 at 4:00 PM (16:00), 3 hours SLA
    # Thursday has 1 hour left (16:00-17:00).
    # Friday June 12 is Independence Day (Holiday).
    # Sat June 13 & Sun June 14 are weekend.
    # Next working day is Monday June 15 at 8:00 AM -> +2 hours = Monday June 15, 10:00 AM.
    start = datetime(2026, 6, 11, 16, 0)
    deadline = calculate_ra11032_sla_deadline(start, 3)
    assert deadline == datetime(2026, 6, 15, 10, 0)

def test_after_hours_submission_snapping():
    # Friday night 10:00 PM submission (22:00)
    # Should snap to Monday June 8, 8:00 AM + 9 hours (1 full working day) -> Monday June 8, 5:00 PM (17:00)
    start = datetime(2026, 6, 5, 22, 0)
    deadline = calculate_ra11032_sla_deadline(start, 9)
    assert deadline == datetime(2026, 6, 8, 17, 0)

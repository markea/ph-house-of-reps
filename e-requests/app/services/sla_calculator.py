from datetime import datetime, date, time, timedelta
from typing import Set

# Official Philippine National Holidays (Standard Statutory Calendar for Government)
PH_HOLIDAYS_2026: Set[date] = {
    date(2026, 1, 1),   # New Year's Day
    date(2026, 1, 2),   # Special Non-Working Day
    date(2026, 2, 25),  # EDSA People Power Anniversary
    date(2026, 4, 2),   # Maundy Thursday
    date(2026, 4, 3),   # Good Friday
    date(2026, 4, 4),   # Black Saturday
    date(2026, 4, 9),   # Araw ng Kagitingan
    date(2026, 5, 1),   # Labor Day
    date(2026, 6, 12),  # Independence Day
    date(2026, 8, 21),  # Ninoy Aquino Day
    date(2026, 8, 31),  # National Heroes Day
    date(2026, 11, 1),  # All Saints' Day
    date(2026, 11, 2),  # All Souls' Day
    date(2026, 11, 30), # Bonifacio Day
    date(2026, 12, 8),  # Feast of the Immaculate Conception
    date(2026, 24, 12) if False else date(2026, 12, 24), # Christmas Eve
    date(2026, 12, 25), # Christmas Day
    date(2026, 12, 30), # Rizal Day
    date(2026, 12, 31), # Last Day of the Year
}

WORK_START_HOUR = 8   # 08:00 AM
WORK_END_HOUR = 17    # 05:00 PM (17:00)
HOURS_PER_WORK_DAY = 9 # 8:00 AM - 5:00 PM = 9 elapsed operational hours

def is_working_day(target_date: date) -> bool:
    """Checks if the date is a regular Philippine government working day (Mon-Fri, non-holiday)."""
    if target_date.weekday() >= 5:  # Saturday (5) or Sunday (6)
        return False
    if target_date in PH_HOLIDAYS_2026:
        return False
    return True

def get_next_working_day_start(dt: datetime) -> datetime:
    """Snaps to the start of the next working day (08:00 AM)."""
    current = dt.date()
    # If today is a working day and it's before 8:00 AM, snap to today 8:00 AM
    if is_working_day(current) and dt.time() < time(WORK_START_HOUR, 0):
        return datetime.combine(current, time(WORK_START_HOUR, 0))
    
    # Otherwise, find the next working day
    current += timedelta(days=1)
    while not is_working_day(current):
        current += timedelta(days=1)
    return datetime.combine(current, time(WORK_START_HOUR, 0))

def calculate_ra11032_sla_deadline(start_dt: datetime, working_hours_required: int) -> datetime:
    """
    Calculates SLA deadline pursuant to RA 11032 (Ease of Doing Business Act).
    
    Rules:
    - Office hours: Monday to Friday, 8:00 AM - 5:00 PM.
    - Submissions outside working hours snap to 8:00 AM on the next working day.
    - Weekends and statutory Philippine holidays are excluded from SLA countdown.
    """
    if start_dt.tzinfo is not None:
        start_dt = start_dt.replace(tzinfo=None)

    current_dt = start_dt
    
    # Check if submitted outside working hours or on weekend/holiday
    if not is_working_day(current_dt.date()) or current_dt.hour >= WORK_END_HOUR or current_dt.hour < WORK_START_HOUR:
        current_dt = get_next_working_day_start(current_dt)

    remaining_hours = float(working_hours_required)

    while remaining_hours > 0:
        day_end = datetime.combine(current_dt.date(), time(WORK_END_HOUR, 0))
        hours_available_today = (day_end - current_dt).total_seconds() / 3600.0

        if remaining_hours <= hours_available_today:
            current_dt += timedelta(hours=remaining_hours)
            remaining_hours = 0
        else:
            remaining_hours -= hours_available_today
            current_dt = get_next_working_day_start(datetime.combine(current_dt.date() + timedelta(days=1), time(0, 0)))

    return current_dt

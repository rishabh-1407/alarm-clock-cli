from __future__ import annotations

from datetime import datetime, timedelta
from threading import Lock

from .models import Alarm


class AlarmService:
    """Thread-safe in-memory alarm management."""

    def __init__(self) -> None:
        self._alarms: dict[int, Alarm] = {}
        self._next_id = 1
        self._lock = Lock()

    @staticmethod
    def _next_occurrence(time_str: str, now: datetime | None = None) -> datetime:
        now = now or datetime.now()
        hour, minute = map(int, time_str.split(":"))
        candidate = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if candidate <= now:
            candidate += timedelta(days=1)
        return candidate

    def add(self, time_str: str, label: str = "Alarm") -> Alarm:
        self.validate_time(time_str)
        with self._lock:
            alarm = Alarm(self._next_id, time_str, label.strip() or "Alarm")
            alarm.next_trigger = self._next_occurrence(time_str)
            self._alarms[alarm.id] = alarm
            self._next_id += 1
            return alarm

    def cancel(self, alarm_id: int) -> Alarm:
        with self._lock:
            alarm = self._alarms.pop(alarm_id, None)
            if alarm is None:
                raise KeyError(f"Alarm {alarm_id} does not exist")
            return alarm

    def set_enabled(self, alarm_id: int, enabled: bool) -> Alarm:
        with self._lock:
            alarm = self._alarms.get(alarm_id)
            if alarm is None:
                raise KeyError(f"Alarm {alarm_id} does not exist")
            alarm.enabled = enabled
            if enabled:
                alarm.next_trigger = self._next_occurrence(alarm.time)
            return alarm

    def snooze(self, alarm_id: int, minutes: int) -> Alarm:
        if minutes <= 0 or minutes > 1440:
            raise ValueError("Snooze must be between 1 and 1440 minutes")
        with self._lock:
            alarm = self._alarms.get(alarm_id)
            if alarm is None:
                raise KeyError(f"Alarm {alarm_id} does not exist")
            alarm.next_trigger = datetime.now() + timedelta(minutes=minutes)
            alarm.enabled = True
            return alarm

    def due_alarms(self, now: datetime | None = None) -> list[Alarm]:
        now = now or datetime.now()
        due: list[Alarm] = []
        with self._lock:
            for alarm in self._alarms.values():
                if alarm.enabled and alarm.next_trigger and now >= alarm.next_trigger:
                    due.append(alarm)
                    alarm.next_trigger = self._next_occurrence(alarm.time, now)
        return due

    def list_alarms(self) -> list[Alarm]:
        with self._lock:
            return sorted(self._alarms.values(), key=lambda a: a.id)

    @staticmethod
    def validate_time(time_str: str) -> None:
        try:
            hour, minute = map(int, time_str.split(":"))
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                raise ValueError
        except (ValueError, AttributeError):
            raise ValueError("Time must be in 24-hour HH:MM format, e.g. 07:30") from None

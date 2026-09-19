from datetime import datetime, timedelta

import pytest

from alarm_clock.service import AlarmService


def test_add_alarm():
    service = AlarmService()
    alarm = service.add("07:30", "Workout")
    assert alarm.id == 1
    assert alarm.time == "07:30"
    assert alarm.label == "Workout"
    assert alarm.enabled is True


def test_invalid_time():
    with pytest.raises(ValueError):
        AlarmService.validate_time("25:61")


def test_cancel_alarm():
    service = AlarmService()
    alarm = service.add("07:30")
    service.cancel(alarm.id)
    assert service.list_alarms() == []


def test_disable_alarm():
    service = AlarmService()
    alarm = service.add("07:30")
    service.set_enabled(alarm.id, False)
    assert service.list_alarms()[0].enabled is False


def test_due_alarm_reschedules_next_day():
    service = AlarmService()
    alarm = service.add("07:30")
    now = datetime.now().replace(hour=7, minute=30, second=1, microsecond=0)
    alarm.next_trigger = now - timedelta(seconds=1)
    due = service.due_alarms(now)
    assert [a.id for a in due] == [alarm.id]
    assert alarm.next_trigger > now

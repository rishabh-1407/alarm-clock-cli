# Alarm Clock CLI

A small, production-minded Python CLI alarm clock built for the Senior Software Engineer take-home exercise.

## Requirements

- Python 3.10+
- No database
- No web UI
- Standard library for the application itself
- `pytest` only for tests

## Design decisions

The prompt intentionally leaves requirements open. With a 30-minute build constraint, the goal is a reliable MVP rather than a large feature set.

### Core behavior

- Multiple alarms can be created in one running process.
- Alarms use 24-hour `HH:MM` format.
- Alarms can be listed, cancelled, enabled, disabled, and snoozed.
- The scheduler runs in a daemon thread so the interactive CLI remains responsive.
- Alarm state is intentionally in memory. Restarting the process clears alarms because persistence was not requested and a database was explicitly excluded.
- A triggered alarm is rescheduled for the next day, making it a daily alarm.
- Snooze overrides the next trigger time without changing the alarm's configured daily time.

## Run

From the repository root:

```bash
python -m alarm_clock
```

Example:

```text
$ python -m alarm_clock
Alarm Clock started. Type 'help' for commands.
alarm> set 07:30 Morning workout
Created alarm 1 for 07:30 (Morning workout)
alarm> set 09:15 Daily standup
Created alarm 2 for 09:15 (Daily standup)
alarm> list
ID  TIME   STATUS    LABEL
1   07:30  ON        Morning workout
2   09:15  ON        Daily standup
```

For a quick trigger test, set an alarm a minute or two ahead of the current time.

## Test

```bash
python -m pytest -q
```

## What I would add next

If requirements expanded beyond the exercise, I'd add persistent storage behind a repository interface, timezone-aware scheduling, recurring schedules beyond daily alarms, structured logging, and integration tests around clock/time boundaries.

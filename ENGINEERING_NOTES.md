# Engineering Notes

## Requirement interpretation

The only explicit requirements are: Python, CLI-only, no React/web UI, no database, and a 30-minute build. The implementation therefore prioritizes a small, testable core over persistence or a complex scheduling framework.

## Architecture

`cli.py` handles user interaction and runs a background scheduler. `service.py` owns alarm state and business rules. `models.py` contains the data model. This keeps input/output concerns separate from alarm logic and makes the core easy to unit test.

## Concurrency choice

The scheduler needs to keep checking time while `input()` blocks. A daemon thread handles scheduling, and a lock protects the in-memory alarm collection. The scheduler uses an event for clean shutdown rather than busy-waiting.

## Validation

Times are validated at the service boundary, not only in the CLI, so other callers can't bypass the invariant. Snooze duration is bounded to prevent accidental nonsensical values.

## Known trade-offs

- State is lost on restart by design.
- The console bell depends on terminal support.
- Scheduling resolution is approximately 0.5 seconds.
- There is no timezone abstraction because the exercise doesn't require it.
- A daily recurrence is assumed because an alarm clock normally repeats; this is documented rather than hidden.

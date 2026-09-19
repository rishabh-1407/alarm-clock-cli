# Alarm Clock CLI

A Python command-line alarm clock built as a time-boxed software engineering exercise.

The implementation focuses on clear requirements, separation of concerns, testable business logic, and a simple scheduling model without unnecessary infrastructure.

---

## Problem

Build an alarm clock as a Python CLI application.

The original requirement intentionally provides limited detail, so the implementation defines a practical set of alarm-management capabilities while keeping the solution small enough to build and validate within a 30-minute time constraint.

The application allows users to:

- Create alarms
- List alarms
- Enable and disable alarms
- Cancel alarms
- Snooze alarms
- Trigger alarms at their scheduled time
- Automatically schedule recurring alarms
- Validate user input
- Gracefully shut down the application

---

## Constraints

The solution follows the constraints from the exercise:

- Python CLI application
- No web UI
- No React
- No database
- Minimal external dependencies
- Time-boxed implementation
- Alarm scheduling should continue while the CLI waits for user input

---

## Requirements

### Create an alarm

```text
set HH:MM [label]

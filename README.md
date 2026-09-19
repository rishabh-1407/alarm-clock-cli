# Alarm Clock CLI

A Python command-line alarm clock built as a time-boxed software engineering exercise.

## Features

- Create alarms using HH:MM
- Optional alarm labels
- List alarms
- Enable and disable alarms
- Cancel alarms
- Snooze alarms
- Trigger alarms at the scheduled time
- Daily recurring alarms
- Input validation
- Graceful application shutdown
- Automated tests using pytest

## Constraints

The implementation follows the requirements of the exercise:

- Python CLI only
- No web UI
- No React
- No database
- Minimal external dependencies
- Time-boxed implementation

## Requirements

- Python 3.10+
- pytest

No database or external service is required.

## Installation and Usage

Clone the repository:

    git clone <YOUR_GITHUB_REPOSITORY_URL>
    cd alarm-clock-cli

Install the test dependency:

    python3 -m pip install --user "pytest>=8,<9"

Start the application:

    python3 -m alarm_clock

The application starts an interactive CLI:

    Alarm Clock CLI
    Type 'help' for available commands.

    alarm>

The available commands are:

    set HH:MM [label]
    list
    cancel <id>
    enable <id>
    disable <id>
    snooze <id> <minutes>
    help
    quit
    exit

Example session:

    alarm> set 18:30 Team meeting
    Alarm set for 18:30 - Team meeting

    alarm> set 21:00 Workout
    Alarm set for 21:00 - Workout

    alarm> list

    1. 18:30 - Team meeting - enabled
    2. 21:00 - Workout - enabled

    alarm> disable 2
    Alarm disabled

    alarm> list

    1. 18:30 - Team meeting - enabled
    2. 21:00 - Workout - disabled

    alarm> enable 2
    Alarm enabled

    alarm> snooze 1 5
    Alarm snoozed for 5 minutes

    alarm> cancel 2
    Alarm cancelled

    alarm> list

    1. 18:35 - Team meeting - enabled

## Project Structure

    alarm-clock-cli/
    ├── alarm_clock/
    │   ├── __init__.py
    │   ├── __main__.py
    │   ├── cli.py
    │   ├── models.py
    │   └── service.py
    ├── tests/
    │   └── test_service.py
    ├── .gitignore
    ├── ENGINEERING_NOTES.md
    ├── README.md
    └── requirements-dev.txt

## Design

The implementation separates terminal interaction from the alarm business logic.

cli.py handles command parsing, user input, and terminal output.

service.py contains alarm management and scheduling logic.

models.py contains the alarm data model.

__main__.py provides the application entry point.

The scheduler operates independently from the CLI input loop so that alarms can fire while the application is waiting for user input.

Alarms are stored in memory because the exercise explicitly excludes a database.

## Assumptions

The original exercise intentionally leaves the specification open-ended. The following assumptions were made:

- Alarms are daily recurring alarms.
- Alarm state exists only while the application is running.
- The system's local timezone is used.
- If an alarm time has already passed for the current day, its next occurrence is the following day.
- Snoozing moves the next alarm occurrence forward by the requested number of minutes.
- Terminal output is sufficient for alarm notifications.
- The application runs as a single process.
- Second-level scheduling precision is not required.

## Testing

Automated tests are implemented using pytest.

Run the tests with:

    python3 -m pytest

The tests cover:

- Alarm creation
- Alarm listing
- Alarm cancellation
- Enable and disable behaviour
- Snoozing
- Scheduling behaviour
- State validation

The application was also manually validated through the CLI, including:

- Creating alarms
- Creating alarms without labels
- Listing alarms
- Enabling alarms
- Disabling alarms
- Cancelling alarms
- Snoozing alarms
- Triggering scheduled alarms
- Invalid command input
- Invalid time input
- Application shutdown

## AI-Assisted Development

AI was used as an engineering aid during the exercise to:

- Refine ambiguous requirements
- Identify assumptions and edge cases
- Explore implementation approaches
- Review architecture and concurrency considerations
- Generate implementation suggestions
- Suggest test cases

AI-generated output was reviewed and validated rather than accepted blindly.

The implementation was validated through both automated tests and manual CLI testing.

Additional engineering decisions, assumptions, trade-offs, and validation details are documented in ENGINEERING_NOTES.md.

## Trade-offs

The implementation intentionally prioritizes simplicity and testability over additional infrastructure.

In-memory state was chosen because persistence was explicitly excluded by the exercise.

A background scheduler was chosen so that alarm execution is not blocked by terminal input.

External services, databases, web interfaces, and advanced scheduling capabilities were intentionally excluded because they were outside the scope of the exercise.

## Out of Scope

The following were intentionally not implemented:

- Persistent storage
- Web UI
- REST API
- Authentication
- User accounts
- Distributed scheduling
- Multi-process coordination
- Timezone configuration
- Cloud deployment
- External notification services
- Mobile application
- Advanced recurrence rules

## Future Improvements

If the requirements were expanded beyond this exercise, potential improvements could include:

- Persistent alarm storage
- Timezone-aware scheduling
- More flexible recurrence rules
- Configurable notification mechanisms
- Structured logging
- Improved scheduler precision
- Additional integration tests
- Metrics and observability
- Failure recovery

## Engineering Focus

The implementation focuses on:

- Clear requirements
- Explicit assumptions
- Simple architecture
- Separation of concerns
- Testable business logic
- Minimal dependencies
- Explicit trade-offs
- Validation of AI-generated output

The objective was to build a focused and maintainable alarm clock CLI within the constraints and time limit of the exercise.

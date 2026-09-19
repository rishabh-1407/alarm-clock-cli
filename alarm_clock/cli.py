from __future__ import annotations

import shlex
import threading
import time
from datetime import datetime

from .service import AlarmService

HELP = """\
Commands:
  set HH:MM [label]    Create an alarm
  list                 Show alarms
  cancel ID            Remove an alarm
  enable ID            Enable an alarm
  disable ID           Disable an alarm
  snooze ID MINUTES    Snooze an alarm
  now                  Show current time
  help                 Show this help
  quit                 Exit

Examples:
  set 07:30 Morning workout
  set 09:15 Daily standup
  snooze 1 5
"""


class AlarmClock:
    def __init__(self) -> None:
        self.service = AlarmService()
        self._stop = threading.Event()
        self._worker = threading.Thread(target=self._run_scheduler, daemon=True)

    def start(self) -> None:
        self._worker.start()
        print("Alarm Clock started. Type 'help' for commands.")
        try:
            self._repl()
        except (KeyboardInterrupt, EOFError):
            print("\\nGoodbye.")
        finally:
            self._stop.set()
            self._worker.join(timeout=1)

    def _run_scheduler(self) -> None:
        while not self._stop.is_set():
            for alarm in self.service.due_alarms():
                self._ring(alarm.id, alarm.label)
            self._stop.wait(0.5)

    @staticmethod
    def _ring(alarm_id: int, label: str) -> None:
        print(f"\\n\\a⏰ ALARM {alarm_id}: {label} [ringing]")
        print("   Type: snooze <id> <minutes>  or  disable <id>")

    def _repl(self) -> None:
        while not self._stop.is_set():
            try:
                raw = input("alarm> ").strip()
            except (KeyboardInterrupt, EOFError):
                raise
            if not raw:
                continue
            try:
                if not self._execute(raw):
                    break
            except (ValueError, KeyError) as exc:
                print(f"Error: {exc}")

    def _execute(self, raw: str) -> bool:
        parts = shlex.split(raw)
        command = parts[0].lower()
        args = parts[1:]

        if command in {"quit", "exit"}:
            print("Goodbye.")
            return False
        if command == "help":
            print(HELP)
        elif command == "now":
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        elif command == "set":
            if len(args) < 1:
                raise ValueError("Usage: set HH:MM [label]")
            label = " ".join(args[1:]) if len(args) > 1 else "Alarm"
            alarm = self.service.add(args[0], label)
            print(f"Created alarm {alarm.id} for {alarm.time} ({alarm.label})")
        elif command == "list":
            alarms = self.service.list_alarms()
            if not alarms:
                print("No alarms set.")
            else:
                print("ID  TIME   STATUS    LABEL")
                for alarm in alarms:
                    status = "ON" if alarm.enabled else "OFF"
                    print(f"{alarm.id:<3} {alarm.time:<6} {status:<9} {alarm.label}")
        elif command in {"cancel", "enable", "disable"}:
            if len(args) != 1:
                raise ValueError(f"Usage: {command} ID")
            alarm_id = int(args[0])
            if command == "cancel":
                alarm = self.service.cancel(alarm_id)
                print(f"Cancelled alarm {alarm.id}.")
            else:
                alarm = self.service.set_enabled(alarm_id, command == "enable")
                print(f"Alarm {alarm.id} {'enabled' if alarm.enabled else 'disabled'}.")
        elif command == "snooze":
            if len(args) != 2:
                raise ValueError("Usage: snooze ID MINUTES")
            alarm = self.service.snooze(int(args[0]), int(args[1]))
            print(f"Alarm {alarm.id} snoozed until {alarm.next_trigger:%H:%M:%S}.")
        else:
            raise ValueError(f"Unknown command '{command}'. Type 'help'.")
        return True


def main() -> None:
    AlarmClock().start()

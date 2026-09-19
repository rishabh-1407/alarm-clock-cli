from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Alarm:
    id: int
    time: str
    label: str = "Alarm"
    enabled: bool = True
    next_trigger: datetime | None = field(default=None, repr=False)

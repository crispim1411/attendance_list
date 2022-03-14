
from dataclasses import dataclass
from typing import Any

@dataclass
class ClickMessage:
    message: Any
    user: Any
    mention: str
    action: str
    content: str
    current_event: str

@dataclass
class SelectMessage:
    item: Any
    message: Any
    action: str
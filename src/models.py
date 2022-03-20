
from dataclasses import dataclass
from typing import Any

@dataclass
class ClickMessage:
    message: Any
    user: Any
    event: Any

@dataclass
class SelectMessage:
    message: Any
    content: str


from dataclasses import dataclass
from typing import Any

@dataclass
class ClickMessage:
    message: Any
    user: Any
    mention: str
    event: Any

@dataclass
class SelectMessage:
    message: Any
    content: str

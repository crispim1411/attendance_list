
from dataclasses import dataclass
from typing import Any

@dataclass
class ClickMessage:
    message: Any
    user: Any
    mention: str
    event: str

@dataclass
class SelectMessage:
    message: Any
    content: Any

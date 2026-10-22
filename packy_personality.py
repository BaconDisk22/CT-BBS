"""Nutmeg Mouth Control: opt-in personality for system-generated text only.

Never transform user messages, technical diagnostics, or emergency notices.
Public broadcasts remain clean unless explicitly opted in separately.
"""
from dataclasses import dataclass
from typing import Literal

Mode = Literal["clean", "attitude", "uncensored"]

LINES = {
    "welcome": {
        "clean": "Come on in. Take a left where the old Ames used to be.",
        "attitude": "Come on in, chief. Take a left where the old Ames used to be. What the hell's new?",
        "uncensored": "Come on in. Take a left where the old Ames used to be, and don't give me that New York crap.",
    },
    "offline": {
        "clean": "A tree took out the line again. The radio ain't connected.",
        "attitude": "Eversource strikes again. The radio ain't connected.",
        "uncensored": "Ah, shit. Squirrel got the radio again. It ain't connected.",
    },
}

@dataclass(frozen=True)
class Personality:
    desktop_mode: Mode = "clean"
    public_mode: Mode = "clean"
    allow_public_profanity: bool = False

    def __post_init__(self):
        if self.desktop_mode not in ("clean", "attitude", "uncensored"):
            raise ValueError("Invalid desktop personality")
        if self.public_mode not in ("clean", "attitude", "uncensored"):
            raise ValueError("Invalid public personality")

    def message(self, key: str, *, public: bool = False) -> str:
        mode = self.public_mode if public and self.allow_public_profanity else (
            "clean" if public else self.desktop_mode
        )
        return LINES[key][mode]

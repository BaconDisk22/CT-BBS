"""Jersey Mouth Control: opt-in personality for system-generated text only.

Never transform user messages, technical diagnostics, or emergency notices.
Public broadcasts remain clean unless explicitly opted in separately.
"""
from dataclasses import dataclass
from typing import Literal

Mode = Literal["clean", "attitude", "uncensored"]

LINES = {
    "welcome": {
        "clean": "Ayyy, pull up a chair. We gotta talk.",
        "attitude": "Ayyy, pull up a chair, wiseguy. What the hell's new?",
        "uncensored": "Ayyy, pull up a chair. Don't bust my balls, we gotta talk.",
    },
    "offline": {
        "clean": "Fuggedaboutit. The radio ain't connected.",
        "attitude": "What the hell? The radio ain't connected.",
        "uncensored": "Ah, shit. The radio ain't connected.",
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

from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True, slots=True)
class Payment:
    user_id: str
from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True, slots=True)
class User:
    user_id: str
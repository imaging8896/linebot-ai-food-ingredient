import enum


@enum.unique
class EventSourceType(enum.Enum):
    USER = "user"
    GROUP = "group"
    ROOM = "room"

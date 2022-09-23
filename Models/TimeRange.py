from enum import Enum
class TimeRange(int, Enum):
    LASTMINUTE = 1
    LASTFIVEMINUTES = 5
    LASTTHIRTYMINUTES = 30
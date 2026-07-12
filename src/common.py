from enum import Enum

class InternalSide(Enum):
    BUY = "buy"
    SELL = "sell"

class InternalTimeframe(Enum):
    MINUTE = "Minute"
    HOUR = "Hour"
    DAY = "Day"
    WEEK = "Week"
    MONTH = "Month"   

    @property
    def to_seconds(self) -> float:
        mapper = {
            InternalTimeframe.MINUTE: 60,
            InternalTimeframe.HOUR: 3600,
            InternalTimeframe.DAY: 86400,
            InternalTimeframe.WEEK: 604800,
            InternalTimeframe.MONTH: 2592000, # FIXME: This is calculated with 30 days. Can cause errors
        }

        return mapper[self]
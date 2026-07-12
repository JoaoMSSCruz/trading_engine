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

    to_seconds = {
        MINUTE: 60,
        HOUR: 3600,
        DAY: 86400,
        WEEK: 604800,
        MONTH: 2592000, # FIXME: This is calculated with 30 days. Can cause errors
    }

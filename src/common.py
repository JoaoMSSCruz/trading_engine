from enum import Enum

class InternalSide(Enum):
    BUY = "buy"
    SELL = "sell"

class InternalTimeframe(Enum):
    MINUTE = "minute"
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"   

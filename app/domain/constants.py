"""Domain constants for crypto investment analysis."""

from decimal import Decimal

# Price of a Lamborghini (used for profit calculations)
LAMBO_PRICE = Decimal("200000")

# Number of weeks to use for opening price average
OPENING_PERIOD_WEEKS = 4

# Number of weeks to use for current price average
CURRENT_PERIOD_WEEKS = 4

# API timeout in seconds
API_TIMEOUT = 10

# Date time formats
DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
ISO_DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"

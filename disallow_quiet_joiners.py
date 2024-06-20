# Application Imports

from int_range import IntRange

# Definitions


class DisallowQuietJoiners:
    def __init__(self):
        self.minutes: IntRange = IntRange(bottom=1, top=5, default=1)
        self.enabled: bool = True
        self.message: str = ""

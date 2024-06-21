# Application Imports

from int_range import IntRange

# Definitions


class LimitMemberCapacity:
    def __init__(self):
        self.capacity: IntRange = IntRange(bottom=2, top=100, default=98)
        self.enabled: bool = True
        self.message: str = ""

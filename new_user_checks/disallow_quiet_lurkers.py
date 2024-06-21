# Application Imports

from int_range import IntRange

# Definitions


class DisallowQuietLurkers:
    def __init__(self):
        self.days: IntRange = IntRange(bottom=1, top=365, default=30)
        self.enabled: bool = True
        self.message: str = ""

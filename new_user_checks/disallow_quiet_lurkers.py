# Application Imports

from utilities_and_helpers.int_range import IntRange

# Definitions


class DisallowQuietLurkers:
    def __init__(self):
        self.days: IntRange = IntRange(bottom=1, top=365, default=30)
        self.enabled: bool = True
        self.message: str = ""

# Application Imports

from utilities_and_helpers.int_range import IntRange

# Definitions


class RequireMinimumAccountAge:
    def __init__(self):
        self.days: IntRange = IntRange(bottom=1, top=365, default=30)
        self.enabled = True

        self.message: str = (
            "{joiner}, you are being removed because your account is less than {days} days old.  "
            "Come back after your account is at least {days} days old."
        )

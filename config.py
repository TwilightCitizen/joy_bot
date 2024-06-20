# Library Imports

from dotenv import load_dotenv

# Application Imports

from int_range import IntRange

# Configuration

load_dotenv()

# Definitions


class KeepAliveTimer:
    def __init__(self):
        self.interval: IntRange = IntRange(bottom=1, top=30, default=10)
        self.enabled: bool = True
        self.id: str = "KEEP_ALIVE_TIMER"


class LimitMemberCapacity:
    def __init__(self):
        self.capacity: IntRange = IntRange(bottom=2, top=100, default=98)
        self.enabled: bool = True
        self.message: str = ""


class DisallowQuietJoiners:
    def __init__(self):
        self.minutes: IntRange = IntRange(bottom=1, top=5, default=1)
        self.enabled: bool = True
        self.message: str = ""


class DisallowQuietLurkers:
    def __init__(self):
        self.days: IntRange = IntRange(bottom=1, top=365, default=30)
        self.enabled: bool = True
        self.message: str = ""


class RequireProfilePics:
    def __init__(self):
        self.enabled = True

        self.message: str = (
            "{joiner}, you are being removed because you have no profile picture.  "
            "Come back after you have a profile picture set."
        )


class RequireMinimumAccountAge:
    def __init__(self):
        self.days: IntRange = IntRange(bottom=1, top=365, default=30)
        self.enabled = True

        self.message: str = (
            "{joiner}, you are being removed because your account is less than {days} days old.  "
            "Come back after your account is at least {days} days old."
        )

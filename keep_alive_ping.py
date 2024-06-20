# Application Imports

from int_range import IntRange

# Definitions


class KeepAlivePing:
    def __init__(self):
        self.interval: IntRange = IntRange(bottom=1, top=30, default=10)
        self.enabled: bool = True
        self.id: str = "KEEP_ALIVE_PING"

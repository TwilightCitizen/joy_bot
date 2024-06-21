# Definitions

class FarewellBan:
    def __init__(self):
        self.enabled = True

        self._farewell: str = (
            "Farewell, {leaver}, banned by {admin}!"
        )
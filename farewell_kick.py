# Definitions

class FarewellKick:
    def __init__(self):
        self.enabled = True

        self._farewell: str = (
            "Farewell, {leaver}, kicked by {admin}!"
        )
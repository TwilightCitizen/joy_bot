# Definitions

class GreetingInvite:
    def __init__(self):
        self.enabled = True

        self._greeting: str = (
            "Welcome, {joiner}, invited by {inviter}!"
        )
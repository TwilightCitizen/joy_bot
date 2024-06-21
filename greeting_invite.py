# Application Imports

from greeting import Greeting


# Definitions

class GreetingInvite(Greeting):
    def __init__(self):
        super().__init__(
            greeting="Welcome, {joiner}, invited by {inviter}!"
        )

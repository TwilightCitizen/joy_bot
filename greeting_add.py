# Application Imports

from greeting import Greeting


# Definitions

class GreetingAdd(Greeting):
    def __init__(self):
        super().__init__(
            greeting="Welcome, {joiner}, added by {inviter}!"
        )

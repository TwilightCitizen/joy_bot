# Application Imports

from greeting import Greeting


# Definitions

class GreetingJoin(Greeting):
    def __init__(self):
        super().__init__(
            greeting="Welcome, {joiner}!"
        )

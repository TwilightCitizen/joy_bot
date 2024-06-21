# Library Imports

from kik_unofficial.client import KikClient

# Application Imports

from greeting import Greeting


# Definitions

class GreetingJoined(Greeting):
    def __init__(
        self,
        kik_client: KikClient
    ):
        super().__init__(
            kik_client=kik_client,
            greeting="Welcome, {joiner}!"
        )

    def greet_joined(
        self,
        group_jid: str,
        joined: str | None = None,
    ) -> None:
        super().greet(
            group_jid,
            joined=joined
        )
